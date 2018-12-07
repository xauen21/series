import os

from resources.lib import jsonpickle
from resources.series.common.utils import Utils

jsonpickle.set_encoder_options( "json", sort_keys = False, indent = 4)

class Settings:
	def __init__(self):
		if not os.path.exists(Settings._getPath()): os.mkdir(Settings._getPath())
		settings_path = Settings._getPath() + "/settings.json"
		if os.path.exists(settings_path):
			with open(settings_path) as settings_file: settings_str = settings_file.read()
			self.__dict__ = jsonpickle.decode(settings_str).__dict__
		else:
			self.rpc_host = "localhost"
			self.rpc_port = "9091"
			self.rpc_user = ""
			self.rpc_password = ""
			self.write()
	
	@staticmethod
	def _getPath():
		return Utils.getDataDir()

	def __str__(self):
		return jsonpickle.encode(self)

	def get_transmission_params(self):
		params = {
			'address': self.rpc_host,
			'port': self.rpc_port,
			'user': self.rpc_user,
			'password': self.rpc_password,
		}
		return params

	def write(self):
		if not os.path.exists(Settings._getPath()): os.makedirs(Settings._getPath())
		settings_path = Settings._getPath() + "/settings.json"
		with open(settings_path, 'w') as settings_file: settings_file.write(jsonpickle.encode(self))