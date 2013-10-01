'''
Get song on youtube from itunes radio
'''
import re
import subprocess
from subprocess import Popen, PIPE
import sys
import requests
from add_albumart import *

def get_album():
  scpt = '''
    tell application "iTunes"
      get album of current track
    end tell'''

  p = Popen('osascript', stdin=PIPE, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate(scpt)
  album_name = stdout.rstrip()
  return album_name

def get_song_and_artist():
  scpt = '''
    tell application "iTunes"
      set tr to name of current track
      set ar to artist of current track
      get tr & "," & ar
    end tell'''

  p = Popen('osascript', stdin=PIPE, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate(scpt)
  x = stdout

  for index,letter in enumerate(x):
    if letter == ',':
      song = x[0:index]
      comma_index = index
      break
  artist = x[comma_index+1:len(x)-1]

  return song,artist


def youtube_search(track_name):

    'Search Youtube for a given song from iTunes'
    #Api here: https://developers.google.com/youtube/2.0/reference#Searching_for_videos

    y_url = "https://gdata.youtube.com/feeds/api/videos?q=%s&max-results=2&alt=json" % (track_name)
    r = requests.get(y_url)
    data = r.json()

    x = convert_keys_to_string(data['feed'])
    y = convert_keys_to_string(x['entry'])
    z = convert_keys_to_string(y[0])
    w = convert_keys_to_string(z['link'])

    a = w[0]
    b = convert_keys_to_string(a)
    c = b['href']
    d = c.encode('ascii', 'ignore')

    for index,letter in enumerate(d):
      if letter == '&':
        link = d[0:index]

    return link


def convert_keys_to_string(dic):
  """Recursively converts dic keys to strings."""
  if not isinstance(dic, dict):
      return dic
  return dict((str(k), convert_keys_to_string(v))
      for k, v in dic.items())


def get_path():
  user_download_path = raw_input("Enter download path: ")
  return user_download_path

def start_download(link,user_path):
  cmd = ['youtube-dl', "--extract-audio", "--audio-format", "mp3", "-o", user_path, link]
  p = Popen(cmd, stdout=PIPE, stderr=PIPE)
  stdout,stderr = p.communicate()

  a = re.findall("Destination: .+", stdout)
  b = a[1]
  name_of_mp3 = b[13:]
  return name_of_mp3


if __name__ == '__main__':
  try:
    track, artist = get_song_and_artist()
    album = get_album()
    temp_query = track + " " + artist
    query =  '+'.join(temp_query.split(' '))
    link = youtube_search(query)
    print "Finding song, artist and youtube link"
    print "Done."
    print "--------------------------------------"
  except Exception as e:
    print "Couldn't find the song, artist and link"
    raise e


  try:
    download_path = get_path()
    corrected_path = str(download_path) + "/%(title)s.%(ext)s"
    print "Starting Download. Be Patient"
    mp3 = start_download(link,corrected_path)
    print "Done."
    print "--------------------------------------"
  except Exception as e:
    print "Couldn't start the download"
    raise e

  try:
    print "Linking mp3 name to get the album"
    song = get_song_from_file(mp3)
    print "Done"
    print "--------------------------------------"
  except Exception as e:
    print "Couldnt get the filename correctly"
    raise e

  try:
    print "Finding the appropriate Album Art"
    artname, artformat = get_album_art_from_web()
    print "Done"
    print "--------------------------------------"
    print "Linking the album art to the song"
    add_album_to_ID3(song,artname,artformat)
    print "Done"
    print "--------------------------------------"
    print "Deleting the downloaded album art"
    delete_art_after_link(artname)
    print "Done"
  except Exception as e:
    print "Couldnt get the album art from web"
    raise e