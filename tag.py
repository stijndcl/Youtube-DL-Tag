import glob
import os

import eyed3

from alias import get


def tag(info):
    album = None
    albumArtist = None
    totalTracks = None
    year = None
    label = None

    print("\n")
    fileName = glob.glob("./*{}*.mp3".format(info["id"]))[0]

    # Ask the user for all the info
    artist = info["uploader"].replace(" - Topic", "")
    artist = get("artists", promptResponse(artist, input("Artist ({}): ".format(artist))))

    title = promptResponse(info["title"], input("Title ({}): ".format(info["title"])))

    album = title.replace(" [Extended Mix]", "").replace(" (Extended Mix)", "") + " - Single"
    album = get("albums", promptResponse(album, input("Album ({}): ".format(album))))

    # If album was an alias, parse all data out
    if isinstance(album, dict):
        totalTracks = album["total"]
        year = album["year"]
        albumArtist = album["artist"]
        label = album["label"]
        album = album["album"]

    if albumArtist is None:
        albumArtist = get("artists", promptResponse(artist, input("Album Artist ({}): ".format(artist))))

    track = "1" if "extended" not in info["title"].lower() else "2"
    track = promptResponse(track, input("Track ({}): ".format(track)))

    if totalTracks is None:
        totalTracks = promptResponse("2", input("Total Tracks (2): "))

    if year is None:
        year = promptResponse(info["upload_date"][:4], input("Year ({}): ".format(info["upload_date"][:4])))

    if label is None:
        label = get("labels", input("Label: "))

    print("\nAdding tags...")

    # Tag
    file = eyed3.load(fileName)
    file.tag.title = title
    file.tag.artist = artist
    file.tag.album = album
    file.tag.album_artist = albumArtist
    file.tag.track = track
    file.tag.track_total = totalTracks
    file.tag.release_year = year
    file.tag.publisher = label
    file.tag.images.set(3, open("thumbnail.jpeg", "rb").read(), "image/jpeg")
    file.tag.save()

    print("\nRenaming original file...")
    os.rename(r"{}".format(fileName), r"{} - {}.mp3".format(artist, title))

    print("\nRemoving temporary files...")
    os.remove(glob.glob("./*.info.json")[0])
    os.remove(glob.glob("./thumbnail.jpeg")[0])
    exit(0)


# After asking the user to fill in a field, format their response
def promptResponse(original, prompt):
    # Nothing was entered, indicating the user thought it was good
    if not prompt:
        return original

    # Can add another artist to the string by starting your input with a "+"
    if prompt.startswith("+"):
        return original + prompt[1:]

    # The user gave their own response
    return prompt

