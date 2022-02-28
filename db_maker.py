# This file is not a dependency or class, etc. for shout out
# This file's purpose is to gather, generate, and organize large amounts of dictionary data!
import logging
import sys, os, requests, json
from lang_manager import Manager


class dbFunctions:

    def __init__(self):
        self.mode = ["download", "gather", "organize"]
        sys.argv = self.mode.insert(0, "db_maker.py")

        try:
            os.mkdir("lang_storage/wordlist_data")
            logging.info("INFO: Made the 'wordlist_data' directory for storing "
                         "un-compiled words and definitions for construction")
        except FileExistsError as e:
            logging.info(f"INFO: Folder 'wordlist_data' already exists! \n{e}")


    def sifter(self, file):
        # Manage wordlist for total words to obtain data of. These may be multiple ways besides just using ne API, etc.
        with open(file, 'w+') as doc:
            pass


    def downloader(self):
        # Request one word
        Manager.request("en", "word", "jsondef")
