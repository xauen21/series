import unittest

from resources.series.common.utils import Utils

class TestUtils(unittest.TestCase):
	def test_getPlugins(self):
		plugins = Utils.getPlugins("info", "imdb")
		self.assertEqual(plugins['resources.series.plugins.info.imdb'],'Imdb')

if __name__ == '__main__':
	unittest.main()
	