import requests
import datetime
import json
import re

from resources.series.model.serie import Episode
from resources.series.plugins.info.info import Info
from resources.series.common.code import Code
from resources.series.common.utils import Utils

class Imdb:
	url = "https://www.imdb.com/"

	@staticmethod
	def searchEpisodesBySeason(id, name, season):
		episodes = []
		
		# SEARCH SERIE CODE IN IMDB
		parameters = (('title', name), ('title_type', 'tv_series,tv_miniseries'), ('view', "simple"))
		link, code = Utils.getFirstLink(url = Imdb.url + "search/title", parameters = parameters, pattern = "adv_li_tt")
		if code != Code.found: return None, code
		imdb_id = link.split("/")[2]

		# SEARCH EPISODES
		parameters = (('season', season), ('ref_', 'tt_eps_sn_' + str(season)))
		content, code = Utils.getContent(Imdb.url + "title/" + imdb_id + "/episodes", parameters = parameters)
		if code == Code.connectionError: return None, code
		if not "Season " + str(season) in content: return None, Code.notFound
		links, code = Utils.getLinks(content = content, parameters = parameters, pattern = "ttep_ep[0-9]+")
		if code != Code.found: return None, code
		for link in list(set(links)):
			episode = Episode(season, int(re.sub(".*ttep_ep", "", link)))
			episodes.append(episode)
		
		return episodes, Code.found