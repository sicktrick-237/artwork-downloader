import subprocess


def search_using_ydl(search_term):
    search = "ytsearch1:%s" % search_term
    query = 'youtube-dl --get-id "%s"' % search
    video_id = subprocess.run(query, stdout=subprocess.PIPE).stdout.decode('utf-8')
    return video_id
