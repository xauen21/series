import requests
import datetime
import json

from series.model.serie import Episode
from series.plugins.info.info import Info

class Imdb:
	apikey = "e59be340"
	url = "http://www.omdbapi.com/"

	@staticmethod
	def searchEpisodesBySeason(name, season):
		episodes = []
		
		parameters = (('apikey', Imdb.apikey), ('t', name), ('Season', season))
		response = requests.get(Imdb.url, params = parameters)
		if response.status_code != 200: return None, Info.connectionError
		
		information = response.json()
		if information["Response"] == "False": return None, Info.notFound
		
		for episodeJson in information["Episodes"]:
			episode = Episode(season, int(episodeJson["Episode"]))
			episode.onair = episodeJson["Released"]
			episodes.append(episode)
		
		return episodes, Info.found