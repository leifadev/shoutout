"""
Shoutout!s daemon, primarily for it's notifications

"""

"""
Tasks:
- Output logging to .log stdout
- Sends notifications, sound, etc.
- Pulls from scheduleconfig.json file
- Inherits Cocoa, Foundation, or python modules for fetching time zones, etc.
- All daemon tasks and semantics are handled with some documentation for clearance
"""

# Python modules
import lockfile, wget
import logging, os, sys, time, getpass, json


class Daemon:
    logging.info("Starting up daemon class...")

    def __init__(self):
        self.hourly = bool
        self.pidfile_path = '/tmp/shoutout.pid'
        self.configPath = f"/Users/{getpass.getuser()}/Library/Application Support/shoutout/"
        self.daemonPath = f"/Users/{getpass.getuser()}/Library/LaunchAgents/"
        self.pidfile = lockfile.FileLock('/var/run/shoutout.pid')
        self.time = ""
        self.resourcesURL = \
            "https://raw.githubusercontent.com/leifadev/shoutout/main/resources/"  # Link to current config

        self.weekday_dict = {
            6: "sunday", 0: "monday", 1: "tuesday",
            2: "wednesday", 3: "thursday", 4: "friday",
            5: "saturday"
        }

        self.timepools = {
            "NTP Project": "2.pool.ntp.org",
            "Apple": "time.apple.com",
        }


        # Create log file!
        if os.path.isfile(self.configPath + "daemonlogs.log"):
            try:
                f = open(self.configPath + "daemonlogs.log", "w")
                f.close()
            except:
                pass
        else:
            logging.info("daemonlogs.log is already created, skipping instruction")

    # Make pid file functional
    def pid(self):
        pass

    def fetchtime(self):
        """
        Fetch UTC time, priority being a time pool server, if no connection is made
        retrieves from system time

        For now time pool servers incorporated here can't be accurate timezone wise
        with ntplib, using datetime module with local system time instead

        :return: String UTC timestamp
        """
        import datetime

        # try:
            # ntpdata = ntplib.NTPClient()
            # from datetime import datetime
            # # Requesting online time pool, apples servers
            # response = ntpdata.request(self.timepools["Apple"], version=3)
            # self.time = arrow.get(response.tx_time)
            # logging.info(f"Stored time value from NTP Server!\n{self.time}")

            # Don't use NTP server for now because it doesn't
            # support different time-zones
        #     self.time = datetime.datetime.today()
        #     return self.time
        #
        # except ntplib.NTPException as e:
            # logging.error(f"There was an exception with the NTP Server connection!\n{e}")
            # logging.warning("Internet connection lost? Don't worry, using your local machine time!")
        self.time = datetime.datetime.today()
        return self.time

    def clock(self):
        """
        When used detects the date and time and returns true for
        sending a notification based on the user's configuration

        :return: True or False
        """
        # Download schedule config file if not present
        if not os.path.isfile(self.configPath + "scheduleconfig.json"):
            wget.download(self.resourcesURL + 'scheduleconfig.json', self.configPath + "scheduleconfig.json")

        project_dir = "resources/scheduleconfig.json"  # for testing
        with open(self.configPath + "scheduleconfig.json", mode="r") as config:
            try:
                data = json.loads(config.read())
            except json.decoder.JSONDecodeError as e:
                from src import backendTasks
                task = backendTasks()
                task.otherConfigFiles()
                logging.warning(f"Schedule config file is probably corrupted... "
                                f"Created a new one, error is below hopefully with the index where JSON failed\n{e}")
                data = json.loads(config.read())

            # Get two dictionaries for alerts and days into two variables
            days_active = data["days"]
            alert_dates = data["hours"]

            # Check if there is any hourly requirements
            if int or str or list or dict or \
                    tuple or float in list(alert_dates.values()):
                self.hourly = True
            else:
                self.hourly = False

            # Fetch UTC time in date format into date and time
            self.time = str(self.fetchtime())

            # Trim down UTC time into just month-day without 0's
            month_day = int(self.time.split(" ")[0].split("-")[2].replace("0", ""))

            # Weekday integer from datetime module
            import datetime
            utc_weekday = datetime.datetime.today().weekday()

            # System time, substitute for timezone-bound NTP server time
            system_hour = datetime.datetime.now().hour

            # Print month-day, weekday, and hour integer
            NSLog(month_day, utc_weekday, system_hour)

            # Loop for checking for all day values in config
            for key, value in days_active.items():
                # https://pythontic.com/datetime/date/weekday
                weekday = self.weekday_dict[utc_weekday]  # Index weekday int from datetime to string
                if key == weekday and value:  # If config day (key) is what the day is today,
                    # check if it's true (if needs notification)
                    logging.info(f"Today is {weekday}, checking for hours!")
                    NSLog("Day is active!")

                    if self.hourly:
                        # Loop for hours
                        for alert, hour in alert_dates.items():
                            if hour == system_hour:
                                logging.info(f"Hour: {hour} is the hour to notify!")
                                NSLog(f"Hour: {hour} is the hour to notify!")
                                return True
                    else:
                        return True

    # Some operating functions for the daemon
    @staticmethod
    async def shutdown(error="No error specified"):
        if error is not None and str:
            logging.warning("Shutting down shoutout daemon!")
            await sys.exit(0)
        else:
            logging.error("Invalid invoke of shutdown method!\nMust be string arg")
            await sys.exit(128)

    @staticmethod
    async def sleep(duration: int, msg="Sleeping..."):
        """
        Sleeps the daemon
        zzz...

        :param duration: Duration for sleeping time, in seconds
        :param msg: Optional message
        :return:
        """
        # Sleep daemon, (print statement for pure sys.stdout)
        NSLog(f"Message to sleep: {msg}")
        time.sleep(duration)

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

if __name__ == "__main__":
    # Set umask for UNIX perms
    umask = os.umask(0o013)  # Allowed Permissions rwxrw-r--
    os.umask(umask)
    daemon = Daemon()

    # When script is run checks if config is true then sends notification
    if daemon.clock():
        from notifications import NotificationScheduler

        nc = NotificationScheduler()
        nc.sendNotificationRequest("Shoutout!", f"Subtitle",
                                   f"You have a word of the day to check!")
        import Cocoa
        Cocoa.NSRunLoop.currentRunLoop()

"""
Q: When will this run?
;
A: This will be triggered from a plist from Apple's launch daemon,
'launchd' to be more specific.

The plist is in the resources folder of the project directory,
it should run every hour or so every day.

It is really a Launch Agent instead of Daemon because it is on the
user level instead but yeah.

------------------------

Launch Agent/Daemon Directories MacOS

 ~/Library/LaunchAgents     --> Per-user agents provided by the user. <-- Using this one
 /Library/LaunchAgents          Per-user agents provided by the administrator.
 /Library/LaunchDaemons         System-wide daemons provided by the administrator.

 /System/Library/LaunchAgents   Per-user agents provided by Apple.
 /System/Library/LaunchDaemons  System-wide daemons provided by Apple.

Daemon Setup Methods 
# https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html#//apple_ref/doc/uid/10000172i-SW7-BCIEDDBJ
# https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/#tut # No longer using this method

"""
