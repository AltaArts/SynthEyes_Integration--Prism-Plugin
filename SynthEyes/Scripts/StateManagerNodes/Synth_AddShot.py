# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.
###########################################################################
###########################################################################
#
#                    SynthEyes Integration for Prism2
#
#       https://github.com/AltaArts/SynthEyes_Integration--Prism-Plugin
#
#
#                           Joshua Breckeen
#                              Alta Arts
#                          josh@alta-arts.com
#
###########################################################################


import os
import logging


from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher

logger = logging.getLogger(__name__)

#   Global Colors
COLOR_GREEN = QColor(0, 130, 0)
COLOR_YELLOW = QColor(200, 150, 0)
COLOR_ORANGE = QColor(150, 100, 0)
COLOR_RED = QColor(130, 0, 0)
COLOR_BLACK = QColor(0, 0, 0, 0)
COLOR_WHITE = QColor(255, 255, 255, 255)

#   Icon to be used for State
scriptDir = os.path.dirname(os.path.dirname(__file__))
STATE_ICON = os.path.join(scriptDir, "Icons", "Image.png")



class Synth_AddShotClass(object):
    className = "AddShot"
    listType = "Import"
    stateCategories = {"Import2d": [{"label": className, "stateType": className}]}


    @err_catcher(name=__name__)
    def setup(
        self,
        state,
        core,
        stateManager,
        importPath=None,
        stateData=None,
        settings=None,
    ):

        #   Checks if the ATTR Already Exists and Assigns if Not
        self.core = getattr(self, "core", core)
        self.state = getattr(self, "state", state)
        self.stateManager = getattr(self, "stateManager", stateManager)
        self.synthFuncts = getattr(self, "synthFuncts", self.core.appPlugin)
        self.synthEyes = self.synthFuncts.synthEyes


        if not hasattr(self, "mediaChooser"):
            self.mediaChooser = ReadMediaDialog(self, self.core)
            
        self.stateMode = "AddShot"
        self.taskName = ""
        self.setName = ""
        self.stateStatus = None
        self.shotUUID = None

        #   State name stuff
        stateNameTemplate = "{entity}_{version}"
        self.stateNameTemplate = self.core.getConfig(
            "globals",
            "defaultImportStateName",
            configPath=self.core.prismIni,
        ) or stateNameTemplate
        self.e_name.setText(self.stateNameTemplate)

        self.b_browse.setContextMenuPolicy(Qt.CustomContextMenu)
        
        #   Hide unused UI elements
        self.l_name.setVisible(False)
        self.e_name.setVisible(True)
        self.l_class.setVisible(True)
        self.w_autoUpdate.setVisible(False)

        #   Sets colors
        self.oldPalette = self.b_importLatest.palette()
        self.updatePalette = QPalette()
        self.updatePalette.setColor(QPalette.Button, COLOR_ORANGE)
        self.updatePalette.setColor(QPalette.ButtonText, COLOR_WHITE)

        font = self.l_curVersion.font()
        font.setBold(True)
        self.l_curVersion.setFont(font)

        font = self.l_latestVersion.font()
        font.setBold(True)
        self.l_latestVersion.setFont(font)


    ####   Do one of the following:     ####

        ##   1. Load State from Comp Data
        if stateData is not None:
            self.loadData(stateData)
            logger.debug("Loaded State from saved data")

            self.nameChanged()
            self.updateUi()


        ##   2. If passed from FusFuncts. Receive importData via "settings" kwarg
        # elif settings:
        #     comp = self.fuseFuncts.getCurrentComp()

        #     #   Create State UUID
        #     self.stateUID = Helper.createUUID()

        #     #   Check if there is Prism Data passed (from Orphaned Loaders)
        #     if "pData" in settings:
        #         #   Get ImportData from Settings
        #         self.importData = settings["pData"]

        #         #   Update State UUID
        #         updateData = {"stateUID": self.stateUID}

        #         for tool in settings["tools"]:
        #             #   Update Loader
        #             Fus.updateToolData(tool["loader"], updateData)

        #             #   Get Connected Tools
        #             connectedUIDs = Fus.getConnectedNodes(comp, tool["loader"])
        #             for uid in connectedUIDs:
        #                 tool = Fus.getToolByUID(comp, uid)
        #                 Fus.updateToolData(tool, updateData)

        #         #   Make State Data
        #         result = self.makeImportData(self.importData)

        #     #   Just get the Prism Context Data
        #     else:
        #         self.importData = settings
        #         self.importLatest(refreshUi=False, selectedStates=False, setChecked=True)
        
        #     self.nameChanged()
        #     self.refresh()

        #     logger.debug("Created State from passed Settings")


        ##   3. Opens Media Popup to select import
        elif (
            importPath is None
            and stateData is None
            # and not createEmptyState
            and not settings
            and not self.stateManager.standalone
            ):

            #   Open MediaChooser to get import
            requestResult = self.callMediaWindow()
          
            if requestResult == "Cancelled":
                logger.debug("Media Import cancelled")
                return False
            
            if requestResult == "Empty":
                return False
            
            if not requestResult:
                logger.warning("ERROR: Unable to Import Image from MediaBrowser.")
                self.core.popup("Unable to Import Image from MediaBrowser.")
                return False
        
            self.setImportPath(requestResult[0])
            self.importData = requestResult[1]

            result = self.addShot(requestResult[0], requestResult[1])

            if result:
                self.shotUUID = result

            self.nameChanged()
            self.updateUi()


        ##   4. If error
        else:
            logger.warning("ERROR: Unable to Import Image.")
            self.core.popup("Unable to Import Image.")
            return False
        

        getattr(self.core.appPlugin, "sm_import_startup", lambda x: None)(self)

        self.connectEvents()
        self.setToolTips()
        self.setStateMode(self.stateMode)

        self.stateManager.saveImports()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def connectEvents(self):
        self.e_name.textChanged.connect(self.nameChanged)
        self.e_name.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.b_browse.clicked.connect(self.browse)
        self.b_browse.customContextMenuRequested.connect(self.openFolder)
        self.b_importLatest.clicked.connect(self.importLatest)
        self.chb_autoUpdate.stateChanged.connect(self.autoUpdateChanged)
        self.e_camName.editingFinished.connect(
            lambda: self.updateCamName(self.e_camName.text())
            )



    #########################
    #                       #
    #       Wrapped         #
    #   Prism Functions     #
    #                       #
    #########################


    #   Returns the version label name from version filepath
    @err_catcher(name=__name__)
    def getMasterVersionLabel(self, filepath:str) -> str:
        return self.core.mediaProducts.getMasterVersionLabel(filepath)
    

    #   Returns highest version context from a given context
    @err_catcher(name=__name__)
    def getLatestVersion(self, context:dict, includeMaster:bool) -> dict:
        mediaProducts = self.synthFuncts.core.mediaProducts
        return mediaProducts.getLatestVersionFromIdentifier(context, includeMaster=includeMaster)
    

    #   Returns a context from the currently selected version
    @err_catcher(name=__name__)
    def getCurrentVersion(self) -> dict:
        try:
            self.mediaBrowser = self.mediaChooser.w_browser
            self.mediaPlayer = self.mediaBrowser.w_preview.mediaPlayer
            return self.mediaBrowser.getCurrentVersion()
        
        except Exception as e:
            logger.warning(f"ERROR:  Unable to get Current Version from Prism Functions:\n\n{e}")
    

    #   Returns a list of AOV dicts for a given context
    @err_catcher(name=__name__)
    def getAOVsFromVersion(self, version:dict) -> list:
        try:
            return self.core.mediaProducts.getAOVsFromVersion(version)
        except Exception as e:
            logger.warning(f"ERROR:  Unable to get AOVs from Prism Functions:\n\n{e}")


    #   Returns a list of all the image files for a given context
    @err_catcher(name=__name__)
    def getFilesFromContext(self, aovItem:dict) -> list:
        try:
            return self.fuseFuncts.core.mediaProducts.getFilesFromContext(aovItem)
        except Exception as e:
            logger.warning(f"ERROR:  Unable to get Files from Prism Context Functions:\n\n{e}")




    #########################
    #                       #
    #         STATE         #
    #                       #
    #########################


    @err_catcher(name=__name__)
    def setStateMode(self, stateMode):
        self.stateMode = stateMode
        self.l_class.setText(stateMode)


    #   Set State Name and Icon
    @err_catcher(name=__name__)
    def nameChanged(self, text=None):
        name = self.e_name.text()

        if text:
            name = text
        else:
            try:
                name = self.importData['identifier']
            except Exception as e:
                name = text

        #   Set the name for the State list
        self.e_name.setText(name)
        self.state.setText(0, name)

        #   Add icon to State name
        self.state.setIcon(0, QIcon(STATE_ICON))

        self.stateManager.saveImports()
        self.stateManager.saveStatesToScene()


    #   Opens Media Chooser to select version
    @err_catcher(name=__name__)
    def browse(self):
        title = "Change Shot Images"
        text = ("Please Note:\n\n"
                "Changing the Shot Images could affect\n"
                "an existing solve.  Please save the file before changing\n"
                "the images.\n\n\n"
                "Would you like to continue?")

        result = self.core.popupQuestion(text, title)

        if result != "Yes":
            return False

        currVersion = self.getCurrentVersion()

        if currVersion:
            #   Call the MediaWindow with the MediaId
            requestResult = self.callMediaWindow(currVersion)
        else:
            #   Just call without a MediaId
            requestResult = self.callMediaWindow()

        if requestResult == "Cancelled":
            logger.debug("Media Import cancelled")
            return False
        
        if requestResult == "Empty":
            return False
        
        if not requestResult:
            logger.warning("ERROR: Unable to Import Image from MediaBrowser.")
            self.core.popup("Unable to Import Image from MediaBrowser.")
            return False
    
        self.setImportPath(requestResult[0])
        basefile = requestResult[0]
        self.importData = requestResult[1]

        result = self.changeShotImages(basefile, self.importData)

        self.updateUi()


    @err_catcher(name=__name__)
    def importLatest(self):
        title = "Change Shot Images"
        text = ("Please Note:\n\n"
                "Changing the Shot Images could affect\n"
                "an existing solve.  Please save the file before changing\n"
                "the images.\n\n\n"
                "Would you like to continue?")

        result = self.core.popupQuestion(text, title)

        if result != "Yes":
            return False

        versionData = self.getLatestVersion(self.importData, includeMaster=True)
        basefile = self.getFilepathFromVersion(versionData)
        self.importData = versionData
        self.setImportPath(basefile)

        result = self.changeShotImages(basefile, self.importData)

        self.updateUi()


    @err_catcher(name=__name__)
    def openFolder(self, pos):
        path = self.getImportPath()

        if os.path.isfile(path):
            path = os.path.dirname(path)

        self.core.openFolder(path)


    @err_catcher(name=__name__)
    def getImportPath(self):
        path = getattr(self, "importPath", "")
        if path:
            path = os.path.normpath(path)

        return path


    @err_catcher(name=__name__)
    def setImportPath(self, path):
        self.importPath = path
        self.l_text_Current.setToolTip(path)
        self.stateManager.saveImports()
        self.stateManager.saveStatesToScene()


    #   Updates the Auto-update UI
    @err_catcher(name=__name__)
    def autoUpdateChanged(self, checked):
        self.w_importLatest.setVisible(not checked)

        try:
            if checked:
                curVersion, latestVersion = self.checkLatestVersion()
                if self.chb_autoUpdate.isChecked():
                    if (curVersion.get("version")
                        and latestVersion.get("version")
                        and curVersion["version"] != latestVersion["version"]
                        ):
                        self.importLatest(refreshUi=True, selectedStates=False)

            self.stateManager.saveImports()
            self.stateManager.saveStatesToScene()

        except Exception as e:
            logger.warning(f"ERROR:  AutoUpdate Change failed:\n\n{e}")


    @err_catcher(name=__name__)
    def runSanityChecks(self, cachePath):
        result = True

        if getattr(self.core.appPlugin, "hasFrameRange", True):
            result = self.checkFrameRange(cachePath)

        if not result:
            return False

        return True

   
    
    #########################
    #                       #
    #          UI           #
    #                       #
    #########################


    @err_catcher(name=__name__)
    def setToolTips(self):
        tip = "Media Identifier of Imported Shot"
        self.e_name.setToolTip(tip)

        tip = "Opens the Media Browser to select a specific version"
        self.b_browse.setToolTip(tip)

        tip = "Will import the latest version of the media."
        self.b_importLatest.setToolTip(tip)

        tip = ("Name of SynthEyes Camera for the Shot.\n\n"
               "You may change the name and it will be\n"
               "reflected in SynthEyes.  Also the version\n"
               "number (if any) will be updated with changes\n"
               " to the selected version.")
        self.l_camName.setToolTip(tip)
        self.e_camName.setToolTip(tip)


    #   Opens the Custom MediaBrowser window to choose import
    @err_catcher(name=__name__)
    def callMediaWindow(self, itemData=None):
        #   Sets objects
        self.mediaBrowser = self.mediaChooser.w_browser
        self.mediaPlayer = self.mediaBrowser.w_preview.mediaPlayer

        #   If passed itemData, navigate to the Media Item
        if itemData:
            try:
                #   Navigate to the correct tab/table
                self.mediaBrowser.navigateToEntity(itemData)
                #   Get the item title
                mediaId = (itemData.get("displayName")
                        or itemData.get("mediaId")
                        or itemData.get("identifier")
                        )

                #   Find and select the Identifier
                items = self.mediaBrowser.tw_identifier.findItems(
                    mediaId,
                    Qt.MatchFlag(Qt.MatchExactly & Qt.MatchCaseSensitive ^ Qt.MatchRecursive)
                    )
                
                if items:
                    self.mediaBrowser.tw_identifier.setCurrentItem(items[0])
            except:
                logger.debug("ERROR:  Unable to navigate to State's entity in the MediaBrowser")

        #   Connects clicked signal
        self.mediaChooser.mediaSelected.connect(lambda selResult: self.setSelectedMedia(selResult))
        #   Calls the MediaBrowser and receives result
        result = self.mediaChooser.exec_()

        #   If cancelled
        if result == QDialog.Rejected:
            return "Cancelled"
        
        #   If error
        if not self.selResult:
            return False

        #   Gets the result
        clicked = self.selResult[0]
        self.importData = self.selResult[1]

        #   Makes funct call based on what was clicked (Identifier or Version)
        if clicked == "version":
            versionData = self.getCurrentVersion()

        if clicked == "identifier":
            versionData = self.getLatestVersion(self.importData, includeMaster=True)

        basefile = self.getFilepathFromVersion(versionData)

        if not result:
            return False
        
        if result == "Empty":
            return False
        
        else:
            return basefile, versionData
        

    def getFilepathFromVersion(self, versionContext):
        aovs = self.core.mediaProducts.getAOVsFromVersion(versionContext)

        if aovs:
            mediaFiles = self.core.mediaProducts.getFilesFromContext(aovs[0])

        else:
            basePath = versionContext["path"]
            mediaFiles = [
                os.path.join(basePath, f)
                for f in os.listdir(basePath)
                if os.path.isfile(os.path.join(basePath, f))
            ]
            mediaFiles = sorted(mediaFiles)

        validFiles = self.core.media.filterValidMediaFiles(mediaFiles)

        return validFiles[0]


    #   Sets the Selected Result from the MediaChooser
    @err_catcher(name=__name__)
    def setSelectedMedia(self, selResult):        
        self.selResult = selResult


    @err_catcher(name=__name__)
    def updateCamName(self, camName=None):
        #   Get Shot Camera Object
        camObj = self.synthFuncts.getCamFromShotUUID(self.shotUUID)

        if not camObj:
            return
        
        #   If Passed a New Name, Change it
        if camName:
            with self.synthFuncts.UNDO_BLOCK("Rename Camera"):
                self.synthFuncts.setObjName(camObj, camName)

        #   Get the Camera Name and Set it in the UI
        camName = self.synthFuncts.getCamName(self, camObj)
        self.e_camName.setText(camName)


    @err_catcher(name=__name__)
    def setStateColor(self, status):
        if status == "ok":
            statusColor = COLOR_GREEN
        elif status == "warning":
            statusColor = COLOR_ORANGE
        elif status == "error":
            statusColor = COLOR_RED
        else:
            statusColor = COLOR_BLACK

        self.statusColor = statusColor
        self.stateManager.tw_import.repaint()


    @err_catcher(name=__name__)
    def updateUi(self):
        self.updateCamName()

        versions = self.checkLatestVersion()

        if not versions:
            logger.debug("Skipped setting Latest Version Status")
            return

        if versions:
            curVersion, latestVersion = versions
        else:
            curVersion = latestVersion = ""

        if curVersion.get("version") == "master":
            filepath = self.getImportPath()
            curVersionName = self.getMasterVersionLabel(filepath)
        else:
            curVersionName = curVersion.get("version")

        if latestVersion.get("version") == "master":
            filepath = latestVersion["path"]
            latestVersionName = self.getMasterVersionLabel(filepath)
        else:
            latestVersionName = latestVersion.get("version")

        self.l_curVersion.setText(curVersionName or "-")
        self.l_latestVersion.setText(latestVersionName or "-")

        self.stateStatus = "error"

        if self.chb_autoUpdate.isChecked():
            if curVersionName and latestVersionName and curVersionName != latestVersionName:
                self.importLatest(refreshUi=False, selectedStates=False)

            if latestVersionName:
                self.stateStatus = "ok"
        else:
            useSS = getattr(self.core.appPlugin, "colorButtonWithStyleSheet", False)

            if (
                curVersionName
                and latestVersionName
                and curVersionName != latestVersionName
                and not curVersionName.startswith("master")
            ):
                self.stateStatus = "warning"
                if useSS:
                    self.b_importLatest.setStyleSheet(
                        "QPushButton { background-color: rgb(200,100,0); }"
                    )
                else:
                    self.b_importLatest.setPalette(self.updatePalette)
            else:
                if curVersionName and latestVersionName:
                    self.stateStatus = "ok"

                if useSS:
                    self.b_importLatest.setStyleSheet(
                        "QPushButton { background-color: rgb(0, 130, 0); }"
                    )
                else:
                    self.b_importLatest.setPalette(self.oldPalette)

        self.nameChanged()
        self.setStateColor(self.stateStatus)

        getattr(self.core.appPlugin, "sm_import_updateUi", lambda x: None)(self)

        self.stateManager.saveImports()
        self.stateManager.saveStatesToScene()



    #########################
    #                       #
    #         DATA          #
    #                       #
    #########################


    @err_catcher(name=__name__)
    def loadData(self, data):
        self.importData = data

        if "statename" in data:
            self.e_name.setText(data["statename"])
        if "statemode" in data:
            self.setStateMode(data["statemode"])
        if "shotUID" in data:
            self.shotUUID = data["shotUID"]
        if "taskname" in data:
            self.taskName = data["taskname"]
        if "setname" in data:
            self.setName = data["setname"]
        if "autoUpdate" in data:
            checked = eval(data["autoUpdate"])
            self.chb_autoUpdate.setChecked(checked)
            self.autoUpdateChanged(checked)

        if "filepath" in data:
            data["filepath"] = getattr(
                self.core.appPlugin, "sm_import_fixImportPath", lambda x: x
            )(data["filepath"])
            self.setImportPath(data["filepath"])

        self.core.callback("onStateSettingsLoaded", self, data)


    @err_catcher(name=__name__)
    def checkLatestVersion(self):
        try:
            path = self.getImportPath()

            curVerData = {"version": self.importData["version"], "path": path}

            latestVerDict = self.getLatestVersion(self.importData, includeMaster=True)

            lastestVerName = latestVerDict["version"]
            lastestVerPath = latestVerDict["path"]

            if latestVerDict:
                latestVersionData = {"version": lastestVerName, "path": lastestVerPath}
            else:
                latestVersionData = {}
            
            #   Sets Tooltips
            curVerPath = curVerData["path"]
            self.l_text_Current.setToolTip(curVerPath)
            self.l_curVersion.setToolTip(curVerPath)

            latestVerPath = latestVersionData["path"]
            self.l_text_Latest.setToolTip(latestVerPath)
            self.l_latestVersion.setToolTip(latestVerPath)

            return curVerData, latestVersionData
        
        except:
            logger.debug("ERROR:  Unable to get Latest Version.")
            return None


    @err_catcher(name=__name__)
    def preDelete(self, item):
        self.core.popup("NOTE: At this time, Shots cannot be deleted from SynthEyes")

        # if not self.core.uiAvailable:
        #     action = "Yes"
        # else:
        #     action = "No"
          
        # text = "Do you want to Delete the Shot?"
        # action = self.core.popupQuestion(text, title="Delete Shot", parent=self.stateManager)

        # if action == "Yes":
        #     self.synthEyes.Begin()

        #     shots = self.synthEyes.Shots()

        #     self.core.popup(f"shots:  {shots}")							#	TESTING

        #     #   Delete each tool
        #     for shot in shots:

        #         self.core.popup(f"STATE ID:  {str(self.shotUUID)}\n"
        #                         f"SHOT ID: {str(shot.UniqID())}")							#	TESTING
        #         self.core.popup(f"match:  :  {str(self.shotUUID) == str(shot.UniqID())}")							#	TESTING

        #         if shot.uniqueID == self.shotUUID:
        #             self.synthEyes.Delete(shot)

        #     self.synthEyes.Accept("Delete Shot")
               

    @err_catcher(name=__name__)
    def getStateProps(self):
        self.importData["statename"] = self.e_name.text()
        self.importData["statemode"] = self.stateMode
        self.importData["shotUID"] = self.shotUUID
        self.importData["filepath"] = self.getImportPath()
        self.importData["autoUpdate"] = str(self.chb_autoUpdate.isChecked())
        self.importData["taskname"] = self.taskName

        return self.importData
    

    @err_catcher(name=__name__)
    def addShot(self, imagePath, versionData):
        mode = self.synthFuncts.addShot_mode
        result = self.synthFuncts.sm_addShot(self, mode, imagePath, versionData)

        return result
    

    @err_catcher(name=__name__)
    def changeShotImages(self, baseFile, versionData):
        baseName, extension = os.path.splitext(baseFile)
        ext = extension.lower()

        if ext not in self.core.media.supportedFormats:
            logger.warning(f"ERROR: Filetype {ext} in not supported")
            self.core.popup(f"ERROR: Filetype {ext} in not supported")
            return

        if extension in self.core.media.videoFormats:
            frameCount = self.core.media.getVideoDuration(baseFile)

        else:
            mediaFiles = self.core.mediaProducts.getFilesFromContext(versionData)
            validFiles = self.core.media.filterValidMediaFiles(mediaFiles)

            if validFiles:
                baseFile = validFiles[0]
                seqFiles = self.core.media.detectSequence(validFiles, baseFile=baseFile)

                start, end = self.core.media.getFrameRangeFromSequence(seqFiles, baseFile=baseFile)
                frameCount = end - start

        verStr = versionData.get("version")

        camName = self.e_camName.text()
        shot = self.synthFuncts.getShotFromCamName(camName)

        result = self.synthFuncts.sm_changeShotImages(self, shot, baseFile, verStr, frameCount)

        return result



    #########################
    #                       #
    #        CLASSES        #
    #                       #
    #########################


