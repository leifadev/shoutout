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

import daemon, signal, lockfile
import logging, os, sys, time


try:
    os.mkdir("/private/etc/shoutout")
except FileExistsError as e:
    logging.info("Config already created!")
except PermissionError as p:
    logging.error("Don't have permission!")

os.chdir("/private/etc/shoutout")
print(os.getcwd())


class Daemon():

    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/shoutout.pid'
        self.pidfile_timeout = 5
        logging.info("Successfully instanciated I/O var paths")


    def run(self):
        while True:
            print("Loop de doop")
            logging.warning("Daemon looped the action!")

    def shutoff(self, signum, frame):
        sys.exit(0)


    with open("catch", "w") as f:
        f.write("wer")


    # with daemon.DaemonContext(
    #         # files_preserve=reserved_files,
    #         # chroot_directory="/",
    #         working_directory="/private/etc/shoutout",
    #         stdout=sys.stdout,
    #         stderr=sys.stderr,
    #         umask=0o000,
    #         uid=6969,
    #         gid=666,
    #         pidfile=lockfile.FileLock('/var/run/shoutout.pid'),
    #         signal_map={
    #             signal.SIGTERM: shutoff,
    #             signal.SIGTSTP: shutoff
    #         }):
    #     umask = os.umask(0)
    #     os.umask(umask)
    #     print(umask)
    #     print(os.getuid(), os.getgid())
    #     print(os.getcwd())





    """Internal clockwork and data (notifications) managment"""




# https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html#//apple_ref/doc/uid/10000172i-SW7-BCIEDDBJ
# https://dpbl.wordpress.com/2017/02/12/a-tutorial-on-python-daemon/#tut