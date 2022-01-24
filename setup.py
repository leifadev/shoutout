"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = ['shoutout_main.xib']
OPTIONS = {'argv_emulation': True, 'iconfile':'images/shoutout_logo.icns',
           'plist': {
               'PyRuntimeLocations': [
                '/Library/Frameworks/Python.framework/Versions/3.9/bin/python3'
               ]
           }}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)