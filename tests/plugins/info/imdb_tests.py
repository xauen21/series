import unittest

from series.plugins.info.imdb import Imdb
from series.plugins.info.info import Info

class TestImdb(unittest.TestCase):
	@unittest.SkipTest
	def test_searchEpisodesBySeasonFound(self):
		episodes, code = Imdb.searchEpisodesBySeason("criminal minds", 6)
		if (code != Info.connectionError):
			self.assertIsNotNone(episodes)
			self.assertEqual(len(episodes), 24)
			self.assertEqual(code, Info.found)

	@unittest.SkipTest
	def test_searchEpisodesBySeasonNotFound(self):
		episodes, code = Imdb.searchEpisodesBySeason("criminal minds", 20)
		if (code != Info.connectionError):
			self.assertIsNone(episodes)
			self.assertEqual(code, Info.notFound)

if __name__ == '__main__':
	unittest.main()