import datetime
import importlib
import os, inspect, sys
import shutil
import imp
import re
import requests

from requests.utils import quote
from resources.series.common.log import Log
from resources.series.common.code import Code

class Utils:
	@staticmethod
	def getName(path):
		return os.path.basename(path).replace(".py","")

	@staticmethod
	def getPluginElement(path, file):
		return {path + "." + Utils.getName(file): Utils.getName(file).capitalize()}

	@staticmethod
	def getDataDir():
		return  Utils.getResourcesDir() + "/data"

	@staticmethod
	def getResourcesDir():
		return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

	@staticmethod
	def getPlugins(type, plugin = ""):
		modules = {}
		type = type.lower()
		url = "resources.series.plugins." + type
		type_url = url + "." + type
		module = importlib.import_module(type_url)
		path = os.path.dirname(module.__file__)
		files = os.listdir(path)
		filters = [type, "__", ".pyo"]
		files = list(filter(lambda file: plugin in file and not any(elem in file for elem in filters), files))
		[(lambda file: file)(modules.update(Utils.getPluginElement(url, file))) for file in files]
		return modules

	@staticmethod
	def getLinks(url = None, parameters = None, content = None, pattern = ""):
		try: 
			if not content: 
				content, code = Utils.getContent(url, parameters)
				if not code == Code.connectionSuccess: return None, code
			links = re.findall('<a [^>]*' + pattern + '[^>]*>', content)
			links = [(lambda link: link)(re.sub('<a [^>]*href="([^>"]*' + pattern + '[^>"]*)"[^>]*>', "\\1", link)) for link in links]
			if links and len(links): 
				if url: message = "Links found in " + url + " with pattern " + pattern
				else: message = "Links found with pattern " + pattern
				Log.trace(code = Code.found, message = message)
				return links, Code.found
			else: raise Exception(Code.notFound)
		except Exception as ex:
			if url: message = "Links found in " + url + " with pattern " + pattern
			else: message = "Links found with pattern " + pattern
			Log.trace(code = Code.notFound, message = message)
			return None, Code.notFound
	
	@staticmethod
	def getFirstLink(url = None, parameters = None, content = None, pattern = ""):
		links, code = Utils.getLinks(url, parameters, content, pattern)
		if not code == Code.found: return None, code
		return links[0], code
	
	@staticmethod
	def getContent(url, parameters, json = False):
		try: 
			response = requests.get(url, params = parameters)
			Log.debug(code = Code.connectionSuccess, message = "Connected to " + response.url)
			if json: return response.json(), Log.connectionSuccess
			else: return response.text, Code.connectionSuccess
		except Exception as ex:
			print(ex)
			Log.trace(code = Code.connectionError, message = url)
			return None, Code.connectionError

	@staticmethod
	def unpack(input, output, working_dir):
		subtitle_file = None

		try:
			import xbmc, xbmcvfs
			from urllib import quote_plus
			if ".rar" in input:
				src = 'archive' + '://' + quote_plus(input) + '/'
				(cdirs, cfiles) = xbmcvfs.listdir(src)
				for cfile in cfiles:
					fsrc = '%s%s' % (src, cfile)
					xbmcvfs.copy(fsrc, working_dir + cfile)
			else:
				xbmc.executebuiltin("XBMC.Extract(%s, %s)" % (input.encode("utf-8"), working_dir.encode("utf-8")), True)
		except:
			try:
				import patoolib
				os.environ["PATH"] += os.pathsep + Utils.getResourcesDir() + "/7z/App/7-Zip"
				patoolib.extract_archive(input, outdir = working_dir, verbosity = -1)
			except:
				pass
		
		files = os.listdir(working_dir)
		for srt_file in files:
			if ".srt" in srt_file:
				shutil.move(working_dir + "/" + srt_file, output)
				subtitle_file = output

		if subtitle_file: return True
		else: return False