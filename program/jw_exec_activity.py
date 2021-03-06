"""
ACTIVITIES RELATED FUNCTION
"""
import jw_config
import jw_common

import xbmcplugin
import xbmcgui
import xbmc

import re
import urllib

from BeautifulSoup import BeautifulSoup 

# List of available news
def showActivityIndex():

	language    = jw_config.language

	url 		= jw_common.getUrl(language)
	url 		= url + jw_config.const[language]["activity_index"]

	html 		= jw_common.loadUrl(url)

	# sections[n][0] = section link
	# sections[n][1] = section title

    # <p><a href="/it/testimoni-di-geova/attivit%C3%A0/ministero/" title="Ministero pubblico" class="btnLink">
    # VEDI TUTTO</a></p>

	regexp_section = '<p><a href="([^"]+)" title="([^"]+)" class="btnLink">[^<]+</a></p>'
	sections = re.findall (regexp_section, html)

	# iages[n][0] = full url of thumb
	regexp_images = "data-img-size-sm='([^']+)'"
	images = re.findall (regexp_images, html)	

	for section  in sections :
		title = jw_common.cleanUpText( section[1] ) 
		listItem = xbmcgui.ListItem( 
			label  			= title,
			# no thumbnail available from website, will be used standard folder icon
		)	
		params = {
			"content_type"  : "executable", 
			"mode" 			: "open_activity_section", 
			"url"			: section[0]
		} 
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.plugin_pid, 
			url			= url, 
			listitem	= listItem, 
			isFolder	= True 
		) 
		
		count = 0

	xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)

	return



def showActivitySection(url):

	url 	= "http://www.jw.org" + url
	html 	= jw_common.loadUrl(url)
	soup 	= BeautifulSoup(html)

    # container of news, so we can leave out the sidebar
	article = soup.findAll("div", {'id' : 'article'})

	news 	= article[0].findAll('div', {'class' : re.compile(r'\bPublicationArticle')})

	for n in news : 

		anchor = n.findAll("a")
		link = anchor[1].get("href")

		# Lookup news title

		#detect first item
		title = n.findAll('div', {'class' : "itemAdText"})
		if len(title)>0 :
			title = jw_common.cleanUpText(anchor[1].get("title").encode("utf-8"))
		else :
			content = anchor[1].findAll(text=True)
			content_string = " ".join(content)
			title = jw_common.cleanUpText(content_string.encode("utf-8"))

		image = n.findAll("img")
		image_src = image[0].get("src")

		listItem = xbmcgui.ListItem( 
			label  			= title,
			thumbnailImage	= image_src,
		)	

		params = {
			"content_type"  : "executable", 
			"mode" 			: "open_activity_article", 
			"url"			: link
		} 
		url = jw_config.plugin_name + '?' + urllib.urlencode(params)
		xbmcplugin.addDirectoryItem(
			handle		= jw_config.plugin_pid, 
			url			= url, 
			listitem	= listItem, 
			isFolder	= False 
		) 

	xbmcplugin.endOfDirectory(handle=jw_config.plugin_pid)

	return

def showArticle(url):

	url 	= "http://www.jw.org" + url
	html 	= jw_common.loadUrl(url)

	activity = Activity()
	activity.customInit(html)
	activity.doModal()
	del activity
	xbmc.executebuiltin('Action("back")')
	return



# Window showing activity related news text

#get actioncodes from https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h
ACTION_MOVE_UP 		= 3
ACTION_MOVE_DOWN 	= 4
ACTION_PAGE_UP 		= 5
ACTION_PAGE_DOWN 	= 6
ACTION_SCROLL_UP	= 111
ACTION_SCROLL_DOWN	= 112

class Activity(xbmcgui.WindowDialog):

	def __init__(self):
		if jw_config.emulating: xbmcgui.Window.__init__(self)

	def customInit(self, text):

		border = 50 # px relative to 1280/720 fixed grid resolution

		# width is always 1280, height is always 720.
		bg_image = jw_config.dir_media + "blank.png"
		self.ctrlBackgound = xbmcgui.ControlImage(
			0,0, 
			1280, 720, 
			bg_image
		)
		
		self.ctrlBackgound2 = xbmcgui.ControlImage(
			0,0, 
			1280, 90, 
			bg_image
		)
		self.ctrlTitle= xbmcgui.ControlTextBox(
			border, 0, 
			1280 - border *2, 90, 
			'font35_title', "0xFF0000FF"
		)
		self.ctrlText= xbmcgui.ControlTextBox(
            border, 20, 
            1280 - border *2, 10000, # Really long articles already found !
            'font30', "0xFF000000"
        )
		
		self.addControl (self.ctrlBackgound)
		self.addControl (self.ctrlText)
		self.addControl (self.ctrlBackgound2)
		self.addControl (self.ctrlTitle)
		
		self.ctrlTitle.setText( self.getTitle(text) )
		self.ctrlText.setText( self.getText(text) )
		

	def onAction(self, action):
		(x,y) =  self.ctrlText.getPosition()

		if action == ACTION_MOVE_UP or action == ACTION_SCROLL_UP :
			if y > 0:
				return
			y = y + 50
			self.ctrlText.setPosition(x,y)
			return

		if action == ACTION_MOVE_DOWN or action == ACTION_SCROLL_DOWN :
			(x,y) =  self.ctrlText.getPosition()
			y = y - 50
			self.ctrlText.setPosition(x,y)
			return

		if action == ACTION_PAGE_UP:
			if y > 0:
				return
			y = y + 500
			self.ctrlText.setPosition(x,y)
			return

		if action == ACTION_PAGE_DOWN:
			(x,y) =  self.ctrlText.getPosition()
			y = y - 500
			self.ctrlText.setPosition(x,y)
			return

		self.close()

	# Grep news title
	def getTitle(self, text):
		regexp_header = "<h1([^>]*)>(.*)</h1>"
		headers = re.findall(regexp_header, text)
		return jw_common.removeHtml(headers[0][1])
		

	def getText(self, text):

		text =  re.sub("<strong>", "[B]", text)
		text =  re.sub("</strong>", "[/B]", text)
		text =  re.sub("<a[^>]+>", "", text)

		regexp_pars = '<p id="p[0-9]+" class="p[0-9]+">(.+)</p>|<h3 class="inline">(.+)</h3>'
		pars = re.findall(regexp_pars, text)


		out = ""
		for par in pars:
			text = par[0] + "[B]"+par[1]+"[/B]"
			out = out + "\n\n" + jw_common.removeHtml(text)
		out = out + "\n\n[COLOR=FF0000FF][I]" + jw_common.t(30038).encode("utf8") + "[/I][/COLOR]"

		return out
		