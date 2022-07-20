from uuid import uuid4
import UserNotifications as UN
import Foundation

DEFAULT_AUTH_OPTIIONS = UN.UNAuthorizationOptions(UN.UNAuthorizationOptionBadge)

class NotificationScheduler:
    center = UN.UNUserNotificationCenter.currentNotificationCenter()
    
    def __init__(self): # Init objects
        self.granted = None
        self.settings = None
        self.timeInterval = 1 # In minutes
        self.repeatNotif = True # Repeat notification? Boolean


        self.center.getNotificationSettingsWithCompletionHandler_(self._settingsHandler)

    def _haveAuthorization(self, block=False):
        if block:
            while self.granted is None:
                pass

        return bool(self.granted)

    def _settingsHandler(self, settings):
        self.settings = settings

        # if settings.authorizationStatus() == UNAuthorizationStatusDenied:
        self.center.requestAuthorizationWithOptions_completionHandler_(DEFAULT_AUTH_OPTIIONS,
                                                                       self._authorizationRequestHandler)

    def _authorizationRequestHandler(self, granted, error):
        self.granted = granted
        print(f"Completion handler granted: {granted}")
        if error:
            print(error)

    def _notificationRequestHandler(self, error):
        print("_notificationRequestHandler")
        if error:
            print(error)

    def addNotificationRequest(self, title, body):
        if not self._haveAuthorization(block=True):
            print("Error: Missing authorization to add notification request.")
            return None

        # Trigger repeats every minute (may not be using this though)
        trigger = UN.UNTimeIntervalNotificationTrigger.triggerWithTimeInterval_repeats_(60, True)

        # Making notification content with instance of UNMutableNotificationContent class
        content = UN.UNMutableNotificationContent.alloc().init()
        content.setTitle_(title)
        content.setSubtitle_("Reminder")
        content.setBody_(body)
        content.setSound_(UN.UNNotificationSound.defaultSound())
        content.setCategoryIdentifier_("Shoutout")

        # Attachments (logo)
        # fileURL = Foundation.NSURL.fileURLWithPath_("/Users/leif/PycharmProjects/shoutout/images/shoutout_logo.png")
        # attachments = UN.UNNotificationAttachment.attachmentWithIdentifier_URL_options_error_\
        #     ("Shoutout_image", fileURL, {}, None)
        # content.setAttachments_([attachments])

        # Actions for notification
        # actmv ion_open = UN.UNNotificationAction.actionWithIdentifier_title_options_("open", "Open", [])
        # category = UN.UNNotificationCategory.categoryWithIdentifier_actions_intentIdentifiers_options_("Shoutout", [action_open], [])
        # self.center.setNotificationCategories_([category])


        # Make a random identifier
        identifier = str(uuid4())

        # Form NotificationRequest object to be sent to current notification center
        request = UN.UNNotificationRequest.requestWithIdentifier_content_trigger_(identifier, content, None)
        self.center.addNotificationRequest_withCompletionHandler_(request, self._notificationRequestHandler)


if __name__ == "__main__":
    notificationScheduler = NotificationScheduler()
    notificationScheduler.addNotificationRequest("Shoutout!", "You have a word of the day to check!")

# Time Interval Class
# https://developer.apple.com/documentation/usernotifications/untimeintervalnotificationtrigger?language=objc