"""
Simple library that provides methods to create, open, modify, and close files using NSFileCoordinator

Why do we need this?
Take advantage of Apple's NSFileCoordinator class which takes care of protecting files, aliases, and
cross-program interference for us!
"""

# Objective-C
from Cocoa import NSURL, NSLog
from AppKit import (
    NSWorkspace,
    NSDocumentController,
    NSDocument,
    NSFileCoordinator,
)
from Foundation import NSError

# Python
import ruamel, json
import os, sys
from typing import Union, Optional

class shoutoutDocument(NSDocument):

    # Is really a class method but I don't want self or cls cause it's objc
    @staticmethod
    def createPathPercentEscapes(string: str, isdirectory=False):
        """
        This function allows you to create a NSURL path object
        from a string encoded with percent escapes.

        This will make your URL work if your string has
        spaces and will ignore URL percent encoding (e.g. adds %20)

        Uses stringByAddingPercentEscapesUsingEncoding: type method

        :param string: A string of a path with or without spaces
        :param isdirectory: True or False is your path a directory?
        :return: Returns NSURL path
        """
        from Foundation import NSUTF8StringEncoding
        from Cocoa import NSString
        path_string = NSString.stringWithString_(string)
        url = NSURL.URLWithString_(
            path_string.stringByAddingPercentEscapesUsingEncoding_(
                NSUTF8StringEncoding))
        return url

    def data(self, data):
        return data

    def readFromData_ofType_error_(self, data, typeName: str, outError):
        readSuccess = False
        if not data and outError:
            # Throw NSFileReadUnknownError if nothing in data parameter (NSData)
            outError, _ = NSError.errorWithDomain_code_userInfo_("NSCocoaErrorDomain", 256, None)
        # Read success if content present
        if data:
            readSuccess = True
        return readSuccess

    def readFromURL_ofType_error_(self, absoluteURL, typeName: str, outError):
        """
        Overridden Apple NSDocument method in sutils/sfiles.py

        Reads the contents of the document to a file or file package located by a
        URL.

        Supports python module and parsing for file types JSON and YML.

        :param absoluteURL: The location to which the document contents are written.
        :param typeName: The string that identifies the document type.
        :param outError: On return, if the document contents could not be written, a pointer
        to an error object that encapsulates the reason they could not be written.
        :return: Returns data read from file URL
        """
        absoluteURL = str(absoluteURL)

        coordinator = NSFileCoordinator.alloc().initWithFilePresenter_(None)

        # Python JSON library
        if typeName == 'json':
            NSLog(f"Type is of json, returning a python json object")
            with open(absoluteURL, "r") as f:
                data = json.load(f)
                return data

        # Using ruamel.yaml library here, could possibly use PyYAML but ruamel is better...
        elif typeName == 'yml':
            NSLog(f"Type is of yml, returning a ruamel yaml object")
            with open(absoluteURL, "r+") as yml:
                data = ruamel.yaml.load(yml, Loader=ruamel.yaml.SafeLoader, preserve_quotes=True)
                return data
        else:
            # If the file type is anything else just read the data with
            # no extra modules for certain file types.
            NSLog(f"Type is not of json or yml, returning raw text type")
            with open(absoluteURL, "r") as f:
                data = f.read()
                return data

        # Note that the outError parameter is passed as a reference to an NSError object
        # rather than as a raw NSError object. In PyObjC, NSError objects are passed as arrays,
        # so you should access the object using the syntax outError[0].
        # if outError:
        #     outError, _ = NSError.errorWithDomain_code_userInfo_("NSCocoaErrorDomain", 4, None)

    def writeToURL_ofType_error_(self, absoluteURL, typeName: str, outError):
        """
        Overridden Apple NSDocument method in sutils/sfiles.py

        Overwrites the contents of a document with the specified payload to write with.
        Again, this method does not add data but completely overwrites the file!

        Supports python module and parsing for file types JSON and YML.

        :param absoluteURL: The location to which the document contents are written.
        :param typeName: The string that identifies the document type.
        :param outError: On return, if the document contents could not be written, a pointer
        to an error object that encapsulates the reason they could not be written.
        :return: YES if the document contents could be written; otherwise, NO.
        """
        from Foundation import NSFileCoordinatorWritingForReplacing

        global success
        success = True
        data = self.data()

        coordinator = NSFileCoordinator.alloc().initWithFilePresenter_(None)

        # Block that writes the data to the file
        def _writeAccessor(newURL):
            NSLog(f'Write accessor is running...')

            # Have a python string class version of NSURL objc object for open()
            pythonStringOfNSURL = str(newURL.path())

            try:
                with open(pythonStringOfNSURL, 'w+') as file:
                    if typeName == "json":
                        json.dump(data, file)
                        NSLog(f"Wrote to a JSON file with type 'json' specified")

                    elif typeName == "yml":
                        ruamel.yaml.dump(data, file, Dumper=ruamel.yaml.RoundTripDumper)
                        NSLog(f"Wrote to a YML file with type 'yml' specified")
                    else:
                        # Includes of course txt files
                        file.write(data)
                        NSLog(f"Wrote to a file raw as plain text no parser or module support")

            except Exception as writeError:
                success = False
                print(writeError)

        # We finally write to the file with NSFileCoordinator simultaneously providing
        # us with special aid and protection from other apps interfering and so on...
        coordinator.coordinateWritingItemAtURL_options_error_byAccessor_(
            absoluteURL, NSFileCoordinatorWritingForReplacing, outError, _writeAccessor
        )

        return success

url = NSURL.fileURLWithPath_("/Users/leif/Desktop/lol.txt")
l = sFiles.alloc().init()
l.writeToURL_ofType_error_(url, "txt", None)



"""
How to subclass NSDocument as a whole:
https://developer.apple.com/library/archive/documentation/DataManagement/Conceptual/DocBasedAppProgrammingGuideForOSX/ManagingLifecycle/ManagingLifecycle.html

NSFileCoordinatorWritingOptions
https://stackoverflow.com/questions/11792987/nsfilecoordinator-correct-usage

To do:
Use NSFileCoordinator methods in depth!

"""
