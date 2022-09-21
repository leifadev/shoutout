# This file is not a dependency or class, etc. for shout out
# This file's purpose is to gather, generate, and organize large amounts of dictionary data!
import html.parser
import io
import logging
import sys, os, json, re, getpass
from pprint import pprint

import requests

from lang_manager import Manager

manager = Manager()


# Remove HTML tags from content (json)
def cleanhtml(html: json):
    """
    Cleans json objects/dictionaries of ridden HTML code

    :param html: Payloads without HTML tags and syntax
    :return:
    """
    CLEANER = re.compile('<.*?>')
    cleantext = re.sub(CLEANER, "", html)
    return cleantext


class dbFunctions:
    """
    This class is for generating dictionary databases for any language (wikitonary)

    It is designed flexibly to accommodate lots of functions and scripting to have
    full control of managing an creating these databases
    """

    def __init__(self):
        self.cacheAddress = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.languages_table = {  # Available languages to query wikitonary from (table)
            'en': "english",  # English (US)
            'es': "spanish",  # Spanish
            'hi': "hindi",  # Hindi
            'de': "german",  # German
            'fr': "french",  # French
            'ja': "japanese",  # Japanese
            'ru': "russian",  # Russian
            'it': "italian",  # Italian
            'ko': "korean",  # Korean
            'ar': "arabic",  # Arabic
            'pl': "polish",  # Polish
            'zh': "chinese",  # Chinese

            # Extra languages
            'nl': "dutch",  # Dutch
            'pt': "portuguese",  # Portuguese
            'cs': "czech"  # Czech
        }


        # Languages in list form
        self.languages = list(self.languages_table.keys())

        # Make language folder if not present for first time
        os.chdir(self.cacheAddress)  # Cd into config directory
        try:
            os.mkdir("lang_storage/")
            logging.info("INFO: Made the 'lang_storage' directory for storing "
                         "words data and definitions...")
        except FileExistsError as e:
            logging.debug(f"INFO: Folder 'lang_storage' already exists! (not an error at all) \n{e}")


    def createfs(self, sourceDir: str, DatabaseName="lang_storage"):
        """
        Creates the official correct filesystem format for language its database

        :param sourceDir: Directory to create the root file system folder in
        :param DatabaseName: Name of root folder of the database being made
        :return:
        """

        os.chdir(sourceDir)

        # Make root folder
        try:
            os.mkdir(DatabaseName)
        except FileExistsError:
            logging.warning("Folder with specified name for database already exists here!")
            return

        os.chdir(DatabaseName)

        # Make all language folders
        logging.info("Creating language folders! (including downloadable ones)")
        for lang_code in self.languages:
            logging.info(f"Creating {lang_code} language folder...")
            try:
                os.mkdir(lang_code)
            except FileExistsError:
                logging.debug(f"Folder {lang_code} already exists")

    def downloader(self, language, source: list or io.TextIOWrapper, overwrite=False):
        """
        Downloads definitions of all words in the provided wordlist (russian.txt, english.txt)
        file or a python list

        :param overwrite: overwrite a definition (the file) if it is already in the database
        :param language: Language that provided words are in (this is crucial, please be accurate!)
        :param source: Source of list of words to provide definitions for
        :return: A definition of each word from a list of words
        """

        # logging.info(
        #     f'Available word-of-the-day lists in languages of:\n{os.listdir("project_resources/")}')

        os.chdir(self.cacheAddress + f"lang_storage/{language}")
        if type(source) is io.TextIOWrapper:
            source = source.readlines()
            source.sort()

            # Remove any empty lines
            for line in source:
                if line == "\n":
                    source.remove(line)

        elif type(source) is list:
            print(f'Using a list...')

        # results = {}

        global fetch
        for word in source:

            if word is not None:

                # Remove escape line characters for file
                word = str(word).replace("\n", "")

                word_path = f'{self.cacheAddress}lang_storage/{language}/{word}.json'

                # Skipping creating definition because it already exists in a file
                if not os.path.isfile(word_path) or overwrite is True:

                    # Request a word
                    fetch = manager.request(language, word, "wikitonary", multiple=False)

                    if type(fetch) != dict:
                        logging.info(f"Skipping file creation of '{word}'...")

                    else:
                        # Compile full dictionary output of definitions (not used in files)
                        # results.update({word: fetch})

                        # Debug msg each download
                        logging.debug(f"Downloading word: '{word}' in language: {language}")

                        # Dump each fetched word from request method into a separate json file
                        self.fileDump(word, {word: fetch}, self.cacheAddress + f"lang_storage/{language}")
                else:
                    pass

    def fileDump(self, title: str, payload: dict or json, location: str):
        """
        Dumps dictionary or json data into a file

        Checks for if a file extension exists, keeps ascii special characters
        intact with the json dump method with ensure_ascii=False

        :param title: name of file
        :param payload: payload of json data, dictionaries are also accepted
        :param location: directory dump file in
        :param overwrite: overwrite existing files
        :return:
        """
        if not location.endswith("/"):  # Make directory selected have a slash
            location = location + "/"
        if location.endswith(".json"):  # Check if we need to add a .json file extension if not present
            pass
        else:
            title = title + ".json"

        # Create and dump the file!
        with open(location + title, "w+") as file:
            json.dump(payload, file, ensure_ascii=False,
                      indent=2)  # Leave ensure_ascii on for special lang characters (chinese, etc.)
            # logging.info(f"Writing definition to file {title} at location {location}...")

    def databaseStats(self, sourceDirName):
        """
        Returns statistics of the language database

        :param sourceDirName: Directory of database
        :return: Returns per-language folder sizes and defintion counts
        """

        self.dbstats = {
            "languages": {
                # 'example_lang': {
                #     "dbsize": int,
                #     "definitionCount": int
                # }
            }
        }

        # This returns stats about the database like how many files are in
        # each lang folder etc. (Use this info is front end?)
        os.chdir(sourceDirName)

        # Loop through language database
        for folder in os.listdir():

            if folder != ".DS_Store":

                # Count languages in storage
                self.dbstats["languages"].update({folder: {}})

                from humanize import naturalsize

                # Get size of each language folder
                os.chdir(self.cacheAddress + "lang_storage")

                size = 0

                for file in os.listdir(folder):
                    if file != ".DS_Store":
                        l = os.path.getsize(f'{folder}/' + file)
                        logging.debug(f'{folder}: {file} is {naturalsize(l)} in size!')
                        size += l
                size = naturalsize(size)

                self.dbstats['languages'][folder].update({"dbsize": size})

                count = os.listdir(folder)
                # Remove .DS_Store
                for i in count:
                    if i == ".DS_Store":
                        count.remove(i)

                count = str(len(count))

                self.dbstats['languages'][folder].update({"definitionCount": count})


        return pprint(self.dbstats)


