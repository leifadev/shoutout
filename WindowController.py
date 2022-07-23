import os

# Objective-C
import Cocoa, objc
from AppKit import NSApp


# Global stuff
version = "beta~v0.0.1"


class mainWindow(Cocoa.NSWindowController):

    outlet = objc.IBOutlet()

    def __init__(self):
        self.theme = ["dark", "light"]
        self.count = 0
        self.definitionFull = {
            "word": "",
            "definition": "",
            "phoentics": "",
            "pronounceAudio": ""
        }


    def windowDidLoad(self):
        Cocoa.NSWindowController.windowDidLoad(self)


    @objc.IBAction
    def helplink_(self, sender):
        url = ("https://github.com/leifadev/shoutout/wiki")
        print(f"{url} launched")
        x = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(x)

    # Increment numbers display stuff (from dawes.wordpress.com)
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

    @objc.IBAction
    def showAWindow_(self, sender):
        print("Showing preferences!")
        viewControllerPref = prefWindow.alloc().initWithWindowNibName_("shoutout_preferences")
        viewControllerPref.showWindow_(viewControllerPref)


class prefWindow(Cocoa.NSWindowController):

    outlet = objc.IBOutlet()

    def __init__(self):
        self.theme = ["dark", "light"]
        self.complexity = [1, 2, 3]
        self.notification_config = {
         "perDay": 1,
         "delay": 360 # 6 hours, **in minutes**
        }

    @objc.IBAction
    def openlink_(self, sender):
        url = ("https://github.com/leifadev/shoutout/")
        print(f"{url} launched")
        x = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(x)


# Starting window!

if __name__ == "__main__":
    app = Cocoa.NSApplication.sharedApplication()

    # Initiate the controller with a XIB
    viewController = mainWindow.alloc().initWithWindowNibName_("shoutout_main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)

    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()


# Make Landing Page!
# https://carrd.co/build#landing
