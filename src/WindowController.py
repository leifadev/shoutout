"""
Window Controller for the main window, holds code relevant to it's functioning features

"""

# Objective-C
import logging

import Cocoa, objc

# Shoutout modules
from sutils import CGImageUtils
from sutils.langutils import Manager as langutils
from sutils.tasks import backendTasks as tasks

# Python Modules
import getpass

# Inherit from preferences subclass of NSWindowController
from prefController import prefWindow


class mainWindow(prefWindow):
    """
    Main Controller for main window, inherits from prefWindow class

    """
    directoryToIndex = objc.ivar()
    definitionField = objc.IBOutlet()
    definition = """
    """

    def windowDidLoad(self):
        self.definitionField.setEditable_(False) # Lock definition text field


    @objc.IBAction
    def helplink_(self, sender):
        url = "https://github.com/leifadev/shoutout/wiki"
        NSLog(f"{url} opened!")
        link = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(link)

    @objc.IBAction
    def changeDefinition_(self, sender):
        # current_def = self.definitionField.stringValue()
        lang = tasks.getYAML()
        print(lang)

        # self.definitionField.setStringValue_(lang)
        # print("Set string, and the text field is now locked...")


    @objc.IBAction
    def chooseFile_(self, sender):
        # we are setting up an NSOpenPanel to select only a directory and then
        # we will use that directory to choose where to place our index file and
        # which files we'll read in to make searchable.
        op = Cocoa.NSOpenPanel.openPanel()
        op.setCanChooseDirectories_(True)
        op.setCanChooseFiles_(False)
        op.setResolvesAliases_(True)
        op.setAllowsMultipleSelection_(False)
        result = op.runModalForDirectory_file_types_(None, None, None)
        if result == Cocoa.NSOKButton:
            self.directoryToIndex = op.filename()
            self.uploadLanguage(self.directoryToIndex)
            # self.directoryTextField.setStringValue_(self.directoryToIndex)

    # def uploadLanguage(self, path):
    #     # Custom language db to upload, make folder for it automatically
    #     # Scan through it's contents and only accept it being all JSON files, otherwse reject
    #     pass


class UIElements:
    imageView = objc.IBOutlet()
    scaleYView = objc.IBOutlet()
    textScaleYView = objc.IBOutlet()

    _rotation = objc.ivar.float()
    _scaleX = objc.ivar.float()
    _scaleY = objc.ivar.float()
    _translateX = objc.ivar.float()
    _translateY = objc.ivar.float()
    _preserveAspectRatio = objc.ivar.bool()

    openImageIOSupportedTypes = objc.ivar()

    def __init__(self):
        self.backendDir = f'/Users/{getpass.getuser()}/Library/Application Support/'
        self.configDir = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.resourcesURL = \
            "https://raw.githubusercontent.com/leifadev/shoutout/main/resources/"  # Link to current config

    def cycleLanguage(self, forward: bool, force_lang=""):
        """
        Cycle a language forwards or backwards, forward is false then it goes back a
        language (to the left instead of right)

        :param forward: Supply true to move forward a language (right), or false for backwards (left)
        :param force_lang: force cycling to a specific language
        :return:
        """

        # Grab and update value from config #

        from setup import langs
        # Fetch config, update it's new cycled language
        selected = tasks.getYAML()
        selected = selected[0]['Main']['selectedlang']

        current_key = langs.index(selected)
        if forward:
            current_key += 1
        else:
            current_key -= 1

        next_selection = langs[current_key]
        # NSLog(current_key, next_selection)

        tasks.updateConfig('selectedlang', next_selection)

    def cycleUI(self, language):
        """
        Works with cycle() and rotates the selected languages, but does the UI animation
        part for the flags

        :return:
        """
        from utils import CGImageUtils
        import time # Delay animation
        self.openImageIOSupportedTypes = None

        # Ask CFBundle for the location of our demo image
        url = Cocoa.CFBundleCopyResourceURL(
            Cocoa.CFBundleGetMainBundle(), "demo", "png", None
        )
        if url is not None:
            # And if available, load it
            self.imageView.setImage_(CGImageUtils.IICreateImage(url))
        else:
            logging.warning("")
