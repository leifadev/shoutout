"""
Setup.py is the file that is run to build the app and that holds
the universal variables for the whole project as well

Usage:
    python3 setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = ['shoutout_main.xib', 'sutils/config.py', 'AppDelegate.py',
              'WindowController.py', 'sutils/langutils.py', 'sutils/tasks.py',
              'notifications.py',
              'resources/images/']

OPTIONS = {'iconfile': 'resources/images/shoutout_logo.icns',
           'arch': "arm64",
           'plist': {
               'PyRuntimeLocations': [
                   '/Library/Frameworks/Python.framework/Versions/3.9/bin/python3',
                   '/Library/Frameworks/Python.framework/Versions/3.8/bin/python3',
               ],
               'NSRequiresAquaSystemAppearance': False,
               # 'LSPrefersPPC': True,  # Force application to run translated with Rosseta by default
               'CBBundleDisplayName': 'Shoutout!',
               'CFBundleName': 'Shoutout!',
               'CFBundleVersion': 'alpha~0.0.1',
               'CFBundleDevelopmentRegion': 'en-US',
               'CFBundleIdentifier': 'com.leifadev.shoutout',
               'CFBundleSpokenName': 'Shoutout exclamation mark',
               'NSHumanReadableCopyright': 'GNU General Public License v2.0'
                                           '\nCopyright © 1989, 1991 Free Software Foundation, Inc.'
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
Common or important plist keys to use
https://py2app.readthedocs.io/_/downloads/en/stable/pdf/#section.1.7
"""

"""

Compile the daemon binary with setup_daemon.py

Version Number Protocol (from Apple Documentation)

The first number represents the most recent major release, max four digits.
The second number represents the most recent significant revision, max two digits.
The third number represents the most recent minor bug fix, max two digits.

Docs
https://py2app.readthedocs.io/en/latest/tweaking.html
https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html#//apple_ref/doc/uid/TP40009254-SW1

"""
