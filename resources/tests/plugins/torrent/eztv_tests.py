import unittest

from resources.series.model.episode import Episode
from resources.series.plugins.torrent.eztv import Eztv
from resources.series.plugins.torrent.torrent import Torrent
from resources.series.common.code import Code

class TestEztv(unittest.TestCase):
	@unittest.SkipTest
	def test_serarchUrlFound(self):
		link, code = Eztv.searchUrl("ncis", Episode(16,1))
		if (code != Code.connectionError):
			self.assertEqual(code, Code.found)
			self.assertIsNotNone(link)

	@unittest.SkipTest
	def test_serarchCandidates(self):
		links, code = Eztv.searchCandidates("ncis", Episode(16,1))
		if (code != Code.connectionError):
			self.assertGreaterEqual(len(links), 4)
	
	@unittest.SkipTest
	def test_serarchUrlNotFound(self):
		link, code = Eztv.searchUrl("ncis", Episode(1,199))
		if (code != Code.connectionError):
			self.assertEqual(code, Code.notFound)
			self.assertIsNone(link)

if __name__ == '__main__':
	unittest.main()