#!/usr/bin/python3
import os
import sys
import time
import urllib.request
from PIL import Image
import requests
import json
import tag
import glob
import youtube_dl
import progressBar


info = None


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
        print("\n", end="")
        print('Converting to {}...'.format(d["filename"][:-4] + "mp3"))


def download(link: str):
    global info
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
    info = glob.glob("./*.info.json")[0]
    with open(info, "r") as fp:
        info = json.load(fp)


# Removes the video id out of the filename
def renameFile():
    global info

    audioFile = glob.glob("./*{}.mp3".format(info["id"]))[0]
    newName = audioFile.replace("-{}".format(info["id"]), "")
    os.rename(audioFile, newName)


# Saves the album cover
def saveAlbumArt():
    global info

    thumbnails = sorted(info["thumbnails"], key=lambda x: x["width"], reverse=True)

    # Download & save the file
    urllib.request.urlretrieve(thumbnails[0]["url"], "thumbnail.webp")
    im = Image.open("thumbnail.webp").convert("RGB")
    im.save("thumbnail.jpeg", "jpeg")
    os.remove("thumbnail.webp")

    # Cut the cover out of it
    im = Image.open("thumbnail.jpeg")
    w, h = im.size
    im.crop(((w - h)//2, 0, (w + h)//2, h)).save("thumbnail.jpeg")


def parseDescription():
    with open(glob.glob("*.description"), "r") as fp:
        description = fp.readline()
    dic = {}


download(sys.argv[1])
saveAlbumArt()
tag.tag(info)
# renameFile()
