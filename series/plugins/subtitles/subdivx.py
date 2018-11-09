from requests_html import HTMLSession

from series.model.serie import Serie
from series.plugins.subtitles.subtitles import Subtitles

class Subdivx:
	url = "https://www.subdivx.com/index.php"
	
	@staticmethod
	def searchUrl(name, episode):
		parameters = (('buscar', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('accion', 5), ('oxdown', 1))
		session = HTMLSession()
		response = session.get(Subdivx.url, params = parameters)
		session.close()
		if response.status_code != 200: return None, Subtitles.connectionError
		
		links = response.html.absolute_links
		if not links: return None, Subtitles.notFound
		
		links = list(filter(lambda link: "bajar.php" in link, list(links)))
		if not links: return None, Subtitles.notFound
		
		return links.pop(), Subtitles.found
