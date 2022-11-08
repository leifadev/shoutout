# Main Modules
import os

# Objective-C
import Cocoa, objc
from AppKit import NSApp

# Shoutout modules
from sutils.tasks import backendTasks as tasks


class prefWindow(Cocoa.NSWindowController):
    """
    Window controller of preferences window
    (Inherits from NSWindowController)

    """

    # def __init__(self):
    #     self.complexitySlider = ""
    #     self.notificationDate = ""
    #     self.notificationDay = ""

    settingsStepper = objc.IBOutlet()
    light_button = objc.IBOutlet()
    dark_button = objc.IBOutlet()
    date1 = objc.IBOutlet()
    date2 = objc.IBOutlet()
    value = objc.ivar()
    complexity_bar = objc.IBOutlet()
    complexity_slider = objc.IBOutlet()


    def windowDidLoad(self):
        Cocoa.NSWindowController.windowDidLoad(self)
        self.count = 0

    @objc.IBAction
    def getSliderTick_(self, sender):
        print("ddd")
        x = self.complexity_slider.tickMarkValueAtIndex_(0)
        print(x)
        # self.complexity_bar.setEditable_(True)
        # self.complexity_bar.setDoubleValue_(2)

    @objc.IBAction
    def openlink_(self, sender):
        url = "https://github.com/leifadev/shoutout/wiki"
        print(f"{url} launched")
        x = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(x)

    @objc.IBAction
    def increment_(self, sender):
         self.count += 1
         self.updateDisplay()

    @objc.IBAction
    def decrement_(self, sender):
        self.count -= 1
        self.updateDisplay()


    def updateDisplay(self):
        self.settingsStepper.setStringValue_(self.count)


# Starting window!

if __name__ == "__main__":

    # Initiate the controller with a XIB
    viewController = prefWindow.alloc().initWithWindowNibName_("shoutout_main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)
