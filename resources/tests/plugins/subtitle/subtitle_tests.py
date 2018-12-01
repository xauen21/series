import unittest
import datetime
import os

from resources.series.plugins.subtitle.subtitle import Subtitle
from resources.series.model.serie import Serie
from resources.series.model.serie import Episode
from resources.series.common.code import Code

class TestSubtitles(unittest.TestCase):
	@staticmethod
	def searchUrl(name, episode, plugin_module, plugin_class):
		if (name == "name in subdivx" and episode == Episode(1, 1)):
			return "http://subdivx.com/subtitle?name:" + name + "&episode:" + str(episode.season) + "x" + str(episode.episode), Code.found
		if (name == "name in subdivx" and episode == Episode(1, 2)):
			return None, Code.notFound
		else: return None, Code.connectionError
	
	@staticmethod
	def _getSeriesPath():
		return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/data/series"

	@staticmethod
	def _getSubtitlesPath():
		return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/data/subtitles"
	
	def setUp(self):
		Subtitle.searchUrl = TestSubtitles.searchUrl
		Serie._getPath = TestSubtitles._getSeriesPath
		Subtitle._getPath = TestSubtitles._getSubtitlesPath

	def test_searchSubtitle(self):
		serie = Serie("test_searchSubtitle", ["missing name in test", "name in subdivx"], [Episode(1, 1)])
		serie = Subtitle.updateSerie(serie)
		self.assertTrue(serie.episodes[0].__dict__["subtitle"])
		self.assertEqual(serie.__dict__["Subdivx"], "name in subdivx")

	def test_searchSubtitleNotFound(self):
		serie = Serie("test_searchSubtitleNotFound", ["missing name in test", "name in subdivx"], [Episode(1, 2)])
		serie = Subtitle.updateSerie(serie)
		self.assertFalse("Subdivx" in serie.__dict__)
		self.assertFalse(serie.episodes[0].__dict__["subtitle"])

	@unittest.SkipTest
	def test_downloadEpisode(self):
		episode = Episode(1, 1)
		episode.__dict__.update({"Subdivx" : "http://www.subdivx.com/bajar.php?id=194981&u=5"})
		subtitle_file, code = Subtitle.download("csi", episode)
		if (code != Code.connectionError):
			self.assertEqual(code, Subtitle.found)
			self.assertTrue(os.path.isfile(subtitle_file))
			os.remove(subtitle_file)

if __name__ == '__main__':
	unittest.main()