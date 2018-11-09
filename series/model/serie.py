import jsonpickle
import os
import pkg_resources

from series.model.episode import Episode
from pathlib import Path

jsonpickle.set_encoder_options( "json" , sort_keys = False , indent = 4 )
series_path = pkg_resources.resource_filename("data", "series")

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
		serie_path = series_path + "/" + self.id + ".json"
		if not os.path.exists(serie_path): return False
		with open(series_path + "/" + self.id + ".json") as serie_file: serie_str = serie_file.read()
		self.__dict__ = jsonpickle.decode(serie_str).__dict__
		return True
	
	def __eq__(self, other):
		if not self.names == other.names:
			return False
		if not self.episodes == other.episodes:
			return False
		return True

	def __str__(self):
		return jsonpickle.encode(self)

	def write(self):
		if not os.path.exists(series_path): os.mkdir(series_path)
		with open(series_path + "/" + self.id + ".json", 'w') as serie_file: serie_file.write(jsonpickle.encode(self))
	
	def delete(self):
		serie_path = series_path + "/" + self.id + ".json"
		if not os.path.exists(serie_path): return False
		os.remove(serie_path)
		return True

	def getMaxEpisode(self):
		if self.episodes: return max(self.episodes)
		return None

	def getMaxEpisodeOnAir(self):
		if not self.episodes: return None
		episodes = list(filter(lambda x: x.onair != False, self.episodes))
		if episodes: return max(list(filter(lambda x: x.onair != False, self.episodes)))
		return None
	
	def addEpisode(self, newEpisodes):
		if type(newEpisodes) is Episode: newEpisodes = [newEpisodes]
		if not type(newEpisodes) is list: return False
		
		maxEpisode = self.getMaxEpisode()
		if maxEpisode: newEpisodes = list(filter(lambda episode: maxEpisode < episode, newEpisodes))
		
		newEpisodes = list(filter(lambda episode: episode not in self.episodes, newEpisodes))
		if not newEpisodes: return False
		
		self.episodes.extend(newEpisodes)
		return True

	@staticmethod
	def getSeries():
		series_files = os.listdir(series_path)
		series = [(lambda x: Serie(x))(Path(serie_file).stem) for serie_file in series_files]
		return series
	

