import importlib
import os 
import pkg_resources

from requests_html import HTMLSession
from series.model.serie import Serie
from pathlib import Path

class Subtitles:
	plugins_path = pkg_resources.resource_filename("series.plugins", "subtitles")

	@staticmethod
	def updateSerie(serie):
		names = serie.names

		if 'subdivx' in serie.__dict__:
			names = [serie.subdivx]

		for plugin_module, plugin_class in Subtitles.getPlugins().items():
			plugin_name = plugin_class.lower()
			if plugin_name in serie.__dict__:
				names = [serie.__dict__[plugin_name]]
			
			for name in names:
				for episode in serie.episodes:
					if plugin_module in episode.__dict__ or episode.watched:
						continue

					link, message = Subtitles.searchUrl(plugin_module, plugin_class, name, episode)
					print("[serie = " + name + "] [season = " + str(episode.season) + "] [episode = " + str(episode.episode) + "] [plugin = " + plugin_module + "] " + message)
					if not link:
						continue
					
					episode.__dict__[plugin_name] = link
					serie.__dict__[plugin_name] = name
			
				if plugin_name in episode.__dict__:
					break
			
			serie.write()
	
	@staticmethod
	def getPlugins():
		modules = {}
		plugin_files = os.listdir(Subtitles.plugins_path)
		plugin_names = list(filter(lambda x: "__" not in x and "subtitles.py" not in x, plugin_files))
		[(lambda x: x)(modules.update({"series.plugins.subtitles." + Path(x).stem: Path(x).stem.capitalize()})) for x in plugin_names]
		return modules

	@staticmethod
	def searchUrl(plugin_module, plugin_class, name, episode):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchUrl(name, episode)