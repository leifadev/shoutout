"""
App Delegate, manages events about the app and the window controllers and so on...

"""

# Objective-C
import Cocoa, objc
from AppKit import *

# Shoutout modules
from WindowController import mainWindow

# Python modules
# ---

class AppDelegate(Cocoa.NSObject):
    """
    App delegate for Shoutout!
    """

    app = Cocoa.NSApplication.sharedApplication()

    # Initiate the controller with a XIB
    viewController = mainWindow.alloc().initWithWindowNibName_("shoutout_main")
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)

    def applicationShouldHandleReopen_hasVisibleWindows_(self, theApplication, flag):
        return True

    def applicationDidFinishLaunching_(self, aNotification):
        print("Finished loading!")


delegate = AppDelegate.alloc().init().retain()
NSApplication.sharedApplication().setDelegate_(delegate)
