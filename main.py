import platform as platform
import getpass

import Cocoa
from Cocoa import *
import Foundation
from AppKit import *


class mainWindow(Cocoa.NSWindowController):

    def __init__(self):
        self.keys = {} # api keys
        self.OS = platform.uname()
        self.date = ""
        self.timezone = ""
        self.theme = "dark"
        self.lang = "english"
        self.version = "beta~v0.0.1"
        self.launchWord = False
        self.backendDir = f'/Users/{getpass.getuser()}/Library/Application Support/'
        self.settingDir = f'/Users/{getpass.getuser()}/Library/Application Support/Shoutout'

        self.definitionFull = {

            "word": "",
            "definition": "",
            "phoentics": "",
            "pronounceAudio": ""
        }

    def windowDidLoad(self):
        Cocoa.NSWindowController.windowDidLoad(self)

    @objc.IBAction
    def increment_(self, sender):
        self.count += 1
        self.updateDisplay()

    @objc.IBAction
    def decrement_(self, sender):
        self.count -= 1
        self.updateDisplay()


    def updateDisplay(self):
        self.counterTextField.setStringValue_(self.count)



# Loop it and stuff

if __name__ == "__main__":
    app = Cocoa.NSApplication.sharedApplication()

    # Initiate the contrller with a XIB
    viewController = mainWindow.alloc().initWithWindowNibName_("shoutout_main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    Cocoa.NSApp.activateIgnoringOtherApps_(True)

    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()


# Make Landing Page!
# https://carrd.co/build#landing