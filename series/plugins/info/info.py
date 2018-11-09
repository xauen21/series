import datetime
import importlib
import pkg_resources
import os

from series.model.serie import Serie
from series.model.serie import Episode
from pathlib import Path

class Info:
	plugins_path = pkg_resources.resource_filename("series.plugins", "info")
	found = "Episodes found."
	notFound = "Episodes not found"
	connectionError = "Connection error"

	@staticmethod
	def updateSerie(serie, season = None, save = True, verbose = True):
		# not search episodes if the last episode with date is not onair
		maxEpisodeOnAir = serie.getMaxEpisodeOnAir()
		today = datetime.date.today().strftime(Serie.dateformat)
		if maxEpisodeOnAir and maxEpisodeOnAir.onair != "N/A" and maxEpisodeOnAir.onair >= today: return serie
		
		maxEpisode = serie.getMaxEpisode()
		if not season and maxEpisode: season = maxEpisode.season
		elif not season: season = 1
		
		for plugin_module, plugin_class in Info.getPlugins().items():
			plugin_name = plugin_class.lower()
			if plugin_name in serie.__dict__: names = [serie.__dict__[plugin_name]]
			else: names = serie.names
			
			for name in names:
				episodes, code = Info.searchEpisodesBySeason(plugin_module, plugin_class, name, season)
				if verbose: print("[serie = " + name + "] [season = " + str(season) + "] [plugin = " + plugin_module + "] " + code)
				serie.addEpisode(episodes)
				if not episodes: continue
				
				serie.__dict__[plugin_name] = name
				Info.updateSerie(serie, season + 1, save = save, verbose = verbose)
				break
		
		if save: serie.write()
		return serie
	
	@staticmethod
	def getPlugins():
		modules = {}
		plugin_files = os.listdir(Info.plugins_path)
		plugin_names = list(filter(lambda x: "__" not in x and "info.py" not in x, plugin_files))
		[(lambda x: x)(modules.update({"series.plugins.info." + Path(x).stem: Path(x).stem.capitalize()})) for x in plugin_names]
		return modules

	@staticmethod
	def searchEpisodesBySeason(plugin_module, plugin_class, name, season):
		plugin_module = importlib.import_module(plugin_module)
		plugin_class = getattr(plugin_module, plugin_class)
		return plugin_class.searchEpisodesBySeason(name, season)


