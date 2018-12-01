import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
from resources.series.model.serie import Serie
from resources.series.plugins.info.info import Info
from resources.series.plugins.subtitle.subtitle import Subtitle
from resources.series.plugins.torrent.torrent import Torrent

_url = sys.argv[0]
_handle = int(sys.argv[1])

def get_url(**kwargs):
	return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_series():
	xbmcplugin.setPluginCategory(_handle, 'My Series Collection')
	xbmcplugin.setContent(_handle, 'videos')
	for serie in Serie.getSeries():
		list_item = xbmcgui.ListItem(label = serie.id.capitalize())
		url = get_url(action = 'listing', serie = serie.id)
		xbmcplugin.addDirectoryItem(_handle, url, list_item, True)
	xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.endOfDirectory(_handle)


def list_episodes(serie):
	xbmcplugin.setPluginCategory(_handle, serie)
	xbmcplugin.setContent(_handle, 'videos')
	serie = Serie(serie)
	for episode in serie.episodes:
		name = serie.id.capitalize() + " S" + str(episode.season).zfill(2) + "E" + str(episode.episode).zfill(2)
		if episode.subtitle: name += " (S)"
		if episode.torrent: name += " (T)"
		list_item = xbmcgui.ListItem(label = name)
		#list_item.setInfo('video', {'title': name, 'mediatype': 'video'})
		#list_item.setProperty('IsPlayable', 'true')
		url = get_url(action = 'download', serie = serie.id, season = episode.season, episode = episode.episode)
		xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
	xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
	xbmcplugin.endOfDirectory(_handle)

def download_episode(serie, season, episode):
	return

def play_video(path):
	play_item = xbmcgui.ListItem(path=path)
	xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
	params = dict(parse_qsl(paramstring))
	if params:
		if params['action'] == 'listing':
			list_episodes(params['serie'])
		if params['action'] == 'download':
			download_episode(params['serie', 'season', 'episode'])
		else:
			raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
	else:
		list_series()


if __name__ == '__main__':
	router(sys.argv[2][1:])
