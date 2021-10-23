import platform as platform
from Cocoa import *
from Foundation import *

"""
Features:
 - Timezones
 - Multi-language support
 - Settings
 - Themes
 - Notifications (daemon)
 - Customizable intervals
    - Change words per day
    - Change notification delay
    - Change complexity
 - Simple UI
 - Landing page website (carrd.co) 
"""


class mainWindow(NSWindowController):
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





Make Landing Page!
# https://carrd.co/build#landing
