# Main Modules

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
            tasks.updateConfig("complexity", "easy")
            logging.debug(f"Value at: {slider_value}, low end")
        elif slider_value < 68:
            tasks.updateConfig("complexity", "normal")
            self.complexity_bar.setDoubleValue_(2)
            logging.debug(f"Value at: {slider_value}, mid")
        elif slider_value > 72:
            tasks.updateConfig("complexity", "hard")
            self.complexity_bar.setDoubleValue_(3)
            logging.debug(f"Value at: {slider_value}, high end")

    @objc.IBAction
    def selectDay_(self, sender):
        # date_value = self.datePicker.dateValue()
        # # Example return value for dateValue -> 2022-11-13 00:17:04 +0000
        # date_value = date_value.split(" ")[1].split(':')[1:3] # Get hour and minute in a list with each other
        # date = {
        #     'hour': date_value[0],
        #     'minute': date_value[1]
        # }
        # selected_item = self.weekSelectButton.selectedItem()
        # print(selected_item.state())
        # if selected_item.state() == 1:
        #     selected_item.setState_(0)
        #     print(f"changed state to: 0")
        # elif selected_item.state() == 0:
        #     selected_item.setState_(1)
        #     print(f"changing state to: 1")
        if self.aState is False:
            self.aState = True
        else:
            self.aState = False

        print(self.aState)


        print(selected_item)
        selected_item.setState_(1)
        # self.weekSelectButton.selectItem_(selected_item)

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
