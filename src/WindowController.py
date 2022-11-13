"""
Window Controller for the main window, holds code relevant to it's functioning features

"""

# Objective-C
import logging
import os

import Cocoa, objc, Foundation

# Shoutout modules
from sutils.langutils import Manager as langutils
from sutils.tasks import backendTasks as tasks

from sutils.config import configDir

# Python Modules

# Inherit from preferences subclass of NSWindowController
from prefController import prefWindow


class mainWindow(prefWindow):
    """
    Main Controller for main window, inherits from prefWindow class

    """
    directoryToIndex = objc.ivar()
    definitionField = objc.IBOutlet()
    flagImage = objc.IBOutlet()


    def windowDidLoad(self):
        # Create language database if not made
        # if os.path.isdir(configDir + "lang_storage/"):
        #     tasks.downloadLangDb()
        # tasks.handleConfig()
        self.definitionField.setEditable_(False) # Lock definition text field
        # self.getCurrentDefinition()


    def getCurrentDefinition(self):
        """
        Gets the current definition from the config.yml

        :return: A tuple with the current word and the current language in config
        """
        lang = tasks.getYAML()[0]['Main']
        from sutils.config import language_codes
        current_word, current_language = lang['selectedword'], language_codes[lang['selectedlang']]
        payload = langutils.read(configDir + f"lang_storage/{current_language}/{current_word}.json")

        return payload


    def loadDefinition(self, word=None, language=None):
        """
        Indexes word database and loads word into the UI

        :param word: Word
        :param language:
        :return:
        """
        from src.sutils.config import language_codes
        import random
        lang = language_codes[language]
        path = configDir + f"lang_storage/"

        # Get random index of a word from the languages database
        index = random.randrange(1, len(os.listdir(path + lang)))
        file = os.listdir(path + lang)[index]
        word = os.path.splitext(file)[0]

        payload = langutils.read(configDir + f"lang_storage/{lang}/{file}.json")
        content = payload[word]

        html = f"""<p><b>{word}</b> - {language}</p>
        <p><i>Phonetics</i> - {content['partOfSpeech']}</p>
        <p><i>{content['parsedExamples']['example']}</i></p>
        <p>Definition - {content['definitions']['definition']}</p>
        """

        # Make an NSData object with the html string in it
        html = Foundation.NSData.dataWithBytes_length_(html, len(html))
        # Make an instance of an Attributed String
        attrString = Foundation.NSAttributedString.alloc().init()
        # Instantiate attributed string with the NSData html string
        definition = attrString.initWithHTML_documentAttributes_(html, {})
        print(definition)

        return definition

    @objc.IBAction
    def helplink_(self, sender):
        print('KDKD')
        url = "https://github.com/leifadev/shoutout/wiki"
        NSLog(f"{url} opened!")
        link = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(link)

    @objc.IBAction
    def test_(self, sender):
        html = u"""<p><b>Word</b> - English</p>
        <p><i>Phonetics</i> - Noun</p>
        <p><i>A love this word!</i></p>
        <p>Definition - An abstraction</p>
        """
        new_html = str.encode(html) # Turn html into byte code for NSData

        # Make an NSData object with the html string in it
        html = Cocoa.NSData.alloc().initWithBytes_length_(new_html, len(new_html))
        # print(html)
        # Make an instance of an Attributed String
        attrString = Foundation.NSAttributedString.alloc()

        # Instantiate attributed string with the NSData html string
        definition = attrString.initWithHTML_documentAttributes_(html, None)

        self.definitionField.setAttributedStringValue_(definition)

    @objc.IBAction
    def changeDefinition_(self, sender):
        # current_def = self.definitionField.stringValue()
        lang = tasks.getYAML()
        for image in os.listdir("resources/images"):
            if lang['selectedlang'] in image:
                print(image)
                self.flagImage.setImage_(image)

        definition = self.loadDefinition(language=lang['selectedlang'])
        self.definitionField.setAttributedStringValue_(definition)
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

    scaleYView = objc.IBOutlet()
    textScaleYView = objc.IBOutlet()

    _rotation = objc.ivar.float()
    _scaleX = objc.ivar.float()
    _scaleY = objc.ivar.float()
    _translateX = objc.ivar.float()
    _translateY = objc.ivar.float()
    _preserveAspectRatio = objc.ivar.bool()

    openImageIOSupportedTypes = objc.ivar()

    def cycleLanguage(self):#, forward: bool, force_lang=""):
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

        tasks.updateConfig('selectedlang', next_selection)

    def cycleUI(self):
        """
        Works with cycle() and rotates the selected languages, but does the UI animation
        part for the flags

        :return:
        """
        from sutils import CGImageUtils
        self.openImageIOSupportedTypes = None

        lang = tasks.getYAML()
        for image in os.listdir("resources/images"):
            if lang['selectedlang'] in image:
                print(image)
                self.flagImage.setImage_(image)

        # Ask CFBundle for the location of our demo image
        url = Cocoa.CFBundleCopyResourceURL(
            Cocoa.CFBundleGetMainBundle(), "demo", "png", None
        )
        if url is not None:
            # And if available, load it
            self.flagImage.setImage_(CGImageUtils.IICreateImage(url))
        else:
            logging.warning("")

    @objc.IBAction
    def testMoveImage_(self, sender):
        image = NSImage.imageNamed_("resources/images/english_us-flag.png")
        # self.flagImage.setImage_(image)
        print(image)