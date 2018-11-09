import unittest

from series.model.episode import Episode

class TestEpisode(unittest.TestCase):
	def test_episodeOperators(self):
		self.assertTrue(Episode(1, 1) == Episode(1, 1))
		self.assertFalse(Episode(1, 1) == Episode(1, 2))
		self.assertFalse(Episode(1, 2) == Episode(1, 1))

		self.assertFalse(Episode(1, 1) < Episode(1, 1))
		self.assertTrue(Episode(1, 1) < Episode(1, 2))
		self.assertFalse(Episode(1, 2) < Episode(1, 1))

		self.assertFalse(Episode(1, 1) > Episode(1, 1))
		self.assertFalse(Episode(1, 1) > Episode(1, 2))
		self.assertTrue(Episode(1, 2) > Episode(1, 1))

		self.assertFalse(Episode(1, 1) != Episode(1, 1))
		self.assertTrue(Episode(1, 1) != Episode(1, 2))
		self.assertTrue(Episode(1, 2) != Episode(1, 1))

		self.assertTrue(Episode(1, 1) >= Episode(1, 1))
		self.assertFalse(Episode(1, 1) >= Episode(1, 2))
		self.assertTrue(Episode(1, 2) >= Episode(1, 1))

		self.assertTrue(Episode(1, 1) <= Episode(1, 1))
		self.assertTrue(Episode(1, 1) <= Episode(1, 2))
		self.assertFalse(Episode(1, 2) <= Episode(1, 1))

if __name__ == '__main__':
	unittest.main()
	