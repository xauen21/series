import unittest
import datetime
import os

from series.plugins.subtitles.subtitles import Subtitles
from series.model.serie import Serie
from series.model.serie import Episode

class TestSubtitles(unittest.TestCase):
	@staticmethod
	def searchUrl(plugin_module, plugin_class, name, episode):
		if (name == "name in subdivx" and episode == Episode(1, 1)):
			return "http://subdivx.com/subtitle?name:" + name + "&episode:" + str(episode.season) + "x" + str(episode.episode), Subtitles.found
		if (name == "name in subdivx" and episode == Episode(1, 2)):
			return None, Subtitles.notFound
		else: return None, Subtitles.connectionError
	
	def setUp(self):
		Subtitles.searchUrl = TestSubtitles.searchUrl

	def test_searchSubtitle(self):
		serie = Serie("name in subdivx", ["missing name in test", "name in subdivx"], [Episode(1, 1)])
		serie = Subtitles.updateSerie(serie, save = False, verbose = False)
		self.assertTrue("subdivx" in serie.episodes[0].__dict__["subdivx"])
		self.assertEqual(serie.__dict__["subdivx"], "name in subdivx")

	def test_searchSubtitleNotFound(self):
		serie = Serie("name in subdivx", ["missing name in test", "name in subdivx"], [Episode(1, 2)])
		serie = Subtitles.updateSerie(serie, save = False, verbose = False)
		self.assertFalse("subdivx" in serie.__dict__)
		self.assertFalse("subdivx" in serie.episodes[0].__dict__)

	def test_downloadEpisode(self):
		episode = Episode(1, 1)
		episode.__dict__.update({"subdivx" : "http://www.subdivx.com/bajar.php?id=194981&u=5"})
		subtitle_file = Subtitles.download(episode)
		self.assertTrue(os.path.isfile(subtitle_file))
		os.remove(subtitle_file)

if __name__ == '__main__':
	unittest.main()