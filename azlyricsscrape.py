#!/usr/bin/env python3
# encoding=utf8

__author__	= "Brett Chalabian"
__license__	= "GPL"


import sys
from bs4 import BeautifulSoup, SoupStrainer
from optparse import OptionParser
from time import sleep
import random
import pathlib
import os
import requests

def parseSong(songurl):
	title = ((songurl.split('/'))[-1]).split('.')[0]
	songhtml = requests.get(songurl.replace("..", "https://www.azlyrics.com"), 
						headers = {'User-Agent': random.choice(user_agents)})
	songsoup = BeautifulSoup(songhtml, "html.parser")

	''' Parse the lyrics (this is kinda janky) ''' 
	songsoup = songsoup.find('div', class_=False, id=False)
	song = songsoup.prettify()
	song = song.replace("<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->", "")
	song = song.replace("<br/>", "")
	song = song.replace("<div>", "")
	song = song.replace("</div>", "")
	
	''' write the lyrics to disk ''' 
	with open(title + ".txt", 'w') as f:
		f.write(song)

	print("Successfully wrote " + title + ".txt to disk.")

def main():

	''' Get input data '''
	version_msg = "%prog 0.1"
	usage_msg = """%prog [URL] """
	parser = OptionParser(version=version_msg, usage=usage_msg)
	args = parser.parse_args(sys.argv[1:])

	if len(sys.argv) == 1:
		parser.error("Please provide azlyrics artist link.")		

	url = args[1][0];
	''' html = urlopen(url) '''
	html = requests.get(url, headers = {'User-Agent': random.choice(user_agents)})

	''' Set up new directory for songs ''' 
	artist = url.split('/')[-1].split('.')[0]
	pathlib.Path(artist).mkdir(parents=True, exist_ok=True) 
	os.chdir(artist)
	print(artist)

	''' Isolate the list of songs ''' 
	song_list = SoupStrainer(id="listAlbum")
	soup = BeautifulSoup(html, "html.parser", parse_only=song_list)


	''' Parse each song link ''' 
	for s in soup.find_all('a', href=True):
		sleep(random() * 2.0 + 5)
		parseSong(s['href'])


user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']


if __name__ == "__main__":
    main()

