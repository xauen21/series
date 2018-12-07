from resources.series.model.serie import Serie
from resources.series.model.episode import Episode
from resources.series.plugins.info.info import Info
from resources.series.plugins.subtitle.subtitle import Subtitle
from resources.series.plugins.torrent.torrent import Torrent
from resources.series.common.download import Download

if __name__ == '__main__':
	#if Serie("Humans").id == None: Serie("Humans", ["Humans"], [Episode(1, 1)]).write()
	#if Serie("Daredevil").id == None: Serie("Daredevil", ["Daredevil"], [Episode(1, 1)]).write()
	#for serie in Serie.getSeries():	
		#Info.download(serie, serie.episodes[1])
	#	Info.updateSerie(serie)
	#	Torrent.updateSerie(serie)
	#	Subtitle.updateSerie(serie)
	humans = Serie("Humans")
	Info.updateSerie(humans)
	Torrent.updateSerie(humans)
	
	daredevil = Serie("Daredevil")
	Info.updateSerie(daredevil)
	Torrent.updateSerie(daredevil)

	#Download.download(daredevil, daredevil.episodes[0])