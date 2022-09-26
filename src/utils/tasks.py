# Tasks for Shoutout! to work, utilities
import _io
import json
import logging
import os, getpass, download, requests
import subprocess

import ruamel.yaml
from pprint import pprint

# Objective-C
import Foundation

# print(Foundation.NSUserName())
# print(Foundation.NSFullUserName())
# print(Foundation.NSHomeDirectory())
# print(Foundation.NSHomeDirectoryForUser('root'))
# print(Foundation.NSTemporaryDirectory())


backendDir = f'/Users/{getpass.getuser()}/Library/Application Support/'
configDir = f'/Users/{getpass.getuser()}/Library/Application Support/shoutout/'
ymlDir = configDir + "config.yml"
scheduleDir = configDir + "scheduleconfig.json"
resourcesURL = \
    "https://raw.githubusercontent.com/leifadev/shoutout/main/resources/"  # Link to current config


class backendTasks:
    """
    Contains all automated backend tasks that the program needs for backend functionality

    """

    @staticmethod
    def regenConfig(config):
        if config == "config":
            newConfig = requests.get(resourcesURL + "config.yml").text
            dir = ymlDir
        elif config == "scheduleconfig":
            newConfig = requests.get(resourcesURL + "scheduleconfig.json").text
            dir = scheduleDir
        else:
            logging.error("Supply config or schedule config when using regenConfig()")
            return
        with open(dir, "r+") as file:
            file.truncate(0)
            file.write(newConfig)

    @classmethod
    def configFolder(cls):
        """
        Create the config folder and it's sub folders
        """
        try:
            os.mkdir(configDir)  # make folder because im a god
        except FileExistsError:
            pass
        finally:
            logging.info("Config folder is completed!")

        # Make sub directories
        for i in ("images", "resources"):
            try:
                os.mkdir(configDir + i)
            except FileExistsError:
                pass
            finally:
                logging.info("Config sub-folders created!")

    @classmethod
    def getYAML(cls):
        """
        Safe load the config.yml or any .yml. By default, it will refer to the shoutout config folder,
        but you can specify another file directory to load in kwargs!

        :param dir: Custom other file directory to choose from besides Application Support/shoutout/config.yml
        :return: Loaded Yml content
        """
        with open(ymlDir, "r+") as yml:
            try:
                data = ruamel.yaml.load(yml, Loader=ruamel.yaml.SafeLoader, preserve_quotes=True)
            except ruamel.yaml.constructor.DuplicateKeyError:
                logging.warning(
                    "YML file loaded with getYAML has duplicate keys, illegal! Returning NoneType value instead..."
                    "\nRegenerating config...")
                cls.regenConfig("config")
                f = open(ymlDir, "r+")
                data = ruamel.yaml.load(f, Loader=ruamel.yaml.SafeLoader, preserve_quotes=True)
                f.close()
                return data

            except ruamel.yaml.scanner.ScannerError:
                logging.warning(
                    "YML file loaded with getYAML is invalid, could not scan! Returning NoneType value instead..."
                    "\nRegenerating config...")

                cls.regenConfig("config")
                f = open(ymlDir, "r+")
                data = ruamel.yaml.load(f, Loader=ruamel.yaml.SafeLoader, preserve_quotes=True)
                f.close()
                return data

        return data

    @classmethod
    def handleOtherConfig(cls):
        """
        Handles extra configuration files besides the main config.yml
        This includes generating, updating, and restoring data

        :return:
        """

        import urllib.error
        if not os.path.isfile(configDir + "scheduleconfig.json"):
            try:
                download.download(resourcesURL + "scheduleconfig.json", configDir)
                print("Generating new schedule config... (scheduleconfig.json)")
            except urllib.error.URLError:
                logging.warning("Could not connect to internet to download scheduleconfig.json!")
        else:
            pass

        # Download Launch Daemon plist
        if not os.path.isfile(configDir + 'com.shoutout.Shoutout.plist'):
            try:
                download.download(
                    f'https://raw.githubusercontent.com/leifadev/shoutout/main/resources/com.leifadev.Shoutout.plist',
                    configDir + "resources")
            except urllib.error.URLError:
                logging.warning("Could not connect to internet to download com.shoutout.Shoutout.plist!")

        ## Update scheduleconfig.json ##
        with open(f"{configDir}scheduleconfig.json", "r") as config:
            try:
                config = json.load(config)
            except json.decoder.JSONDecodeError as c:
                logging.error(f"Error accessing your schedule config (scheduleconfig.json)!\n"
                              f"Please fix your configuration file or delete it to generate a new one, here's the traceback\n{c}")

            hours_active = config['times']

            # Load the newest online config and compare it to the exisiting one
            # to update any changes
            newestConfig = requests.get(resourcesURL + "scheduleconfig.json").text
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
                with open(f"{configDir}scheduleconfig.json", "r+") as config:
                    data = json.load(config)
                    config.seek(0)
                    struct = {
                        'days': data['days'],
                        'times': new_data
                    }
                    pprint(struct)
                    json.dump(struct, config, indent=4, ensure_ascii=True)

    @classmethod
    def handleConfig(cls):
        """
        Runs tasks such as detecting if the config is corrupted, empty, or if
        it is out of date to a newer config of shoutout, and preserves the old options when it
        restores it

        :return: None
        """
        # Check if config file is present or is very low size
        if not os.path.isfile(ymlDir) or os.path.getsize(ymlDir) <= 20:
            logging.info("Creating the settings.yml")

            # Go to config folder
            os.chdir(configDir)
            cls.regenConfig("config")

        else:  # If config is present check if is outdated/broken
            logging.info("Opening current config.YML")

            current_raw_data = cls.getYAML()

            # Change to config directory
            os.chdir(configDir)

            # Fetch new config form github servers (newest resources/config.yml commit)
            logging.info("\nRequesting online copy of config.yml from github repo")
            newestConfig = requests.get(resourcesURL + "config.yml").text

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
                logging.warning("Config outdated! Updating config.yml to the new version "
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
                print(os.getcwd())
                # Dump new updated data/dictionaries to yml
                with open(ymlDir, "r+") as wyml:
                    # Add header comment
                    # Gets first top two lines of YML for preserving comment
                    download.download(resourcesURL + "config.yml", "temp_config.yml")
                    with open("temp_config.yml", "r") as temp:
                        lines = temp.readlines()
                        for i in lines[0:2]:
                            wyml.write(i)
                    os.remove("temp_config.yml")
                    yaml = ruamel.yaml.YAML()  # defaults to round-trip if no parameters given
                    yaml.dump(data, wyml)

    @classmethod
    def updateSchedule(cls, category, option, value):
        """
        Update the scheduleconfig.json file, configuration for notification scheduling.

        Example use: updateSchedule('hours', 'alert1', '14')
                     updateSchedule('days', 'tuesday', 'true')

        :param category: Supply with either 'times' or 'days'
        :param option: key to modify within the two categories
        :param value: value of the key
        :return:
        """
        with open(scheduleDir, "r+") as config:
            try:
                data = json.load(config)
            except json.decoder.JSONDecodeError:
                logging.warning(f"Received no data, regenerating the scheduleconfig.json")
                cls.regenConfig("scheduleconfig")
                data = json.load(config)

            try:
                data[category][option] = value
            except KeyError:
                logging.warning("Category or key specified does not exist!")

            config.truncate(0)
            json.dump(data, config)


    @classmethod
    def updateConfig(cls, option: str, value, configdir=configDir):

        data = cls.getYAML()

        try:
            data[0]['Main'][option] = value
        except TypeError as r:
            logging.warning(f"Received no data, regenerating the config.yml")
            cls.regenConfig("config")

        wyml = open(configDir + "config.yml", "r+")
        wyml.truncate(0)
        yaml = ruamel.yaml.YAML()
        yaml.dump(data, wyml)
        wyml.close()

    @classmethod
    def downloadLangDb(cls):

        # Get all language folders/zips available in github repository database
        database_contents = subprocess.run(
            'curl -H "Accept: application/vnd.github+json" -H "Authorization: Bearer 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" https://api.github.com/repos/leifadev/shoutout/contents/resources/lang_storage',
            capture_output=True
        )
        database_contents = json.loads(str(database_contents))
        for i in database_contents:
            if i['name'].endswith('.tar.gz'):
                download.download(f"https://github.com/leifadev/shoutout/blob/main/resources/lang_storage/{i['name']}",
                                  configDir + "resources")


# Set umask perms for dealing with files
umask = os.umask(0o013)  # Allowed Permissions rwxrw-r--
os.umask(umask)

backendTasks.updateSchedule("hours", "alert3", False)