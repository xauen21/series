import datetime
import importlib
import os, re

from resources.series.model.serie import Serie
from resources.series.model.serie import Episode
from resources.series.common.utils import Utils
from resources.series.common.log import Log
from resources.series.common.code import Code
from resources.series.plugins.subtitle.subtitle import Subtitle
from resources.series.plugins.torrent.torrent import Torrent

class Info:

	@staticmethod
	def updateSerie(serie, season = None, save = True, verbose = True):
		maxEpisode = serie.getMaxEpisode()
		if not season and maxEpisode: season = maxEpisode.season
		elif not season: season = 1
		
		for plugin_module, plugin_class in Utils.getPlugins("info").items():
			plugin_name = plugin_class.lower()
			
			if plugin_class in serie.__dict__: names = [serie.__dict__[plugin_class]]
			else: names = serie.names
			
			for name in names:
				episodes, code = Info.searchEpisodesBySeason(serie.id, name, season, plugin_module, plugin_class)
				Log.info(serie = serie.id, season = season, plugin = plugin_class, code = Code.found, message = "Searching info.")
				if code != Code.found: continue
				
				episodes.sort()
				serie.addEpisode(episodes)
				
				serie.__dict__[plugin_class] = name
				Info.updateSerie(serie, season + 1, save = save, verbose = verbose)
				break
			if not plugin_class in serie.__dict__:
				Log.error(serie = serie.id, season = season, plugin = plugin_class, code = Code.notFound, message = "Serie does not exist in this plugin")
		
		if save: serie.write()
		return serie
	
	@staticmethod
	def searchEpisodesBySeason(id, name, season, plugin_module, plugin_class):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchEpisodesBySeason(id, name, season)


	@staticmethod
	def findSubTorrentLinks(serie, episode):
		for sub_module, sub_class in Utils.getPlugins("Subtitle").items():
			sub_name_list = ()
			final_sub_link = ""
			final_torrent_link = ""

			if sub_class in serie.__dict__: sub_names = [serie.__dict__[sub_class]]
			else: sub_names = serie.names
			for sub_name in sub_names:
				sub_name_list = re.split(" |_|\.|\-|\(|\)|\[|\]", sub_name.lower())
				sub_candidates, code = Subtitle.searchCandidates(sub_name, episode, sub_module, sub_class)
				Log.info(serie = sub_name, season = episode.season, episode = episode.episode, plugin = sub_class, code = code, message = "Searching subtitle cadidates.")
				if code == Code.found: break

			for torrent_module, torrent_class in Utils.getPlugins("Torrent").items():
				if torrent_class in serie.__dict__: torrent_names = [serie.__dict__[torrent_class]]
				else: torrent_names = serie.names
				for torrent_name in torrent_names:
					torrent_name_list = re.split(" |_|\.|\-|\(|\)|\[|\]", torrent_name.lower())
					torrent_candidates, code = Torrent.searchCandidates(torrent_name, episode, torrent_module, torrent_class)
					Log.info(serie = torrent_name, season = episode.season, episode = episode.episode, plugin = sub_class, code = code, message = "Searching torrent cadidates.")
					if code != Code.found: continue
					
					final_intersections = 0
					for sub_link, sub_string in sub_candidates.items():
						sub_list = re.split(" |_|\.|\-|\(|\)|\[|\]", sub_string.lower())
						sub_list = set(x for x in sub_list if x != "" and x not in sub_name_list)
						for torrent_link, torrent_string in torrent_candidates.items():
							torrent_list = re.split(" |_|\.|\-|\(|\)|\[|\]", torrent_string.lower())
							torrent_list = set(x for x in torrent_list if x != "" and x not in torrent_name_list)
							intersections = len(sub_list.intersection(torrent_list))
							if intersections > final_intersections:
								final_sub_link = sub_link
								final_torrent_link = torrent_link
								final_intersections = intersections
					return final_sub_link, final_torrent_link
					break