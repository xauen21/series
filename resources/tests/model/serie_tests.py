import unittest
import os
import datetime

from resources.series.model.serie import Serie
from resources.series.model.episode import Episode
from resources.series.model.episode import Episode

class TestDecodeEncode(unittest.TestCase):
	@staticmethod
	def _getSeriesPath():
		return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/tests/data/series"

	def setUp(self):
		Serie._getPath = TestDecodeEncode._getSeriesPath
	
	def test_encodeDecode(self):
		serie_input = Serie("test_encodeDecode1", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		serie_input.write()
		serie_output = Serie("test_encodeDecode1")
		serie_output.delete()
		self.assertEqual(serie_output, serie_input)
	
	def test_getSeries(self):
		serie1 = Serie("test_getSeries1", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		serie1.write()
		serie2 = Serie("test_getSeries2", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		serie2.write()
		series = Serie.getSeries()
		serie1.delete()
		serie2.delete()
		self.assertIsNotNone(series)
		self.assertGreater(len(series), 2)

	def test_getMaxEpisode(self):
		serie = Serie("test_getMaxEpisode1", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		self.assertEqual(serie.getMaxEpisode(), Episode(1, 3))

		serie = Serie("test_getMaxEpisode2", ["name 1", "name 2"])
		self.assertEqual(serie.getMaxEpisode(), None)

	@unittest.SkipTest
	def test_getMaxEpisodeOnAir(self):
		serie = Serie("test serie", ["name 1", "name 2"], [Episode(1, 1, datetime.date.today().strftime(Serie.dateformat)), Episode(1, 2), Episode(1, 3)])
		self.assertEqual(serie.getMaxEpisodeOnAir(), Episode(1, 1))
	
		serie = Serie("test serie", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		self.assertEqual(serie.getMaxEpisodeOnAir(), None)
	
		serie = Serie("test serie", ["name 1", "name 2"])
		self.assertEqual(serie.getMaxEpisodeOnAir(), None)

if __name__ == '__main__':
	unittest.main()
	