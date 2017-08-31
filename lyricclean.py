#!/usr/bin/env python3
# encoding=utf8

import os
import re
import pathlib
import sys
import argparse

def removeDuplicateLines(song, nolinebreak, noversebreak):
	song = re.sub(r'<i>[\S\s]*<\/i>', '', song)
	song = (re.sub(r'[_+-.,!?@#$%^&*()<>"]', ' ', song)).lower()
	lines = (song.lstrip()).split('\n')
	dedupLines = []

	newlinecount = 0

	for i in lines:
		i = i.lstrip()
		if len(dedupLines) is 0 or i != dedupLines[-1]:
			if i.isspace() or i is "":
				newlinecount += 1
			else:
				if newlinecount == 1 and not nolinebreak:
					dedupLines.append("NEWLINE")
					newlinecount = 0
				if newlinecount > 1 and not noversebreak:
					dedupLines.append("NEWVERSE")
					newlinecount = 0
				dedupLines.append(i)

	dedup = ""
	for l in dedupLines:
		dedup += l + "\n"

	return dedup

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-nlb", "--nolinebreaks", action='store_true', help="Do not maintain line breaks as a character")
	parser.add_argument("-ndlb", "--nodoublelinebreaks", action='store_true', help="Do not maintain breaks between verses")
	parser.add_argument("-ne", "--noend", action='store_true', help="Do not track the ends of songs relative to the next song")
	parser.add_argument("subdir", help="Subdirectory of song lyrics.")
	args = parser.parse_args()
	totalsong = ""

	subdir = args.subdir
	try:
		os.chdir(subdir)
	except OSError:
		print("Subdirectory cannot be opened.")

	endsong = "\nENDSONG\n\n"
	if args.noend:
		endsong = ""

	arr = os.listdir()
	for f in arr:
		if f.find(".txt") != -1:
			with open(f, 'r') as openf:
				song = openf.read()
				song = removeDuplicateLines(song, args.nolinebreaks, args.nodoublelinebreaks)
				totalsong += song + endsong

	output = "output"
	pathlib.Path(output).mkdir(parents=True, exist_ok=True) 
	os.chdir(output)

	

	with open("out.txt", 'w') as f:
			f.write(totalsong)