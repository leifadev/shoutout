import requests, os, getpass, json
import logging
from typing import Optional


# For caching, fetching, and managing data, and more from the Free Dictionary API ==> https://dictionaryapi.dev/


# -*- coding: utf-8 -*-

class Manager():

    def __init__(self):
        self.cacheAddress = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.languages = [
            "en_US",  # USA
            "fr_FR",  # france
            "de_DE",  # germany
            "jp_JP",  # japan
            "es_ES",  # spain
            "pl_PL",  # poland
            "ru_RU"  # russia
        ]

    # Requests all relevant data for specified word and language, returns it in >>> self.output! <<<
    def request(self, lang, word): #, query: int):
        api_address = f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{word}"
        # print(api_address) # print output for debug

        self.coreDefinings = {
                "word": "",
                "partOfSpeech": "",
                "phonetic": "",
                "definition": "",
                "example": "",
                "origin": ""
            }

        try:
            self.output = {}

                # Fetch definition data: word, phonetics, origin, part of speech, definition, example
            data = requests.get(api_address).json()
            for i in data[0]:
                if i in self.coreDefinings.keys():
                    output = (data[0][i])
                    if output != None:
                        # print(i, output)
                        self.output.update({i:output})

            meanings = data[0]["meanings"][0] # abreviation for the path to get too the definition stuff
            self.output.update({"partOfSpeech":meanings["partOfSpeech"]})
            self.output.update({"definition":meanings["definitions"][0]["definition"]})
            self.output.update({"example":meanings["definitions"][0]["example"]})

            self.output = json.dumps(self.output, ensure_ascii=False, indent=2) # convert to json for file conversion!

            print(self.output) # print filtered output of my desired objects for shoutout

        except requests.ConnectionError as e:
            logging.error(f"No connection!\nError: {e}")
        except KeyError as l:
            logging.error(f"There was a error with finding objects! An API object wasn\'t available, error key: {l}")



    # Read/write dictionary fetched data to json files (temporary or possibly for permanent logging
    # for caching already known words for simplicity)
    def write(self, file, input): # call with self.output
        print("Use this functions file argument with a file extension!")
        try:
            with open(file) as cacheFile:
                cacheFile.write(input)
                logging.info("Written in the file successfully! :D")
        except PermissionError as x:
            logging.error(f"No permission to write file!\nError: {x}")


    # stores written data in values to be shown in main window when needed,
    # can be used live online or locally depending on config
    def fetch(self, lang, customdir: Optional[str]):
        try:
            if customdir is None:
                customdir = "lang_storage"
            for file in os.listdir():
                if file == lang:
                    with open(f"{customdir}/{lang}.json") as fetchFile:
                        data = fetchFile.read()
                        logging.info(f"Read the file, {lang}.json successfully! :D")
                    return data # output read file
                else:
                    logging.debug(f"Passed file {lang}.json!")
        except PermissionError as x:
            logging.error(f"No permission to read {lang}.json!\nError: {x}")





# You must initialize logging, otherwise you'll not see debug output
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = False


# Invoked Request...
nice = Manager()
nice.request("en", "nice")

