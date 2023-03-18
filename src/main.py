# Main file for Shoutout!
import AppDelegate
import WindowController
import prefController
from sutils import (
    tasks,
    langutils,
    config,
    sfiles
    )

if __name__ == "__main__":
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()