"""
Setup.py is the file that is ran to build the app and that holds
the universal variables for the whole project as well

Usage:
    python3 setup.py py2app
"""

from setuptools import setup

langs = [
    "english",  # English (US)
    "spanish",  # Spanish
    "hindi",  # Hindi
    "german",  # German
    "french",  # French
    "japanese",  # Japanese
    "russian",  # Russian
    "italian",  # Italian
    "korean",  # Korean
    "arabic",  # Arabic
    "polish",  # Polish
    "chinese",  # Chinese
    "dutch",  # Dutch
    "portuguese",  # Portuguese
    "czech"  # Czech
]

APP = ['main.py']
DATA_FILES = ['shoutout_main.xib', 'AppDelegate.py',
              'WindowController.py', 'daemon',
              'notifications.py',
              'resources/images/']

OPTIONS = {'iconfile': 'resources/images/shoutout_logo.icns',
           'plist': {
               'PyRuntimeLocations': [
                   '/Library/Frameworks/Python.framework/Versions/3.9/bin/python3'
               ],
               'CBBundleDisplayName': 'Shoutout!',
               'CFBundleName': 'Shoutout!',
               'CFBundleVersion': 'alpha~0.0.1',
               'CFBundleDevelopmentRegion': 'en-US',
               'CFBundleIdentifier': 'com.leifadev.shoutout',
               'CFBundleSpokenName': 'Shoutout exclamation mark'
                }
           }

if __name__ == "__main__":
    setup(
        app=APP,
        data_files=DATA_FILES,
        options={'py2app': OPTIONS},
        setup_requires=['py2app']
    )

"""
Version Number Protocol (from Apple Documentation)

The first number represents the most recent major release, max four digits.
The second number represents the most recent significant revision, max two digits.
The third number represents the most recent minor bug fix, max two digits.

Docs
https://py2app.readthedocs.io/en/latest/tweaking.html
https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html#//apple_ref/doc/uid/TP40009254-SW1

"""