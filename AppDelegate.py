# App Delegate
# Manages events and stuff that happens to the windows

# Objective-C
import Cocoa, objc
from WindowController import mainWindow
from AppKit import *


class AppDelegate(Cocoa.NSObject):
    """
    App delegate for Shoutout!
    """

    def __init__(self):
        self.app = Cocoa.NSApplication.sharedApplication()
        # Initiate the controller with a XIB
        viewController = mainWindow.alloc().initWithWindowNibName_("shoutout_main")
        viewController.showWindow_(viewController)

        # Bring app to top
        NSApp.activateIgnoringOtherApps_(True)

    def applicationShouldHandleReopen_hasVisibleWindows_(self, theApplication, flag):
        print("werty")

    def applicationDidFinishLaunching(self, aNotification):
        print("Finished loading!")
