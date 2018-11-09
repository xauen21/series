import unittest
import os
import datetime

from series.model.serie import Serie
from series.model.episode import Episode

class TestDecodeEncode(unittest.TestCase):
	def test_encode_decode(self):
		serie_input = Serie("test serie", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		serie_input.write()
		serie_output = Serie("test serie")
		serie_output.delete()
		self.assertEqual(serie_output, serie_input)
	
	def test_getSeries(self):
		serie1 = Serie("test serie", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		serie1.write()
		serie2 = Serie("test serie2", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		serie2.write()
		series = Serie.getSeries()
		serie1.delete()
		serie2.delete()
		self.assertIsNotNone(series)
		self.assertEqual(len(series), 2)

	def test_getMaxEpisode(self):
		serie = Serie("test serie", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		self.assertEqual(serie.getMaxEpisode(), Episode(1, 3))

		serie = Serie("test serie", ["name 1", "name 2"])
		self.assertEqual(serie.getMaxEpisode(), None)

	def test_getMaxEpisodeOnAir(self):
		serie = Serie("test serie", ["name 1", "name 2"], [Episode(1, 1, datetime.date.today().strftime(Serie.dateformat)), Episode(1, 2), Episode(1, 3)])
		self.assertEqual(serie.getMaxEpisodeOnAir(), Episode(1, 1))

		serie = Serie("test serie", ["name 1", "name 2"], [Episode(1, 1), Episode(1, 2), Episode(1, 3)])
		self.assertEqual(serie.getMaxEpisodeOnAir(), None)

		serie = Serie("test serie", ["name 1", "name 2"])
		self.assertEqual(serie.getMaxEpisodeOnAir(), None)

if __name__ == '__main__':
	unittest.main()
	