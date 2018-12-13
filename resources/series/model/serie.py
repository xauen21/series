import os, importlib

from resources.lib import jsonpickle
from resources.series.model.episode import Episode
from resources.series.common.utils import Utils
from resources.series.common.log import Log
from resources.series.common.code import Code

jsonpickle.set_encoder_options( "json", sort_keys = False, indent = 4)

class Serie:
	dateformat = "%Y-%m-%d"

	def __init__(self, *args, **kwargs):
		if len(args) == 1: 
			self.id = args[0]
			self.__read__()
		if len(args) == 2:
			self.id = args[0]
			self.names = args[1]
			self.episodes = []
		if len(args) == 3:
			self.id = args[0]
			self.names = args[1]
			self.episodes = args[2]

	def __read__(self):
		if not os.path.exists(Serie._getPath()): os.mkdir(Serie._getPath())
		serie_path = Serie._getPath() + "/" + self.id + ".json"
		if not os.path.exists(Serie._getPath()):
			Log.debug(serie = self.id, message = serie_path, code = Code.notfound)
			self.id = None
			return False
		with open(serie_path) as serie_file: serie_str = serie_file.read()
		self.__dict__ = jsonpickle.decode(serie_str).__dict__
		Log.debug(serie = self.id, message = serie_path, code = Code.read)
		return True
	
	def __eq__(self, other):
		if not self.names == other.names:
			return False
		if not self.episodes == other.episodes:
			return False
		return True

	def __str__(self):
		return jsonpickle.encode(self)
	
	@staticmethod
	def _getPath():
		return Utils.getDataDir() + "/series"

	def write(self):
		if not os.path.exists(Serie._getPath()): os.makedirs(Serie._getPath())
		serie_path = Serie._getPath() + "/" + self.id + ".json"
		with open(serie_path, 'w') as serie_file: serie_file.write(jsonpickle.encode(self))
		Log.debug(serie = self.id, message = serie_path, code = Code.saved)
	
	def delete(self):
		if not os.path.exists(Serie._getPath()): os.makedirs(Serie._getPath())
		serie_path = Serie._getPath() + "/" + self.id + ".json"
		if not os.path.exists(serie_path): 
			Log.debug(serie = self.id, message = serie_path, code = Code.notFound)
			return False
		os.remove(serie_path)
		Log.debug(serie = self.id, message = serie_path, code = Code.deleted)
		return True

	def getMaxEpisode(self):
		if self.episodes: return max(self.episodes)
		return None

	def getEpisode(self, season, episode):
		try: 
			pos = self.episodes.index(Episode(season, episode))
			return self.episodes[pos]
		except:
			return None

	
	#def getMaxEpisodeOnAir(self):
	#	if not self.episodes: return None
	#	episodes = list(filter(lambda x: x.onair != False, self.episodes))
	#	if episodes: return max(list(filter(lambda x: x.onair != False, self.episodes)))
	#	return None
	
	def addEpisode(self, newEpisodes):
		if type(newEpisodes) is Episode: newEpisodes = [newEpisodes]
		if not type(newEpisodes) is list: return False

		maxEpisode = self.getMaxEpisode()
		if maxEpisode: newEpisodes = list(filter(lambda episode: maxEpisode < episode, newEpisodes))
		
		newEpisodes = list(filter(lambda episode: episode not in self.episodes, newEpisodes))
		if not newEpisodes: return False
		
		self.episodes.extend(newEpisodes)
		return 
		
	def updateEpisode(self, episode, subtitle = None, torrent = None):
		pos = self.episodes.index(episode)
		if subtitle: self.episodes[pos].subtitle = subtitle
		if torrent: self.episodes[pos].torrent = torrent
		self.write()

	@staticmethod
	def getSeries(onlyUnwatcher = True, onlyWitSubtitles = True, onlyWithTorrent = True):
		if not os.path.exists(Serie._getPath()): os.mkdir(Serie._getPath())
		series_files = os.listdir(Serie._getPath())
		series = [(lambda x: Serie(x))(os.path.basename(serie_file).replace(".json", "")) for serie_file in series_files]
		return series
	