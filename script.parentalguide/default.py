# -*- coding: utf-8 -*-
import sys
import xbmc
import xbmcaddon
import xbmcgui
import traceback
#import requests

# Import the common settings
from resources.lib.settings import Settings
from resources.lib.scraper import KidsInMindScraper
from resources.lib.scraper import IMDBScraper
from resources.lib.scraper import DoveFoundationScraper
from resources.lib.scraper import MovieGuideOrgScraper
from resources.lib.viewer import DetailViewer
from resources.lib.viewer import SummaryViewer
from resources.lib.settings import log
from resources.lib import imdb

if sys.version_info >= (2, 7):
    import json
else:
    import simplejson as json

# Import the common settings
from resources.lib.settings import log
#from resources.lib.core import ParentalGuideCore
#from core import ParentalGuideCore

ADDON = xbmcaddon.Addon(id='script.parentalguide')
CWD = ADDON.getAddonInfo('path')#.decode("utf-8")

def getIsTvShow():
    if xbmc.getCondVisibility("Container.Content(tvshows)"):
        return True
    if xbmc.getCondVisibility("Container.Content(Seasons)"):
        return True
    if xbmc.getCondVisibility("Container.Content(Episodes)"):
        return True
    if xbmc.getInfoLabel("container.folderpath") == "videodb://tvshows/titles/":
        return True  # TvShowTitles

    return False

def runForVideo(videoName, IMDBID, isTvShow=False):
        log("ParentalGuideCore: Video Name = %s" % videoName)
        # Get the initial Source to use
        searchSource = Settings.getDefaultSource()

        selectedViewer = Settings.getDefaultViewer()
        dataScraper = IMDBScraper.parentsguide(IMDBID)
        details = dataScraper
        viewer = SummaryViewer("summary.xml", CWD, title=videoName, details=details)
        log(details)
        viewer.doModal()
        del viewer
        # while searchSource is not None:
            # dataScraper = None
            # searchMatches = []
            # xbmc.executebuiltin("ActivateWindow(busydialog)")
            # try:
                # if searchSource == Settings.KIDS_IN_MIND:
                    # dataScraper = KidsInMindScraper(videoName, IMDBID, isTvShow)
                # elif searchSource == Settings.DOVE_FOUNDATION:
                    # dataScraper = DoveFoundationScraper(videoName, isTvShow)
                # elif searchSource == Settings.MOVIE_GUIDE_ORG:
                    # dataScraper = MovieGuideOrgScraper(videoName, isTvShow)
                # else:
                    # dataScraper = IMDBScraper.imdb_parentsguide(IMDBID)

                # searchMatches = dataScraper.getSelection()
            # except:
                # log(searchMatches &  "runForVideo: Failed to run scraper: %s" % traceback.format_exc(), xbmc.LOGERROR)
                # xbmc.executebuiltin('Notification(%s,%s,3000,%s)' % (ADDON.getLocalizedString(32001).encode('utf-8'), ADDON.getLocalizedString(32037).encode('utf-8'), ADDON.getAddonInfo('icon')))

            # xbmc.executebuiltin("Dialog.Close(busydialog)")
            # selectedItem = None

            # # Work out what provider we would switch to if the user wants to switch
            # switchSource = Settings.getNextSource(searchSource)

            # if len(searchMatches) < 1:
                # # Offer searching by the other provider if there is one
                # if switchSource is not None:
                    # msg1 = "%s %s" % (ADDON.getLocalizedString(32005), videoName)
                    # msg2 = "%s %s" % (ADDON.getLocalizedString(32010), ADDON.getLocalizedString(switchSource))
                    # switchSearch = xbmcgui.Dialog().yesno(ADDON.getLocalizedString(32001), msg1, msg2)
                    # # If the user wants to switch the search then tidy up then loop again
                    # if switchSearch:
                        # searchSource = switchSource
                    # else:
                        # searchSource = None
                # else:
                    # searchSource = None
            # elif len(searchMatches) == 1:
                # selectedItem = searchMatches[0]
            # elif len(searchMatches) > 1:
                # displayList = []
                # for aMatch in searchMatches:
                    # displayList.append(aMatch["name"])
                # select = xbmcgui.Dialog().select(ADDON.getLocalizedString(32004), displayList)
                # if select == -1:
                    # log("ParentalGuide: Cancelled by user")
                    # selectedItem = None
                    # msg = "%s %s" % (ADDON.getLocalizedString(32010), ADDON.getLocalizedString(switchSource))
                    # switchSearch = xbmcgui.Dialog().yesno(ADDON.getLocalizedString(32001), msg)
                    # # If the user wants to switch the search then tidy up then loop again
                    # if switchSearch:
                        # searchSource = switchSource
                    # else:
                        # searchSource = None
                # else:
                    # log("ParentalGuide: Selected item %d" % select)
                    # selectedItem = searchMatches[select]

            # displayTitle = None
            # displayContent = ""
            # details = None

            # if selectedItem is None:
                # log("ParentalGuide: No matching movie found")
            # else:
                # xbmc.executebuiltin("ActivateWindow(busydialog)")
                # try:
                    # # Now get the details of the single film
                    # displayTitle = "%s: %s" % (ADDON.getLocalizedString(searchSource), selectedItem["name"])
                    # log("ParentalGuide: Found film with name: %s" % selectedItem["name"])

                    # details = dataScraper.getParentalGuideData(selectedItem["link"])
                    # print(details)
                    # log(details)
                    # if details not in [None, ""]:
                        # displayContent = dataScraper.getTextView(details)
                # except:
                    # log("runForVideo: Failed to run scraper: %s" % traceback.format_exc(), xbmc.LOGERROR)
                    # xbmc.executebuiltin('Notification(%s,%s,3000,%s)' % (ADDON.getLocalizedString(32001).encode('utf-8'), ADDON.getLocalizedString(32037).encode('utf-8'), ADDON.getAddonInfo('icon')))

                # xbmc.executebuiltin("Dialog.Close(busydialog)")

                # # Clear the search source as that will be used to decide if we close the window or
                # # loop again
                # searchSource = None

            # if dataScraper not in [None, ""]:
                # del dataScraper

            # if displayContent not in [None, ""]:
                # # Allow TvTunes to continue playing
                # xbmcgui.Window(12000).setProperty("TvTunesContinuePlaying", "True")

                # changingViewer = True
                # while changingViewer:
                    # viewer = None
                    # # Create the type of viewer we need
                    # if selectedViewer == Settings.VIEWER_DETAILED:
                        # viewer = DetailViewer.createDetailViewer(switchSource, displayTitle, displayContent)
                    # else:
                        # #viewer = SummaryViewer.createSummaryViewer(switchSource, displayTitle, details["details"])
                        # # viewer = SummaryViewer.createSummaryViewer(displayTitle, details["details"])
                        # viewer = SummaryViewer("summary.xml", CWD, title=displayTitle, details=details)

                        
                    # # Display the viewer
                    # viewer.doModal()

                    # # Dialog has been exited, check if we need to reload with a different view
                    # changingViewer = viewer.isChangeViewer()
                    # if changingViewer:
                        # if selectedViewer == Settings.VIEWER_DETAILED:
                            # selectedViewer = Settings.VIEWER_SUMMARY
                        # else:
                            # selectedViewer = Settings.VIEWER_DETAILED
                    # else:
                        # # Check if the user wants to just switch providers
                        # if viewer.isSwitch():
                            # searchSource = switchSource
                        # else:
                            # searchSource = None
                    # del viewer

                # # No need to force TvTunes now we have closed the dialog
                # xbmcgui.Window(12000).clearProperty("TvTunesContinuePlaying")


