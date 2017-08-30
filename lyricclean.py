#!/usr/bin/env python3
# encoding=utf8

import os
import re
from optparse import OptionParser
import pathlib
import sys

def main():
	''' Get input data '''
	version_msg = "%prog 0.1"
	usage_msg = """%prog [DIR] """
	parser = OptionParser(version=version_msg, usage=usage_msg)
	args = parser.parse_args(sys.argv[1:])

	if len(sys.argv) == 1:
		parser.error("Please provide valid subdirectory.")		

	subdir = args[1][0];

	try:
		os.chdir(subdir)
	except OSError:
		print("Subdirectory cannot be opened.")

	totalsong = ""

	arr = os.listdir()
	for f in arr:
		with open(f, 'r') as openf:
			song = openf.read()
			song = (re.sub(r'[_+-.,!?@#$%^&*()<>"]', ' ', song)).lower()
			song = removeDuplicateLines(song)
			print(song)
			totalsong += song

	output = "output"
	pathlib.Path(output).mkdir(parents=True, exist_ok=True) 
	os.chdir(output)
	with open("out.txt", 'w') as f:
			f.write(totalsong)

def removeDuplicateLines(s):
	newl = ["\n"]
	lines = s.split('\n')
	filteredlines = filter(lambda x: not re.match(r'^\s$', x), lines)

	for i in filteredlines:
		if i == newl[-1] or i == '\n':
			continue
		else:
			newl.append(i)

	nodup = ""
	for eachline in newl:
		nodup += eachline + "\n"

	return nodup

if __name__ == "__main__":
    main()