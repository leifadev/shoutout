"""
Contains core variables for the project such as user's home directory or Shoutout
config directory

"""
import Foundation

# Foundation.NSFullUserName()
# Foundation.NSHomeDirectoryForUser('root')

homeDir = Foundation.NSHomeDirectory()
tempDir = Foundation.NSTemporaryDirectory()
backendDir = f'/Users/{Foundation.NSUserName()}/Library/Application Support/'
configDir = f'/Users/{Foundation.NSUserName()}/Library/Application Support/shoutout/'
ymlDir = configDir + "config.yml"
scheduleDir = configDir + "scheduleconfig.json"
resourcesURL = \
    "https://raw.githubusercontent.com/leifadev/shoutout/main/src/resources/"  # Link to current config

language_codes = {
    "english": "en",  # English (US)
    "spanish": "es",  # Spanish
    "hindi": 'hi',  # Hindi
    "german": 'de',  # German
    "french": 'fr',  # French
    "japanese": 'jp',  # Japanese
    "russian": 'ru',  # Russian
    "italian": 'it',  # Italian
    "korean": 'ko',  # Korean
    "arabic": 'ar',  # Arabic
    "polish": 'pl',  # Polish
    "chinese": 'zh',  # Chinese
    "dutch": 'nl',  # Dutch
    "portuguese": 'pt',  # Portuguese
    "czech": 'cz'  # Czech
}

# Reverses dictionary language_codes keys and values
codes_to_languages = dict([(value, key) for key, value in language_codes.items()])
