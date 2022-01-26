from dataclasses import dataclass
import requests, os, getpass
import logging
from pprint import pprint

# For cacheing, fetching, and managing data, and more from the Free Dictionary API ==> https://dictionaryapi.dev/


# -*- coding: utf-8 -*-

@dataclass
class data:
    max_tries: int = 3
    api_address: str = "https://api.dictionaryapi.dev/api/v2/entries/"
    cacheAddress: str = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'



class Manager():

    # You must initialize logging, otherwise you'll not see debug output
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


    # Requests all relevant data for specified word and language, returns it in >>> self.output! <<<
    def request(self, lang, word):
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

            pprint(f'{self.output}') # print filtered output of my desired objects for shoutout

        except ConnectionError as e:
            print(f"Error!\n{e}")
        except KeyError as l:
            print(f'There was a error with finding objects! A API object wasn\'t available (e.g. example)\n{l}')

    def write(self, input):
        pass



# Invoked Request...
nice = Manager()
nice.request("en", "verbose")