class ReadMediaDialog(QDialog):

    mediaSelected = Signal(object)

    def __init__(self, state, core):
        super(ReadMediaDialog, self).__init__()
        self.state = state
        self.stateManager = self.state.stateManager
        self.synthFuncts = self.state.synthFuncts
        self.core = core

        self.isValid = False
        self.setupUi()


    @err_catcher(name=__name__)
    def setupUi(self):
        title = "Select Media"
        self.setWindowTitle(title)
        self.core.parentWindow(self)

        import MediaBrowser
        self.w_browser = MediaBrowser.MediaBrowser(core=self.core)
        self.w_browser.headerHeightSet = True

        ##   Disconnect native function of showing versionInfo, and connect to import the version
        #   This is disabled unless the main code gets something connected to the ID table list widget
        # self.w_browser.tw_identifier.itemDoubleClicked.disconnect()
        self.w_browser.tw_identifier.itemDoubleClicked.connect(self.ident_dblClk)
        self.w_browser.lw_version.itemDoubleClicked.disconnect()
        self.w_browser.lw_version.itemDoubleClicked.connect(self.ver_dblClk)

        #   Disconnect native right-click-list and connect custom
        self.w_browser.tw_identifier.customContextMenuRequested.disconnect()
        # self.w_browser.tw_identifier.customContextMenuRequested.connect(self.customRclList)

        #   Create main window
        self.lo_main = QVBoxLayout()
        self.setLayout(self.lo_main)

        #   Create bottom layout
        self.lo_bottom = QHBoxLayout()

        #   Add instructions label text to bottom
        instructionsText = ("      Double-click Identifier to Import Latest Version      --      "
                            "Double-click Version to Load Version into State")
        l_instructions = QLabel(instructionsText)

        #   Add button box
        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Import Selected", QDialogButtonBox.AcceptRole)
        ##  vvvvv    Disabled until functions added  vvvvvvvv    ##
        # self.bb_main.addButton("Import Custom", QDialogButtonBox.AcceptRole)
        # self.bb_main.addButton("Open Project Browser", QDialogButtonBox.AcceptRole)
        ##  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^   ##
        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.bb_main.clicked.connect(self.buttonClicked)

        # Add widgets to the bottom layout
        self.lo_bottom.addWidget(l_instructions)
        self.lo_bottom.addStretch()  # Expanding spacer
        self.lo_bottom.addWidget(self.bb_main)

        #   Add main Browser to window
        self.lo_main.addWidget(self.w_browser)
        # Add bottom layout to window
        self.lo_main.addLayout(self.lo_bottom)

        tip = ("Double-click Identifier to Load\n"
               "and Import the Latest Version.")
        self.w_browser.tw_identifier.setToolTip(tip)

        tip = ("Double-click Version to Load\n"
               "the Version into the State.")
        self.w_browser.lw_version.setToolTip(tip)

        tip = ("Single-selection:  load the selected version into the State.")
        self.bb_main.setToolTip(tip)


    #   Handles clicked buttons
    @err_catcher(name=__name__)
    def buttonClicked(self, button):
        if button == "select" or button.text() == "Import Selected":
            self.handelImportButton()
        elif button.text() == "Import Custom":
            self.core.popup("Not Yet Implemented")                                      #    TESTING
        elif button.text() == "Open Project Browser":                                   #   TODO
            self.reject()
            self.openProjectBrowser()
        elif button.text() == "Cancel":
            self.reject()  # Close the dialog with no selection
        else:
            self.reject()  # Close the dialog with no selection


    #   Handles if the Import Selected button clicked
    def handelImportButton(self):
        selectedItems = self.w_browser.tw_identifier.selectedItems()

        if len(selectedItems) == 0:
            self.core.popup("No Items Selected")

        if len(selectedItems) == 1:
            data = self.w_browser.getCurrentSource()
            if not data:
                data = self.w_browser.getCurrentAOV()
                if not data:
                    data = self.w_browser.getCurrentVersion()
                    if not data:
                        data = self.w_browser.getCurrentIdentifier()

            if not data:
                msg = "Invalid version selected."
                self.core.popup(msg, parent=self)
                return
            
            selResult = ["version", data]

            self.mediaSelected.emit(selResult)
            self.accept()

        # elif len(selectedItems) > 1:
        #     self.handleRclImport(selectedItems)


    #   Handle import from custom RCL
    # @err_catcher(name=__name__)
    # def handleRclImport(self, selectedItems):
    #     #   Close Dialogue
    #     self.reject()

    #     #   If single item, import directly in this state
    #     if len(selectedItems) == 1:
    #         self.ident_dblClk(selectedItems[0])
    #     #   If multiple items, call the import through the main plugin
    #     elif len(selectedItems) > 1:
    #         for item in selectedItems:
    #             iData = item.data(0, Qt.UserRole)
    #             self.fuseFuncts.addImportState(self.stateManager, "Image_Import", useUi=False, settings=iData)
    #     else:
    #         logger.debug("No Media Items Selected")


    #   Sends data back to the main code to import the latest version
    @err_catcher(name=__name__)
    def ident_dblClk(self, item, column=None):
        #   Get Item Data
        data = item.data(0, Qt.UserRole)

        #   Return if No Data or is a Group (folder)
        if not data or data.get("isGroup") is True:
            return

        selResult = ["identifier", item.data(0, Qt.UserRole)]

        self.mediaSelected.emit(selResult)
        self.accept() 


    #   Sends data back to main code to populate the version
    @err_catcher(name=__name__)
    def ver_dblClk(self, item):
        data = self.w_browser.getCurrentSource()

        if not data:
            data = self.w_browser.getCurrentAOV()
            if not data:
                data = self.w_browser.getCurrentVersion()
                if not data:
                    data = self.w_browser.getCurrentIdentifier()

        if not data:
            msg = "Invalid version selected."
            self.core.popup(msg, parent=self)
            return
        
        selResult = ["version", data]

        self.mediaSelected.emit(selResult)
        self.accept()  


    @err_catcher(name=__name__)
    def openProjectBrowser(self):
        self.core.projectBrowser()
        if self.core.pb:
            self.core.pb.showTab("Libraries")

