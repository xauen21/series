import unittest

from series.model.episode import Episode
from series.plugins.subtitles.subdivx import Subdivx
from series.plugins.subtitles.subtitles import Subtitles

class TestSubdivx(unittest.TestCase):
	def test_serarchUrlFound(self):
		link, code = Subdivx.searchUrl("ncis", Episode(1,1))
		if (code != Subtitles.connectionError):
			self.assertEqual(code, Subtitles.found)
			self.assertIsNotNone(link)

	def test_serarchUrlNotFound(self):
		link, code = Subdivx.searchUrl("ncis", Episode(1,199))
		if (code != Subtitles.connectionError):
			self.assertEqual(code, Subtitles.notFound)
			self.assertIsNone(link)

if __name__ == '__main__':
	unittest.main()