# This file is not a dependency or class, etc. for shout out
# This file's purpose is to gather, generate, and organize large amounts of dictionary data!

import sys, os, requests, json


class dbFunctions():

    def __init__(self):
        self.mode = ["download", "gather", "organize"] # make code execution dependent on different modes
        # [download] is for downloading data from API's and distributing it
        # [gather] is for different libraries and API's to manually search for other language defition data
        # such as organize and use multiple sources from scratch and make an unsupported Free Dictionary API language
        # [organize] is
        sys.argv = self.mode.insert(0, "db_maker.py")
        self.api = ""


    def scrape(self): # indexes and downloads data in bulk, the goal being to localize it for less internet reliance
        pass