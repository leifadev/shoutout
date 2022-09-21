# Tasks for Shoutout! to work
import _io
import json
import logging
import os, getpass, wget, requests
import ruamel.yaml
from pprint import pprint

# Objective-C
import Foundation


# print(Foundation.NSUserName())
# print(Foundation.NSFullUserName())
# print(Foundation.NSHomeDirectory())
# print(Foundation.NSHomeDirectoryForUser('root'))
# print(Foundation.NSTemporaryDirectory())


class backendTasks:
    """
    Contains all automated backend tasks that the program needs for backend functionality
    """

    def __init__(self):  # Set initial variables
        self.backendDir = f'/Users/{getpass.getuser()}/Library/Application Support/'
        self.configDir = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
        self.ymlDir = self.configDir + "config.yml"
        self.resourcesURL = \
            "https://raw.githubusercontent.com/leifadev/shoutout/main/resources/"  # Link to current config

    def configFolder(self):
        """
        Create the config folder
        """
        if not os.path.exists(self.configDir):
            os.mkdir(self.configDir)  # make folder because im a god
        else:
            logging.info("Config folder is completed!")


    def otherConfigFiles(self):
        # schedule config etc.
        import urllib.error
        if not os.path.isfile(self.configDir + "scheduleconfig.json"):
            try:
                wget.download(self.resourcesURL + "scheduleconfig.json", self.configDir)
                print("Generating new schedule config... (scheduleconfig.json)")
            except urllib.error.URLError:
                logging.warning("Could not connect to internet to download scheduleconfig.json!")
        else:
            pass

        ## Update scheduleconfig.json ##
        with open(f"{self.configDir}scheduleconfig.json", "r") as config:
            try:
                config = json.load(config)
            except json.decoder.JSONDecodeError as c:
                logging.error(f"Error accessing your schedule config (scheduleconfig.json)!\n"

                              f"Please fix your configuration file or delete it to generate a new one, here's the traceback\n{c}")

            hours_active = config['times']

            # Load the newest online config and compare it to the exisiting one
            # to update any changes
            newestConfig = requests.get(self.resourcesURL + "scheduleconfig.json").text
            newestConfig = json.loads(newestConfig)['times']  # Only updates times section
            if newestConfig.keys() == hours_active.keys():
                pass  # Do nothing if same
            else:
                new_data = {}
                preserve_keys = hours_active.keys() & newestConfig.keys()
                list(preserve_keys).reverse()

                # Loops through keys that exist within the new config AND the
                # old one, includes those with there existing settings with any newly
                # added settings
                for key in preserve_keys:
                    for x, y in hours_active.items():
                        if key == x:
                            new_data.update({x: y})
                    for i, e in newestConfig.items():
                        if i not in new_data.keys():
                            new_data.update({i: e})
                new_data = dict(sorted(new_data.items()))

                # Dump updated config
                with open(f"{self.configDir}scheduleconfig.json", "r+") as config:
                    data = json.load(config)
                    config.seek(0)
                    struct = {
                        'days': data['days'],
                        'times': new_data
                    }
                    pprint(struct)
                    json.dump(struct, config, indent=4, ensure_ascii=True)

    def handleConfig(self):
        """
        Runs tasks such as detecting if the config is corrupted, empty, or if
        it is out of date to a newer config of shoutout, and preserves the old options when it
        restores it

        :return: None
        """
        # Check if config file is present or is very low size
        if not os.path.isfile(self.ymlDir) or os.path.getsize(self.ymlDir) <= 20:
            logging.info("Creating the settings.yml")

            # Go to config folder
            os.chdir(self.configDir)

            # Remove invalid old config first
            try:
                os.remove("config.yml")
                logging.info("Removing old config.yml...")
            except:
                pass
            # Download new one
            wget.download(self.resourcesURL + "config.yml")

        else:  # If config is present check if is outdated/broken
            logging.info("Opening current config.YML")

            # Open file and load with yaml module
            with open(self.ymlDir, "r") as yml:
                current_raw_data = ruamel.yaml.load(yml, Loader=ruamel.yaml.SafeLoader)

                # Change to config directory
                os.chdir(self.configDir)

                # Fetch new config form github servers (newest resources/config.yml commit)
                logging.info("\nRequesting online copy of config.yml from github repo")
                newestConfig = requests.get(self.resourcesURL + "config.yml").text

                # Convert get request to yaml via safe-load
                logging.info("\nConverting github text payload to yaml dict (safeload)...")
                newdata = ruamel.yaml.safe_load(newestConfig)

                # Getting into actual options
                newdata = newdata[0]['Main']

                current_data = current_raw_data[0]['Main']

                # Check if settings is newer BY KEY!
                if newdata.keys() == current_data.keys():
                    logging.info("\nConfig up to date!")
                else:
                    # If not equal it options, updating to new ones
                    import datetime
                    logging.warning("Config outdated! Updating config.yml to the new version"
                                    f"as of {datetime.date.today()}\n"
                                    "All settings will be preserved...\n")

                    # Inherit new dictionary with old options first
                    finalData = current_data
                    # Loop through the new config options, if key already from it
                    # already is existing in the current config file ignore it and add new config ones
                    for key, value in newdata.items():
                        if key in current_data.keys():
                            pass
                        else:
                            finalData.update({key: value})

                    # Makes back structure of original file
                    data = [
                        {
                            'Main': finalData
                        }
                    ]

                    # Dump new updated data/dictionaries to yml
                    with open("config.yml", "r+") as wyml:
                        # Add header comment
                        # Gets first top two lines of YML for preserving comment
                        wget.download(self.resourcesURL + "config.yml", "temp_config.yml")
                        with open("temp_config.yml", "r") as temp:
                            lines = temp.readlines()
                            for i in lines[0:2]:
                                wyml.write(i)
                        os.remove("temp_config.yml")
                        yaml = ruamel.yaml.YAML()  # defaults to round-trip if no parameters given
                        yaml.dump(payload, wyml)


    def updateConfig(self, option: str, value):
        if not os.path.isfile(self.configDir + "config.yml"):
            print(self.configDir + "config.yml")
            wget.download(self.resourcesURL + "config.yml", self.configDir)
            logging.warning("\nDownloading new config.yml file, none found...")
        else:
            pass

        with open(self.configDir + "config.yml", "r+") as wyml:
            from ruamel import yaml

            data = yaml.round_trip_load(wyml, preserve_quotes=True)
            yaml.safe_load(wyml)

            try:
                data[0]['Main'][option] = value
            except TypeError as r:
                logging.warning(f"Received no data, regenerating the config.yml")
                os.remove(self.configDir + "config.yml")
                wget.download(self.resourcesURL + "config.yml", self.configDir + "config.yml")

            # with open(self.configDir + "config.yml", "w+") as clear:
            #     clear.write("# lol \n")

            # yaml = ruamel.yaml.YAML()
            # yaml.dump(data, wyml)


# Set umask perms for dealing with files
umask = os.umask(0o013)  # Allowed Permissions rwxrw-r--
os.umask(umask)

tasks = backendTasks()
tasks.updateConfig("darkMode", False)
