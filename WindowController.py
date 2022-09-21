# Main Modules
import os

# Objective-C
import Cocoa, objc
from AppKit import NSApp

# Inherit from preferences subclass of NSWindowController
from prefController import prefWindow


class mainWindow(prefWindow):
    """
    Main Controller for main window

    (Inherits from prefWindow class, prefController.py)
    """

    # Outlets

    def __init__(self):
        self.cool = "cool"
        self.version = "beta~v0.0.1"
        word = objc.IBOutlet()
        definition = objc.IBOutlet()
        example = objc.IBOutlet()

    @objc.IBAction
    def helplink_(self, sender):
        url = ("https://github.com/leifadev/shoutout/wiki")
        print(f"{url} launched")
        link = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(link)


class UIElements:
    pass




# Starting window!

if __name__ == "__main__":

    # Initiate the controller with a XIB
    viewController = mainWindow.alloc().initWithWindowNibName_("shoutout_main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)

