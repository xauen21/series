import unittest

from resources.series.model.episode import Episode
from resources.series.plugins.subtitle.subdivx import Subdivx
from resources.series.plugins.subtitle.subtitle import Subtitle
from resources.series.common.code import Code

class TestSubdivx(unittest.TestCase):
	@unittest.SkipTest
	def test_serarchUrlFound(self):
		link, code = Subdivx.searchUrl("ncis", Episode(1,1))
		if (code != Subtitle.connectionError):
			self.assertEqual(code, Code.found)
			self.assertIsNotNone(link)
	
	@unittest.SkipTest
	def test_serarchUrlNotFound(self):
		link, code = Subdivx.searchUrl("ncis", Episode(1,199))
		if (code != Subtitle.connectionError):
			self.assertEqual(code, Code.notFound)
			self.assertIsNone(link)

if __name__ == '__main__':
	unittest.main()