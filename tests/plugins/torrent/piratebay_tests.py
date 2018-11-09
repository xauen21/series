import unittest

from series.model.episode import Episode
from series.plugins.torrent.piratebay import Piratebay
from series.plugins.torrent.torrent import Torrent

class TestPiratebay(unittest.TestCase):
	def test_serarchUrlFound(self):
		link, code = Piratebay.searchUrl("ncis", Episode(1,1))
		if (code != Torrent.connectionError):
			self.assertEqual(code, Torrent.found)
			self.assertIsNotNone(link)

	def test_serarchUrlNotFound(self):
		link, code = Piratebay.searchUrl("ncis", Episode(1,199))
		if (code != Torrent.connectionError):
			self.assertEqual(code, Torrent.notFound)
			self.assertIsNone(link)

if __name__ == '__main__':
	unittest.main()