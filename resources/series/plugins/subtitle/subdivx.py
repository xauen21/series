import requests
import re

from resources.series.common.utils import Utils
from resources.series.common.code import Code

class Subdivx:
	url = "https://www.subdivx.com/index.php"
	  
	@staticmethod
	def searchUrl(name, episode):
		parameters = (('buscar', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('accion', 5), ('oxdown', 1))
		return Utils.getFirstLink(url = Subdivx.url, parameters = parameters, pattern = "bajar.php")

	@staticmethod
	def searchCandidates(name, episode):
		candidates = []
	
		parameters = (('buscar', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('accion', 5), ('oxdown', 1))

		# SEARCH EPISODES
		content, code = Utils.getContent(url = Subdivx.url, parameters = parameters)
		links, code = Utils.getLinks(content = content, pattern = "bajar.php")
		if code != Code.found: return None, code
		
		details = re.findall('.*"buscador_detalle_sub".*', content)

		details = [(lambda detail: detail)(re.sub('<div id="buscador_detalle_sub">([^<^\\\]*)[\<]*.*', "\\1", detail)) for detail in details]
		candidates = dict(zip(links, details))
		return candidates, Code.found

