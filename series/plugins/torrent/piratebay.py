from requests_html import HTMLSession

from series.model.serie import Serie
from series.plugins.torrent.torrent import Torrent

class Piratebay:
	url = "https://thepiratebay.icu/s/"

	@staticmethod
	def searchUrl(name, episode):
		parameters = (('q', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('orderby', 99))
		session = HTMLSession()
		response = session.get(Piratebay.url, params = parameters)
		session.close()
		if response.status_code != 200: return None, Torrent.connectionError
		
		links = response.html.absolute_links
		if not links: return None, Torrent.notFound
		
		links = list(filter(lambda link: "magnet" in link, list(links)))
		if not links: return None, Torrent.notFound
		
		return links.pop(), Torrent.found