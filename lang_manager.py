from dataclasses import dataclass
import requests, os, getpass
import pprint as pprint


# For cacheing, fetching, and managing data, and more from the Free Dictionary API ==> https://dictionaryapi.dev/


# -*- coding: utf-8 -*-

@dataclass
class data:
    max_tries: int = 3
    api_address: str = "https://api.dictionaryapi.dev/api/v2/entries/"
    cacheAddress: str = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'



class Manager():

    # Requests
    def request(self, lang, word):
        api_address = f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{word}"
        # print(api_address) # print output for debug

        self.coreDefinings = [
                "word",
                "phonetic",
                "origin",
                "partOfSpeech",
                "definition",
                "example"
            ]


        try:
            self.output = []

            # Fetch definition data: word, phonetics, origin, part of speech, definition, example

            data = requests.get(api_address).json()
            for i in data[0]:
                if i in self.coreDefinings:
                    output = print((data[0][i]))
                    self.output.append(output)

            meanings = data[0]["meanings"][0]
            self.output.append(meanings["partOfSpeech"])
            self.output.append(meanings["definitions"][0]["definition"])
            for l in self.output:
                if l is None:
                    self.output.remove(l)

            print(meanings)

        except requests.exceptions.ConnectionError as e:
            print(f"Error!\n{e}")





# Invoked Request...
nice = Manager()
nice.request("en", "pole")



langAPI = [{'word': 'pole', 'phonetic': 'pəʊl', 'phonetics': [{'text': 'pəʊl', 'audio': '//ssl.gstatic.com/dictionary/static/sounds/20200429/pole--1_gb_3.mp3'}], 'origin': 'late Old English pāl (in early use without reference to thickness or length), of Germanic origin; related to Dutch paal and German Pfahl, based on Latin palus ‘stake’.', 'meanings': [{'partOfSpeech': 'noun', 'definitions': [{'definition': 'a long, slender, rounded piece of wood or metal, typically used with one end placed in the ground as a support for something.', 'example': 'a tent pole', 'synonyms': ['post', 'pillar', 'stanchion', 'standard', 'paling', 'pale', 'stake', 'stick', 'picket', 'palisade', 'support', 'prop', 'batten', 'mast', 'bar', 'shaft', 'rail', 'rod', 'beam', 'spar', 'crosspiece', 'upright', 'vertical', 'staff', 'stave', 'cane', 'spike', 'baton', 'truncheon'], 'antonyms': []}, {'definition': 'another term for perch3 (sense 1 of the noun).', 'synonyms': [], 'antonyms': []}]}, {'partOfSpeech': 'verb', 'definitions': [{'definition': 'propel (a boat) by pushing a pole against the bottom of a river, canal, or lake.', 'example': 'the boatman appeared, poling a small gondola', 'synonyms': [], 'antonyms': []}]}]}, {'word': 'pole', 'phonetic': 'pəʊl', 'phonetics': [{'text': 'pəʊl', 'audio': '//ssl.gstatic.com/dictionary/static/sounds/20200429/pole--1_gb_3.mp3'}], 'origin': 'late Middle English: from Latin polus ‘end of an axis’, from Greek polos ‘pivot, axis, sky’.', 'meanings': [{'partOfSpeech': 'noun', 'definitions': [{'definition': 'either of the two locations ( North Pole or South Pole ) on the surface of the earth (or of a celestial object) which are the northern and southern ends of the axis of rotation.', 'synonyms': [], 'antonyms': []}]}]}, {'word': 'pole', 'phonetic': 'pəʊl', 'phonetics': [{'text': 'pəʊl', 'audio': '//ssl.gstatic.com/dictionary/static/sounds/20200429/pole--1_gb_3.mp3'}], 'meanings': [{'partOfSpeech': 'noun', 'definitions': [{'definition': 'short for pole position.', 'synonyms': [], 'antonyms': []}]}]}, {'word': 'Pole', 'phonetic': 'pəʊl', 'phonetics': [{'text': 'pəʊl', 'audio': '//ssl.gstatic.com/dictionary/static/sounds/20200429/pole--1_gb_3.mp3'}], 'origin': 'via German from Polish Polanie, literally ‘field-dwellers’, from pole ‘field’.', 'meanings': [{'partOfSpeech': 'noun', 'definitions': [{'definition': 'a native or inhabitant of Poland, or a person of Polish descent.', 'synonyms': [], 'antonyms': []}]}]}]

