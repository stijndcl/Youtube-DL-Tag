#!/usr/bin/python3
import sys
import time

import requests
import json
import eyed3
import youtube_dl
import progressBar


class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def hook(d):
    if d["status"] == "downloading":
        # progressBar.progress(int(d["_percent_str"].split(".")[0]))
        print("Downloaded {:,}/{:,} bytes ({}) at {} - ETA: {} seconds {}".format(
            int(d["downloaded_bytes"]), int(d["total_bytes"]), d["_percent_str"].strip(),
            d["_speed_str"].strip(), d["eta"], progressBar.createProgressBar(int(d["_percent_str"].split(".")[0]))
            ),
              end="\r")
    if d['status'] == 'finished':
        print('Converting to {}...'.format(d["filename"][:-4] + "mp3"))


def download(link: str):
    ydl_opts = {
        "writeinfojson": True,
        "format": "251",
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'logger': Logger(),
        'progress_hooks': [hook],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


download(sys.argv[1])
