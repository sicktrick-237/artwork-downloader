import glob
import os
import urllib.request
import itunespy
import mutagen
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3

global cwd
cwd = os.getcwd()


def write_artwork(original_name, track_name):
    global cwd
    image_name = original_name + '.jpg'

    track_path = os.path.join(cwd, track_name)
    image_path = os.path.join(cwd, image_name)

    audio = MP3(track_path, ID3=ID3)

    try:
        audio.add_tags()
    except error:
        pass

    audio.tags.add(APIC(mime='image/jpg', type=3, desc=u'Cover', data=open(image_path, 'rb').read()))
    audio.save()

    os.remove(image_path)  # Removing Image


def get_artwork(search_query, track_name):
    track = False
    try:
        track = itunespy.search_track(search_query)
    except:
        return
    if track:
        print(track[0].get_artwork_url())
        artwork_url = track[0].get_artwork_url()
        urllib.request.urlretrieve(artwork_url, "%s.jpg" % search_query)  # Writing same as audio file
        write_artwork(search_query, track_name)
    else:
        print("Artwork not found for : %s" % search_query)


def embed_artwork():
    for audio_file in glob.glob("*.mp3"):
        clean_name = str(audio_file).replace('-', "").replace(".mp3", "").replace("(Original Mix)", "").replace("(Extended Mix)", "")
        clean_name = clean_name.replace("(Official Music Video)", "").replace("(Official Video)", "")
        print(clean_name)
        get_artwork(clean_name, audio_file)


embed_artwork()
# # Write ID3 Tag
# trackname = 'LVNDSCAPE - Dive With Me (ft. Cathrine Lassen).mp3'
# imagename = 'LVNDSCAPE  Dive With Me (ft. Cathrine Lassen).jpg'
#
# audio_path = cwd + "\\" + trackname
# image_path = cwd + "\\" + imagename
#
# audio = MP3(audio_path, ID3=ID3)
#
# try:
#     audio.add_tags()
# except error:
#     pass
#
# audio.tags.add(APIC(mime='image/jpg', type=3, desc=u'Cover', data=open(image_path, 'rb').read()))
# audio.save()
# # audio = ID3('Padé - The Olive (In The Air Tonight).mp3')
# # print(audio)
# # audio.ad
