import requests

from resources.series.common.utils import Utils
from resources.series.model.serie import Serie
from resources.series.plugins.torrent.torrent import Torrent
from resources.series.common.code import Code
import re
import urllib

class Eztv:
	url = "https://eztv.io/search/"

	@staticmethod
	def searchUrl(name, episode):
		parameters = ()
		url = Eztv.url + name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)
		pattern =  "dn=" + name.replace(" ", "[\+\. _-]+") + "[\+\. _-]+s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)
		return Utils.getFirstLink(url = url, pattern = pattern)

	@staticmethod
	def searchCandidates(name, episode):
		candidates = []
		parameters = ()

		url = Eztv.url + name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)
		pattern =  "dn=" + name.replace(" ", "[\+\. _-]+") + "[\+\. _-]+s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)
		links, code = Utils.getLinks(url = url, pattern = pattern)
		if code != Code.found: return None, code
		
		details = links
		
		details = [(lambda detail: detail)(urllib.parse.unquote(detail)) for detail in details]
		details = [(lambda detail: detail)(re.sub('.*dn=', "", detail)) for detail in details]
		details = [(lambda detail: detail)(re.sub('&.*', "", detail)) for detail in details]
		candidates = dict(zip(links, details))
		
		return candidates, Code.found

