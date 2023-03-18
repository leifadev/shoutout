"""
Responsible for summoning notifications from the Apple framework Gods

Includes the new UserNotifications API that is compatible with MacOS 10.14/Mojave and up
and includes all features available from attachments to options etc.
"""

from uuid import uuid4
import UserNotifications as UN
import Foundation, Cocoa
import logging
from Cocoa import NSLog

def checkOldNotifications():
    # Fetch version of MacOS
    MacOSVersion = str(Foundation.NSProcessInfo.alloc().init().operatingSystemVersionString())
    # MacOSVersion = 'Version 10.15.2 (Build 22A400)' # Testing string
    # Separate version number from string, concatenate into list of all the 3 numbers
    MacOSVersion = MacOSVersion.split(" ")[1].split(".")
    # Add major and minor number (move decimal to left twice) together
    MacOSVersion = int(MacOSVersion[0]) + int(MacOSVersion[1]) / 100
    print(MacOSVersion)

    if MacOSVersion < 10.14: # Detect if the version number is higher than 10.14 (Mojave)
        old_notifications = True
    else:
        old_notifications = False
    return old_notifications


DEFAULT_AUTH_OPTIIONS = UN.UNAuthorizationOptions(UN.UNAuthorizationOptionBadge and UN.UNAuthorizationOptionSound)


class NotificationScheduler:
    center = UN.UNUserNotificationCenter.currentNotificationCenter()

    def __init__(self):  # Init objects
        self.granted = None
        self.settings = None
        self.timeInterval = 1  # In minutes
        self.repeatNotif = True  # Repeat notification? Boolean

        self.center.getNotificationSettingsWithCompletionHandler_(self._settingsHandler)

    def _haveAuthorization(self, block=False):
        if block:
            while self.granted is None:
                pass

        return bool(self.granted)

    def _settingsHandler(self, settings):
        self.settings = settings

        # if settings.authorizationStatus() == UN.UNAuthorizationStatusDenied:
        self.center.requestAuthorizationWithOptions_completionHandler_(DEFAULT_AUTH_OPTIIONS,
                                                                       self._authorizationRequestHandler)
        NSLog("Requested Auth!")

    def _authorizationRequestHandler(self, granted, error):
        self.granted = granted
        NSLog(f"Completion handler granted: {granted}")
        if error:
            NSLog(error)

    def _notificationRequestHandler(self, error):
        # NSLog("_notificationRequestHandler")
        if error:
            NSLog(error)

    def sendNotificationRequest(self, title, subtitle, body):
        """
        Sends a user notification with the User Notifications framework

        “Send me a notiii!”

        \- leifadev

        :param title: title of notification
        :param subtitle: subtitle of notification
        :param body: body text of the notification
        :return:
        """
        if not self._haveAuthorization(block=True):
            NSLog("Error: Missing authorization to add notification request.")
            return None

        # Trigger repeats every minute (may not be using this though)
        # trigger = UN.UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(60, False)

        # Making notification content with instance of UNMutableNotificationContent class
        content = UN.UNMutableNotificationContent.alloc().init()
        content.setTitle_(title)
        content.setSubtitle_(subtitle)
        content.setBody_(body)
        content.setSound_(UN.UNNotificationSound.defaultSound())
        content.setCategoryIdentifier_("Shoutout")

        # Attachments (logo)
        # import Foundation
        # fileURL = Foundation.NSURL.fileURLWithPath_("/Users/leif/PycharmProjects/shoutout/images/shoutout_logo.png")
        # import Cocoa
        # fileURL = Cocoa.NSURL.fileURLWithPath_(Cocoa.NSBundle.mainBundle().pathForResource_ofType_("shoutout_logo", "png"))
        # attachments = UN.UNNotificationAttachment.attachmentWithIdentifier_URL_options_error_\
        #     ("Shoutout_image", fileURL, {}, None)
        # content.setAttachments_([attachments])

        # Actions for notification
        action_open = UN.UNNotificationAction.actionWithIdentifier_title_options_(
            "foregroundAction",
            "Word",
            UN.UNNotificationActionOptions(UN.UNNotificationActionOptionForeground))  # Brings app to foreground

        category = UN.UNNotificationCategory.categoryWithIdentifier_actions_intentIdentifiers_options_(
            "Shoutout",
            [action_open],
            [], UN.UNNotificationCategoryOptions(UN.UNNotificationCategoryOptionNone))
        self.center.setNotificationCategories_([category])

        # Make a random identifier
        identifier = str(uuid4())

        # Form NotificationRequest object to be sent to current notification center
        request = UN.UNNotificationRequest.requestWithIdentifier_content_trigger_(identifier, content, None)
        self.center.addNotificationRequest_withCompletionHandler_(request, self._notificationRequestHandler)

    def sendNotificationRequestOld(self, title, subtitle, body):
        """
        Sends a notfication with the NSUserNotifications framework for support for
        older versions. 10.14 (Mojave) and under.

        :param title: title of notification
        :param subtitle: subtitle of notification
        :param body: body text of the notification
        :return:
        """
        noti = Cocoa.NSUserNotification.alloc().init()
        noti.setTitle_(title)
        noti.setSubtitle_(subtitle)
        noti.setInformativeText_(body)

        # Cocoa.NSUserNotificationCenter.defaultUserNotificationCenter().setDelegate_()

        nc = Cocoa.NSUserNotificationCenter.defaultUserNotificationCenter()
        nc.deliverNotification_(noti)

        logging.info("Notification method has been called!")


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

if __name__ == "__main__":
    notificationScheduler = NotificationScheduler()
    if checkOldNotifications():
        notificationScheduler.sendNotificationRequest("Shoutout!", f"Reminder", "You have a word of the day to check!")
    else:
        notificationScheduler.sendNotificationRequestOld("Shoutout!", f"Reminder", "You have a word of the day to check!")

    # Runs an event loop to keep the interpreter running to give Cocoa time to make a second thread for
    # the completion handler to run, thus so Python doesn't crash with an error. (zsh: illegal hardware instruction)
    Cocoa.NSRunLoop.currentRunLoop()  # Returns the run loop for the current thread (once?)
    # https://github.com/ronaldoussoren/pyobjc/issues/482

# Time Interval Class
# https://developer.apple.com/documentation/usernotifications/untimeintervalnotificationtrigger
