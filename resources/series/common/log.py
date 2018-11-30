import logging

class Level:
	# Level codes
	error = "error"
	info = "info"
	debug = "debug"
	warning = "warning"
	trace = "trace"

class Log:

	@staticmethod
	def debug(message = None, code = None, serie = None, season = None, episode = None, plugin = None): 
		Log.__log(Level.debug, message, code, serie, season, episode, plugin)

	@staticmethod
	def info(message = None, code = None, serie = None, season = None, episode = None, plugin = None): 
		Log.__log(Level.info, message, code, serie, season, episode, plugin)

	@staticmethod
	def error(message = None, code = None, serie = None, season = None, episode = None, plugin = None): 
		Log.__log(Level.error, message, code, serie, season, episode, plugin)

	@staticmethod
	def warning(message = None, code = None, serie = None, season = None, episode = None, plugin = None): 
		Log.__log(Level.warning, message, code, serie, season, episode, plugin)


	@staticmethod
	def trace(message = None, code = None, serie = None, season = None, episode = None, plugin = None): 
		Log.__log(Level.trace, message, code, serie, season, episode, plugin)
	
	@staticmethod
	def __log(level, message = None, code = None, serie = None, season = None, episode = None, plugin = None):
		if episode: episode = str(episode).zfill(2)
		if season: season = str(season).zfill(2)
		if not code: code = ""
		if not serie: serie = ""
		if not plugin: plugin = ""
		if not season: season = ""
		if not episode: episode = ""
		text = "[" + level.capitalize().ljust(7) + "] "
		text += "[serie" + " = " + serie.capitalize().ljust(20) + "] "
		text += "[season" + " = " + season.ljust(2) + "] "
		text += "[episode" + " = " + episode.ljust(2) + "] "
		text += "[plugin" + " = " + plugin.capitalize().ljust(10) + "] "
		text += "[code" + " = " + code.capitalize().ljust(20) + "] "
		if message: text += "[message".ljust(8) + " = " + message.capitalize() + "] "
		#if Level.info.lower() in level.lower():
		#	logging.info(message)
		#if Level.debug.lower() in level.lower():
		#	logging.debug(message)
		#if Level.error.lower() in level.lower():
		#	logging.error(message)
		#if Level.warning.lower() in level.lower():
		#	logging.warning(message)
		if level != Level.trace: print(text)