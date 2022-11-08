"""
App Delegate, manages events about the app and the window controllers and so on...

"""

# Objective-C
import Cocoa, objc
from AppKit import *
from Cocoa import NSLog

# Shoutout modules
from WindowController import mainWindow
from sutils.tasks import backendTasks as tasks
# from utils.langutils import Manager as langutils

# Python modules
# ---

class AppDelegate(Cocoa.NSObject):
    """
    App delegate for Shoutout!
    
    """

    app = Cocoa.NSApplication.sharedApplication()

    viewController = mainWindow.alloc().initWithWindowNibName_("shoutout_main")
    viewController.showWindow_(viewController)
    # bundle = Foundation.NSBundle.mainBundle().loadNibNamed_owner_topLevelObjects_("shoutout_main", None, None)
    # from pprint import pprint
    # pprint(bundle[1][0:20])

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)

    def applicationShouldHandleReopen_hasVisibleWindows_(self, theApplication, flag):
        print("Handling reopen...")

    def applicationDidFinishLaunching_(self, aNotification):
        self.loadUIElements()

    def loadUIElements(self):
        """
        Loads and sets all UI Elements on startup

        :return:
        """
        yml_contents = tasks.getYAML()





# Set this class as the delegate class!
delegate = AppDelegate.alloc().init().retain()
NSApplication.sharedApplication().setDelegate_(delegate)
