"""
Window Controller for the main window

"""

# Objective-C
import Cocoa
import objc
import Foundation

# Shoutout modules
from sutils.langutils import Manager as langutils
from sutils.sfiles import shoutoutdocument
from sutils.tasks import backendTasks as tasks

from sutils.config import configDir

# Python Modules
import copy
import itertools
import logging
import os
import shutil

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
        tasks.handleConfig()
        # tasks.handleScheduleConfig()
        self.definitionField.setEditable_(False)  # Lock definition text field
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

    @objc.python_method
    def loadDefinitionUI(self, word: str, phonetic: str, definition: str, partOfSpeech: str):
        """
        Loads the definition of the provided word and allows
        custom indexing of all the payloads other keys such as
        phonetic or part of speech

        :param word: definition word
        :param phonetic: phonetics of the word
        :param definition: the definition of the word
        :param partOfSpeech: the words part of speech
        :return:
        """

        # Fetch the image flag of selected language
        lang = tasks.getYAML()
        for image in os.listdir("resources/images"):
            if lang['selectedlang'] in image:
                print(image)
                self.flagImage.setImage_(image)

        # Import attributed text class methods, along with NSFont and NSColor of course
        from Foundation import NSMakeRange, NSMutableParagraphStyle, NSMutableAttributedString
        from AppKit import NSFont, NSColor

        # Create an attributed string with some custom attributes
        attributedWord = NSMutableAttributedString.alloc().initWithString_(
            f"{word}\n")
        attributedPhonetics = NSMutableAttributedString.alloc().initWithString_(
            f"{phonetic}\n")
        attributedDefinition = NSMutableAttributedString.alloc().initWithString_(
            f"{definition}\n")
        attributedPartOfSpeech = NSMutableAttributedString.alloc().initWithString_(
            f"{partOfSpeech}")

        # Enumeration cases for the bold or italic font masks
        # AppKit > NSFontManager
        NSBoldFontMask = 0x00000002
        NSItalicFontMask = 0x00000001

        paragraphStyle0 = NSMutableParagraphStyle.alloc().init()
        paragraphStyle0.setAlignment_(2)  # 2 is center

        # NSDictionary of attributes that centers text it's applied too (that's all this is important for now)
        attributesUniversal = {
            "NSParagraphStyle": paragraphStyle0,  # Change text alignment
            "NSFont": NSFont.systemFontOfSize_(12)  # Change the font if ya want :D
        }
        attributesBigFont = {  # Big font
            "NSParagraphStyle": paragraphStyle0,
            "NSFont": NSFont.systemFontOfSize_(16)
        }

        # Bold and size the first line of text (The word)
        attributedWord.applyFontTraits_range_(NSBoldFontMask, NSMakeRange(0, len(word)))

        # Italicize the next line (phonetics)
        attributedPhonetics.applyFontTraits_range_(NSItalicFontMask, NSMakeRange(0, len(phonetic)))

        # Add all lines together
        attributedWord.appendAttributedString_(attributedPhonetics)
        attributedWord.appendAttributedString_(attributedDefinition)
        attributedWord.appendAttributedString_(attributedPartOfSpeech)

        # Apply universal attributes like centering and font choice
        attributedWord.setAttributes_range_(attributesUniversal, NSMakeRange(0, len(attributedWord)))
        # Make word font bigger to 16
        # NOTE: The addAttribute:value:range: method would not work to separately change the word
        # to size 16 up above
        attributedWord.setAttributes_range_(attributesBigFont, NSMakeRange(0, len(word)))

        # Set attributed string to the text field in main app window for definition
        self.definitionField.setAttributedStringValue_(attributedWord)

    @objc.IBAction
    def helplink_(self, sender):
        url = "https://github.com/leifadev/shoutout/wiki"
        NSLog(f"{url} opened!")
        link = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(link)

    @objc.python_method
    def getDefinitionData(self, language: str, word: str):
        """
        Fetches the definition data of a given word and its source langauge

        For the language parameter you can supply either the alpha-2 country code
        or the full name of the langauge (e.g. "chinese", "zh")

        :param language: code of source langauge of the given word
        :param word: word you want definition data from
        """
        from sutils.config import codes_to_languages, language_codes
        import random
        path = configDir + f"lang_storage/"

        # Isn't country code? Convert it if so
        if not len(language) == 2:
            logging.info("Your langauge you specified is a country code not a name, converting it!")
            lang = language_codes[language]
            path = configDir + f"lang_storage/"
        else:
            lang = language

        # Get a random (index of a) word from the selected languages database
        index = random.randrange(1, len(os.listdir(path + lang)))
        file = os.listdir(path + lang)[index]
        # file_name_word = os.path.splitext(file)[0] # Gets word of name by the file name not JSON payload

        payload = langutils.read(configDir + f"lang_storage/{lang}/{word}.json")

        # Load NSAttributedText definition with given language
        self.loadDefinitionUI(word=payload['word'],
                              phonetic=payload['phonetic'],
                              definition=payload['definition'],
                              partOfSpeech=payload['partOfSpeech']
                              )

    @objc.IBAction
    def chooseFile_(self, sender):
        # We are setting up an NSOpenPanel to select only a directory, and then
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

    @staticmethod
    def uploadLanguage(path: str):
        # Custom language db to upload, make folder for it automatically
        # Scan through its contents and only accept it being all JSON files, otherwise reject

        # Get directory
        filename = path.split("/")[::-1]
        for i in filename:
            if i != "":
                filename = i
                break

        yml = tasks.getYAML()
        current_customs = yml['Other']['custom_languages']

        if current_customs is None:
            x = [filename]
            tasks.generateExampleLang()
        else:
            x = current_customs

        tasks.updateConfig(category='Other', option='custom_languages', value=x)
        if logging.getLogger().level <= 10:
            os.system(f"cp -va '{path}' '{configDir + filename}'")
        elif logging.getLogger().level > 10:
            os.system(f"cp -a '{path}' '{configDir + filename}'")

    _rotation = objc.ivar.float()
    _scaleX = objc.ivar.float()
    _scaleY = objc.ivar.float()
    _translateX = objc.ivar.float()
    _translateY = objc.ivar.float()
    _preserveAspectRatio = objc.ivar.bool()

    openImageIOSupportedTypes = objc.ivar()

    def cycleLanguage(self):  # , forward: bool, force_lang=""):
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

        tasks.updateConfig('Main', 'selectedlang', next_selection)

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
        print("SSS")
        image = Cocoa.NSImage.imageNamed_("english_us-flag.png")
        self.flagImage.setImage_(image)

    @classmethod
    def updateDisplay(cls):
        config = backendTasks.getYAML()
        # Images
        image = Cocoa.NSImage.imageNamed_(f"{config['Main']['selected_lang']}-flag.png")
        self.flagImage.setImage_(image)

        # Text Boxes
        # WindowController.mainWindow.flagImage.set()


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
