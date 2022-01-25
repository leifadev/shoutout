from dataclasses import dataclass
import requests, os, pprint # request api online data and make files for it etc.
import aiohttp

# For cacheing, fetching, and managing data, and more from the Free Dictionary API ==> https://dictionaryapi.dev/


@dataclass
class data:
    os.getcwd()



class Manager():

    # Requests
    def request(self, lang, word):
        api_address = f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{word}"
            requests.get()
            print(data)

nice = Manager()
nice.request("en", "nice")