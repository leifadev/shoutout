import requests, os, getpass, json, logging
from pprint import pprint


# For caching, fetching, and managing data, and more from the Free Dictionary API ==> https:#dictionaryapi.dev/


# -*- coding: utf-8 -*-

class Manager:

    def __init__(self):
        self.cacheAddress = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.languages = [ # overall available languages for shoutout, provided by me (polish as of now) and API itself
            'hi', 	 # Hindi
            'en',    # English (US)
            'en-uk', # English (UK)
            'es', 	 # Spanish
            'fr',	 # French
            'ja',    # Japanese
            'cs',    # Czech
            'nl',    # Dutch
            'sk',    # Slovak
            'ru',	 # Russian
            'de', 	 # German
            'it', 	 # Italian
            'ko',	 # Korean
            'pt-BR',  # Brazilian Portuguese
            'ar',    # Arabic
            'tr',     # Turkish
            'pl'      # Polish <-- {NOT PROVIDED BY API, BUILT FROM IT AND OTHER SOURCES}
        ]

        self.coreDefinings = {
            "word": "",
            "partOfSpeech": "",
            "phonetic": "",
            "definition": "",
            "example": "",
            "origin": ""
        }


    def request(self, lang, word, type):
        """
        Requests a query for provided word to Free Dictionary API to
        fetch it's contents (definition, example, etc.).

        :param lang: type of language, set as global locale codes such as en, ru, pl, jp, etc.
            :type lang: str
        :param word: word of choice to get definition from
            :type word: str
        :param type: return the raw data [raw], filtered data (first definition) [def], or JSON filtered data [jsondef]
            :type type: str
        :return: returns the requested data from https:#api.dictionaryapi.dev
        """

        api_address = f"https:#api.dictionaryapi.dev/api/v2/entries/{lang}/{word}"

        try:
            self.output = {}

            # Fetch definition data: word, phonetics, origin, part of speech, definition, example
            data = requests.get(api_address).json()
            for i in data[0]:
                if i in self.coreDefinings.keys():
                    output = (data[0][i])
                    if output is not None:
                        # print(i, output)
                        self.output.update({i:output})

            meanings = data[0]["meanings"][0] # abreviation for the path to get too the definition stuff
            self.output.update({"partOfSpeech":meanings["partOfSpeech"]})
            self.output.update({"definition":meanings["definitions"][0]["definition"]})
            self.output.update({"example":meanings["definitions"][0]["example"]})

            if type == "raw":
                self.output = data
            elif type == "def":
                self.output = self.output
            elif type == "defjson":
                self.output = json.dumps(self.output, ensure_ascii=False, indent=2) # convert to json for file conversion!

            return self.output

        except requests.ConnectionError as e:
            logging.error(f"No connection!\nError: {e}")
        except KeyError as l:
            logging.error(f"There was a error with finding objects! An API object wasn\'t available, error key: {l}")


    def write(self, file, mode, input):
        """
        Writes inputted data to any file. Please use 'json' or 'raw' for write modes.
        Choose json for any dictionaries or possibly arrays.

        :param file: Specify file to write too!
        :param mode: Choose using the JSON module
        :param input:
        :return:
        """
        print("Use this functions file argument with a file extension!")
        try:
            with open(file, 'w+') as cacheFile:
                if mode == "json":
                    json.dump(cacheFile, input, ensure_ascii=False, indent=2)
                elif mode == "raw":
                    cacheFile.write(input)
                else:
                    logging.error("Supply the 'json' or 'raw' argument to the mode "
                                  "argment in the function: write, you just called")
            logging.info("INFO: Written in the file successfully! :D")
        except PermissionError as x:
            logging.error(f"No permission to write file!\nError: {x}")


    def read(self, file):
        """
        Reads a files data, special formatting modules applied, just python.

        :param file: file selected to read
        :return: returns read data
        """
        print("This function is top read files, use it correctly!")
        try:
            with open(file, 'r') as cacheFile:
                data = cacheFile.read()
                logging.info("INFO: Read file data successfully! To see its output below "
                             "for debugging, please enable debug mode in logging.")
                logging.debug(f"Read the file data below:\n{data}")
            return data
        except PermissionError as e:
            logging.error(f"Permission error! Error:\n{e}")
        except FileNotFoundError as e:
            logging.error(f"File not found error! Error:\n{e}")



    def fetch(self, lang, customdir="lang_storage"):
        """
        Meant to automatically fetch any of the language JSON files locally
        from the project directory, or specify a custom path to one.

        :param lang: language file selected
        :param customdir: optional argument to specify any directory (absolute or local)
        :return: returns value of data read from said JSON file
        """
        logging.debug("Only json files! 'lang_storage' is the default folder")
        try:
            logging.info(f"INFO: Custom directory: {customdir} selected!")
            print(os.listdir())
            for file in os.listdir():
                if file == lang:
                    with open(f"{customdir}/{lang}.json") as fetchFile:
                        self.data = json.dumps(fetchFile, ensure_ascii=False, indent=2)
                        logging.info(f"INFO: Read the file, {lang}.json successfully! :D")
                        pprint(self.data)
                    return self.data  # output read file
            else:
                logging.debug(f"Passed file {lang}.json!")
        except PermissionError as x:
            logging.error(f"No permission to read {lang}.json!\nError: {x}")


    def sort(self, data, sort="alphabetical"):
        """
        Most likely called with the above fetch function, to parse through the language data from Free Dictionary API.

        :param data: data passed through the function to have "word" keys sorted
        :param sort: type of sorting algorithm for each word iterated through;
        options are alphabetical, reverse, complexity

        :return: returns value of sorted data passed
        """

        words = {}
        tk = [] # tmp keys, tmp values
        tv = []

        # loop through definition' word values, assign key values
        for key, value in enumerate(data):
            tk.append(key)
            tv.append(value["word"])
            if sort == "alphabetical":
                tk.sort()
                tv.sort()
            elif sort == "reverse":
                tv.sort(reverse=True)
            elif sort == "complexity":
                tv.sort(key=len)
            else:
                logging.error("Called collect function with invalid sort argument!")

        l = -1
        for i in tv:
            l += 1
            words.update({l: i})
        print(f"Sorting method: {sort}\n{words}")
        return words, tv


    def extract(self, file, path="."):
        """
        Easily extract things, that's it...

        :param file: specify file your referring too
        :param path: optional path argument
        :return:
        """
        from zipfile import ZipFile as zipfile
        from zipfile import BadZipFile

        with zipfile(file, "r") as zip:
            try:
                zip.extractall(path=path)
            except BadZipFile as e:
                logging.error(f"Bad zip file! Zip file extracted corrupted and unable to decompress! Error:\n{e}")
            finally:
                logging.error("No other exceptions eacher for raised ZipFile error.")


    def collect(self, action, string="", *files):  # collect items to group, move, delete, or compress them
        """
        Collect is a function to group, move, delete, or compress bulk amounts of files at once.
        This may be a very common one to use and is wise to as well. Add as many files as you need
        after the first two arguments.

        :param action: Type of action you want to invoke for the file(s): group, move, delete, compress
        :param string: String input corresponding to each action (e.g. name of file or folder, destination folder, etc.)
        :param files: Any amount of files to be fed through the function.
        :return:
        """

        global items
        if string == "":
            logging.error("Please apply a string to support for your chosen action!")
            return

        for i in files: #
            items = []
            items.append(i)
        logging.debug("Added all selected files to cache!")

        from zipfile import ZipFile as zipfile
        import shutil

        if action == "group":
            try:
                os.mkdir(string)
            except FileExistsError as e:
                logging.error(f"Couldn't make folder because the name given already exists for a file. \nError:{e}")
            for i in items:
                shutil.move(str(i), f'{string}/')
                logging.debug(f"Successfully moved item; {i} to {string}")

        elif action == "move":
            try:
                for i in items:
                    shutil.move(str(i), f'{string}')
            except FileNotFoundError as e:
                logging.error(f'Directory destination is not found! \nError: {e}')

        elif action == "delete":
            for i in items:
                os.remove(i)
                logging.debug(f"Deleted item {i}")

        elif action == "compress":
            try:
                os.mkdir(string)
            except FileExistsError as e:
                logging.error(f"Couldn't make folder because the name given already exists for a file. \nError:{e}")
            for i in items:
                shutil.move(str(i), f'{string}/')
                logging.debug(f"Successfully moved item; {i} to {string}")
            with zipfile(string, "r") as zip:
                zip.write(string, f'{string}.zip')
        else:
            logging.error("Called collect function with invalid action argument!")
            return


