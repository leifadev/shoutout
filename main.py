import platform as platform
import getpass, os, time


from Cocoa import *
from Foundation import *
from Cocoa import NSWorkspace
from AppKit import *


class mainWindow(NSWindowController):
    link = objc.IBOutlet()
    inc = objc.IBOutlet()

    def __init__(self):
        self.keys = {} # api keys
        self.OS = platform.uname()
        self.date = ""
        self.timezone = time.tzname[0]
        self.theme = "dark"
        self.lang = "english"
        self.version = "beta~v0.0.1"
        self.launchWord = False
        self.backendDir = f'/Users/{getpass.getuser()}/Library/Application Support/'
        self.settingDir = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout'
        self.count = 0
        self.gitUrl = ("https://github.com/leifadev/sheath")
        self.definitionFull = {
            "word": "",
            "definition": "",
            "phoentics": "",
            "pronounceAudio": ""
        }


    def windowDidLoad(self): # calling windowDidLoad from Cocoa!
        NSWindowController.windowDidLoad(self)


    @objc.IBAction
    def helplink_(self, sender):
        print("Help URL Launched!")
        x = NSURL.alloc().initWithString_(self.gitUrl)
        NSWorkspace.alloc().init().openURL_(x)


    @objc.IBAction
    def increment_(self, sender):
        self.count += 1
        print(self.count)
        self.updateDisplay()


    @objc.IBAction
    def decrement_(self, sender):
        self.count -= 1
        print(self.count)
        self.updateDisplay()


    def updateDisplay(self):
        self.outlet.setStringValue_(self.count)


    def configFolder(self):
        if not os.path.exists(self.settingDir):
            os.mkdir(self.settingDir) # make folder because im a god
        else:
            print("Config folder is completed!")




# Loop it and stuff

if __name__ == "__main__":
    app = NSApplication.sharedApplication()

    # Initiate the contrller with a XIB
    viewController = mainWindow.alloc().initWithWindowNibName_("shoutout_main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)

    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()


# Make Landing Page!
# https://carrd.co/build#landing
