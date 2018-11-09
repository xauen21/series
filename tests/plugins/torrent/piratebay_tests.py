import unittest

from series.model.episode import Episode
from series.model.serie import Serie
from series.plugins.torrent.piratebay import Piratebay

class TestSubdivx(unittest.TestCase):
	def test_update_serie(self):
		Piratebay.updateSerie(Serie("criminal minds"))

	def test_serarch_url(self):
		link = Piratebay.searchUrl("ncis", Episode(1,1))
		self.assertIsNotNone(link)

if __name__ == '__main__':
	unittest.main()