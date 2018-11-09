import unittest
import datetime
import os

from series.plugins.torrent.torrent import Torrent
from series.model.serie import Serie
from series.model.serie import Episode

class TestTorrent(unittest.TestCase):
	@staticmethod
	def searchUrl(plugin_module, plugin_class, name, episode):
		if (name == "name in piratebay" and episode == Episode(1, 1)):
			return "magnet:http://piratebay/torrent?name:" + name + "&episode:" + str(episode.season) + "x" + str(episode.episode), Torrent.found
		if (name == "name in subdivx" and episode == Episode(1, 2)):
			return None, Torrent.notFound
		else: return None, Torrent.connectionError
	
	def setUp(self):
		Torrent.searchUrl = TestTorrent.searchUrl

	def test_searchSubtitle(self):
		serie = Serie("name in piratebay", ["missing name in test", "name in piratebay"], [Episode(1, 1)])
		serie = Torrent.updateSerie(serie, save = False, verbose = False)
		self.assertTrue("piratebay" in serie.episodes[0].__dict__["piratebay"])
		self.assertEqual(serie.__dict__["piratebay"], "name in piratebay")

	def test_searchSubtitleNotFound(self):
		serie = Serie("name in subdivx", ["missing name in test", "name in piratebay"], [Episode(1, 2)])
		serie = Torrent.updateSerie(serie, save = False, verbose = False)
		self.assertFalse("piratebay" in serie.__dict__)
		self.assertFalse("piratebay" in serie.episodes[0].__dict__)

	@unittest.SkipTest
	def test_downloadEpisode(self):
		episode = Episode(1, 1)
		episode.__dict__.update({"piratebay" : "http://www.subdivx.com/bajar.php?id=194981&u=5"})
		subtitle_file = Torrent.download(episode, save = False)
		self.assertTrue(os.path.isfile(subtitle_file))
		os.remove(subtitle_file)

if __name__ == '__main__':
	unittest.main()