from requests_html import HTMLSession

from series.model.serie import Serie

class Piratebay:
	_url = "https://thepiratebay.icu/s/"

	@staticmethod
	def updateSerie(serie):
		names = serie.names

		if 'piratebay' in serie.__dict__:
			names = [serie.piratebay]

		for name in names:
			for episode in serie.episodes:
				if not 'piratebay' in episode.__dict__ and not episode.watched:
					link, message = Piratebay.searchUrl(name, episode)
					print(message)
					if link:
						episode.piratebay = link
						serie.piratebay = name
			if 'piratebay' in serie.__dict__:
				break
		serie.write()
	
	@staticmethod
	def searchUrl(name, episode):
		link = None
		message = ""
		try:
			parameters = (('q', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('orderby', 99))
			session = HTMLSession()
			response = session.get(Piratebay._url, params = parameters)
			message = response.url
			links = response.html.absolute_links
			session.close()
			links = list(links)
			link = list(filter(lambda link: "magnet" in link, links)).pop()
			message = message + " found donwload link"
		except:
			message = message + " not found donwload link"
		return link, message
