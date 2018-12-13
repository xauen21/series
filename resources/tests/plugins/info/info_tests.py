import unittest
import datetime
import os

from resources.series.plugins.info.info import Info
from resources.series.model.serie import Serie
from resources.series.model.serie import Episode
from resources.series.common.log import Log
from resources.series.common.code import Code

class TestInfo(unittest.TestCase):
	@staticmethod
	def searchEpisodesBySeason(id, name, season, plugin_module, plugin_class):
		if (name == "name in imdb" and season == 1):
			return [Episode(1, 1), Episode(1, 2)], Code.found
		if (name == "name in imdb" and season == 2):
			return [Episode(2, 1), Episode(2, 2)], Code.found
		if (name == "name in imdb" and season == 3):
			return None, Code.notFound
		else: return None, Code.notFound
	
	@staticmethod
	def _getPath():
		return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + "/data/series"
	
	def setUp(self):
		Info.searchEpisodesBySeason = TestInfo.searchEpisodesBySeason
		Serie._getPath = TestInfo._getPath

	# check episodes are not searched if the las episode on air with date if newer or equal today
	#def test_onAirSearchTestNoNew(self):
	#	serie = Serie("test_onAirSearchTestNoNew", ["missing name in test", "name in imdb"], [Episode(1, 1, datetime.date.today().strftime(Serie.dateformat))])
	#	serie = Info.updateSerie(serie, save = False, verbose = False)
	#	self.assertEqual(len(serie.episodes), 1)

	# check episodes are searched if the las episode on air with date if older than today
	#def test_onAirSearchTestNew(self):
	#	serie = Serie("test_onAirSearchTestNew", ["missing name in test", "name in imdb"], [Episode(1, 1, "2001-01-01")])
	#	serie = Info.updateSerie(serie, save = False, verbose = False)
	#	self.assertEqual(len(serie.episodes), 4)
		
	# new serie search episodes
	def test_onSearchAllNew(self):
		serie = Serie("test_onSearchAllNew", ["missing name in test", "name in imdb"])
		serie = Info.updateSerie(serie, verbose = False)
		self.assertEqual(len(serie.episodes), 4)
		self.assertEqual(serie.__dict__["Imdb"], "name in imdb")

	# check episode 1x1 is not added again because is less than the current episodes in the serie
	def test_onSearchNotAddOld(self):
		serie = Serie("test_onSearchNotAddOld", ["missing name in test", "name in imdb"], [Episode(1, 2)])
		serie = Info.updateSerie(serie, save = False, verbose = False)
		self.assertEqual(len(serie.episodes), 3)
		self.assertNotIn(Episode(1, 1), serie.episodes)

if __name__ == '__main__':
	unittest.main()