#########################
# Main
#########################
if __name__ == '__main__':
    log("ParentalGuide: Started")

    videoName = None
    isTvShow = getIsTvShow()

    # First check to see if we have a TV Show of a Movie
    if isTvShow:
        videoName = xbmc.getInfoLabel("ListItem.TVShowTitle")
        IMDBID = xbmc.getInfoLabel("ListItem.IMDBNumber")
        
    # If we do not have the title yet, get the default title
    if videoName in [None, ""]:
        videoName = xbmc.getInfoLabel("ListItem.Title")
        IMDBID = xbmc.getInfoLabel("ListItem.IMDBNumber")
        print("ListItem.Title")
        print("ListItem.IMDBNumber")

    # If there is no video name available prompt for it
    if videoName in [None, ""]:
        # Prompt the user for the new name
        keyboard = xbmc.Keyboard('', ADDON.getLocalizedString(32032), False)
        keyboard.doModal()

        if keyboard.isConfirmed():
            try:
                videoName = keyboard.getText().decode("utf-8")
            except:
                videoName = keyboard.getText()

    if videoName not in [None, ""]:
        log("ParentalGuide: Video detected %s" % videoName)
        runForVideo(videoName, IMDBID, isTvShow)
        print("ListItem.Title")
        print("ListItem.IMDBNumber")
    else:
        log("ParentalGuide: Failed to detect selected video")
        xbmcgui.Dialog().ok(ADDON.getLocalizedString(32001), ADDON.getLocalizedString(32011))

    log("ParentalGuide: Ended")

#########################
# Main
#########################
#class ParentalGuideCore():
#    @staticmethod
