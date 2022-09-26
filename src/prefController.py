# Main Modules
import os

# Objective-C
import Cocoa, objc
from AppKit import NSApp

# Shoutout modules
from utils.tasks import backendTasks as tasks

class prefWindow(Cocoa.NSWindowController):
    """
    Window controller of preferences window
    (Inherits from NSWindowController)
    """

    def __init__(self):
        self.light_button = objc.IBOutlet()
        self.dark_button = objc.IBOutlet()
        self.settingsStepper = objc.IBOutlet()

    # @objc.IBAction
    # def stepUpNoti(self):
    #     tasks.updateSchedule()


    @objc.IBAction
    def openlink_(self, sender):
        url = ("https://github.com/leifadev/shoutout/")
        print(f"{url} launched")
        x = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(x)

    # Increment numbers display stuff (from dawes.wordpress.com)
    @objc.IBAction
    def increment_(self, sender):
        # self.count += 1
        print("derf")
        # self.updateDisplay()

    @objc.IBAction
    def decrement_(self, sender):
        self.count -= 1
        print(self.count)
        self.updateDisplay()

    # def switchTheme_(self):

    def updateDisplay(self):
        # DO NSStepper
        self.settingsStepper.setStringValue_(self.count)


# Starting window!

if __name__ == "__main__":

    # Initiate the controller with a XIB
    viewController = prefWindow.alloc().initWithWindowNibName_("shoutout_main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)
