import json
import sys
from parse_aliases import get


def _save(cat, key, value):
    if key.startswith("$"):
        key = key[1:]

    with open("files/aliases.json", "r") as fp:
        aliases = json.load(fp)

    aliases[cat][key] = value

    with open("files/aliases.json", "w") as fp:
        json.dump(aliases, fp)


def _album():
    album_artist = get("artists", input("Album artist: "))
    album = input("Album: ")
    aliased_name = input("Album (alias): ")

    total = input("Total tracks: ")
    year = input("Release year: ")
    label = get("labels", input("Label: "))

    alias_dict = {
        "album": album,
        "artist": album_artist,
        "total": total,
        "year": year,
        "label": label
    }

    _save("albums", aliased_name, alias_dict)


def _artist():
    artist = input("Artist: ")
    aliased_name = input("Artist (alias): ")

    _save("artists", aliased_name, artist)


def _label():
    label = input("Label: ")
    aliased_name = input("Label (alias): ")

    _save("labels", aliased_name, label)


if __name__ == "__main__":
    category = sys.argv[1]

    dic = {
        "album": _album,
        "artist": _artist,
        "label": _label
    }

    dic[category]()
