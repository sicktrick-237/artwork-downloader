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


def download_yt_playlist(playlist_url):
    playlist_options = {
        'ignoreerrors': True,
        'quiet': True
    }
    video_ids = []
    with youtube_dl.YoutubeDL(playlist_options) as youdl:
        info_dict = youdl.extract_info(playlist_url, download=False)
        for video in info_dict['entries']:
            if video.get('id'):  # Gives Youtube video ids in a playlist
                video_ids.append('https://www.youtube.com/watch?v=' + video.get('id'))
    if video_ids:
        download(video_ids)


def download(video_ids):
    global options
    if video_ids:
        with youtube_dl.YoutubeDL(options) as youdl:
            youdl.download(video_ids)  # List of url(s)
    embed_artwork()  # Getting all artworks for downloaded tracks


def download_tracklist(tracklist_url):
    tracklist_name, tracklist = generateTracklist(tracklist_url)
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
    if video_ids:
        download(video_ids)
    return


if __name__ == '__main__':
    opt = input("1.Download Tracklist 2.Single Track ? [Enter 1 or 2] : ")
    if 'https://www.1001tracklists.com/tracklist/' in opt:
        download_tracklist(opt)
    elif 'www.youtube.com/watch?v=' in opt and ('list=' or '&index=') not in opt:
        url = opt.split(',')
        url = list(url)
        download(url)
    elif ('&list=' and '&index=') in opt or 'playlist?list=' in opt:
        download_yt_playlist(opt)
    else:
        print("Invalid URL. Exiting....")
        time.sleep(2)