# You must initialize logging, otherwise you'll not see debug output
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = False


if __name__ == "__lang_manager__":
    # lol = [{'word': 'bword', 'phonetic': 'wəːd', 'phonetics': [{'text': 'wəːd', 'audio': '#ssl.gstatic.com/dictionary/static/sounds/20200429/word--_gb_1.8.mp3'}], 'origin': 'Old English, of Germanic origin; related to Dutch woord and German Wort, from an Indo-European root shared by Latin verbum ‘word’.', 'meanings': [{'partOfSpeech': 'noun', 'definitions': [{'definition': 'a single distinct meaningful element of speech or writing, used with others (or sometimes alone) to form a sentence and typically shown with a space on either side when written or printed.', 'example': "I don't like the word ‘unofficial’", 'synonyms': ['term', 'name', 'expression', 'designation', 'locution', 'turn of phrase', 'idiom', 'appellation', 'vocable'], 'antonyms': []}, {'definition': 'a command, password, or signal.', 'example': 'someone gave me the word to start playing', 'synonyms': ['instruction', 'order', 'command', 'signal', 'prompt', 'cue', 'tip-off', 'go-ahead', 'thumbs up', 'green light', 'high sign', 'decree', 'edict', 'mandate', 'bidding', 'will'], 'antonyms': []}, {'definition': "one's account of the truth, especially when it differs from that of another person.", 'example': 'in court it would have been his word against mine', 'synonyms': [], 'antonyms': []}, {'definition': 'the text or spoken part of a play, opera, or other performed piece; a script.', 'example': 'he had to learn his words', 'synonyms': ['script', 'text', 'lyrics', 'libretto'], 'antonyms': []}, {'definition': 'a basic unit of data in a computer, typically 16 or 32 bits long.', 'synonyms': [], 'antonyms': []}]}, {'partOfSpeech': 'verb', 'definitions': [{'definition': 'express (something spoken or written) in particular words.', 'example': 'he words his request in a particularly ironic way', 'synonyms': ['phrase', 'express', 'put', 'couch', 'frame', 'set forth', 'formulate', 'style', 'say', 'utter', 'state'], 'antonyms': []}]}, {'partOfSpeech': 'exclamation', 'definitions': [{'definition': 'used to express agreement or affirmation.', 'example': "Word, that's a good record, man", 'synonyms': [], 'antonyms': []}]}]}, {'word': 'aword', 'phonetics': [{}], 'meanings': [{'partOfSpeech': 'combining form', 'definitions': [{'definition': "denoting a slang word, or one that may be offensive or have a negative connotation, specified by the word's first letter.", 'example': 'the F-word', 'synonyms': [], 'antonyms': []}]}]}, {'word': 'dthe Word', 'phonetics': [{}], 'meanings': [{'definitions': [{'definition': 'the Bible, or a part of it.', 'synonyms': [], 'antonyms': []}, {'definition': 'Jesus Christ.', 'synonyms': [], 'antonyms': []}]}]}]
    cool = Manager()
    data = cool.request("en", "family", "raw")
    cool.sort(data, sort="alphabetical")
