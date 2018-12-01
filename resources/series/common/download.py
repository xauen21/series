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

class Download:
	@staticmethod
	def download(serie, episode):
		subtitle_link, torrent_link = Download.findSubTorrentLinks(serie, episode)

		subtitle_file, code = Subtitle.download(subtitle_link, serie, episode)
		if code == Code.found:
			serie.updateEpisode(episode, subtitle = subtitle_file)
			Log.info(serie = serie.id, season = episode.season, episode = episode.episode, code = code, message = "Downloading " + os.path.basename(subtitle_file))
		else:
			Log.error(serie = serie.id, season = episode.season, episode = episode.episode, code = code, message = "Downloading " + subtitle_link)

		torrent_file, code = Torrent.download(torrent_link, serie, episode)
		if code == Code.found:
			serie.updateEpisode(torrent = torrent_file)
			Log.info(serie = serie.id, season = episode.season, episode = episode.episode, code = code, message = "Downloading " + os.path.basename(torrent_file))
		else:
			Log.error(serie = serie.id, season = episode.season, episode = episode.episode, code = code, message = "Downloading " + torrent_link)

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
				Log.info(serie = sub_name, season = episode.season, episode = episode.episode, plugin = sub_class, code = code, message = "Searching subtitle cadidates")
				if code == Code.found: break

			for torrent_module, torrent_class in Utils.getPlugins("Torrent").items():
				if torrent_class in serie.__dict__: torrent_names = [serie.__dict__[torrent_class]]
				else: torrent_names = serie.names
				for torrent_name in torrent_names:
					torrent_name_list = re.split(" |_|\.|\-|\(|\)|\[|\]", torrent_name.lower())
					torrent_candidates, code = Torrent.searchCandidates(torrent_name, episode, torrent_module, torrent_class)
					Log.info(serie = torrent_name, season = episode.season, episode = episode.episode, plugin = sub_class, code = code, message = "Searching torrent cadidates")
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