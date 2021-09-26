import random
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.font as tkFont
import platform as platform
import datetime

"""
Features:
 - Timezones
 - Multi-language support
 - Settings
 - Themes
 - Notifications
 - Background running
 - Customizable intervals
    - Change words per day
    - Change notification delay
 - Big logo of flag in the middle of the app
"""


class Window:
    def __init__(self):
        self.date = ""
        self.timezone = ""
        self.theme = "dark"
        self.keys = {} # api keys
        self.lang = "english"
        self.word = ""
        self.definition = ""
        self.launchWord = False
        self.OS = platform.uname()