from bs4 import BeautifulSoup


class htmlx:
    """
    Fetch and handle HTML data for word of the day websites (currently merriam-webster.com)

    """

    import datetime

    def fetchWord(self, date: datetime):
        """
        Fetch word of the day on merriam webster dictionary website's word of the day

        :param date: Date of word of the day to fetch, accepts datetime.date.today object
        :return: Word of the day for specified day on merriam-webster dictionary website
        """

        global word

        # Fetch word of the day page
        content = requests.get(f"https://www.merriam-webster.com/word-of-the-day/{date}").text

        # Turn text content into bs4 html parser object
        soup = BeautifulSoup(content, 'html.parser')

        # Roughly find the div containing the word of the day (big word at the center of the page)
        entry = soup.find('div', {"class": "word-and-pronunciation"})

        # Parse through div lines to find word of the day h1 string, remove html tags
        for line in str(entry).splitlines():
            if "<h1>" in line:
                word = line
                break
            else:
                pass

        # Clean it's HTML tags
        word = cleanhtml(word)

        # Remove words that are cognates, have spaces, or have dashes in them (keep it simple)
        # for google translate and wikitonary... and myself
        prohibited_chars = [' ', '-']

        if any(x in word for x in prohibited_chars):  # Pass if ASCII (non-english) characters are present
            logging.info(f"Skipping word: {word} because it's invalid")
        elif not word.isascii():
            logging.info(f"Skipping word: {word} because it's invalid")
        else:
            return word

    def translateGenerator(self, word_input: str, source_lang: str, target_lang: str):
        """
        Translate a word (or phrase) into another language!

        Uses google translate API services B)

        :param word_input: Word to be translated
        :param source_lang: Language translating from
        :param target_lang: Language to translate text into
        :return:
        """

        global result
        from google.cloud import translate_v2, translate_v3
        import six

        # v2 Translate
        # googlebot = translate_v2.Client()
        # text = ""
        # if isinstance(text, six.binary_type):
        #     text = text.decode("utf-8")
        # target = "en"
        # result = googlebot.translate(text, target_language=target)

        betterbot = translate_v3.TranslationServiceClient()

        project_id = "troop-282"
        # model_id = "YOUR_MODEL_ID"
        location = "us-central1"
        parent = f"projects/{project_id}/locations/{location}"
        import google
        try:
            result = betterbot.translate_text(
                request={
                    "contents": [word_input],
                    "target_language_code": target_lang,
                    "source_language_code": source_lang,
                    "parent": parent,
                    "mime_type": "text/plain"
                    # "model": model_path,
                }

            )
        except TypeError:  # Pass if we encounter parsing a NoneType
            pass
        except google.api_core.exceptions.ServiceUnavailable:
            import time
            logging.warning("Network connection failed!")

        # Narrow down google's payload to just -the- text
        x = str(result.translations[0])
        translated_word = re.sub('(^[^"]+|(?<=")[^"]+$)', "", x).replace('"', "")  # Remove everything outside quotes

        return translated_word

    def dateGenerate(self, startDate: tuple, endDate: tuple, language):
        """
        Generates a range of dates, then gets a word of the day for each day within
        the specified date ranges. This uses fetchWord() that takes from merriam-webster's
        word-of-the-day website.

        This function supports also generating words in languages in other languages besides
        english, which translates english word-of-the-days to other languages!

        :param startDate: Tuple type for a starting date (e.g. 2009, 1, 5)
        :param endDate: Tuple for a ending date (e.g. 2018, 5, 5)
        :param language: Language to generate words in (uses translateGenerator function)
        :return: Generates a word of the day for each date within a range of dates
        """

        # Generate dates
        global word
        from datetime import date, timedelta

        start_date = date(startDate[0], startDate[1], startDate[2])
        end_date = date(endDate[0], endDate[1], endDate[2])
        delta = timedelta(days=1)

        while start_date <= end_date:
            looped_data = start_date.strftime("%Y-%m-%d")
            start_date += delta

            if language == "en":
                word = self.fetchWord(looped_data)
            else:
                en_word = self.fetchWord(looped_data)
                word = self.translateGenerator(en_word, "en", language)  # translate word from english too whatever

            # Check if none
            if word is None:
                pass
            else:
                yield word

    def writeFile(self, filename: str, lang: str, source="english.txt"):
        """
        This writes all supplied words from the (default) english.txt file into their newly
        translated forms in another text file

        :param filename: name of file to write too
        :param lang: language to have words translated into
        :param source: source to grab word of the day words from
        :return:
        """
        os.chdir(".")
        count = 0
        with open("/Users/leif/PycharmProjects/shoutout/english.txt", "r") as f:
            import datetime

            # Enable to generate word list from merriam webster dictionary website
            # for i in cool.dateGenerate((2007, 9, 1), (2022, 8, 16), language):
            #     count += 1
            #     print(count)
            #     print(i)
            #     f.write(f'{i}\n')

            with open(filename, "w+") as l:

                for line in f.readlines():
                    if line in l.readlines():
                        pass
                    else:
                        # Remove extra \n from readlines method
                        line = str(line).replace("\n", "")

                        # Count every loop to track words translated
                        count += 1

                        # Pass word through google translate
                        translated = cool.translateGenerator(line, "en", lang).replace("\n", "").replace('\\"', "")
                        l.write(f'{translated}\n')
                        print(translated, f'count {str(count)}')

    def filterWords(self, wordlist: str, mode: str):
        """
        Filters certain word files to be remove etc. in a generated word list from
        translateGenerator or other functions in db_maker.py

        Some translated words (usually from the english.txt wordlist)

        :param wordlist: Name of text file word list (use txt!)
        :param mode:
        contains: Remove words that conatin certain specified characters (!?'")
        doubles: Removes duplicate words,
        long: Removes long words,
        spaces: Removes words that have a certain amount of spaces in them
        capitals: Removes words with certain amounts of capital letters in them

        :return: Filtered list content
        """

        with open(wordlist, "r+") as content:
            for i in content.readlines():

                # Remove \n charcters from readlines method
                i = str(i).replace("\n", "")

                if mode == "contains":
                    pass
                elif mode == "doubles":
                    pass
                elif mode == "long":
                    pass
                elif mode == "spaces":
                    pass
                elif mode == "capitals":
                    pass
                else:
                    logging.error(
                        "Supply the 'contains', 'doubles', 'long', 'spaces', 'capitals' arguments to the mode "
                        "parameter in the function")


if __name__ == "__main__":
    project_dir = f"/Users/{getpass.getuser()}/Library/Application Support/shoutout/"
    os.chdir("//")

    # Functions to run (kind of in order I guess)

    # Instance of classes
    cool = htmlx()
    rad = dbFunctions()

    # Running fetchWord fetches a list of words from merriam-websters word-of-the-day page
    # Then runs dateGenerator to loop through all days of the specified ranges of calender dates with fetchWord
    # for i in cool.dateGenerate((2007, 9, 1), (2022, 8, 17), "en"):
    #     cool.fetchWord(i)

    # Running writeFile that translates a given list of words into another language
    # cool.writeFile("hindi.txt", "hi")

    # Download the definitions of words from a list of them (works in any language of course)
    # lang = "hi"  # Variable to use in the function for brevity
    # with open(f'/Users/leif/PycharmProjects/shoutout/project_resources/wordlist_data/hindi.txt', 'r') as file:
    #     rad.downloader(lang, file, overwrite=False)

    # See statistics of your database
    rad.databaseStats(project_dir + 'lang_storage/')
