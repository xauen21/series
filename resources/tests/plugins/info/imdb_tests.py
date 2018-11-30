import unittest

from resources.series.plugins.info.imdb import Imdb
from resources.series.plugins.info.info import Info
from resources.series.common.code import Code

class TestImdb(unittest.TestCase):
	@unittest.SkipTest
	def test_searchEpisodesBySeasonFound(self):
		episodes, code = Imdb.searchEpisodesBySeason("criminal minds", 6)
		if (code != Code.connectionError):
			self.assertIsNotNone(episodes)
			self.assertEqual(len(episodes), 24)
			self.assertEqual(code, Code.found)

	@unittest.SkipTest
	def test_searchEpisodesBySeasonNotFound(self):
		episodes, code = Imdb.searchEpisodesBySeason("criminal minds", 20)
		if (code != Code.connectionError):
			self.assertIsNone(episodes)
			self.assertEqual(code, Code.notFound)

if __name__ == '__main__':
	unittest.main()