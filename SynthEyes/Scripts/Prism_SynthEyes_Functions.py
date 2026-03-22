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
import sys
import platform
import logging
import ctypes
from ctypes import wintypes
import json
import zlib
import base64
import tempfile
import re
from contextlib import contextmanager
import time



PLUGINROOT = os.path.dirname(os.path.dirname(__file__))
PYTHONLIBS = os.path.join(PLUGINROOT, "PythonLibs", "Python313")

sys.path.append(PYTHONLIBS)
import mss


from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

if eval(os.getenv("PRISM_DEBUG", "False")):
    try:
        del sys.modules["widget_import_scenedata"]
    except:
        pass

from PrismUtils.Decorators import err_catcher as err_catcher


from Prism_SynthEyes_Listener import PrismCommsListener

from Synth_Formats import (SynthFormatNames,
                           SynthExrCompress,
                           SynthMovCodecs,
                           SynthMP4Codecs,
                           SynthMP4Qual,
                           SynthSubSample,
                           SynthInterp)


logger = logging.getLogger(__name__)



#   Helper to Convert Python Bool to SynthEyes 0/1
def boolToBit(boolInp: bool) -> int:
    return int(boolInp)



class Prism_SynthEyes_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.synthEyes = None
        self.importSyPy3()
        self.loadSettings()

        #   Socket Comms Bridge Thread
        self.Listener = PrismCommsListener(self, host="127.0.0.1", port=self.commsPort)
        self.Listener.bridge.commandReceived.connect(self.handleIncomingCommand)
        self.Listener.start()

        ##  CALLBACKS
        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self.plugin, priority=20)
        self.core.registerCallback("onStateManagerShow", self.onStateManagerShow, plugin=self.plugin, priority=20)
        self.core.registerCallback("onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self.plugin)
        self.core.registerCallback("onUserSettingsOpen", self.onUserSettingsOpen, plugin=self.plugin)

        ######  DISABLED - Does Not Improve Performance  #################################
        # self.core.registerCallback("prePublish", self.prePublish, plugin=self.plugin)
        # self.core.registerCallback("postPublish", self.postPublish, plugin=self.plugin)
        ##################################################################################

        ######   NOT USED AS OF NOW   ####################################################
        # self.core.registerCallback("onStateCreated", self.onStateCreated, plugin=self.plugin)
        # self.core.registerCallback("prePlayblast", self.prePlayblast, plugin=self.plugin)
        # self.core.registerCallback("onGenerateStateNameContext", self.onGenerateStateNameContext, plugin=self.plugin)
        ##################################################################################


        self.setupPrismMenu()


    @err_catcher(name=__name__)
    def startup(self, origin):
        if platform.system() == "Linux":
            origin.timer.stop()

            if "prism_project" in os.environ and os.path.exists(
                os.environ["prism_project"]
            ):
                curPrj = os.environ["prism_project"]
            else:
                curPrj = self.core.getConfig("globals", "current project")

            if curPrj != "":
                self.core.changeProject(curPrj)
            return False

        styleSheet = self.core.setActiveStyleSheet("SynthEyes")

        qapp = QApplication.instance()

        if qapp:
            for w in qapp.topLevelWidgets():
                w.setStyleSheet(styleSheet["css"])
                w.update()

        appIcon = QIcon(os.path.join(self.core.prismRoot, "Scripts", "UserInterfacesPrism", "p_tray.png"))
        qapp.setWindowIcon(appIcon)

        origin.timer.stop()
        origin.startAutosaveTimer()


    #   Load from Prism Settings    
    @err_catcher(name=__name__)
    def loadSettings(self):
        synthSettings = self.core.getConfig("SynthEyes")

        if synthSettings:
            self.commsPort = int(synthSettings["commsPort"])
            logger.debug("Loaded Settings")

        else:
            logger.warning("SynthEyes Settings Not Found, using Defaults.")
            self.commsPort = 50555

        #   Write Port to Temp File
        portFile = os.path.join(tempfile.gettempdir(), "prism_synth_port.txt")
        with open(portFile, "w") as f:
            f.write(str(self.commsPort))


    ##########################################################
    ##    TO BE ABLE TO CONNECT FROM SEPARATE PROCESSES     ##
    ## vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv ##
    # import random
    # import string

    # # Generate a Random port (49152 - 65535)
    # def getRandomPort(self):
    #     port = random.randint(49152, 65535)
    #     return port

    # # Generate a Random 12-character Alphanumeric String
    # def getRandomPin(self):
    #     chars = string.ascii_letters + string.digits
    #     pin = ''.join(random.choices(chars, k=12))
    #     return pin
    ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
    ##########################################################



    ###########################################
    ##         PRISM SYNTHEYES BRIDGE        ##
    ###########################################


    #   Parses the Integration Path and Imports SyPy3
    @err_catcher(name=__name__)
    def importSyPy3(self):
        if self.synthEyes:
            return self.synthEyes

        try:
            integrations = self.core.integration.getIntegrations()
            synthData = integrations.get("SynthEyes")

            if not synthData:
                raise RuntimeError("SynthEyes integration not found")

            synthPath = synthData[0]

            if not synthPath or not os.path.exists(synthPath):
                raise RuntimeError(f"Invalid SynthEyes path: {synthPath}")

            if synthPath not in sys.path:
                sys.path.append(synthPath)

            import SyPy3

            self.synthEyes = SyPy3.SyLevel()

            ##########################################################
            ##    TO BE ABLE TO CONNECT FROM SEPARATE PROCESSES     ##
            ## vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv ##
            # self.synth_port = self.getRandomPort()
            # self.synth_pin = self.getRandomPin()
            # self.synthEyes.OpenExisting(self.synth_port, self.synth_pin)
            ## ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ ##
            ##########################################################

            self.synthEyes.OpenExisting()

            logger.debug("Imported SynthEyes SyPy3")
            return self.synthEyes

        except Exception:
            logger.exception("importSyPy3 failed")
            self.synthEyes = None
            return None


    #   Queries Script Menu Items and Finds Prism Script ID's.
    #   Creates Custom Prism Menu in SynthEyes Main Toolbar.
    @err_catcher(name=__name__)
    def setupPrismMenu(self):
        #   Ensure Menus Exist
        self.synthEyes.InitMenu()

        #   Find SynthEyes Prism Script Menu
        mainMenu = self.synthEyes.MainMenu()
        scriptMenu = mainMenu.SubMenuByName("Script")
        prismScriptMenu = scriptMenu.SubMenuByName("Prism")

        if not prismScriptMenu:
            logger.warning(f"ERROR: Prism script menu not found")
            self.core.popup("ERROR:\n\n"
                            "Prism is unable to start.\n"
                            "The Prism Script menu cannot be found in\n"
                            "the SynthEyes script directory.\n"
                            "Try restarting Prism.")
            return
        
        #   Find SynthEyes Menu Action Numbers for Prism Scripts
        for item in range(prismScriptMenu.Count()):
            actID = prismScriptMenu.IDByPos(item)
            actName = prismScriptMenu.NameByPos(item)

            #   Add SynthyEyes Action ID's to Data Dict
            for entry in self.synthMenuData:
                if actName == entry["scriptName"]:
                    entry["actionID"] = actID
                    break

        #   Validate Discovered Prism Menu Items
        missing = [e["scriptName"] for e in self.synthMenuData if e["actionID"] is None]
        if missing:
            logger.warning(f"ERROR: Missing script actions: {missing}")

        #   Build Custom Prism Menu (skip if already exists)
        prismMenu = mainMenu.SubMenuByName("Prism")

        if not prismMenu.Exists():
            prismMenu = mainMenu.AddSubMenu(9, "Prism")

            for entry in sorted(self.synthMenuData, key=lambda x: x["menuPos"]):
                prismMenu.AddMenuItem(
                    entry["menuPos"],
                    entry["menuName"],
                    entry["actionID"]
                )

            self.synthEyes.Redraw()

        logger.debug("Prism Menu Setup Complete")


    #   Receives Signal from Listener Thread
    @err_catcher(name=__name__)
    def handleIncomingCommand(self, msg):
        command = msg.get("command")

        match command:
            case "saveVersion":
                self.saveVersion()

            case "saveComment":
                self.saveComment()

            case "open_ProjectBrowser":
                self.open_ProjectBrowser()

            case "open_StateManager":
                self.open_StateManager()

            case "open_PrismSettings":
                self.open_PrismSettings()



    #######################################
    ##             CALLBACKS             ##
    #######################################


    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        origin.setWindowIcon(QIcon(self.prismAppIcon))
        ss = self.core.getActiveStyleSheet()
        origin.setStyleSheet(ss["css"])


    @err_catcher(name=__name__)
    def onUserSettingsOpen(self, origin):
        origin.setWindowIcon(QIcon(self.prismAppIcon))
        ss = self.core.getActiveStyleSheet()
        origin.setStyleSheet(ss["css"])


    @err_catcher(name=__name__)
    def onStateManagerOpen(self, origin):
        origin.setWindowIcon(QIcon(self.prismAppIcon))
        ss = self.core.getActiveStyleSheet()
        origin.setStyleSheet(ss["css"])

        origin.b_showImportStates.setStyleSheet("padding-left: 1px;padding-right: 1px;")
        origin.b_showExportStates.setStyleSheet("padding-left: 1px;padding-right: 1px;")
        origin.b_createImport.setMinimumWidth(70 * self.core.uiScaleFactor)
        origin.b_createImport.setMaximumWidth(70 * self.core.uiScaleFactor)
        origin.b_createImport.setMinimumHeight(0)
        origin.b_createImport.setMaximumHeight(500 * self.core.uiScaleFactor)
        origin.b_shotCam.setMinimumHeight(0)
        origin.b_shotCam.setMaximumHeight(50 * self.core.uiScaleFactor)
        origin.b_showImportStates.setMinimumWidth(30 * self.core.uiScaleFactor)
        origin.b_showImportStates.setMaximumWidth(30 * self.core.uiScaleFactor)
        origin.b_showExportStates.setMinimumWidth(30 * self.core.uiScaleFactor)
        origin.b_showExportStates.setMaximumWidth(30 * self.core.uiScaleFactor)
        origin.b_createExport.setMinimumWidth(70 * self.core.uiScaleFactor)
        origin.b_createExport.setMaximumWidth(70 * self.core.uiScaleFactor)
        origin.b_createRender.setMinimumWidth(70 * self.core.uiScaleFactor)
        origin.b_createRender.setMaximumWidth(70 * self.core.uiScaleFactor)
        origin.b_createPlayblast.setMinimumWidth(80 * self.core.uiScaleFactor)
        origin.b_createPlayblast.setMaximumWidth(80 * self.core.uiScaleFactor)
        origin.b_description.setMinimumWidth(35 * self.core.uiScaleFactor)
        origin.b_description.setMaximumWidth(35 * self.core.uiScaleFactor)
        origin.b_preview.setMinimumWidth(35 * self.core.uiScaleFactor)
        origin.b_preview.setMaximumWidth(35 * self.core.uiScaleFactor)

        #	Remove Native Buttons
        origin.b_createImport.deleteLater()
        origin.b_createExport.deleteLater()
        origin.b_shotCam.deleteLater()

        #	Create New Scene Button
        origin.b_createShot = QPushButton(origin.w_CreateImports)
        origin.b_createShot.setObjectName("b_createShot")
        origin.b_createShot.setText("New Scene")
        origin.horizontalLayout_3.insertWidget(0, origin.b_createShot)
        origin.b_createShot.clicked.connect(lambda: self.addShot(origin, "create"))

        #   Add Shot Button
        origin.b_addShot = QPushButton(origin.w_CreateImports)
        origin.b_addShot.setObjectName("b_addShot")
        origin.b_addShot.setText("Add Shot")
        origin.horizontalLayout_3.insertWidget(1, origin.b_addShot)
        origin.b_addShot.clicked.connect(lambda: self.addShot(origin, "add"))

        #   Add Mesh Button
        origin.b_addMesh = QPushButton(origin.w_CreateImports)
        origin.b_addMesh.setObjectName("b_addMesh")
        origin.b_addMesh.setText("Mesh")
        origin.horizontalLayout_3.insertWidget(2, origin.b_addMesh)
        origin.b_addMesh.clicked.connect(lambda: origin.createState("Synth_ImportMesh"))

        # Export Scene Button
        origin.b_exportScene = QPushButton(origin.w_CreateExports)
        origin.b_exportScene.setObjectName("b_exportScene")
        origin.b_exportScene.setText("Export Scene")
        origin.b_exportScene.setMaximumSize(QSize(150, 16777215))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        origin.b_exportScene.setSizePolicy(sizePolicy)
        origin.horizontalLayout_4.insertWidget(0, origin.b_exportScene)
        origin.b_exportScene.clicked.connect(lambda: origin.createState("Synth_SceneExport"))

        tip = ("Create New SynthEyes Scene.\n\n"
               "This will start an entirely new scene and import the images(s)\n"
               "This is the same as the 'New' button in the SynthEyes UI.\n\n"
               "Please note this will overwrite any shots in the existing scene.")
        origin.b_createShot.setToolTip(tip)

        tip = ("This will add an additional Shot and Camera to the existing Scene.\n\n"
               "This is the same as the 'Add Shot' button in SynthEyes.")
        origin.b_addShot.setToolTip(tip)

        tip = "Import a 3D Mesh object into the Scene."
        origin.b_addMesh.setToolTip(tip)

        tip = "Export the SynthEyes Scene to the desired format."
        origin.b_exportScene.setToolTip(tip)

        tip = ("Create the Desired Render State:\n\n"
               "ImageRender - Same as SynthEyes 'Save Sequence'\n"
               "STMap Render - Same as SynthEyes 'Write Distortion Maps")
        origin.b_createRender.setToolTip(tip)

        tip = ("Creates a Playblast State.\n\n"
               "This uses the SynthEyes 'Preview Movie' from\n"
               "the Perspective View.")
        origin.b_createPlayblast.setToolTip(tip)

        #   Remove Unused States Except for SynthStates
        for state in list(origin.stateTypes.keys()):
            if state not in self.synthStates:
                try:
                    del origin.stateTypes[state]
                except Exception:
                    logger.debug(f"Unable to remove default state: {state}")


    @err_catcher(name=__name__)
    def onStateManagerShow(self, origin):
        #   Display Import List (Prism closes the list by default)
        origin.gb_import.setChecked(True)



    ########################################################################
    ##               DISABLED - DOES NOT INCREASE PERFORMANCE             ##
    # @err_catcher(name=__name__)
    # def prePublish(self, origin):
    #     self.publishData = {"orig_prefetchEnabled": self.getPrefetch()}
    #     self.setPrefetch(False)
    # @err_catcher(name=__name__)
    # def postPublish(self, origin, pubType, result={}):
    #     self.setPrefetch(self.publishData["orig_prefetchEnabled"])
    #########################################################################




    ###################################################
    ##       Called From SynthEyes Prism Tools       ##   
    ###################################################
    

    @err_catcher(name=__name__)
    def saveVersion(self):
        self.core.saveScene()

    @err_catcher(name=__name__)
    def saveComment(self):
        self.core.saveWithComment()

    @err_catcher(name=__name__)
    def open_ProjectBrowser(self):
        self.core.projectBrowser()

    @err_catcher(name=__name__)
    def open_StateManager(self):
        self.core.stateManager()

    @err_catcher(name=__name__)
    def open_PrismSettings(self):
        self.core.prismSettings()



    @err_catcher(name=__name__)
    def testOne(self):
        self.core.popup("IN TEST ONE")							#	TESTING


    @err_catcher(name=__name__)
    def testTwo(self):
        self.core.popup("IN TEST TWO")							#	TESTING

        # for action in self.synthEyes.Actions():
        #     print(f"NAME: {action}\n"
        #           f"{dir(action)}\n\n"
        #           "********************")
        # return



    ###################################################
    ##                  Synth Stuff                  ##
    ###################################################


    #   Context Wrapper for SynthEyes Undo Blocks
    @contextmanager
    def UNDO_BLOCK(self, undoName:str) -> None:
        '''Context Manager for SynthEyes Undo blocks.\n
           This takes the place of a .Begin()->.Accept()\n
           block.\n\n
           example:\n
               with self.UNDO_BLOCK("Create Mesh):
                   self.synthEyes.CreateNew("mesh)'''
        
        startedHere = False

        if not self.synthEyes.InUndo():
            self.synthEyes.Begin()
            startedHere = True

        try:
            yield

        except Exception as e:
            logger.warning(f"UNDO FAILED: {undoName} - {e}")

            if startedHere:
                try:
                    self.synthEyes.Cancel()
                except Exception as cancel_err:
                    logger.critical(f"UNDO CANCEL FAILED: {cancel_err}")
            raise

        else:
            if startedHere:
                self.synthEyes.Accept(undoName)


    #   Returns SynthEyes Version
    @err_catcher(name=__name__)
    def getAppVersion(self, origin) -> str:
        return self.synthEyes.Version()


    #   Returns Bool of Prefetch is Enabled in SynthEyes
    @err_catcher(name=__name__)
    def getPrefetch(self) -> bool:
        try:
            self.synthEyes.InitMenu()
            shotMenu = self.synthEyes.TopMenu("Shot")

            if shotMenu:
                menu_idx = shotMenu.PosByName("Enable Prefetch")
                isChecked_int = shotMenu.IsCheckedByPos(menu_idx)

            logger.debug("Got the Prefetch Enabled State")

            return bool(isChecked_int == 1)
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to get the Prefetch State.: {e}")
            return False
        

    #   Set the SynthEyes Prefetch Enabled/Disabled
    @err_catcher(name=__name__)
    def setPrefetch(self, enable:bool) -> None:
        isEnabled = self.getPrefetch()

        try:
            if enable:
                if not isEnabled:
                    self.synthEyes.PerformActionByNameAndContinue("Enable Prefetch")
                
            else:
                if isEnabled:
                    self.synthEyes.PerformActionByNameAndContinue("Enable Prefetch")

        except Exception as e:
            logger.warning(f"ERROR: Unable to Set Prefetch State: {e}")


    ##  FRAMES  ##

    @err_catcher(name=__name__)
    def getCurrentFrame(self) -> int:
        try:
            currentFrame = self.synthEyes.Frame()
            return currentFrame + 1
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Current Frame from SynthEyes: {e}")
            return None
        

    @err_catcher(name=__name__)
    def setCurrentFrame(self, frame:int) -> None:
        try:
            self.synthEyes.SetFrame(frame - 1)
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Set Current Frame to SynthEyes: {e}")
            return None


    @err_catcher(name=__name__)
    def getFrameRange(self, origin, shot:object=None) -> tuple[int, int]:
        try:
            if not shot:
                shot = self.synthEyes.Shots()[0]

            start = shot.Get("start") + 1
            end = shot.Get("stop") + 1
            return[start, end]
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Framerange from SynthEyes: {e}")
            return [None, None]


    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame:int, endFrame:int, shot:object=None) -> None:
        try:
            if not shot:
                shot = self.synthEyes.Shots()[0]

            with self.UNDO_BLOCK("Set Framerange"):
                shot.Set("start", startFrame - 1)
                shot.Set("stop", endFrame - 1)
                self.synthEyes.SetAnimStart(startFrame)
                self.synthEyes.SetAnimEnd(endFrame)
            
            logger.debug("Updated Framerange in SynthEyes")

        except Exception as e:
            logger.warning(f"ERROR: Unable to Set Framerange in SynthEyes: {e}")


    @err_catcher(name=__name__)
    def getShotFrameCount(self, shot:object) -> int:
        try:
            return shot.Get("frameCount")
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Shot's Frame Count: {e}")
            return None
        

    @err_catcher(name=__name__)
    def setShotFrameCount(self, shot:object, frameCount:int) -> bool:
        try:
            result = shot.Set("frameCount", frameCount)
            return result
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Set Shot's Frame Count: {e}")
            return False


    ##  OBJECTS  ##

    @err_catcher(name=__name__)
    def getObjByUUID(self, objType:str, uuid:str) -> object:
        try:
            match objType:
                case "shot":
                    objs = self.synthEyes.Shots()
                case "object":
                    objs = self.synthEyes.Objects()
                case "camera":
                    objs = self.synthEyes.Cameras()
                case "mesh":
                    objs = self.synthEyes.Meshes()
                case "light":
                    objs = self.synthEyes.Lights()
                case "extra":
                    objs = self.synthEyes.Extras()

            for obj in objs:
                if obj.UniqID() == uuid:
                    return obj

        except Exception as e:
            logger.warning(f"ERROR: Unable to get {objType} - {uuid}")
            return None


    @err_catcher(name=__name__)
    def deleteObjByUUID(self, objType:str, uuid:str) -> bool:
        try:
            match objType:
                case "shot":
                    objs = self.synthEyes.Shots()
                case "object":
                    objs = self.synthEyes.Objects()
                case "camera":
                    objs = self.synthEyes.Cameras()
                case "mesh":
                    objs = self.synthEyes.Meshes()
                case "light":
                    objs = self.synthEyes.Lights()
                case "extra":
                    objs = self.synthEyes.Extras()

            for obj in objs:
                if obj.UniqID() == uuid:
                    self.synthEyes.Delete(obj)
                    break

            return True

        except Exception as e:
            logger.warning(f"ERROR: Unable to delete {objType} - {uuid}\n{e}")
            return False
    

    @err_catcher(name=__name__)
    def getObjName(self, origin, obj:object) -> str:
        return obj.Name()


    @err_catcher(name=__name__)
    def setObjName(self, synthObj:object, objName:str) -> bool:
        try:
            synthObj.SetName(objName)
            return True

        except Exception as e:
            logger.warning(f"ERROR:  Unable to set Synth Object's Name: {e}")
            return False


    ##  CAMERAS  ##

    @err_catcher(name=__name__)
    def getCamNodes(self, origin=None, cur:bool=False) -> list[object]:
        return self.synthEyes.Cameras()
    

    @err_catcher(name=__name__)
    def getCamName(self, origin, camera:object) -> str:
        return camera.Name()
    
    
    @err_catcher(name=__name__)
    def getCamFromName(self, camName:str) -> object:
        cameras = self.getCamNodes()
        for cam in cameras:
            if cam.Name() == camName:
                return cam
            
        return None
    

    @err_catcher(name=__name__)
    def getCamFromShot(self, shot:object) -> object:
        try:
            return shot.Get("cam")
        
        except Exception as e:
            logger.warning(f"ERROR: Uanble to get Camera from Hot: {e}")
            return None
            

    @err_catcher(name=__name__)
    def getCamFromShotUUID(self, shotUUID:str) -> object:
        shot = self.getObjByUUID("shot", shotUUID)
        if shot:
            return shot.cam
        
        return None


    ##  SHOTS  ##

    @err_catcher(name=__name__)
    def getShotFromCamera(self, shotObj:object) -> object:
        try:
            return shotObj.cam
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Camera from Shot: {e}")
            return None
    

    @err_catcher(name=__name__)
    def getShotFromCamName(self, camName:str) -> object:
        camera = self.getCamFromName(camName)
        if camera:
            return camera.shot
        
        return None
    

    @err_catcher(name=__name__)
    def getShotHasDistort(self, camName:str) -> bool:
        try:
            camera = self.getCamFromName(camName)

            return bool(camera.Get("lensHasDistortion"))
    
        except Exception as e:
            logger.warning(f"ERROR: Unable to Resolve if Lens has Distortion: {e}")
            return False
    

    @err_catcher(name=__name__)
    def getShotHasLensWorkflow(self, camName:str) -> bool:
        try:
            shot = self.getShotFromCamName(camName)
            lensWorkflow_raw = shot.Get("lensflowState")

            if not lensWorkflow_raw:
                return False

            lensWorkflow_json = lensWorkflow_raw.replace("JSON:", "", 1)
            lensWorkflow_data = json.loads(lensWorkflow_json)
            workflow_num = lensWorkflow_data["workflow"]

            return True if int(workflow_num) > 0 else False

        except Exception as e:
            logger.warning(f"ERROR: Unable to Resolve Lens Workflow: {e}")
            return False


    @err_catcher(name=__name__)
    def getShotPreProcessor(self, shotObj:object) -> object:
        try:
            return shotObj.live
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Shot's Image Preprocessor: {e}")
            return None
        

    @err_catcher(name=__name__)
    def changeShotImages(self, shot:object, newPath:str, frameCount:int) -> bool:
        try:
            #   Change Image Path Name
            shot.Set("nm", newPath)

        except Exception as e:
            logger.warning(f"ERROR: Unable to Change Short Images: {e}")
            return False

        #   Update Frame Count
        self.setShotFrameCount(shot, frameCount)
        
        #   Flush Old Image Cache
        shot.Call("Flush")

        return True
        

    @err_catcher(name=__name__)
    def getOutputRez(self, shot:object) -> float:
        try:
            pProc = self.getShotPreProcessor(shot)
            if not pProc:
                return 1.0
            
            return pProc.Get("subsample")
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Shot's Image Sampling: {e}")
            return 1.0
        

    @err_catcher(name=__name__)
    def setOutputRez(self, shot:object, scaleStr:str=None, scaleCode:float=None) -> None:
        try:
            pProc = self.getShotPreProcessor(shot)
            if not pProc:
                return

            #   Get SynthEyes Settings Code
            if scaleStr:
                scaleCode = SynthSubSample[scaleStr]

            #   Set Subsample Value        
            pProc.Set("subsample", scaleCode)

        except Exception as e:
            logger.warning(f"ERROR: Unable to Set Shot's Image Sampling: {e}")
            return
        

    @err_catcher(name=__name__)
    def getOutputSampleFilter(self, shot:object) -> float:
        try:
            pProc = self.getShotPreProcessor(shot)
            if not pProc:
                return 0.0
            
            return pProc.Get("interpolation")
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Shot's Sampling Filter: {e}")
            return 0.0
        

    @err_catcher(name=__name__)
    def setOutputSampleFilter(self, shot:object, filterStr:str=None, filterCode:float=None) -> None:
        pProc = self.getShotPreProcessor(shot)
        if not pProc:
            logger.warning("ERROR: Unable to Get Shot's Image Preprocessor.")
            return
        
        try:
            #   Get SynthEyes Settings Code
            if filterStr:
                filterCode = SynthInterp[filterStr]

            #   Set Subsample Filter
            pProc.Set("interpolation", filterCode)
            
        except Exception as e:
            logger.warning(f"ERROR: Unable to Set Shot's Sampling Filter: {e}")
            return



    ###################################################
    ##                 File Handling                 ##   
    ###################################################


    #   Returns Current SynthEyes File Name/Path
    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin=None, path=True):
        currentFileName = self.synthEyes.SNIFileName()

        if not path:
            currentFileName = os.path.basename(currentFileName)

        return currentFileName
    

    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        return self.sceneFormats[0]


    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        if not filepath.endswith(".sni"):
            return False
        
        filepath = os.path.normpath(filepath)

        try:
            self.synthEyes.OpenSNI(filepath)
            logger.debug(f"Opened Scene: {filepath}")
            return True
        
        except Exception as e:
            logger.warning(f"ERROR:  Unable to open Scenefile: {filepath}\n{e}")
            return False
            

    #   Saves .SNI to New Passed Filepath
    @err_catcher(name=__name__)
    def saveScene(self, origin=None, filepath=None, details={}):
        try:
            if filepath:
                filepath = os.path.normpath(filepath)

                #   Set Filename to Scene
                self.synthEyes.SetSNIFileName(filepath)

            #   Find Save Menu Object
            self.synthEyes.InitMenu()
            fileMenu = self.synthEyes.TopMenu("File")
            menu_idx = fileMenu.PosByName("Save")
            menu_id = fileMenu.IDByPos(menu_idx)

            #   Execute Save Action
            self.synthEyes.PerformActionByIDAndContinue(menu_id)

            return True
        
        except:
            return False


    @err_catcher(name=__name__)
    def copySceneFile(self, core, origFile, targetFile, mode=None):

        self.core.popup(f"copy\n\n"
                        f"core: {core}"
                        f"origFile: {origFile}"
                        f"targetFile: {targetFile}"
                        f"mode: {mode}")							#	TESTING
        

    #   Finds Opsn SynthEyes Window and Captures Screenshot
    @err_catcher(name=__name__)
    def captureViewportThumbnail(self):
        #   Get Current Open Windows
        user32 = ctypes.windll.user32
        EnumWindows = user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
        GetWindowText = user32.GetWindowTextW
        GetWindowTextLength = user32.GetWindowTextLengthW
        IsWindowVisible = user32.IsWindowVisible

        #   Builds the Window Title Prefix from Scene Name
        sceneName = self.getCurrentFileName(path=False)
        sceneName = os.path.splitext(sceneName)[0]
        winPrefix = f"{sceneName} - SynthEyes"

        target_hwnd = None

        #   Helper to Search Window Names
        def foreach_window(hwnd, lParam):
            if IsWindowVisible(hwnd):
                length = GetWindowTextLength(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    GetWindowText(hwnd, buff, length + 1)
                    title = buff.value
                    if title.startswith(winPrefix):
                        nonlocal target_hwnd
                        target_hwnd = hwnd
                        return False
            return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)

        if not target_hwnd:
            logger.warning("ERROR: Thumbnail generation failed.  Could not find SynthEyes Window")
            return None

        rect = wintypes.RECT()
        user32.GetWindowRect(target_hwnd, ctypes.byref(rect))
        left, top = rect.left, rect.top
        width = rect.right - rect.left
        height = rect.bottom - rect.top

        with mss.mss() as sct:
            monitor = {"left": left, "top": top, "width": width, "height": height}
            sct_img = sct.grab(monitor)

            # mss returns BGRA
            img = QImage(sct_img.rgb, sct_img.width, sct_img.height, QImage.Format_RGB888).copy()
            pixmap = QPixmap.fromImage(img)

        return pixmap
    


    #######################################
    ##             Helpers               ##   
    #######################################


    #   Finds and Changes the Version Suffix (_v001, _v002, _master)
    @err_catcher(name=__name__)
    def updateNameVersion(self, currentName:str, newVerStr:str) -> str:
        verPadding = self.core.versionPadding

        pattern = rf"(_v\d{{{verPadding}}}|_master)"
        matches = list(re.finditer(pattern, currentName))

        if matches and newVerStr:
            last_match = matches[-1]
            start, end = last_match.span()

            newName = (
                currentName[:start]
                + f"_{newVerStr}"
                + currentName[end:]
            )

            return newName

        else:
            return None
        

    #   Returns Str of Format Specific Render Settings
    #   (from Synth_Formats.py imports)
    @err_catcher(name=__name__)
    def getRenderOptsStr(self, rSettings):
        format = rSettings["format"]

        if format == ".exr":
            return SynthExrCompress[rSettings["exrCompress"]]
        
        elif format == ".mov":
            return SynthMovCodecs[rSettings["movCodec"]]
        
        elif format == ".mp4":
            return f"{SynthMP4Codecs[rSettings['mp4Codec']]} {SynthMP4Qual[rSettings['mp4Qual']]}"
        
        else:
            return None
    

    #   Waits in QtLoop Until Popup Window is Invalid
    @err_catcher(name=__name__)
    def waitForPopupClose(self, popup, timeout=600.0):
        start_time = time.time()
        loop = QEventLoop()

        def finish():
            if loop.isRunning():
                loop.quit()

        def check():
            try:
                if not popup or not popup.IsValid():
                    finish()
                    return

                if time.time() - start_time > timeout:
                    logger.warning("Preview render timed out")
                    finish()
                    return

                QTimer.singleShot(200, check)

            except Exception as e:
                logger.warning(f"Error during popup wait: {e}")
                finish()

        check()

        loop.exec_()



    #######################################
    ##               Shots               ##   
    #######################################
   

    #   Called from StateManager Button
    @err_catcher(name=__name__)
    def addShot(self, origin, mode):
        if mode == "create":
            question = ("Would you like to Create a New SynthEyes Scene?\n\n"
                        "This will Create a New Clean Scene and Import the Shot.")

        elif mode == "add":
            question = ("Would you like to Add an Additional Shot (Camera) to the\n"
                        "existing Scene?")
        else:
            return False
            
        title = "Create/Add Shot"

        result = self.core.popupQuestion(text=question, title=title)

        if result != "Yes":
            return False

        #   Call to Create the State Creation with Given Mode
        self.addShot_mode = mode
        origin.createState("Synth_AddShot")   


    #   Called from AddShot State Execute
    @err_catcher(name=__name__)
    def sm_addShot(self, origin, mode, shotFilepath, details=None):
        #   Creates New Scene
        if mode == "create":
            try:
                curr_SniName = self.synthEyes.SNIFileName()
                shot = self.synthEyes.NewSceneAndShot(shotFilepath, asp = 0.0)
                self.synthEyes.SetSNIFileName(curr_SniName)
                camSuffix = "SCENE"

            except Exception as e:
                logger.warning(f"ERROR: Unable to Create Scene Shot: {e}")
                return False
            
        #   Adds Additional Shot to Current Scene
        elif mode == "add":
            try:
                shot = self.synthEyes.AddShot(shotFilepath, asp = 0.0)
                camSuffix = "SHOT"

            except Exception as e:
                logger.warning(f"ERROR: Unable to Add Shot: {e}")
                return False

        if details:
            #   Renames Camera
            try:
                camName = f"CAMERA_{camSuffix}-{details['identifier']}_{details['version']}"
            
                for obj in shot.Objects():
                    if obj.Name().lower().startswith("camera"):
                        with self.UNDO_BLOCK("Rename Camera"):
                            self.setObjName(obj, camName)
                        break

            except Exception as e:
                logger.warning(f"ERROR: Unable to Rename Shot: {e}")

        self.synthEyes.Redraw()

        try:
            #   Find Edit Shot Menu Object
            self.synthEyes.InitMenu()
            shotMenu = self.synthEyes.TopMenu("Shot")
            menu_idx = shotMenu.PosByName("Edit Shot")
            menu_id = shotMenu.IDByPos(menu_idx)

            #   Execute Edit Shot Action
            self.synthEyes.PerformActionByIDAndContinue(menu_id)

        except Exception as e:
            logger.warning(f"ERROR: Unable to Call 'Edit Shot' Menu: {e}")

        return shot.UniqID()
    

    #   Called From AddShot State when Changing Version
    @err_catcher(name=__name__)
    def sm_changeShotImages(self, origin, shot, newPath, verStr, frameCount):
        #   Change Images in SynthEyes
        with self.UNDO_BLOCK("Change Shot Images"):
            result = self.changeShotImages(shot, newPath, frameCount)

        if result:
            #   Attempts to Rename Camera with New Version
            try:
                camera = self.getCamFromShot(shot)
                camName_curr = self.getCamName(self, camera)

                camName_new = self.updateNameVersion(camName_curr, verStr)
                if camName_new:
                    with self.UNDO_BLOCK("Rename Camera"):                    
                        self.setObjName(camera, camName_new)

            except Exception as e:
                logger.warning(f"Unable to Update Camera Version Name: {e}")
            
        self.synthEyes.Validate(shot)

        return result



    #######################################
    ##           Import Mesh             ##   
    #######################################


    #   Called from ImportMesh State Execute
    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName, data=None):
        fileName = os.path.splitext(os.path.basename(impFileName))
        ext = fileName[1].lower()

        if ext not in self.importFormats:
            self.core.popup(f"Format {ext} is not supported for SynthEyes Mesh Import.")
            return {"result": False, "doImport": doImport}
        
        filePath = os.path.normpath(impFileName)

        #   Get Existing Mesh
        mesh_orig = self.getObjByUUID("mesh", data["meshUUID"])

        ##   Update Existing Mesh
        if update and mesh_orig:
            #   Capture Original Mesh Data
            meshName_curr = self.getObjName(self, mesh_orig)
            meshTrans_orig = mesh_orig.trans

            with self.UNDO_BLOCK("Update Mesh"):
                #   Load Mesh from New Filepath
                mesh_orig.Call("ReadMesh", impFileName)
                #   Apply Original Transforms
                mesh_orig.Set("trans", meshTrans_orig)

            #   Change Mesh Name
            meshName_new = self.updateNameVersion(meshName_curr, data['version'])
            if not meshName_new:
                meshName_new = meshName_curr

            if meshName_new:
                with self.UNDO_BLOCK("Rename Mesh"):
                    self.setObjName(mesh_orig, meshName_new)

            result = mesh_orig.UniqID()
            doImport = True

        ##   Create New Mesh
        else:
            #   Create Mesh Name
            if data:
                try:
                    meshName = f"{data['product']}_{data['version']}"
                except:
                    pass
            else:
                meshName = fileName[0]

            with self.UNDO_BLOCK("Import Mesh"):
                #   Create New Mesh from Filepath
                scn = self.synthEyes.Scene()
                meshObj = scn.Call("ReadMesh", filePath)

            if not meshObj:
                return {"result": False, "doImport": False}

            with self.UNDO_BLOCK("Rename Mesh"):
                #   Set Mesh Name
                self.setObjName(meshObj, meshName)

            result = meshObj.UniqID()
            doImport = True

        return {"result": result, "doImport": doImport}
        

    @err_catcher(name=__name__)
    def sm_import_preDelete(self, origin, delData:dict):
        try:
            uuid = delData["meshUUID"]

            with self.UNDO_BLOCK("Delete Mesh"):
                self.deleteObjByUUID("mesh", uuid)

        except Exception as e:
            logger.warning(e)
        


    #######################################
    ##             Exporting             ##   
    #######################################


    #   Sanity Check Before State Execution
    @err_catcher(name=__name__)
    def sm_sceneExport_preExecute(self, origin, startFrame, endFrame):
        warnings = []

        cameras = self.getCamNodes()

        for camera in cameras:
            camName = camera.Name()

            #   Check if Shot Camera was Solved with Distortion
            hasDistor = self.getShotHasDistort(camName)

            #   Check if Shot Camera has had Lens Workflow Completed
            hasLensWorkflow = self.getShotHasLensWorkflow(camName)

            if hasDistor and not hasLensWorkflow:
                msg = (f"CAMERA   '{camName}':\n"
                    "                appears to have solved distortion,\n"
                    "                and the Lens Workflow script has not\n"
                    "                been completed.")
                warnings.append([msg, "", 2])

        return warnings
    
    @err_catcher(name=__name__)
    def sm_pre_sceneExport(self, origin, rSettings):
        shot = self.synthEyes.Shots()[0]

        #   Capture Original Settings
        orig_start, orig_end = self.getFrameRange(origin, shot)
        rSettings["orig_start"] = orig_start
        rSettings["orig_end"] = orig_end
        rSettings["orig_play_start"] = self.synthEyes.AnimStart()
        rSettings["orig_play_end"] = self.synthEyes.AnimEnd()
        rSettings["orig_currFrame"] = self.getCurrentFrame()

        #   Update Frame Range
        with self.UNDO_BLOCK("Set Framerange"):
            self.setFrameRange(origin, rSettings["startFrame"], rSettings["endFrame"], shot)

        return rSettings


    #   Called From SceneExport State Execute
    @err_catcher(name=__name__)
    def sm_sceneExport(self, origin, outputType, outputName, details=None):
        try:
            synthFormatType = SynthFormatNames[outputType]["synthName"]
            exportPath = os.path.normpath(outputName)

            self.synthEyes.Export(synthFormatType, exportPath)

            result = True

        except:
            return False

        if result:
            return outputName


    @err_catcher(name=__name__)
    def sm_post_sceneExport(self, origin, rSettings):
        shot = self.synthEyes.Shots()[0]

        #   Restore Frame Range
        with self.UNDO_BLOCK("Restore Framerange"):
            self.setFrameRange(origin, rSettings["orig_start"], rSettings["orig_end"], shot)
            self.synthEyes.SetAnimStart(rSettings["orig_play_start"])
            self.synthEyes.SetAnimEnd(rSettings["orig_play_end"])
            self.setCurrentFrame(rSettings["orig_currFrame"])

        self.synthEyes.Validate(shot)


    @err_catcher(name=__name__)
    def sm_export_preDelete(self, origin):
        pass



    #######################################
    ##             Rendering             ##   
    #######################################


    #   Sanity Check Before State Execution
    @err_catcher(name=__name__)
    def sm_render_preExecute(self, origin, rData):
        warnings = []

        camName = rData["currentCam"]

        #   Check if Shot Camera was Solved with Distortion
        hasDistor = self.getShotHasDistort(camName)

        #   Check if Shot Camera has had Lens Workflow Completed
        hasLensWorkflow = self.getShotHasLensWorkflow(camName)

        if hasDistor and not hasLensWorkflow:
            msg = (f"CAMERA   '{camName}':\n"
                   "             appears to have solved distortion,\n"
                   "             and the Lens Workflow script has not\n"
                   "             been completed.")
            warnings.append([msg, "", 2])

        return warnings
    

    #   Called Before Render to Capture Current Settings
    @err_catcher(name=__name__)
    def sm_render_preRender(self, origin, rSettings):
        shot = self.getShotFromCamName(rSettings["currentCam"])

        #   Capture Original Settings
        orig_start, orig_end = self.getFrameRange(origin, shot)
        rSettings["orig_start"] = orig_start
        rSettings["orig_end"] = orig_end
        rSettings["orig_currFrame"] = self.getCurrentFrame()
        rSettings["orig_renderScale"] = self.getOutputRez(shot)
        rSettings["orig_renderFilter"] = self.getOutputSampleFilter(shot)

        #   Update Frame Range
        with self.UNDO_BLOCK("Set Framerange"):
            self.setFrameRange(origin, rSettings["startFrame"], rSettings["endFrame"], shot)

        #   Sets Output Scaling and Scale Filter
        if rSettings["scaleOverride"]:
            with self.UNDO_BLOCK("Scale Image"):
                self.setOutputRez(shot, scaleStr=rSettings["renderScale"])
                self.setOutputSampleFilter(shot, filterStr=rSettings["renderFilter"])

        return rSettings
    

    #   Renders with SynthEyes 'Save Sequence'
    @err_catcher(name=__name__)
    def sm_render_Sequence(self, origin, stateManager, outputPath, rSettings):
        #   Get Format Specific Render Settings
        optStr = self.getRenderOptsStr(rSettings)

        #   Make Render Include String
        settingsStr = ("imp: "
                       f"{boolToBit(rSettings['include_RGB'])},"
                       f"{boolToBit(rSettings['include_Alpha'])},"
                       f"{boolToBit(rSettings['include_Mesh'])},"
                       "<>"
                    #    f"{boolToBit(rSettings['include_Burnin'])}"            #   TODO - Look at Burn-in
                      )

        stateManager.showMinimized()

        try:
            shot = self.getShotFromCamName(rSettings["currentCam"])

            #   Configure SynthEyes Render Settings
            with self.UNDO_BLOCK("Set RenderSettings"):
                shot.Set("renderFile", outputPath)
                shot.Set("renderCompression", optStr)
                shot.Set("renderSettings", settingsStr)

            #   Run Render
            with self.UNDO_BLOCK("Render"):
                result = shot.Call("Render")

        except Exception as e:
            logger.warning(f"ERROR: Unable to Render Image Sequence: {e}")
            return False
        
        finally:
            QTimer.singleShot(1000, stateManager.showNormal)

        #   Return Bool of SynthEyes Int Result
        return int(result) == 1


    @err_catcher(name=__name__)
    def sm_render_postRender(self, origin, rSettings):
        shot = self.getShotFromCamName(rSettings["currentCam"])

        #   Restore Frame Range
        with self.UNDO_BLOCK("Restore Framerange"):
            self.setFrameRange(origin, rSettings["orig_start"], rSettings["orig_end"], shot)
            self.setCurrentFrame(rSettings["orig_currFrame"])

        #   Restore Render Scale
        with self.UNDO_BLOCK("Restore Image Scale"):
            self.setOutputRez(shot, scaleCode=rSettings["orig_renderScale"])
            self.setOutputSampleFilter(shot, filterCode=rSettings["orig_renderFilter"])
        
        self.synthEyes.Validate(shot)


    #   Sanity Check Before State Execution
    @err_catcher(name=__name__)
    def sm_render_stMap_preSubmit(self, origin, rData):            #   TODO
        warnings = []

        camName = rData["currentCam"]

        #   Check if Shot Camera was Solved with Distortion
        hasDistor = self.getShotHasDistort(camName)

        #   Check if Shot Camera has had Lens Workflow Completed
        hasLensWorkflow = self.getShotHasLensWorkflow(camName)

        if hasDistor and not hasLensWorkflow:
            msg = (f"CAMERA   '{camName}':\n"
                   "             appears to have solved distortion,\n"
                   "             and the Lens Workflow script has not\n"
                   "             been completed.")
            warnings.append([msg, "", 2])

        return warnings


    #   Called Before Render to Capture Current and Set Custom Settings
    @err_catcher(name=__name__)
    def sm_render_preRender_stMap(self, origin, cameraName, rData):

        ##  DISABLED - SynthEyes does not appear to rescale the UnDistort Images  ##
        # shot = self.getShotFromCamName(cameraName)
        # rData["orig_renderScale"] = self.getOutputRez(shot)
        # rData["orig_renderFilter"] = self.getOutputSampleFilter(shot)
        
        ##  Capture Current Settings
        #   EXR Compression Format
        rData["orig_exrUVMcmp"] = self.synthEyes.GetPrefFromVar("exrUVMcmp")
        rData["orig_currFrame"] = self.getCurrentFrame()

        ##  Set Render Settings
        #   EXR Compression Format
        self.synthEyes.BeginPref()
        self.synthEyes.SetPrefFromVar("exrUVMcmp", rData["exrUVMcmp"])
        self.synthEyes.AcceptPref()

        return rData


    @err_catcher(name=__name__)
    def sm_render_stMap(self, origin, stType, rangeType, outputName, rSettings, context):

        # .WriteRedistortImage(filenm, clip)
        # .WriteRedistortSequence(fnm, cmp, flt, walp, clip)
        # .WriteUndistortImage(filenm, clip)
        # .WriteUndistortSequence(fnm, cmp, flt, walp, clip)

        #  Writes a sequence of UVMaps, starting at the given first filename (must include any leading zeros).
        #  Cmp is the compression specification string;
        #  flt=1 for a full floating-point map or =0 for 16bit;
        #  walp is 2 to write premultiplied alpha, 1 for non-premultiplied, or 0 for no alpha;
        #  clp=1 to clip to 0..1, or =0 to allow out-of-range color values (safety areas).

        ######################################################################################
        #   FYI:  STMAP Sequences are not working yet.  Even though it looks like it should,
        #   I am getting a SynthEyes error.  I think it is from the compression specification str.
        ######################################################################################

        args = [outputName]

        if stType == "redistort":
            if rangeType == "sequence":
                stFunct = "WriteRedistortSequence"
                args.extend(["exr: <ZIP-scanline>,45", 1, 0, 0])
            else:
                stFunct = "WriteRedistortImage"

        elif stType == "undistort":
            if rangeType == "sequence":
                stFunct = "WriteUndistortSequence"
                args.extend(["exr: <ZIP-scanline>,45", 1, 0, 0])
            else:
                stFunct = "WriteUndistortImage"

    
        shot = self.getShotFromCamName(rSettings["currentCam"])

        ##  DISABLED - SynthEyes does not appear to rescale the UnDistort Images  ##
        # if rSettings["scaleOverride"]:
        #     #   Sets Output Scaling and Scale Filter
        #     with self.UNDO_BLOCK("Scale Image"):
        #         self.setOutputRez(shot, scaleStr=rSettings["renderScale"])
        #         self.setOutputSampleFilter(shot, filterStr=rSettings["renderFilter"])


        with self.UNDO_BLOCK("Render StMaps"):
            result = shot.Call(stFunct, *args)
  
        result = 1
        return int(result) == 1


    #   Called after Render to Restore Original Settings
    @err_catcher(name=__name__)
    def sm_render_postRender_stMap(self, origin, cameraName, rData):
        ##  DISABLED - SynthEyes does not appear to rescale the UnDistort Images  ##
        # shot = self.getShotFromCamName(cameraName)
        # with self.UNDO_BLOCK("Restore Image Scale"):
        #     self.setOutputRez(shot, scaleCode=oData["orig_renderScale"])
        #     self.setOutputSampleFilter(shot, filterCode=oData["orig_renderFilter"])

        #   EXR Compression Format
        self.synthEyes.BeginPref()
        self.synthEyes.SetPrefFromVar("exrUVMcmp", rData["orig_exrUVMcmp"])
        self.synthEyes.AcceptPref()

        #   Restore Framerange
        with self.UNDO_BLOCK("Restore Framerange"):
            self.setCurrentFrame(rData["orig_currFrame"])


    @err_catcher(name=__name__)
    def sm_playblast_preExecute(self, origin, rData):
        warnings = []

        camName = rData["currentCam"]

        #   Check if Shot Camera was Solved with Distortion
        hasDistor = self.getShotHasDistort(camName)

        #   Check if Shot Camera has had Lens Workflow Completed
        hasLensWorkflow = self.getShotHasLensWorkflow(camName)

        if hasDistor and not hasLensWorkflow:
            msg = (f"CAMERA   '{camName}':\n"
                   "             appears to have solved distortion,\n"
                   "             and the Lens Workflow script has not\n"
                   "             been completed.")
            warnings.append([msg, "", 2])

        return warnings
    

        #   Called Before Render to Capture Current Settings
    @err_catcher(name=__name__)
    def sm_playblast_preRender(self, origin, rSettings):
        shot = self.getShotFromCamName(rSettings["currentCam"])
        camera = self.getCamFromName(rSettings["currentCam"])

        #   Capture Original Settings
        orig_start, orig_end = self.getFrameRange(origin, shot)
        rSettings["orig_start"] = orig_start
        rSettings["orig_end"] = orig_end
        rSettings["orig_currFrame"] = self.getCurrentFrame()
        rSettings["orig_renderScale"] = self.getOutputRez(shot)
        rSettings["orig_renderFilter"] = self.getOutputSampleFilter(shot)

        #   Update Frame Range
        with self.UNDO_BLOCK("Set Framerange"):
            self.setFrameRange(origin, rSettings["startFrame"], rSettings["endFrame"], shot)

        #   Sets Output Scaling and Scale Filter
        if rSettings["scaleOverride"]:
            with self.UNDO_BLOCK("Scale Image"):
                self.setOutputRez(shot, scaleStr=rSettings["renderScale"])
                self.setOutputSampleFilter(shot, filterStr=rSettings["renderFilter"])

        #   Capture Current View
        self.synthEyes.InitMenu()
        currView = self.synthEyes.View()

        #   Set View to Perspective (has to be for Preview Movie)
        if currView != "Prespective":
            rSettings["currView"] = currView
            self.synthEyes.SetView("Perspective")

        #   Set Active Shot (Tracker Host)
        with self.UNDO_BLOCK("Set Camera"):
            self.synthEyes.SetActive(camera)

        return rSettings


    @err_catcher(name=__name__)
    def sm_render_playblast(self, origin, stateManager, outputPath, rSettings):
        #   Get Format Specific Render Settings
        optStr = self.getRenderOptsStr(rSettings)

        include_items = rSettings["include_Items"]
        include_grid = rSettings["include_Grid"]
        include_RGB = rSettings["include_RGB"]
        include_depth = rSettings["include_Depth"]
        include_alpha = rSettings["include_Alpha"]
        include_burnIn = rSettings["include_Burnin"]

        settingsStr = ("prvu: "
                       "0,"                                 #   Unknown
                       f"{boolToBit(include_items)},"       #   Include Viewport Items
                       f"{boolToBit(include_grid)},"        #   Include Grid
                        "1,"                                #   Square Pixels
                       f"{boolToBit(include_RGB)},"         #   Include RGB
                       f"{boolToBit(include_depth)},"       #   Include Depth
                       f"{boolToBit(include_alpha)},"       #   Include Alpha
                       f"{boolToBit(include_burnIn)}")      #   Unknown

        shot = self.getShotFromCamName(rSettings["currentCam"])

        with self.UNDO_BLOCK("Playblast Settings"):
            shot.Set("previewFile", outputPath)
            shot.Set("previewSettings", settingsStr)
            shot.Set("previewCompression", optStr)

        stateManager.showMinimized()

        try:
            #   Get Perspective View Object
            perspVu = self.synthEyes.Main().ByClass("Perspect")
            #   "Click" the Preview Movie Button
            perspVu.PerformActionByNameAndContinue("Persp/Preview Movie")

            time.sleep(1)

            #   Capture the Resulting Popup Window
            popup_preview = self.synthEyes.Popup()

            #   Find and "Click" the Start Button
            start_btn = popup_preview.ByName("Start")
            if start_btn.IsValid():
                start_btn.ClickAndWait()

            #   Wait for Popup to Close
            self.waitForPopupClose(popup_preview)

            return True
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Render Playblast: {e}")
            return False
        
        finally:
            stateManager.showNormal()


    @err_catcher(name=__name__)
    def sm_playblast_postRender(self, origin, rSettings):
        shot = self.getShotFromCamName(rSettings["currentCam"])

        #   Restore Frame Range
        with self.UNDO_BLOCK("Restore Framerange"):
            self.setFrameRange(origin, rSettings["orig_start"], rSettings["orig_end"], shot)
            self.setCurrentFrame(rSettings["orig_currFrame"])

        #   Restore Render Scale
        with self.UNDO_BLOCK("Restore Image Scale"):
            self.setOutputRez(shot, scaleCode=rSettings["orig_renderScale"])
            self.setOutputSampleFilter(shot, filterCode=rSettings["orig_renderFilter"])

        #   Restore View if it Was Not Already Perspective
        if rSettings["currView"] != "Perspective":
            self.synthEyes.SetView(rSettings["currView"])
        
        self.synthEyes.Validate(shot)




    ###################################################
    ##         State Manager States Handling         ##   
    ###################################################

    #   This uses SynthEyes Note objects to store the State Data.
    #   Notes can only store a finite amount of characters, so
    #   the Data is spread over several Note Objects.
    #   The Index Note contains the listing of all the State Notes,
    #   and each State Note contains a compressed version of a State.


    #   Returns Default State String
    @err_catcher(name=__name__)
    def getDefaultState(self):
        defaultState = """{
        "states": [
            {
                "statename": "publish",
                "comment": "",
                "description": ""
            }
        ]
    }
    """
        return defaultState
    

    #   Compresses State String Json
    @err_catcher(name=__name__)
    def compressState(self, data):
        raw = json.dumps(data, separators=(",", ":")).encode()
        return base64.b64encode(zlib.compress(raw)).decode()


    #   Decompresses to Json String
    @err_catcher(name=__name__)
    def decompressState(self, txt):
        return json.loads(zlib.decompress(base64.b64decode(txt)).decode())


    #   Returns Note Object by Note Number
    @err_catcher(name=__name__)
    def getNoteByNumber(self, num):
        for note in self.synthEyes.Notes():
            if note.number == num:
                return note
        return None


    #   Returns Root Index Note Object
    @err_catcher(name=__name__)
    def getIndexNote(self):
        note = self.getNoteByNumber(1000)

        # if not note:
        #     with self.UNDO_BLOCK("Create Index Note"):
        #         note = self.createIndexNote()

        return note


    #   Creates Root Index Note Object
    @err_catcher(name=__name__)
    def createIndexNote(self):
        note = self.synthEyes.CreateNew("NOTE")

        note.number = 1000
        note.shotID = 0
        note.show = 0.0
        note.text = json.dumps({"notes": []})

        return note


    #   Creates Note Object to Store State Data    
    @err_catcher(name=__name__)
    def createStateNote(self, number):
        note = self.synthEyes.CreateNew("NOTE")

        note.number = number
        note.shotID = 0
        note.show = 0.0

        return note
    

    #   Called to Save State Data
    @err_catcher(name=__name__)
    def sm_saveStates(self, origin=None, buf=None):
        data = json.loads(buf)

        index_note = self.getIndexNote()
        if not index_note:
            with self.UNDO_BLOCK("Create Index Note"):
                index_note = self.createIndexNote()

        old_index = json.loads(index_note.text)
        old_notes = set(old_index.get("notes", []))

        note_numbers = []

        for i, state in enumerate(data["states"]):
            number = 1001 + i
            note_numbers.append(number)

            note = self.getNoteByNumber(number)

            with self.UNDO_BLOCK("Create State Note"):
                if not note:
                    note = self.createStateNote(number)

                note.text = self.compressState(state)

        #   Remove Unused Notes
        new_notes = set(note_numbers)
        to_delete = old_notes - new_notes

        for number in to_delete:
            note = self.getNoteByNumber(number)
            if note:
                with self.UNDO_BLOCK("Delete Note:"):
                    self.synthEyes.Delete(note)

        with self.UNDO_BLOCK("Write Index Note"):
            index_note.text = json.dumps({"notes": note_numbers})


    #   Called to Retrieve State Data
    @err_catcher(name=__name__)
    def sm_readStates(self, origin=None):
        index_note = self.getNoteByNumber(1000)

        if not index_note:
            return self.getDefaultState()

        index = json.loads(index_note.text)

        states = []

        for number in index["notes"]:
            note = self.getNoteByNumber(number)

            if note and note.text:
                states.append(self.decompressState(note.text))

        return json.dumps({"states": states}, indent=4)
    

    #   Deletes All State Notes
    @err_catcher(name=__name__)
    def sm_deleteStates(self, origin=None):
        self.synthEyes.Begin()

        index_note = self.getNoteByNumber(1000)

        if not index_note:
            with self.UNDO_BLOCK("Create Index Note"):
                index_note = self.createIndexNote()

        index = json.loads(index_note.text)

        for number in index.get("notes", []):
            note = self.getNoteByNumber(number)

            if note:
                with self.UNDO_BLOCK("Delete Note"):
                    self.synthEyes.Delete(note)

        with self.UNDO_BLOCK("Write Index Note"):
            index_note.text = json.dumps({"notes": []})
