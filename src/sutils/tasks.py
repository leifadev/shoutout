"""
In charge of Shoutout!s tasks to run in the background, essential for the apps
backend functioning

"""

# Python Modules
import ipaddress
import json
import logging
import os, download, requests
import shutil
import subprocess
import tarfile

import multidict
import ruamel.yaml
from pprint import pprint

# Objective-C
import Foundation

homeDir = Foundation.NSHomeDirectory()
tempDir = Foundation.NSTemporaryDirectory()
backendDir = f'/Users/{Foundation.NSUserName()}/Library/Application Support/'
configDir = f'/Users/{Foundation.NSUserName()}/Library/Application Support/shoutout/'
ymlDir = configDir + "config.yml"
scheduleDir = configDir + "scheduleconfig.json"
resourcesURL = \
    "https://raw.githubusercontent.com/leifadev/shoutout/main/src/resources/"  # Link to current config


class backendTasks:
    """
    Contains all automated backend tasks that the program needs for backend functionality

    """

    @staticmethod
    def regenConfig(config):
        """
        Regenerate a config file!

        :param config: "config" or "scheduleconfig"
        :return:
        """
        if config == "config":
            newConfig = requests.get(resourcesURL + "config.yml").text
            logging.info(f"Generating new config.yml in {configDir}")
            directory = ymlDir

        elif config == "scheduleconfig":
            newConfig = requests.get(resourcesURL + "scheduleconfig.json").text
            logging.info(f"Generating new scheduleconfig.json in {configDir}")
            directory = scheduleDir
        else:
            logging.error("Supply config or schedule config when using regenConfig()")
            return
        with open(directory, "w+") as file:
            # file.truncate(0)
            file.write(newConfig)

    @staticmethod
    def createAppConfig():
        """
        Create the whole Shoutout config folder and it's contents in it's entirety!

        :return:
        """
        url = "https://api.github.com/repos/leifadev/shoutout/contents/src/resources/lang_storage"
        database_contents = requests.get(url, headers={"Content-Type": "application/vnd.github+json"})

        database_contents = json.loads(database_contents.text)
        for i in database_contents:
            download.download(f"https://github.com/leifadev/shoutout/blob/main/resources/lang_storage/{i['name']}",
                              configDir + "resources")
        import shutil
        shutil.move("com.leifadev.Shoutout.plist", "~/Library/LaunchAgents/")

    @classmethod
    def handleConfigFolder(cls):
        """
        Create the config folder, and it's sub folders, update any new or deleted files
        """
        logging.info("Handling repairing or restoring a new configuration folder in Application Support/shoutout")
        if not os.path.exists(configDir):
            os.mkdir(configDir)

        global count
        url = "https://api.github.com/repos/leifadev/shoutout/contents/src/resources/"
        database_contents = requests.get(url, headers={"Content-Type": "application/vnd.github+json"})
        os.chdir(configDir)

        # Download all the available items in the lang_storage folder
        database_contents = json.loads(database_contents.text)
        for i in database_contents:
            if i['name'].endswith('.tar.gz'):
                download.download(
                    f"https://raw.githubusercontent.com/leifadev/shoutout/main/src/resources/{i['name']}",
                    configDir + "lang_storage/" + i['name'], replace=True)

    @classmethod
    def getYAML(cls, file=ymlDir):
        """
        Safe load the config.yml or any .yml. By default, it will refer to the shoutout config folder,
        but you can specify another file directory to load in kwargs!

        :param file: Custom other file
        :return: Loaded Yml content
        """
        if not os.path.isfile(ymlDir) and file == ymlDir:
            cls.regenConfig("config")
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
    def handleDaemonConfig(cls):
        """
        Downloads and updates the launch agent plist for Shoutout

        :return:
        """
        # Download Launch Daemon plist
        if not os.path.isfile(configDir + 'com.shoutout.Shoutout.plist'):
            try:
                download.download(
                    f'https://raw.githubusercontent.com/leifadev/shoutout/main/src/resources/com.leifadev.Shoutout.plist',
                    configDir + "resources")
            except urllib.error.URLError:
                logging.warning("Could not connect to internet to download com.shoutout.Shoutout.plist!")

    @classmethod
    def handleScheduleConfig(cls, directory=configDir):
        """
        Downloads or updates the notification schedule config json file for Shoutout
        to its newest version

        :param directory: Specify a custom directory for a Shoutout! scheduleconfig.json other than
        it's default one to the Shoutout config folder
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

        # Update scheduleconfig.json #
        with open(f"{directory}scheduleconfig.json", "r") as config:
            try:
                config = json.load(config)
            except json.decoder.JSONDecodeError as c:
                logging.error(f"Error accessing your schedule config (scheduleconfig.json)!\n"
                              f"Please fix your configuration file or delete it to generate a new one, here's the traceback\n{c}")
                backendTasks.regenConfig("scheduleconfig")

            # Load the newest online config and compare it to the existing one
            # to update any changes
            newestConfig = requests.get(resourcesURL + "scheduleconfig.json").text
            newestConfig = json.loads(newestConfig)  # Only updates times section

            # Find the keys from the old and new config that are still in both there
            preserve_keys = config.keys() & newestConfig.keys()  # & symbol only keeps matching keys
            # Find the keys that have gone away or are being added to the new config from old one
            changing_keys = config.keys() ^ newestConfig.keys()
            # Within the keys that are new or going away, find the ones that apart of the old config,
            # that is, the ones that are going away...
            removed_keys = dict.fromkeys(changing_keys, 0).keys() & dict.fromkeys(config.keys(), 0).keys()
            # Find the changing ones that are being added...
            added_keys = dict.fromkeys(changing_keys, 0).keys() & dict.fromkeys(newestConfig.keys(), 0).keys()

            preserve_keys_new = {}

            if newestConfig.keys() == config.keys():  # If the config file is not different
                # category wise, still add/remove any new values added into a category
                removals = []

                for key in preserve_keys:
                    preserve_keys_new.update({key: {}})
                    # Get values that are already here in current config
                    for x, y in config[key].items():
                        if x in newestConfig[key].keys():
                            preserve_keys_new[key].update({x: y})
                            logging.debug(f"This is added: {x}")
                        else:
                            removals.append(x)
                            logging.debug(f"This key has been removed: {x}")

                    # Get keys that are not yet present in current config
                    for i, e in newestConfig[key].items():
                        if i not in config[key].keys():
                            preserve_keys_new[key].update({i: e})

                if preserve_keys_new.items() == config.items():
                    logging.info("No new changes found for the scheduleconfig.json!")
                else:
                    import datetime
                    logging.warning("Config outdated! Updating scheduleconfig.json to the new version "
                                    f"as of {datetime.date.today()}\n"
                                    f"Values Removed: {removals}")

                    new_data = {}
                    new_data.update(preserve_keys_new)

                    # Dump updated config
                    with open(f"{directory}scheduleconfig.json", "w+") as file:
                        file.seek(0)
                        json.dump(new_data, file, indent=4, ensure_ascii=True)
            else:
                # Find any changed keys within main keys (categories)
                # Loops through keys that exist within the new config AND the
                # old one, includes those with there existing settings with any newly
                # added setting

                for key in preserve_keys:
                    preserve_keys_new.update({key: {}})
                    for x, y in config[key].items():
                        if x in newestConfig[key].keys():
                            preserve_keys_new[key].update({x: y})

                added_keys = list(dict.fromkeys(added_keys))

                added_keys_new = {}

                for i, y in newestConfig.items():
                    if i in added_keys:
                        added_keys_new.update({i: y})

                new_data = {}

                new_data.update(preserve_keys_new)
                new_data.update(added_keys_new)

                logging.debug(f'Removed the keys in current config: {removed_keys}')

                # Dump updated config
                with open(f"{directory}scheduleconfig.json", "w+") as config:
                    config.seek(0)
                    json.dump(new_data, config, indent=4, ensure_ascii=True)

    @classmethod
    def handleConfig(cls):
        """
        Runs tasks such as detecting if the config is corrupted, empty, or if
        it is out of date to a newer config of shoutout, and preserves the old options when it
        restores it

        """
        # Check if config file is present or is very low size
        new_data = {}  # Dictionary for all added changed data

        if not os.path.isfile(ymlDir) or os.path.getsize(ymlDir) <= 20:
            logging.info("Creating the settings.yml")

            # Go to config folder
            try:
                os.chdir(configDir)
            except FileNotFoundError as e:
                # Regenerate folder if it's gone
                cls.handleConfigFolder()
            cls.regenConfig("config")

        else:  # If config is present check if is outdated/broken
            logging.info("Opening current config.YML")
            config = cls.getYAML()

            # Change to config directory
            os.chdir(configDir)

            # Fetch new config form GitHub servers (the newest resources/config.yml commit)
            logging.debug("Requesting online copy of config.yml from github repo")
            newestConfig = requests.get(resourcesURL + "config.yml").text
            # print(newestConfig)

            # Convert the new config into a yaml object that's safe-loaded to work with
            logging.debug("Converting github text payload to yaml dict (safe load)...")
            newestConfig = ruamel.yaml.safe_load(newestConfig)

            # Add any entirely new categories that aren't present
            for category in newestConfig.keys():
                if category not in config.keys():
                    new_data.update({category: newestConfig[category]})

            # Detect categories that are no longer in use
            for category in config.keys():
                if category not in newestConfig.keys():
                    logging.info(f'Removing unneeded category from config.yml: {category}')

            # Loop through the new config options, if key already from it
            for category in config:
                # print(category)
                new_data.update({category: {}})
                # print(config[category].keys())

                # Find the keys from the old and new config that are still in both there
                preserve_keys = config[category].keys() & newestConfig[category].keys()  # & symbol only keeps
                # matching keys
                # Find the keys that have gone away or are being added to the new config from old one
                changing_keys = config[category].keys() ^ newestConfig[category].keys()

                # Within the keys that are new or going away, find the ones that apart from the old config,
                # that is, the ones that are going away...
                removed_keys = dict.fromkeys(changing_keys, 0).keys() & dict.fromkeys(config[category].keys(),
                                                                                      0).keys()
                # Find the changing ones that are being added...
                added_keys = dict.fromkeys(changing_keys, 0).keys() & dict.fromkeys(newestConfig[category].keys(),
                                                                                    0).keys()
                # Get values for preserved keys and new keys from GitHub request config
                for x, y in newestConfig[category].items():
                    if x in added_keys:
                        # print(x, category)
                        new_data[category].update({x: y})
                        # print(f"Adding: {category}: {x}: {y}")

                for i, e in config[category].items():
                    if i in preserve_keys:
                        new_data[category].update({i: e})

                        # print(i, category)

                        # print(f"Preserving: {category}: {i}: {e}")

                # print(f'P: {preserve_keys}', f'C: {changing_keys}', f'R: {removed_keys}', f'A: {added_keys}')

            old_langs = config['Other']['custom_languages']
            new_langs = newestConfig['Other']['custom_languages']

            if 'Example' not in old_langs:
                logging.warning("'Example' is not in the config file as a custom language!"
                                "\nThe example custom language folder may not be present for some reason... Please run tasks.generateExampleLang()")

            # Use bit operators need to change to sets
            old_langs = set(old_langs)
            new_langs = set(new_langs)

            # For loop for custom_languages list
            preserved_langs = old_langs & new_langs
            changing_langs = old_langs ^ new_langs
            # removed_langs = changing_langs & old_langs

            combined_langs = list(preserved_langs.union(changing_langs))

            new_data['Other']['custom_languages'] = combined_langs # Assign new updated languages


            # # Dump new updated data/dictionaries to yml
            # with open(ymlDir, "r+") as wyml:
            #     # Add header comment
            #     # Gets first top two lines of YML for preserving comment
            #     download.download(resourcesURL + "config.yml", "temp_config.yml")
            #     with open("temp_config.yml", "r") as temp:
            #         lines = temp.readlines()
            #         for i in lines[0:2]:
            #             wyml.write(i)
            #     os.remove("temp_config.yml")
            #     yaml = ruamel.yaml.YAML()  # defaults to round-trip if no parameters given
            #     yaml.dump(data, wyml)

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
            config.seek(0)
            try:
                data = json.load(config)
            except json.decoder.JSONDecodeError:
                logging.warning(f"Received no data, regenerating the scheduleconfig.json")
                data = json.loads(requests.get(resourcesURL + "scheduleconfig.json").text)

            try:
                data[category][option] = value
            except KeyError:
                logging.warning("Category or key specified does not exist!")

            config.seek(0)
            config.truncate(0)
            json.dump(data, config, indent=4)

    from typing import Optional
    @classmethod
    def updateConfig(cls, category: Optional, option: str, value, path=configDir):
        """
        Updates a yml file

        :param category: Category if any for the yml file
        :param option: The option to modify
        :param value: Value of change of option
        :param path: Path to file, default is Shoutout config.yml
        :return:
        """

        data = cls.getYAML()

        try:
            data[category][option] = value
        except TypeError as r:
            logging.warning(
                f"Received no data for specified values: {category, option, value}, regenerating the config.yml")
            # cls.regenConfig("config")

        wyml = open(configDir + "config.yml", "r+")
        wyml.truncate(0)  # Also could do w+ too...
        wyml.seek(0)  # Avoid unicode charecter bug thing
        yaml = ruamel.yaml.YAML()
        yaml.dump(data, wyml)
        wyml.close()

    @classmethod
    def downloadLangDb(cls):
        # Get all language folders/zips available in GitHub repository database database_contents = subprocess.call(
        # 'curl -H "Accept: application/vnd.github+json"
        # https://api.github.com/repos/leifadev/shoutout/contents/src/resources/lang_storage', shell=True )

        global count
        url = "https://api.github.com/repos/leifadev/shoutout/contents/src/resources/lang_storage"
        database_contents = requests.get(url, headers={"Content-Type": "application/vnd.github+json"})
        os.chdir(configDir)

        # Download all the available items in the lang_storage folder
        database_contents = json.loads(database_contents.text)
        for i in database_contents:
            if i['name'].endswith('.tar.gz'):
                download.download(
                    f"https://raw.githubusercontent.com/leifadev/shoutout/main/src/resources/lang_storage/{i['name']}",
                    configDir + "lang_storage/" + i['name'], replace=True)

        for file in os.listdir(configDir + 'lang_storage/'):

            if file.endswith("tar.gz") or file.endswith('.tar') or file.endswith('.gz') or file.endswith('.zip'):
                count = 0
                count += 1
                shutil.unpack_archive(configDir + 'lang_storage/' + file, configDir + 'lang_storage/')

        logging.info("Done with downloading the language database!\n"
                     f"Languages downloaded? {count}")

    @staticmethod
    def generateExampleLang():
        logging.info("Generating a custom_languages database...")
        yml = tasks.getYAML()
        current_customs = yml['Other']['custom_languages']
        folder = configDir + "lang_storage/custom_languages/Example"

        if not os.path.isdir(folder):
            import download
            download.download(
                "https://download-directory.github.io/?url=https://github.com/leifadev/shoutout/tree/main/src"
                "/resources/lang_storage/custom_languages/Example",
                configDir + "lang_storage/" + "Example/")
            logging.debug("Making custom_languages folder")
        elif current_customs is None:
            current_customs = ['Example']
            logging.debug("No 'Example' entry in custom_languages in config.yml, adding it now")
        elif 'Example' not in current_customs:
            logging.debug("No 'Example' entry in custom_languages in config.yml, adding it now")
            current_customs.append("Example")

        backendTasks.updateConfig(category='Other', option='custom_languages', value=current_customs)


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

# Set umask perms for dealing with files
umask = os.umask(0o013)  # Allowed Permissions rwxrw-r--
os.umask(umask)

# backendTasks.updateSchedule("hours", "alert3", False)
backendTasks.handleConfig()
