import unittest
import datetime
import os

from resources.series.plugins.torrent.torrent import Torrent
from resources.series.model.serie import Serie
from resources.series.model.serie import Episode
from resources.series.common.code import Code

class TestTorrent(unittest.TestCase):
	@staticmethod
	def searchUrl(name, episode, plugin_module, plugin_class):
		if plugin_class != "Piratebay": return None, Code.notFound
		if (name == "name in piratebay" and episode == Episode(1, 1)):
			return "magnet:http://piratebay/torrent?name:" + name + "&episode:" + str(episode.season) + "x" + str(episode.episode), Code.found
		if (name == "name in piratebay" and episode == Episode(1, 2)):
			return None, Code.notFound
		else: return None, Code.notFound
	
	@staticmethod
	def _getSeriesPath():
		return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/data/series"
	
	def setUp(self):
		Torrent.searchUrl = TestTorrent.searchUrl
		Serie._getPath = TestTorrent._getSeriesPath

	def test_searchTorrent(self):
		serie = Serie("test_searchTorrent", ["missing name in test", "name in piratebay"], [Episode(1, 1)])
		serie = Torrent.updateSerie(serie)
		#self.assertTrue(serie.episodes[0].__dict__["torrent"])
		self.assertEqual(serie.__dict__["Piratebay"], "name in piratebay")

	def test_searchTorrentNotFound(self):
		serie = Serie("test_searchTorrentNotFound", ["missing name in test", "name in piratebay"], [Episode(1, 2)])
		serie = Torrent.updateSerie(serie)
		self.assertFalse("Piratebay" in serie.__dict__)
		#self.assertFalse(serie.episodes[0].__dict__["torrent"])

	@unittest.SkipTest
	def test_downloadEpisode(self):
		episode = Episode(1, 1)
		episode.__dict__.update({"Piratebay" : "http://www.subdivx.com/bajar.php?id=194981&u=5"})
		subtitle_file = Torrent.download(episode)
		self.assertTrue(os.path.isfile(subtitle_file))
		os.remove(subtitle_file)

if __name__ == '__main__':
	unittest.main()