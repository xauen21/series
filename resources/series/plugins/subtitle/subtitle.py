import importlib
import os
import requests
import uuid
import shutil

from resources.series.model.serie import Serie
from resources.series.common.utils import Utils
from resources.series.common.log import Log
from resources.series.common.code import Code

class Subtitle:
	@staticmethod
	def _getPath():
		return Utils.getDataDir() + "/subtitles"

	@staticmethod
	def updateSerie(serie, save = True):
		for episode in serie.episodes:
			if episode.subtitle: continue
			for plugin_module, plugin_class in Utils.getPlugins("subtitle").items():
				if plugin_class in serie.__dict__: names = [serie.__dict__[plugin_class]]
				else: names = serie.names
				for name in names:
					link, code = Subtitle.searchUrl(name, episode, plugin_module, plugin_class)
					Log.info(serie = name, season = episode.season, episode = episode.episode, plugin = plugin_class, code = code, message = "Searching subtitle.")
					if not link: continue
					
					episode.torrent = True
					serie.__dict__[plugin_class] = name
					if save: serie.write()
					break
				if episode.torrent: break
		
		return serie
	
	@staticmethod
	def download(serie, episode, plugin = ""):
		for plugin_module, plugin_class in Utils.getPlugins("subtitle", plugin).items():
			plugin_name = plugin_class.lower()
			if not plugin_name in episode.__dict__: return None, Code.notFound
			url = episode.__dict__[plugin_name]
			id = str(uuid.uuid4())
			working_dir = Subtitle._getPath() + "/" + id
			if not os.path.exists(working_dir): os.makedirs(working_dir)
			try:
				response = requests.get(url)
				if response.status_code != 200: return None, Subtitle.connectionError
				if "content-disposition" in response.headers: download_path =  working_dir + "/" + response.headers['content-disposition']
				elif "rar" in response.headers['Content-Type']: download_path = working_dir + "/" + id + ".rar"
				elif "zip" in response.headers['Content-Type']: download_path = working_dir + "/" + id + ".zip"
				else: download_path = working_dir + "/" + id + ".srt"
				
				with open(download_path, 'wb') as download_file: download_file.write(response.content)
				response.close()
				download_file.close()
			except:
				shutil.rmtree(working_dir)
				return None, Subtitle.connectionError
			
			subtitle_file = Subtitle.subtitles_path + "/" + serie.capitalize() + " S" + str(episode.season).zfill(2) + "E" + str(episode.episode).zfill(2)
			success = Utils.unpack(download_path, subtitle_file, working_dir)
			shutil.rmtree(working_dir)

			if success: return subtitle_file, Code.found
			else: return None, Code.notUnpack

	@staticmethod
	def searchUrl(name, episode, plugin_module, plugin_class):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchUrl(name, episode)

	@staticmethod
	def searchCandidates(name, episode, plugin_module, plugin_class):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchCandidates(name, episode)