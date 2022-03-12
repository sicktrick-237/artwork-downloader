import glob
import os
import urllib.request
import itunespy
import mutagen
import sys
from tqdm import tqdm
from mutagen.id3 import ID3, APIC, error
from mutagen.mp3 import MP3

cwd = os.getcwd()  # Defaults to Current Working Directory


def write_artwork(original_name, track_name, custompath=None):
    global cwd
    if custompath:
        cwd = custompath

    image_name = original_name + '.jpg'
    print(cwd)
    print(custompath)
    track_path = os.path.join(cwd, track_name)
    image_path = os.path.join(cwd, image_name)

    try:
        audio = MP3(track_path, ID3=ID3)
    except:
        print("\nCorrupt File - ", track_name)
        return

    try:
        audio.add_tags()
    except error:
        pass

    audio.tags.add(APIC(mime='image/jpg', type=3, desc=u'Cover', data=open(image_path, 'rb').read()))
    audio.save()

    os.remove(image_path)  # Removing Image


def get_artwork(search_query, track_name, custompath=None):
    track = False
    try:
        track = itunespy.search_track(search_query)
    except:
        return
    if track:
        # print(track[0].get_artwork_url())
        artwork_url = track[0].get_artwork_url()
        urllib.request.urlretrieve(artwork_url, "%s.jpg" % search_query)  # Writing same as audio file
        if custompath:
            write_artwork(search_query, track_name, custompath)
        else:
            write_artwork(search_query, track_name)
    # else:
    # print("Artwork not found for : %s" % search_query)


def embed_artwork(custompath=None):
    for audio_file in tqdm(glob.glob("*.mp3")):
        clean_name = str(audio_file).replace('-', "").replace(".mp3", "").replace("(Original Mix)", "").replace(
            "(Extended Mix)", "")
        clean_name = clean_name.replace("(Official Music Video)", "").replace("(Official Video)", "").replace(
            "(Lyrics Video)", "")
        if custompath:
            get_artwork(clean_name, audio_file, custompath)
        else:
            get_artwork(clean_name, audio_file)
        # print("Looking for %s"%audio_file)


if __name__ == '__main__':
    # global cwd
    try:
        path = sys.argv[1]
        if path:
            os.chdir(path)
            cwd = os.getcwd()
        print(cwd)
    except IndexError as e:
        cwd = os.getcwd()
        print(cwd)
    except FileNotFoundError as e:
        print(e)
    finally:
        embed_artwork()
