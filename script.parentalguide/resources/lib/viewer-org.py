# -*- coding: utf-8 -*-
import xbmcgui
import xbmcaddon

# Import the common settings
from resources.lib.settings import log

ADDON = xbmcaddon.Addon(id='script.parentalguide')
CWD = ADDON.getAddonInfo('path')#.decode("utf-8")
log("Viewer opened")

class ParentalGuideViewer(xbmcgui.WindowXMLDialog):
    TITLE_LABEL_ID = 201
    VIEWER_CHANGE_BUTTON = 301
    CLOSE_BUTTON = 302
    SWITCH_BUTTON = 303
    TEXT2_BOX_ID = 202
    LIST_BOX_ID = 203

    def __init__(self, *args, **kwargs):
        self.isSwitchFlag = False
        self.isChangeViewerFlag = False
        self.switchText = kwargs.get('switchText', '')
        self.title = kwargs.get('title', '').replace("b'","").replace("'","")
        xbmcgui.WindowXMLDialog.__init__(self)

    # Called when setting up the window
    def onInit(self):
        # Update the dialog to show the correct data
        labelControl = self.getControl(ParentalGuideViewer.TITLE_LABEL_ID)
        labelControl.setLabel(self.title)

        # Set the label on the switch button
        switchButton = self.getControl(ParentalGuideViewer.SWITCH_BUTTON)
        if self.switchText in [None, ""]:
            switchButton.setVisible(False)
        else:
            switchButton.setVisible(True)
            switchButton.setLabel(ADDON.getLocalizedString(self.switchText))

        xbmcgui.WindowXMLDialog.onInit(self)

    def onClick(self, controlID):
        # Play button has been clicked
        if controlID == ParentalGuideViewer.CLOSE_BUTTON:
            log("ParentalGuideViewer: Close click action received: %d" % controlID)
            self.close()
        elif controlID == ParentalGuideViewer.SWITCH_BUTTON:
            log("ParentalGuideViewer: Switch click action received: %d" % controlID)
            self.isSwitchFlag = True
            self.close()
        elif controlID == ParentalGuideViewer.VIEWER_CHANGE_BUTTON:
            log("ParentalGuideViewer: Change click action received: %d" % controlID)
            self.isChangeViewerFlag = True
            self.close()

    def close(self):
        log("ParentalGuideViewer: Closing window")
        xbmcgui.WindowXMLDialog.close(self)

    def isSwitch(self):
        return self.isSwitchFlag

    def isChangeViewer(self):
        return self.isChangeViewerFlag


######################################
# Details listing screen
######################################
class SummaryViewer(ParentalGuideViewer):
    TEXT2_BOX_ID = 202
    LIST_BOX_ID = 203
    
    def __init__(self, *args, **kwargs):
        self.details = kwargs.get('details', '')
        if self.details not in [None, ""]:
            self._setProperties(self.details)

        ParentalGuideViewer.__init__(self, *args, **kwargs)

    @staticmethod
    def createSummaryViewer(switchText, title, details):
        return SummaryViewer("script-ParentalGuide-summary.xml", CWD, switchText=switchText, title=title, details=details)

    def close(self):
        log("ParentalGuideViewer: Closing window")
        # Clear all the properties that were previously set
        i = 1
        while i < 9:
            xbmcgui.Window(10000).clearProperty("ParentalGuide.%s.Section" % i)
            xbmcgui.Window(10000).clearProperty("ParentalGuide.%s.Rating" % i)
            i = i + 1
        ParentalGuideViewer.close(self)
        
    def onInit(self):
        # Fill in the text for the details
        # textControl = self.getControl(ParentalGuideViewer.TEXT2_BOX_ID)
        # textControl.setText(self.details)
        #listControl = self.getControl(ParentalGuideViewer.LIST_BOX_ID)
        #listControl.addItem(self.details)

        ParentalGuideViewer.onInit(self)
    # Set all the values to display on the property screen
    def _setProperties(self, details):
        i = 0
        for entry in details:
            if i < 9:
                    y = i + 1
                    sectionTag = "ParentalGuide.%s.Section" % y
                    ratingTag = "ParentalGuide.%s.Rating" % y
                    #idx = details.index('name')
                    xbmcgui.Window(10000).setProperty(sectionTag, str(details[i]['name']))
                    #log(details[idx])
                    #xbmcgui.Window(10000).setProperty(ratingTag, self.details[1])
                    #idx = details.index('score')
                    ratingImage = ("SCORE-0%d.png") % int(details[i]['score'])
                    xbmcgui.Window(10000).setProperty(ratingTag, ratingImage)
            i = i + 1


######################################
# Details listing screen
######################################
class DetailViewer(ParentalGuideViewer):
    TEXT_BOX_ID = 202

    def __init__(self, *args, **kwargs):
        self.content = kwargs.get('content', '')
        ParentalGuideViewer.__init__(self, *args, **kwargs)

    @staticmethod
    def createDetailViewer(switchText, title, content):
        return DetailViewer("script-ParentalGuide-dialog.xml", CWD, switchText=switchText, title=title, content=content)

    # Called when setting up the window
    def onInit(self):
        # Fill in the text for the details
        textControl = self.getControl(DetailViewer.TEXT_BOX_ID)
        textControl.setText(self.content)

        ParentalGuideViewer.onInit(self)
