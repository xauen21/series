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
			if plugin_class in serie.__dict__: names = [serie.__dict__[plugin_class]]
			else: names = serie.names
			if plugin_class in serie.__dict__: 
				names = list(serie.names)
				names.remove(serie.__dict__[plugin_class])
				names.insert(0, serie.__dict__[plugin_class])
			else: names = serie.names
			
			for name in names:
				episodes, code = Info.searchEpisodesBySeason(serie.id, name, season, plugin_module, plugin_class)
				Log.info(serie = serie.id, season = season, plugin = plugin_class, code = Code.found, message = "Searching info")
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
