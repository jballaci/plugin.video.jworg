import xbmc
import xbmcaddon
import sys
import urlparse

plugin_name 	= sys.argv[0]
pluginPid   	= int(sys.argv[1])
plugin_params 	= urlparse.parse_qs((sys.argv[2])[1:])
skin_used 		= xbmc.getSkinDir()

const = {
	"Italiano" 	: {
		"video_path" 		: "http://www.jw.org/it/video",
		"lang_code"			: "I",
		"bible_index_audio"	:  "http://www.jw.org/it/pubblicazioni/bibbia/nwt/libri/",
		"bible_audio_json"  : "http://www.jw.org/apps/I_TRGCHlZRQVNYVrXF?output=json&pub=bi12&fileformat=MP3&alllangs=0&langwritten=I",
		'daily_text_json'	: "http://wol.jw.org/wol/dt/r6/lp-i",
		"music_index"		: "http://www.jw.org/it/pubblicazioni/musica-cantici/",
		"date_format"		: "%d-%m-%Y",
 	},
	"English" 	: {
		"video_path" 		: "http://www.jw.org/en/videos",
		"lang_code"			: "E",
		"bible_index_audio"	: "http://www.jw.org/en/publications/bible/nwt/books/" ,
		"bible_audio_json"  : "http://www.jw.org/apps/E_TRGCHlZRQVNYVrXF?output=json&pub=bi12&fileformat=MP3&alllangs=0&langwritten=E",
		'daily_text_json'	: "http://wol.jw.org/wol/dt/r6/lp-e",
		"music_index"		: "http://www.jw.org/en/publications/music-songs/",
		"date_format"		: "%Y-%m-%d",
	},
}

# Translation util
def t(string_number):
	plugin       = xbmcaddon.Addon("plugin.video.jworg")
	return plugin.getLocalizedString(string_number)
