#!/usr/bin/env python

import re
from json import dumps, loads
import os
# clipman - the Kindle clippings importer

def read_db():
   db_str = ''
   try:
      db_file = open(DBPATH + '/db.json', 'r')
      db_str = db_file.read()
      db_file.close()
   except FileNotFoundError:
      return False
   if db_str == '':
      db = {}
   else:
      db = loads(db_str)
   return db

def check_duplicate(prev_clip, cur_clip):
   """Check if the two strings are duplicates. Returns the longer string."""
   if len(prev_clip) > len(cur_clip):
      if cur_clip in prev_clip:
         return prev_clip
   if prev_clip in cur_clip:
      return cur_clip
   return False

def remove_duplicates(clips):
   """Returns a new clips array with no duplicates"""
   new_clips = []
   new_clips.append(clips[0])
   for i, clip in enumerate(clips):
      clip_text = check_duplicate(new_clips[-1]['highlight'], clip['highlight'])
      # print(new_clips)
      if clip_text:
         new_clips[-1] = clip
      else:
         new_clips.append(clip) # Replace the previous duplicat clip
   return new_clips

def write_db(clips):
   """Write the clippings to the database checking for duplicates."""
   db = read_db()
   if len(clips) == 0:
      return False
   print('#', len(clips))
   db_str = dumps(clips)
   out_file = open(DBPATH + '/db.json', 'w+')
   out_file.write(db_str)
   out_file.close()

def export_org(clips):
    """Export the database as org files"""
    db = {}
    if not os.path.exists(EXPORTPATH):
       os.mkdir(EXPORTPATH)
    for clip in clips:
       clip_key = '{} - {}'.format(clip['title'], clip['author'])
       if clip_key not in db:
          db[clip_key] = []
       db[clip_key].append(clip)
    for entry in db:
       with open(os.path.join(EXPORTPATH, entry) + '.org', 'a+') as f:
          for clip in db[entry]:
             clip_str = "\n* {} on {} at {}\n{}".format(clip['type'].title(), clip['location'][0], clip['timestamp'], clip['highlight'])
             f.write(clip_str)

def export_json():
    """Export the database as JSON files"""

FILEDIR = ''
FILENAME = "My Clippings.txt"
EXPORTPATH = './out'
DBPATH = './records'

# Create empty db if not exists
if not os.path.exists(DBPATH):
   os.mkdir(DBPATH)
# Read the source file
# Open the file, read the data line by line into a list
try:
    file = open(FILEDIR + FILENAME, 'r', encoding = 'utf-8')
except FileNotFoundError:
    print('Error: The file', FILEDIR + FILENAME, 'does not exist.')

print('My Clippings.txt found.')
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
results = p.finditer(clips_str)
# for result in results:
#     print(result.group('highlight'))


# Add to dictionary
clips = []
# Format:
# book: [clip1_dict clip2_dict, ..]
clip = {}
# Format
# id: 12,
# type: 'note',
# text: 'I am a genius',
# timestamp: 2020-10-21
# Genearate the clip object
for result in results:
    clip = {}
    # getting position data
    # TODO: A possible alternative to 'None'
    if result.group('postype') == 'location':
        loc = [result.group('posx'), result.group('posy')]
        page = [None, None]
    elif result.group('postype') == 'page':
        page = [result.group('posx'), result.group('posy')]
        loc = [result.group('locx'), result.group('locy')]
    # extracting timestamp
    # strptime('Fri Mar 01 23:38:40 2019')
    timestring = '{weekday} {month} {day} {hour}:{minute}:{second} {year}'
    timestring = timestring.format(weekday=result.group('wday'), \
                                   month=result.group('month'), \
                                   day=result.group('day'), \
                                   hour=result.group('hr'), \
                                   minute=result.group('min'), \
                                   second=result.group('sec'), \
                                   year=result.group('year'))
    clip['author'] = result.group('author')
    clip['title'] = result.group('title')
    clip['type'] = result.group('ctype').lower()
    clip['timestamp'] = timestring
    clip['highlight'] = result.group('highlight')
    clip['page'] = page
    clip['location'] = loc
    clips.append(clip)

print("# clips read:", len(clips))
clips = remove_duplicates(clips)
print("# clips after duplicate removal:", len(clips))
db = read_db()
print("# clips in database:", sum([len(entry) for entry in db]))
export_org(clips)
# write_db(clips)

# print(read_db())

# Format:
# [ book1: [cl1, cl2, ..]
#   book2: ...
#   .
#   . ]

