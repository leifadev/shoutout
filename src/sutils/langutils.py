"""
Utilities for managing and working with files for Shoutout!'s language database

"""

# Python modules
import requests, os, getpass, json, logging
from pprint import pprint
from typing import Optional


# -*- coding: utf-8 -*-

class Manager:

    def __init__(self):
        self.cacheAddress = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.wikiapi = f'https://en.wiktionary.org/api/rest_v1/'

    def request(self, lang: str, word: str, source: str, multiple=False, format: Optional[str] = ...):
        """
        Queries for provided word to Free Dictionary API to
        fetch it's contents (definition, example, etc.).

        :param lang: type of language, set as global locale codes such as en, ru, pl, jp, etc.
            :type lang: str
        :param word: word of choice to get definition from
            :type word: str
        :param source: source of where the word data is from (Wikitonary or FreeDictionary API)
        :param multiple: Option to set to True if multiple definitions for a word is allowed
        :param format: return the raw data [raw], minimal data (first result) [def], or JSON minimal data [jsondef]

        :return: returns the requested word from it's a specified language with its full definition
        """
        from src.db_maker import cleanhtml

        word = word.lower()

        if source == "wikitonary":
            isWikitonary = True
            api_address = f"https://en.wiktionary.org/api/rest_v1/page/definition/{word}"
            logging.info(api_address)

        elif source == "dictionaryapi":
            isWikitonary = False
            api_address = f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{word}"
            logging.info(api_address)

        else:
            logging.error("Please use either 'wikitonary' or 'dictionaryapi'")
            return

        if isWikitonary:  # Is sourcing from wikitonary
            self.output = {}

            # Get wikitonary data, clean it up of it's html tags, newlines, and backslashed quotes
            raw_data = requests.get(api_address).text.replace("\u2003", "").replace("\n", "").replace('\\"', "")
            cleaned = cleanhtml(raw_data)  # Regex to clean HTML garble
            raw_data = json.loads(cleaned)  # Load it up

            try:
                data = raw_data[lang][0]  # Possibly make this be random?
                pprint(data)
            except KeyError:
                return logging.warning(f"Could not find the definition for the word: '{word}' in the selected language!)"
                                       '\n'
                                       f"You may have spelled it wrong, or we could not find a definition for it!")

            # Reformat the payload from source into shoutout's own format #

            # Index of definition of the word if there's multiple
            word_index = 0
            def_type = "best"

            if def_type == "best":
                word_index = int(0)

            # Find longest definition for secondary option
            elif def_type == "longest":
                stuff = []

                global longest_def
                # Sort dictionary by length
                for y, x in enumerate(data['definitions']):
                    stuff.append(x['definition'])
                    longest_def = sorted(stuff, key=len)[-1]

                # Take longest length definition from for loop above, find the key or place
                # it was in before for later
                for index, e in enumerate(data['definitions']):
                    if e['definition'] == longest_def:
                        word_index = index
                        break

            if multiple:
                definitions = data['definitions']
            else:
                definitions = data['definitions'][word_index]

            # for i in definitions.values():
            #     print(i)

            self.defStruct = {
                "word": word,
                "partOfSpeech": data['partOfSpeech'],
                "language": data['language'],
                "definitions": definitions,
            }

            if self.defStruct is None:
                return "Returned nothing..."

            return self.defStruct


        else:  # Is sourcing from Free Dictionary API
            try:
                self.output = {}

                # Fetch definition data: word, phonetics, origin, part of speech, definition, example
                payload = requests.get(api_address).json()
                for i in payload[0]:
                    if i in self.coreDefinings.keys():
                        output = (payload[0][i])
                        if output is not None:
                            self.output.update({i: output})

                meanings = payload[0]["meanings"][0]  # abbreviation for the path to get too the definition stuff
                self.output.update({"partOfSpeech": meanings["partOfSpeech"]})
                self.output.update({"definition": meanings["definitions"][0]["definition"]})
                self.output.update({"example": meanings["definitions"][0]["example"]})

                # Get data raw, whole payload is outputted without any selected keys (as seen in above code)
                if format == "raw":
                    self.output = payload

                # Get the filtered ideal output in a python dictionary
                elif format == "def":
                    self.output = self.output

                # Get the filtered ideal output in a json object
                elif format == "defjson":
                    self.output = json.dumps(self.output, ensure_ascii=False, indent=2)

                return self.output

            except requests.ConnectionError as e:
                logging.error(f"No connection!\nError: {e}")
            except KeyError as l:
                logging.error(
                    f"There was a error with finding objects! An API object wasn\'t available, error key: {l}")

    @classmethod
    def write(cls, file, mode, your_data: json or dict, overwrite: bool):
        """
        Writes inputted data to any file. Please use 'json' or 'raw' for write modes.
        Choose json for any dictionaries or possibly arrays.

        :param file: Specify file to write too!
        :param mode: Choose using the JSON module
        :param your_data: "json" or "raw":
        Raw mode means you write any type of data possible,
            json means you are using json to dump a json object or python dict type

        :param overwrite: Clear file before you write data
        :return:
        """
        print("Use this functions file argument with a file extension!")
        if overwrite:
            f = open(file, "w+")
            f.truncate(0)
            f.close()
        else:
            pass

        try:
            with open(file, 'w+') as cacheFile:
                if mode == "json":
                    json.dump(cacheFile, your_data, ensure_ascii=False, indent=2)
                elif mode == "raw":
                    cacheFile.write(your_data)
                else:
                    logging.error("Supply the 'json' or 'raw' argument to the mode "
                                  "parameter in the function: write, you just called")
            logging.info("INFO: Written in the file successfully! :D")
        except PermissionError as x:
            logging.error(f"No permission to write file!\nError: {x}")

    @classmethod
    def read(cls, file):
        """
        Reads a files data, special formatting modules applied, just python.

        :param directory: directory to read the file from
        :param file: file selected to read
        :return: returns read data
        """
        print("This function is top read files, use it correctly!")
        try:
            if file.endswith(".json"):
                with open(file, "r") as f:
                    data = json.load(f)
                    logging.info("INFO: Read json file data successfully! To see its output below "
                                 "for debugging, please enable debug mode in logging.")
                    logging.debug(f"Read the file data below:\n{data}")
                    return data
            elif file.endswith(".yml"):
                from tasks import backendTasks as tasks
                tasks.getYAML(file=file)
            else:
                with open(file, 'r') as f:
                    data = f.read()
                    logging.info("INFO: Read file data successfully! To see its output below "
                                 "for debugging, please enable debug mode in logging.")
                    logging.debug(f"Read the file data below:\n{data}")
                    return data
        except PermissionError as e:
            logging.error(f"Permission error! Error:\n{e}")
        except FileNotFoundError as e:
            logging.error(f"File not found error! Error:\n{e}")

    @classmethod
    def fetch(cls, lang, word, directory=f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/lang_storage'):
        """
        Meant to automatically fetch data of a the json word file in
        from the project directory, or specify a custom path to one.

        :param lang: language file selected
        :param word: optional argument to specify any directory (absolute or local)
        :param directory:
        :return: returns value of data read from said JSON file
        """
        logging.debug("Only json files! 'lang_storage' is the default folder")

        try:
            for file in os.listdir(directory):
                if file == word:
                    with open(f"{word}.json") as fetchFile:
                        try:
                            data = json.dumps(fetchFile, ensure_ascii=False, indent=2)
                        except json.encoder.JSONEncoder as a:
                            print(a, "test")
                        logging.info(f"INFO: Read the file, {lang}.json successfully! :D")
                        return data

                elif word not in os.listdir(directory):
                    logging.warning("Word not available!")
            else:
                logging.debug(f"Passed file {lang}.json!")
        except PermissionError as x:
            logging.error(f"No permission to read {lang}.json!\nError: {x}")

    @classmethod
    def extract(cls, file, path=".", deleteZip=False):
        """
        Easily extract files, that's it...

        :param deleteZip: specify if you want the zip file you extracted to be deleted
        :param file: specify file your referring too
        :param path: optional path argument
        :return:
        """
        from zipfile import ZipFile as zipfile
        from zipfile import BadZipFile

        if str(file).endswith(".zip"):

            with zipfile(file, "r") as zip:
                try:
                    zip.extractall(path=path)
                except BadZipFile as e:
                    logging.error(f"Bad zip file! Zip file extracted corrupted and unable to decompress! Error:\n{e}")
                finally:
                    logging.error("No other exceptions teacher for raised ZipFile error.")

        if deleteZip:
            try:
                os.remove(file)
            except FileNotFoundError:
                logging.warning("Unzipped folder to be deleted doesn't exist?")
        else:
            logging.info("Not deleting the extracted zip file...")

    @classmethod
    def collect(cls, action: str, string: str, *files: list):
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
        if string != "group" or "move" or "delete" or "compress":
            logging.error("Please apply a string to support for your chosen action!"
                          "\nOptions: group, move, delete, compress")
            return

        for i in files:
            items = [i]
        logging.debug("Added all selected files to cache!")

        import tarfile
        import shutil

        if action == "group":
            try:
                os.mkdir(string)
                logging.info(f"Making folder in the current directory of: {os.getcwd()}")
            except FileExistsError as e:
                logging.error(f"Couldn't make folder because the name given already exists for a file. \nError:{e}")
                return None

            for i in items:
                shutil.move(str(i), f'{string}/')
                logging.debug(f"Successfully moved item; {i} to {string}")

        elif action == "move":
            try:
                for i in items:
                    shutil.move(str(i), f'{string}')
            except FileNotFoundError as e:
                logging.error(f'Directory destination is not found! \nError: {e}')
                return

        elif action == "delete":
            for i in items:
                os.remove(str(i))
                logging.debug(f"Deleted item {i}")
                return

        elif action == "compress":
            try:
                os.mkdir(string)
            except FileExistsError as e:
                logging.error(f"Couldn't make folder because a folder already exists with that name. \nError:{e}")
            for i in items:
                shutil.move(str(i), f'{string}/')
                logging.debug(f"Successfully moved item; {i} to {string}")
            with tarfile.open(string + ".tar.gz", "w:gz") as f:
                f.add(string)

        elif action == "decompress":
            for i in items:
                with tarfile.open(str(i)) as f:
                    f.extractall()
        else:
            logging.error("Called collect function with invalid action argument!")
            return



logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = False

# if __name__ == "__main__":
#     man = Manager()
#     data = man.request("pl", "cześć", "wikitonary")
#     pprint(data)
