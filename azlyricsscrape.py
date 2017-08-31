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
						headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36", 
										'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
										'Accept_Language': "en-US,en;q=0.8"})
	songsoup = BeautifulSoup(songhtml.text, "html.parser")

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
	html = requests.get(url, headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36", 
										'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
										'Accept_Language': "en-US,en;q=0.8"})

	artist = url.split('/')[-1].split('.')[0]
	pathlib.Path(artist).mkdir(parents=True, exist_ok=True) 
	os.chdir(artist)
	print(artist)

	song_list = SoupStrainer(id="listAlbum")
	soup = BeautifulSoup(html.text, "html.parser", parse_only=song_list)

	for s in soup.find_all('a', href=True):
		sleep(random.random()*4.0 + 7.0)
		parseSong(s['href'])

if __name__ == "__main__":
    main()

