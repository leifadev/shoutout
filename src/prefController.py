"""
Window controller for preferences pane

"""

# Objective-C
import logging

import Cocoa, objc
from AppKit import NSApp

# Shoutout modules
from sutils.tasks import backendTasks as tasks

class prefWindow(Cocoa.NSWindowController):
    """
    Window controller of preferences window
    (Inherits from NSWindowController)

    """

    languageComboBox = objc.IBOutlet()
    weekSelectButton = objc.IBOutlet()
    datePicker = objc.IBOutlet()
    complexity_bar = objc.IBOutlet()
    complexity_slider = objc.IBOutlet()

    sunday = objc.IBOutlet()
    monday = objc.IBOutlet()
    tuesday = objc.IBOutlet()
    wednesday = objc.IBOutlet()
    thursday = objc.IBOutlet()
    friday = objc.IBOutlet()
    saturday = objc.IBOutlet()

    aState = False

    def windowDidLoad(self):
        Cocoa.NSWindowController.windowDidLoad(self)
        self.count = 0

    @objc.IBAction
    def complexitySlider_(self, sender):
        slider_value = self.complexity_slider.doubleValue()
        if slider_value < 27:
            self.complexity_bar.setDoubleValue_(1)
            tasks.updateConfig('Main', "complexity", "easy")
            logging.debug(f"Value at: {slider_value}, low end")

        elif slider_value < 68:
            tasks.updateConfig('Main', "complexity", "normal")
            self.complexity_bar.setDoubleValue_(2)
            logging.debug(f"Value at: {slider_value}, mid")

        elif slider_value > 72:
            tasks.updateConfig('Main', "complexity", "hard")
            self.complexity_bar.setDoubleValue_(3)
            logging.debug(f"Value at: {slider_value}, high end")

    @objc.IBAction
    def selectDay_(self, sender):
        date_value = self.datePicker.dateValue()
        selected_item = self.weekSelectButton.selectedItem()

        # Example return value for dateValue -> 2022-11-13 00:17:04 +0000
        date_value = str(date_value).split(" ")[1].split(':')[1:3] # Get hour then the minute
                                                                   # in a list with each other
        day = str(selected_item.title()).lower()
        date = {
            'hour': date_value[0],
            'minute': date_value[1]
        }
        if selected_item.state() == 1:
            selected_item.setState_(0)
            tasks.updateSchedule('days', day, False)
            logging.debug(f"Changing the day, {day}, to be False, {selected_item.state()}")

            # Grab the date selected
            tasks.updateSchedule('hours', 'alert1', None)
            tasks.updateSchedule('minutes', 'alert1', None)

        elif selected_item.state() == 0:
            selected_item.setState_(1)
            tasks.updateSchedule('days', day, True)

            # Grab the date selected
            tasks.updateSchedule('hours', 'alert1', date['hour'])
            tasks.updateSchedule('minutes', 'alert1', date['minute'])
            logging.debug(f"Changing the day, {day}, to be True, {selected_item.state()}")

    @objc.IBAction
    def openlink_(self, sender):
        url = "https://github.com/leifadev/shoutout/wiki"
        print(f"{url} launched")
        x = Cocoa.NSURL.alloc().initWithString_(url)
        Cocoa.NSWorkspace.alloc().openURL_(x)

    @objc.IBAction
    def increment_(self, sender):
         self.count += 1
         self.updateDisplay()

    @objc.IBAction
    def decrement_(self, sender):
        self.count -= 1
        self.updateDisplay()


    def updateDisplay(self):
        self.settingsStepper.setStringValue_(self.count)


# Starting window!

if __name__ == "__main__":

    # Initiate the controller with a XIB
    viewController = prefWindow.alloc().initWithWindowNibName_("shoutout_main")

    # Show the window
    viewController.showWindow_(viewController)

    # Bring app to top
    NSApp.activateIgnoringOtherApps_(True)
