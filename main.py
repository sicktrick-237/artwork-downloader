from __future__ import unicode_literals
import youtube_dl
import time
from tracklist_parser import generateTracklist
from youtube_search_engine import BypassedSearch
from artwork_downloader import embed_artwork

options = {
    'format': 'bestaudio/best',
    'outtmpl': "%(title)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '256'
    }]
}


def download(video_ids):
    global options
    if video_ids:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download(video_ids)  # List of url(s)
    embed_artwork()  # Getting all artworks for downloaded tracks


def get_tracklist():
    tracklist_name, tracklist = generateTracklist()
    video_ids = []  # Fetching Youtube URL
    byp_search = BypassedSearch()
    if tracklist:
        for track in tracklist:
            print('Fetching Track : %s' % track)
            track_id = byp_search.searchusingscraper(track)
            youtube_url = 'https://www.youtube.com/watch?v=' + track_id
            if "Video Not Found" in youtube_url or "Failed To Generate URL" in youtube_url:
                continue
            video_ids.append(youtube_url)

    return video_ids


def download_tracklist():
    video_ids = get_tracklist()
    if video_ids:
        download(video_ids)


if __name__ == '__main__':
    opt = int(input("1.Download Tracklist 2.Single Track ? [Enter 1 or 2] : "))
    if opt == 1:
        download_tracklist()
    elif opt == 2:
        url = (input("Enter Youtube Url : ")).split(',')
        url = list(url)
        download(url)
    else:
        print("Invalid Selection. Exiting....")
        time.sleep(2)
