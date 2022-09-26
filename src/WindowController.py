"""
Window Controller for the main window, holds code relevant to it's functioning features

"""

# Objective-C
import logging

import Cocoa, objc

# Shoutout modules
from utils.langutils import Manager as langutils
from utils.tasks import backendTasks as tasks
import utils.CGImageUtils as imageutils  # Ronald Roussen Core Graphics Utils

# Python Modules
import getpass

# Inherit from preferences subclass of NSWindowController
from prefController import prefWindow


class mainWindow(prefWindow):
    """
    Main Controller for main window, inherits from prefWindow class

    """

    def __init__(self):
        word = objc.IBOutlet()
        definition = objc.IBOutlet()

    @objc.IBAction
    def helplink_(self, sender):
        url = "https://github.com/leifadev/shoutout/wiki"
        print(f"{url} opened!")
        link = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(link)


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
        # print(current_key, next_selection)

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




ui = UIElements()
ui.cycle(True)
