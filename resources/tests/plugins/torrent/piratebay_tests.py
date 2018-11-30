import unittest

from resources.series.model.episode import Episode
from resources.series.plugins.torrent.piratebay import Piratebay
from resources.series.plugins.torrent.torrent import Torrent
from resources.series.common.code import Code

class TestPiratebay(unittest.TestCase):
	@unittest.SkipTest
	def test_serarchUrlFound(self):
		link, code = Piratebay.searchUrl("ncis", Episode(1,1))
		if (code != Code.connectionError):
			self.assertEqual(code, Code.found)
			self.assertIsNotNone(link)
	
	@unittest.SkipTest
	def test_serarchUrlNotFound(self):
		link, code = Piratebay.searchUrl("ncis", Episode(1,199))
		if (code != Code.connectionError):
			self.assertEqual(code, Code.notFound)
			self.assertIsNone(link)

if __name__ == '__main__':
	unittest.main()