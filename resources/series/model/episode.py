import json
from resources.lib.jsonpickle import jsonpickle
from resources.series.common.code import Code

class Episode:
	def __init__(self, season = -1, episode = -1, onair = False, watched = False):
		self.season = season
		self.episode = episode
		self.subtitle = False
		self.torrent = False
		self.watched = watched

	def __str__(self):
		return jsonpickle.encode(self)

	def __eq__(self, other):
		if not self.season == other.season or not self.episode == other.episode: return False
		return True

	def __ne__(self, other):
		if self.season != other.season or self.episode != other.episode: return True
		return False

	def __lt__(self, other):
		if self.season < other.season: return True
		elif self.season == other.season and self.episode < other.episode: return True
		return False

	def __gt__(self, other):
		if self.season > other.season: return True
		elif self.season == other.season and self.episode > other.episode: return True
		return False

	def __le__(self, other):
		if self.season <= other.season and self.episode <= other.episode: return True
		return False

	def __ge__(self, other):
		if self.season >= other.season and self.episode >= other.episode: return True
		return False
