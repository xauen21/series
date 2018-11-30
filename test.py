from resources.series.model.serie import Serie
from resources.series.plugins.info.info import Info
from resources.series.plugins.subtitle.subtitle import Subtitle
from resources.series.plugins.torrent.torrent import Torrent

if __name__ == '__main__':
	for serie in Serie.getSeries():
		#Info.updateSerie(serie)
		#Torrent.updateSerie(serie)
		#Subtitles.updateSerie(serie)

		Serie = Serie("penny dreadful")
		Info.download(serie, serie.episodes[1])