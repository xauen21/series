import requests

from resources.series.common.utils import Utils
from resources.series.model.serie import Serie
from resources.series.plugins.torrent.torrent import Torrent
from resources.series.common.code import Code
import re

class Piratebay:
	url = "https://thepiratebay.icu/s/"

	@staticmethod
	def searchUrl(name, episode):
		parameters = (('q', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('orderby', 99))
		pattern =  "dn=" + name.replace(" ", "[\+\. _-]+") + "[\+\. _-]+s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)
		return Utils.getFirstLink(url = Piratebay.url, parameters = parameters, pattern = pattern)

	@staticmethod
	def searchCandidates(name, episode):
		candidates = []

		parameters = (('q', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('orderby', 99))

		# SEARCH EPISODES
		content, code = Utils.getContent(url = Piratebay.url, parameters = parameters)
		links, code = Utils.getLinks(content = content, pattern = "magnet", strict= True)
		if code != Code.found: return None, code
		
		details, code = Utils.getLinks(content = content, pattern = "/torrent/")
		if code != Code.found: return None, code
		
		details = [(lambda detail: detail)(re.sub('.*/', "", detail)) for detail in details]
		candidates = dict(zip(links, details))

		return candidates, Code.found

