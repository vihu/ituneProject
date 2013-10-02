#Introduction
>Download current playing song from Youtube on iTunes Radio
>
>Find and add ID3 tag from Last FM

#Requirements
>virtualenv env
>
>pip install -r requirements.txt
>
>source env/bin/activate
>
>python itune_radio.py

#How it works
>Finds the song currently playing on iTunes (doesn't matter if its on Radio or local)
>
>Finds the Youtube video based on the Track and Artist
>
>Downloads the video
>
>Converts it to MP3 format
>
>Finds the appropriate ID3 tags from LastFM and attaches it to the song

#Known issues
>Last FM API key needed, which doesn't work (yet).
>
>No ID3 tagging except album art (yet).

#Disclaimer
>I assume no responsibility if you're caught by the FBI using this.
>
>This is just a test project for me to learn python