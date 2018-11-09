from requests_html import HTMLSession

from series.model.serie import Serie

class Subdivx:
	url = "https://www.subdivx.com/index.php"

	@staticmethod
	def updateSerie(serie):
		names = serie.names

		if 'subdivx' in serie.__dict__:
			names = [serie.subdivx]

		for name in names:
			for episode in serie.episodes:
				if not 'subdivx' in episode.__dict__ and not episode.watched:
					link, message = Subdivx.searchUrl(name, episode)
					print(message)
					if link:
						episode.subdivx = link
						serie.subdivx = name
			if 'subdivx' in serie.__dict__:
				break
		serie.write()
	
	@staticmethod
	def searchUrl(name, episode):
		link = None
		message = ""
		try:
			parameters = (('buscar', name + " s" + str(episode.season).zfill(2) + "e" + str(episode.episode).zfill(2)), ('accion', 5), ('oxdown', 1))
			session = HTMLSession()
			response = session.get(Subdivx.url, params = parameters)
			message = response.url
			links = response.html.absolute_links
			session.close()
			links = list(links)
			link = list(filter(lambda link: "bajar.php" in link, links)).pop()
			message = message + " found donwload link"
		except:
			message = message + " not found donwload link"
		return link, message
