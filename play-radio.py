#!/bin/env python3

import json
import pathlib
import argparse
import subprocess

import requests
from pyfzf.pyfzf import FzfPrompt

# TODO: add exclusive groups to arguments
def arguments():
    parser = argparse.ArgumentParser(description="I am playing radio")
    parser.add_argument("-r", "--refresh", action="store_true")
    parser.add_argument("-p", "--play", action="store_true")
    parser.add_argument("-t", "--tagplay")
    return parser.parse_args()


def download_station_list(url):
    response = requests.get(url)
    return response.text


def save_station_list(response, file_path):
    with open(file_path, "w") as f:
        f.write(response)
    return 0


def search_by_name(json_input):
    name_list = []
    for item in json_input:
        name_list.append((item["name"]))
    fzf = FzfPrompt()
    selection = fzf.prompt(name_list)
    return selection[0]


def get_stream_url(json_input, station_name):
    for element in json_input:
        if element["name"] == station_name:
            stream_url = element["url"]
    return stream_url


def play_radio_station(station_url):
    command = f"mpv --quiet {station_url}".split()
    subprocess.run(command)
    return 0


def main(args):
    BASE_PATH = f"{pathlib.Path.home()}/.local/share"
    stations_path = f"{BASE_PATH}/stations.txt"
    URL = "http://de1.api.radio-browser.info/json/stations"
    if args.refresh == True:
        http_response = download_station_list(URL)
        save_station_list(http_response, stations_path)
        return 0
    if args.play == True:
        with open(stations_path) as f:
            json_list = json.load(f)
    elif args.tagplay != None:
        json_raw = download_station_list(f"{URL}/bytag/{args.tagplay}")
        json_list = json.loads(json_raw)
    selected = search_by_name(json_list)
    selected_url = get_stream_url(json_list, selected)
    play_radio_station(selected_url)
    return 0


if __name__ == "__main__":
    main(arguments())
