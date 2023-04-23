"""
Simple library that provides methods to create, open, modify, and close files using NSFileCoordinator

Why do we need this?
Take advantage of Apple's NSFileCoordinator class which takes care of protecting files, aliases, and
cross-program interference for us!
"""
import objc
# Objective-C
from Cocoa import NSURL, NSLog
from AppKit import (
    NSWorkspace,
    NSDocumentController,
    NSDocument,
    NSFileCoordinator,
)
from Foundation import NSError
from objc import python_method, super

# Python
import ruamel, json
import os, sys
from typing import Union, Optional


class shoutoutdocument(NSDocument):
    """
    Shoutout!'s subclass of NSDocument that supports macOS system file
    operations with its python code

    Uses NSFileCoordinator methods an overrides NSDocument methods to
    properly function and cooperate smoothly with macOS.

    """

    def init(self):
        self = super().init()
        if self is None:
            return None
        self.data = None

        return self

    @staticmethod
    def createPathPercentEscapes(string: str, isdirectory=False):
        """
        This function allows you to create a NSURL path object
        from a string encoded with percent escapes.

        This will make your URL work if your string has
        spaces and will ignore URL percent encoding (e.g. adds %20)

        Uses stringByAddingPercentEscapesUsingEncoding: type method

        :param string: A string of a path with or without spaces
        :param isdirectory: True or False is your path a directory, does it end with a /?
        :return: Returns NSURL path
        """
        from Foundation import NSUTF8StringEncoding
        from Cocoa import NSString
        path_string = NSString.stringWithString_(string)

        # Use fileURLWithPath: if the given path is a directory
        if isdirectory:
            # Check if path is a valid directory path
            if str(path_string).endswith("/"):
                url_path = NSURL.fileURLWithPath_(
                    path_string.stringByAddingPercentEscapesUsingEncoding_(
                        NSUTF8StringEncoding)
                )
            else:
                raise Exception("For a directory supply a string that ends with a forward slash"
                                " for a correct parse") from shoutoutdocument
        else:
            url_path = NSURL.URLWithString_(
                path_string.stringByAddingPercentEscapesUsingEncoding_(
                    NSUTF8StringEncoding)
            )
        return url_path

    @python_method
    def setData(self, data):
        """
        Sets the data class attribute for specified data

        Set this to whatever class type you want, this
        will be used by other functions

        """
        self.data = data
        NSLog(f'Setting your data {type(data)} in the class to be used')

    def readFromData_ofType_error_(self, data, typeName: str, outError):
        """
        Overridden Apple NSDocument method in sutils/sfiles.py

        Sets the contents of this document by reading from data of a specified type.

        """
        readSuccess = False
        if not data and outError:
            # Throw NSFileReadUnknownError if nothing in data parameter (NSData)
            outError, _ = NSError.errorWithDomain_code_userInfo_("NSCocoaErrorDomain", 256, None)
        # Read success if content present
        if data:
            readSuccess = True
        return readSuccess

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

        # Set success variable to true by default unless changed to false if error happens
        success = True

        # Get data specified by the data class attribute
        # Warn if no data has been set
        data = self.data
        if not self.data:
            NSLog("No has been data set! Please use shoutoutdocument.setData method to set the content to write.")

        # Introduce and use NSFileCoordinator
        coordinator = NSFileCoordinator.alloc().initWithFilePresenter_(None)

        # Block that writes the data to the file
        def _writeAccessor(newURL):
            # I'm so cool cus im using nonlocal lmao this is such an obscure statement
            # that like not everyone knows about really at first, so they like have to
            # google it, and then they know so yeah that's why it cool lol basically it makes
            # the variable here accessible out of the scope of this function, so then I can reference
            # its default value which is True so then later I can set it to false if there's
            # an error so yeah lol in your face l0s3r
            nonlocal success
            NSLog(f'Write accessor is running...')

            # Have a python string class version of NSURL objc object for open()
            pythonStringOfNSURL = str(newURL.path())

            try:
                # Write the data using python open() builtin or yaml and json modules
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
                NSLog(str(writeError))

        # Write data to the file using the block (accessor) above
        coordinator.coordinateWritingItemAtURL_options_error_byAccessor_(
            absoluteURL, NSFileCoordinatorWritingForReplacing, outError, _writeAccessor
        )

        return success

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
        :return: Returns tuple with success boolean and the data read
        """

        # Set success variable to true by default unless changed to false if error happens
        success = True
        data = None

        # Introduce and use NSFileCoordinator
        coordinator = NSFileCoordinator.alloc().initWithFilePresenter_(None)

        # Block that writes the data to the file
        def _readerAccessor(newURL):
            nonlocal success
            nonlocal data
            NSLog(f'Read accessor is running...')

            # Have a python string class version of NSURL objc object for open()
            pythonStringOfNSURL = str(newURL.path())

            try:
                # Write the data using python open() builtin or yaml and json modules
                with open(pythonStringOfNSURL, 'r') as file:
                    if typeName == "json":
                        data = json.load(file)
                        NSLog(f"Wrote to a JSON file with type 'json' specified")

                    elif typeName == "yml":
                        data = ruamel.yaml.load(yml, Loader=ruamel.yaml.SafeLoader, preserve_quotes=True)
                        NSLog(f"Wrote to a YML file with type 'yml' specified")
                    else:
                        # Includes of course txt files
                        data = file.read()
                        NSLog(f"Wrote to a file raw as plain text no parser or module support")

            except Exception as writeError:
                success = False
                NSLog(writeError)

        # Write data to the file using the block (accessor) above
        coordinator.coordinateReadingItemAtURL_options_error_byAccessor_(
            absoluteURL, NSFileCoordinatorWritingForReplacing, outError, _readerAccessor
        )

        return success, data


url = NSURL.fileURLWithPath_("/Users/leif/Desktop/lol.txt")
l = shoutoutdocument.alloc().init()
l.writeToURL_ofType_error_(url, "txt", None)

"""
How to subclass NSDocument as a whole:
https://developer.apple.com/library/archive/documentation/DataManagement/Conceptual/DocBasedAppProgrammingGuideForOSX/ManagingLifecycle/ManagingLifecycle.html

NSFileCoordinatorWritingOptions
https://stackoverflow.com/questions/11792987/nsfilecoordinator-correct-usage

To do:
Use NSFileCoordinator methods in depth!

"""