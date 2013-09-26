from itune_radio import *
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
import requests
from PIL import Image
from StringIO import StringIO

def get_song_from_file(name_of_song):
  audio = MP3(name_of_song, ID3=ID3)
  return audio

def add_album_to_ID3(song,image_name,image_format):
  # add ID3 tag if it doesn't exist
  try:
      song.add_tags()
  except error:
      pass

  song.tags.add(
      APIC(
          encoding=3, # 3 is for utf-8
          mime='image/'+image_format, # image/jpeg or image/png
          type=3, # 3 is for the cover image
          desc=u'Cover',
          data=open('/Users/rahul/Dev/random/ituneProject/' + image_name).read()
      )
  )
  song.save()

def get_album_art_from_web():
  # test_url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=bd221fa33740b25dcce42dac36c86b60&artist=Cher&album=Believe"

  #my lastfm api key
  API_KEY = "bd221fa33740b25dcce42dac36c86b60"

  #getting track,artist and album using itune_radio.py
  track,artist = get_song_and_artist()
  album = get_album()

  #generating the api url for lastfm
  url = "http://ws.audioscrobbler.com/2.0/?method=album.getinfo&api_key=%s&artist=%s&album=%s&format=json" %(API_KEY,artist,album)

  #getting the relevant album art url from lastfm
  r = requests.get(url)
  data = r.json()
  content = data['album']
  all_img = content['image']
  extralarge = all_img[3]
  img_url = extralarge['#text'].encode('ascii','ignore')

  #returning the obtained image
  i = requests.get(img_url)
  img = Image.open(StringIO(i.content))
  img_format = img.format.lower()

  img_name = album + "." + img_format
  img.save(img_name)

  return img_name, img_format