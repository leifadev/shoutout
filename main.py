import platform as platform
from ruamel import yaml
import getpass, os, time, logging as log

import Cocoa, Foundation, objc
from AppKit import NSApp
from lang_manager import Manager as lmanager # provides



class mainWindow(Cocoa.NSWindowController):

    inc = objc.IBOutlet()

    def __init__(self):
        self.keys = {} # api keys
        self.OS = platform.uname()
        self.theme = "dark"
        self.lang = "english"
        self.version = "beta~v0.0.1"
        self.launchWord = False
        self.backendDir = f'/Users/{getpass.getuser()}/Library/Application Support/'
        self.settingDir = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.count = 0
        self.gitUrl = ("https://github.com/leifadev/shoutout")
        self.languages = ["english", "spanish", "russian", ] # available languages to choose from!
        self.definitionFull = {
            "word": "",
            "definition": "",
            "phoentics": "",
            "pronounceAudio": ""
        }

        self.configPayload = {
                'Options': {
                    'defaultDir': 1,
                    'errorChoice': 1,
                    'changedDefaultDir': 1,
                    'internet': False
                }
            }



    def startUpTasks(self):
        if not os.path.isfile(self.fileLoc):
            path = os.path.join(self.fileLoc)
            os.makedirs(self.settingDir, exist_ok=True)
            print("Folder generated...")
        if not os.path.isfile(self.ymldir) or os.path.getsize(self.ymldir) == 0:
            print("Creating the settings.yml,\nThis is NOT a restored version of a previously deleted one!")
            os.chdir(self.fileLoc)
            print(os.getcwd())
            f = open("settings.yml","w+")
            yaml.dump(self.payload, f, Dumper=yaml.RoundTripDumper)
            print("if statement passes")
            f.close()
        # makes a copy of the newest yml/settings structure
        os.chdir(self.fileLoc)
        cache = open(self.cachedir, "w+")
        yaml.dump(self.payload, cache, Dumper=yaml.RoundTripDumper)
        cache.close()
        print("Cache updated!")




    def windowDidLoad(self):
        Cocoa.NSWindowController.windowDidLoad(self)


    @objc.IBAction
    def helplink_(self, url):
        print("Help URL Launched!")
        self.gitUrl = ("https://github.com/leifadev/shoutout/wiki")
        x = Cocoa.NSURL.alloc().initWithString_(self.gitUrl)
        Cocoa.NSWorkspace.alloc().openURL_(x)


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



class appTasks(Foundation.NSNotification):

    def __init__(self):
        self.date = ""
        self.timezone = time.tzname[0]
        self.clockOff = False # Value determines if the clock/schedule for sending notifications is disabled


    def sendNotif(self):
        # Find out class methods who send notifications, and other related data objects


        log.info("Notification method has been called!")




# Loop it and stuff

if __name__ == "__main__":
    app = Cocoa.NSApplication.sharedApplication()

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
