# Daemon for shoutout

"""
Tasks:
- initiate stdin, stdout, and sterr stream inputs constantly
- have constant daemon clock that logs every minutes as a value
- requires main.py class methods for sending notifications, sound, etc.
- has ability too modify values stored in config.yml for frequency, etc.
- logs any errors handled, or crashes (unhandled errors)
- inherits Cocoa, Foundation, or python modules for fetching time zones
- all daemon tasks and semantics are handled with some documentation for clearance
"""
# self.working_directory = "/private/etc/shoutout", plist file does this

import lockfile, ntplib, arrow
import logging, os, sys, time, getpass, json


# Try to make config now
try:
    os.mkdir(f"/Users/{getpass.getuser()}/Library/Application Support/shoutout/")

except FileExistsError as e:
    logging.info(f"Config already created!")
except PermissionError as p:
    logging.error(f"We don't have permission! This means our daemon (python 3.6+ script) doesn't have correct permissions\nto create the config folder in /etc/!\nOUTPUT: {p}")



class Daemon():

    print("Starting up daemon class...")
    def __init__(self):
        self.pidfile_path =  '/tmp/shoutout.pid'
        self.configPath = f"/Users/{getpass.getuser()}/Library/Application Support/shoutout/"
        self.pidfile_timeout = 5
        self.pidfile=lockfile.FileLock('/var/run/shoutout.pid')
        self.onlineNTP = True
        self.timepools = {
            "NTP Project": "2.pool.ntp.org",
            "Apple": "time.apple.com",
        }
        logging.info("Initiated variables! :D")
        f = open(self.configPath + "daemonlogs.log", "w")
        f.close()


    def fetchtime(self):
        self.time = ""
        if self.onlineNTP: # Fetch time local or not!
            ntpdata = ntplib.NTPClient()
            try:
                response = ntpdata.request(self.timepools["Apple"], version=3)
                self.time = arrow.get(response.tx_time)
                logging.info(f"Stored time value from NTP Server!\n{time}")
            except ntplib.NTPException as e:
                logging.error(f"There was an exception with the NTP Server connection or something else.\n{e}")
                logging.warning("Now using local time!")
                self.time = arrow.utcnow()
        else:
            self.time = arrow.utcnow()
            print(self.time)
            logging.info(f"Using local UTC time instead!")


    def clock(self):
        with open(self.configPath + "scheduleconfig.json", mode="w") as config:
            c = json.load(config)


    def shutoff(self, error):
        if error != None:
            logging.error(f"Shoutout error when shutting off!\n{error}")
            sys.exit(1)
        else:
            logging.info("Exiting program")
            sys.exit(0)


    """Internal clockwork and data (notifications) managment"""



if __name__ == "__main__":
    umask = os.umask(0o013)  # Allowed Permissions rwxrw-r-- #
    os.umask(umask)
    while True:
        Daemon().fetchtime() # Run daemon class, does clock timing, signals, config, variables

"""Documentation"""
# https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html#//apple_ref/doc/uid/10000172i-SW7-BCIEDDBJ
# https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/#tut
