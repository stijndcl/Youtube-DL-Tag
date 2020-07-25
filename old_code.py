#!/usr/bin/python3
import sys
import requests
import json
import eyed3
import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    while d['status'] != "finished":
        print(d["downloaded_bytes"])
    if d['status'] == 'finished':
        print('Done downloading {}, now converting to {}...'.format(d["tmpfilename"], d["filename"]))


def download(link: str):
    ydl_opts = {
        "writeinfojson": True,
        "format": "251",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'logger': MyLogger(),
        'progress_hooks': [my_hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


args = sys.argv
download(args[1])