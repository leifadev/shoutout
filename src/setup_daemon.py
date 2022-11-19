"""
Setup_daemon.py is the file that is ran to build the Shoutout! daemon binary

Usage:
    python3 setup.py py2app
"""

from setuptools import setup

APP = ['daemon.py']
DATA_FILES = ['notifications.py']

OPTIONS = {
           'plist': {
               'PyRuntimeLocations': [
                   '/Library/Frameworks/Python.framework/Versions/3.9/bin/python3'
               ],
               'CBBundleDisplayName': 'shoutout_daemon',
               'CFBundleName': 'shoutout_daemon',
               'CFBundleVersion': 'alpha~0.0.1',
               'CFBundleIdentifier': 'com.leifadev.shoutout.daemon',
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

Version Number Protocol (from Apple Documentation)

The first number represents the most recent major release, max four digits.
The second number represents the most recent significant revision, max two digits.
The third number represents the most recent minor bug fix, max two digits.

Docs
https://py2app.readthedocs.io/en/latest/tweaking.html
https://developer.apple.com/library/archive/documentation/General/Reference/InfoPlistKeyReference/Articles/AboutInformationPropertyListFiles.html#//apple_ref/doc/uid/TP40009254-SW1

"""