import importlib
import os 
import pkg_resources
import requests
import uuid
import patoolib
import shutil

from series.model.serie import Serie
from pathlib import Path

class Torrent:
	plugins_path = pkg_resources.resource_filename("series.plugins", "torrent")
	torrents_path = pkg_resources.resource_filename("data", "torrents")
	found = "Magnet found."
	notFound = "Magnet not found"
	connectionError = "Connection error"

	@staticmethod
	def updateSerie(serie, save = True, verbose = True):
		for plugin_module, plugin_class in Torrent.getPlugins().items():
			plugin_name = plugin_class.lower()
			if plugin_name in serie.__dict__: names = [serie.__dict__[plugin_name]]
			else: names = serie.names
			
			for name in names:
				for episode in serie.episodes:
					if plugin_module in episode.__dict__: continue
					
					link, code = Torrent.searchUrl(plugin_module, plugin_class, name, episode)
					if verbose: print("[serie = " + name + "] [episode = " + str(episode.season) + "x" + str(episode.episode) + "] [plugin = " + plugin_module + "] " + code)
					if not link: continue
					
					episode.__dict__[plugin_name] = link
					serie.__dict__[plugin_name] = name

				if plugin_name in episode.__dict__:
					break
			
			if save: serie.write()
		
		return serie
	
	@staticmethod
	def download(episode, plugin = None):
		for plugin_module, plugin_class in Torrent.getPlugins(plugin).items():
			plugin_name = plugin_class.lower()
			if not plugin_name in episode.__dict__: return None
			url = episode.__dict__[plugin_name]
			response = requests.get(url)
			if response.status_code != 200: return None
			
			id = str(uuid.uuid4())
			working_dir = Torrent.subtitles_path + "/" + id
			if not os.path.exists(working_dir): os.makedirs(working_dir)
			
			if "content-disposition" in response.headers: download_path =  working_dir + "/" + response.headers['content-disposition']
			elif "rar" in response.headers['Content-Type']: download_path = working_dir + "/" + id + ".rar"
			elif "zip" in response.headers['Content-Type']: download_path = working_dir + "/" + id + ".zip"
			else: download_path = working_dir + "/" + id + ".srt"
			
			with open(download_path, 'wb') as download_file: download_file.write(response.content)
			response.close()
			download_file.close()
			
			# rar
			os.environ["PATH"] = os.environ["PATH"] + ";" + pkg_resources.resource_filename("7z", "App") + "/7-Zip"
			patoolib.extract_archive(download_path, outdir = working_dir, verbosity = -1)
			for srt_file in os.listdir(working_dir):
				if ".srt" in srt_file:
					shutil.move(working_dir + "/" + srt_file, Torrent.subtitles_path + "/" + Path(srt_file).name)
					subtitle_file = Torrent.subtitles_path + "/" + Path(srt_file).name
					break
			
			shutil.rmtree(working_dir)
			return subtitle_file
	
	@staticmethod
	def getPlugins(plugin = None):
		modules = {}
		plugin_files = os.listdir(Torrent.plugins_path)
		plugin_names = list(filter(lambda x: "__" not in x and "torrent.py" not in x and (not plugin or plugin + ".py" == x), plugin_files))
		[(lambda x: x)(modules.update({"series.plugins.torrent." + Path(x).stem: Path(x).stem.capitalize()})) for x in plugin_names]
		return modules

	@staticmethod
	def searchUrl(plugin_module, plugin_class, name, episode):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchUrl(name, episode)