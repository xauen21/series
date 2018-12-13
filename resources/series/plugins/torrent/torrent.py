import importlib
import os 
import requests
import uuid
import shutil
import transmissionrpc

from resources.series.model.serie import Serie
from resources.series.common.utils import Utils
from resources.series.common.log import Log
from resources.series.common.code import Code
from resources.series.common.settings import Settings

class Torrent:
	transmissionClient = None

	@staticmethod
	def _getPath():
		return Utils.getDataDir() + "/torrents"
	
	@staticmethod
	def updateSerie(serie, save = True, verbose = True):
		for episode in serie.episodes:
			if episode.torrent: continue
			for plugin_module, plugin_class in Utils.getPlugins("torrent").items():
				if plugin_class in serie.__dict__: 
					names = list(serie.names)
					names.remove(serie.__dict__[plugin_class])
					names.insert(0, serie.__dict__[plugin_class])
				else: names = serie.names
				for name in names:
					link, code = Torrent.searchUrl(name, episode, plugin_module, plugin_class)
					Log.info(serie = name, season = episode.season, episode = episode.episode, plugin = plugin_class, code = code, message = "Searching torrent")
					if not link: continue
					
					episode.torrent = True
					serie.__dict__[plugin_class] = name
					if save: serie.write()
					break
				if episode.torrent: break
		
		return serie
	
	@staticmethod
	def searchUrl(name, episode, plugin_module, plugin_class):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchUrl(name, episode)


	@staticmethod
	def searchCandidates(serie, episode, plugin_module = None, plugin_class = None):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchCandidates(serie, episode)

	@staticmethod
	def getClient():
		if Torrent.transmissionClient == None:
			params = Settings().get_transmission_params()
			Torrent.transmissionClient = transmissionrpc.Client(**params)
		return Torrent.transmissionClient


	@staticmethod
	def download(url, serie, episode):
		try:
			return Torrent.getClient().add_torrent(url), Code.found
		except:
			return None, Code.notFound