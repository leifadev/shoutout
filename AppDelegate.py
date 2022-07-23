

# Objective-C
import Cocoa, objc
import AppKit

# App Delegate
# Manages events and stuff that happens to the windows

class AppDelegate(Cocoa.NSObject):
    """
    App delegate for Shoutout!
    """

    myWindowController = objc.ivar()

    def applicationDidFinishLaunching_(self, notification):
        print("Finished loading!")
