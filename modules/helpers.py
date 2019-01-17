# -----------------------------------------------------------------------------
# DOWNLOAD FILES by Andrew Chavez
# -----------------------------------------------------------------------------
import os, errno
import requests

def download_file(url, file_path, directoryName):
    file_name = url.rsplit('/', 1)[-1]
    destination = os.path.join(directoryName + '/media/', file_name)

    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(destination, 'wb') as f:
            for chunk in r:
                f.write(chunk)

def download_photo(handle, media_url, to=''):
    download_file(media_url, to, handle)

def download_video(handle, video_info, to=''):
    videos = filter(lambda x: x['content_type'] == 'video/mp4',
                    video_info['variants'])
    highest_res = sorted(videos, key=lambda k: k['bitrate'], reverse=True)[0]
    download_file(highest_res['url'], to, handle)