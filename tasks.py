import os, sys, getpass, requests
from ruamel import yaml

# Objective-C
import Foundation

print(Foundation.NSUserName())
print(Foundation.NSFullUserName())
print(Foundation.NSHomeDirectory())
print(Foundation.NSHomeDirectoryForUser('root'))
print(Foundation.NSTemporaryDirectory())


class backendTasks():
    """
    Contains all backend tasks that the program needs for backend functionality
    """

    def __init__(self): # Set inital variables
        self.backendDir = f'/Users/{getpass.getuser()}/Library/Application Support/'
        self.settingDir = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.configPayload = {
            'Options': {
                'defaultDir': 1,
                'errorChoice': 1,
                'changedDefaultDir': 1,
                'internet': False
            }
        }
        self.configURL = "https://github.com/leifadev/shoutout/" # Link to current config

    def configFolder(self):
        """
        Create the config folder
        """
        if not os.path.exists(self.settingDir):
            os.mkdir(self.settingDir) # make folder because im a god
        else:
            print("Config folder is completed!")

    def startUpTasks(self):
        """
        Core Startup Tasks in one function
        """

        if not os.path.isfile(self.ymldir) or os.path.getsize(self.ymldir) == 0:
            print("Creating the settings.yml")

            # Go to config folder
            os.chdir(self.backendDir)
            print(os.getcwd()) # Print cwd
            
            f = open("settings.yml", "w+")
            configYML = requests.get(self.configURL)
            yaml.dump(self.payload, f, Dumper=yaml.RoundTripDumper)
            f.close()
            
        # Makes a copy of the newest yml/settings structure
        os.chdir(self.backendDir)
        cache = open(self.cachedir, "w+")
        yaml.dump(self.payload, cache, Dumper=yaml.RoundTripDumper)
        cache.close()
        print("Cache updated!")
