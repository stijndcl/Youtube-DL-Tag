#!/usr/bin/python3
import os
import sys
import time
import urllib.request
from PIL import Image
import requests
import json
import eyed3
import glob
import youtube_dl
import progressBar


artist = None


class Logger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def hook(d):
    if d["status"] == "downloading":
        print("Downloaded {:,}/{:,} bytes ({}) at {} - ETA: {} seconds {}".format(
            int(d["downloaded_bytes"]), int(d["total_bytes"]), d["_percent_str"].strip(),
            d["_speed_str"].strip(), d["eta"], progressBar.createProgressBar(int(d["_percent_str"].split(".")[0]))
            ),
              end="\r")
    if d['status'] == 'finished':
        print("\n")
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


# Removes the video id out of the filename
def renameFile():
    info = glob.glob("./*.info.json")[0]
    with open(info, "r") as fp:
        info = json.load(fp)

    audioFile = glob.glob("./*{}.mp3".format(info["id"]))[0]
    newName = audioFile.replace("-{}".format(info["id"]), "")
    os.rename(audioFile, newName)


# Saves the album cover
def saveAlbumArt():
    info = glob.glob("./*.info.json")[0]
    with open(info, "r") as fp:
        info = json.load(fp)

    thumbnails = sorted(info["thumbnails"], key=lambda x: x["width"], reverse=True)

    urllib.request.urlretrieve(thumbnails[0]["url"], "thumbnail.webp")
    im = Image.open("thumbnail.webp").convert("RGB")
    im.save("thumbnail.jpeg", "jpeg")
    os.remove("thumbnail.webp")


# download(sys.argv[1])
saveAlbumArt()
# renameFile()
