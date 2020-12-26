#!/usr/bin/env python

import re
# clipman - the Kindle clippings importer

FILEDIR = ""
FILENAME = "My Clippings.txt"

# Read the source file
# Open the file, read the data line by line into a list
try:
    file = open(FILEDIR + FILENAME, 'r', encoding = 'utf-8')
except FileNotFoundError:
    print('Error: The file', FILEDIR + FILENAME, 'does not exist.')
    exit(1)

clips_str = file.read()
file.close()
# print('[DEBUG]\n' + clips_str)

REGEX_PATTERN = ''
# Format:
# Title (Author)
# - Your Highlight on page X | Location X-X | Added on LongDate
#
# Highlight string
# ==========
# p = re.compile(r"(?P<title>[\S ]+) \((?P<author>[\S ]+)\)\r\n" \
#                "- Your (?P<ctype>Highlight|Note|Bookmark) " \
#                "(on|at) (?P<postype>location|page) " \
#                "(?P<posx>\d+)(-?(?P<posy>\d+))?" \
#                "( \| location (?P<locx>\d+)(-?(?P<locy>\d+))?)? \| " \
#                # Getting the timestamp
#                "Added on (?P<wday>[a-zA-Z]{3})[a-zA-Z]{,3}day, " \
#                "(?P<day>\d{1,2}) (?P<month>[a-zA-Z]{3})[a-zA-Z]* " \
#                "(?P<year>\d{4}) (?P<hr>\d\d):(?P<min>\d\d):(?P<sec>\d\d)" \
#                "\r\n\r\n(?P<highlight>[\S ]+)\r\n==========", re.MULTILINE)

p = re.compile(r"^(?P<title>[\S ]+) \((?P<author>[\S ]+)\)\n" \
               "- Your (?P<ctype>Highlight|Note|Bookmark) " \
               "(on|at) (?P<postype>location|page) " \
               "(?P<posx>\d+)(-?(?P<posy>\d+))?" \
               "( \| location (?P<locx>\d+)(-?(?P<locy>\d+))?)? \| " \
               # Getting the timestamp
               "Added on (?P<wday>[a-zA-Z]{3})[a-zA-Z]{,3}day, " \
               "(?P<day>\d{1,2}) (?P<month>[a-zA-Z]{3})[a-zA-Z]* " \
               "(?P<year>\d{4}) (?P<hr>\d\d):(?P<min>\d\d):(?P<sec>\d\d)\n\n" \
               "(?P<highlight>[\S ]+)\n==========", re.MULTILINE)
res = p.findall(clips_str)
for result in res:
    print(result)
