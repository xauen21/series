import unittest

from series.model.episode import Episode
from series.model.serie import Serie
from series.plugins.subtitles.subdivx import Subdivx

class TestSubdivx(unittest.TestCase):
	def test_update_serie(self):
		Subdivx.updateSerie(Serie("criminal minds"))

	def test_serarch_url(self):
		link = Subdivx.searchUrl("ncis", Episode(1,1))
		self.assertIsNotNone(link)

if __name__ == '__main__':
	unittest.main()