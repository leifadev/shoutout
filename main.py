import platform as platform
from Cocoa import *
from Foundation import *
#import wiktionaryparser
import getpass

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
 
 
 ## Version naming:
Betas:
 - beta~v0.0.1
 - beta~v0.0.2
 Beta releases dont have any rhyme or reason for there increments in numbers. However, 
 
Releases:
 First major release should be
 - v1.0.0
 - v1.1.0
 - v1.2.0
 - v2.0.0
and so on in this pattern :)

"""



class mainWindow(NSWindowController):
    self.date = ""
    self.timezone = ""
    self.theme = "dark"
    self.lang = "english"
    self.version = "beta~v0.0.1"
    self.launchWord = False
    self.backendDir = f'/Users/{getpass.getUser}/Library/Application Support/'
    self.settingDir = f'/Users/{getpass.getUser}/Library/Application Support/Shoutout'
    self.definitionFull = {
        
        "word": "",
        "definition": "",
        "phoentics": "",
        "pronounceAudio": ""
        
        
}

    def __init__(self):
        self.keys = {} # api keys
        self.OS = platform.uname()






# Make Landing Page!
# https://carrd.co/build#landing
