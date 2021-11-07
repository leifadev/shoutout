import platform as platform
from Cocoa import Cocoa
from Foundation import Cocoa
import getpass
import random

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
Beta:
 - beta~v0.0.1
 - beta~v0.0.2
 Beta releases dont have any rhyme or reason for there increments in numbers. However, 
 
Release:
 -


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

    self.definitionFull["word"] = "spicey"

    def __init__(self):
        self.keys = {} # api keys
        self.OS = platform.uname()






# Make Landing Page!
# https://carrd.co/build#landing
