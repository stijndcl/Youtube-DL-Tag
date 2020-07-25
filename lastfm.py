import glob
import json

import requests


def searchTrack(artist=""):
    info = glob.glob("./*.info.json")[0]
    with open(info, "r") as fp:
        info = json.load(fp)
    answer = requests.get("http://ws.audioscrobbler.com/2.0/?method=track.search&track={}&artist={}&api_key={}&format=json".format(
        info["title"], artist, getAPIKey())).json()
    print(answer)


def getAPIKey():
    with open("apikey.txt", "r") as file:
        return file.readlines()[1].split(":")[1].strip()
