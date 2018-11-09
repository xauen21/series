import unittest
import datetime

from series.plugins.info.info import Info
from series.model.serie import Serie
from series.model.serie import Episode

class TestInfo(unittest.TestCase):
	@staticmethod
	def searchEpisodesBySeason(plugin_module, plugin_class, name, season):
		if (name == "name in imdb" and season == 1):
			return [Episode(1, 1), Episode(1, 2)], Info.found
		if (name == "name in imdb" and season == 2):
			return [Episode(2, 1), Episode(2, 2)], Info.found
		if (name == "name in imdb" and season == 3):
			return None, Info.notFound
		else: return None, Info.connectionError
	
	def setUp(self):
		Info.searchEpisodesBySeason = TestInfo.searchEpisodesBySeason

	# check episodes are not searched if the las episode on air with date if newer or equal today
	def test_onAirSearchTestNoNew(self):
		serie = Serie("info test serie", ["missing name in test", "name in imdb"], [Episode(1, 1, datetime.date.today().strftime(Serie.dateformat))])
		serie = Info.updateSerie(serie, save = False, verbose = False)
		self.assertEqual(len(serie.episodes), 1)

	# check episodes are searched if the las episode on air with date if older than today
	def test_onAirSearchTestNew(self):
		serie = Serie("info test serie", ["missing name in test", "name in imdb"], [Episode(1, 1, "2001-01-01")])
		serie = Info.updateSerie(serie, save = False, verbose = False)
		self.assertEqual(len(serie.episodes), 4)
		
	# new serie search episodes
	def test_onSearchAllNew(self):
		serie = Serie("info test serie", ["missing name in test", "name in imdb"])
		serie = Info.updateSerie(serie, save = False, verbose = False)
		self.assertEqual(len(serie.episodes), 4)
		self.assertEqual(serie.__dict__["imdb"], "name in imdb")

	# check episode 1x1 is not added again because is less than the current episodes in the serie
	def test_onSearchNotAddOld(self):
		serie = Serie("info test serie", ["missing name in test", "name in imdb"], [Episode(1, 2)])
		serie = Info.updateSerie(serie, save = False, verbose = False)
		self.assertEqual(len(serie.episodes), 3)
		self.assertNotIn(Episode(1, 1), serie.episodes)

if __name__ == '__main__':
	unittest.main()