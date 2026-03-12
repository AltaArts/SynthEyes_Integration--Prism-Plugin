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
import random
import string
import ctypes
from ctypes import wintypes
import json
import zlib
import base64


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

logger = logging.getLogger(__name__)



class Prism_SynthEyes_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.synthEyes = None
        self.importSyPy3()

        ##  CALLBACKS

        self.core.registerCallback("onStateManagerOpen", self.onStateManagerOpen, plugin=self.plugin, priority=20)
        self.core.registerCallback("onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self.plugin)
        self.core.registerCallback("onUserSettingsOpen", self.onUserSettingsOpen, plugin=self.plugin)
        # self.core.registerCallback("onStateCreated", self.onStateCreated, plugin=self.plugin)
        # self.core.registerCallback("prePlayblast", self.prePlayblast, plugin=self.plugin)
        # self.core.registerCallback("onGenerateStateNameContext", self.onGenerateStateNameContext, plugin=self.plugin)

        #   Dict of UI Display Names, SynthEyes Names, and Extensions
        self.synthFormatNames = {
            "USD  (.usda)": {
                    "synthName": "USD ASCII Scene",
                    "format": ".usda"
                    },
            "FBX  (.fbx)": {
                    "synthName": "Filmbox FBX",
                    "format": ".fbx"
                    },
            "Alembic  (.abc)": {
                    "synthName": "Alembic 1.5+",
                    "format": ".abc"
                    },
            "Blender  (.py)": {
                    "synthName": "Blender (Python)",
                    "format": ".py"
                    },
            "Maya  (.ma)": {
                    "synthName": "Maya ASCII Updated",
                    "format": ".ma"
                    },
            "BMD Fusion  (.comp)": {
                    "synthName": "Fusion Composition",
                    "format": ".comp"
                    },
            "Nuke  (.nk)": {
                    "synthName": "Nuke (Current)",
                    "format": ".nk"
                    },
           }


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


    # # Generate a Random port (49152 - 65535)                  #   NOT SEEMILY NEEDED
    # def getRandomPort(self):
    #     port = random.randint(49152, 65535)
    #     return port


    # # Generate a Random 12-character Alphanumeric String      #   NOT SEEMILY NEEDED
    # def getRandomPin(self):
    #     chars = string.ascii_letters + string.digits
    #     pin = ''.join(random.choices(chars, k=12))
    #     return pin


    #   Parses the Integration Path and Imports SyPy3
    @err_catcher(name=__name__)
    def importSyPy3(self):
        if not self.synthEyes:
            integrations = self.core.integration.getIntegrations()
            synthPath = integrations["SynthEyes"][0]
            sys.path.append(synthPath)

            import SyPy3

            self.synthEyes = SyPy3.SyLevel()

            # self.synth_port = self.getRandomPort()
            # self.synth_pin = self.getRandomPin()
            # self.synthEyes.OpenExisting(self.synth_port, self.synth_pin)

            self.synthEyes.OpenExisting()

            logger.debug("Imported SynthEyes SyPy3")


    # @err_catcher(name=__name__)
    # def autosaveEnabled(self, origin):
    #     if bpy.app.version < (2, 80, 0):
    #         return bpy.context.user_preferences.filepaths.use_auto_save_temporary_files
    #     else:
    #         return bpy.context.preferences.filepaths.use_auto_save_temporary_files

    # @err_catcher(name=__name__)
    # def sceneOpen(self, origin):
    #     if self.core.shouldAutosaveTimerRun():
    #         origin.startAutosaveTimer()



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
        # origin.b_createImport.setMinimumWidth(70 * self.core.uiScaleFactor)
        # origin.b_createImport.setMaximumWidth(70 * self.core.uiScaleFactor)
        # origin.b_createImport.setMinimumHeight(0)
        # origin.b_createImport.setMaximumHeight(500 * self.core.uiScaleFactor)
        # origin.b_shotCam.setMinimumHeight(0)
        # origin.b_shotCam.setMaximumHeight(50 * self.core.uiScaleFactor)
        origin.b_showImportStates.setMinimumWidth(30 * self.core.uiScaleFactor)
        origin.b_showImportStates.setMaximumWidth(30 * self.core.uiScaleFactor)
        origin.b_showExportStates.setMinimumWidth(30 * self.core.uiScaleFactor)
        origin.b_showExportStates.setMaximumWidth(30 * self.core.uiScaleFactor)
        # origin.b_createExport.setMinimumWidth(70 * self.core.uiScaleFactor)
        # origin.b_createExport.setMaximumWidth(70 * self.core.uiScaleFactor)
        origin.b_createRender.setMinimumWidth(70 * self.core.uiScaleFactor)
        origin.b_createRender.setMaximumWidth(70 * self.core.uiScaleFactor)
        # origin.b_createPlayblast.setMinimumWidth(80 * self.core.uiScaleFactor)
        # origin.b_createPlayblast.setMaximumWidth(80 * self.core.uiScaleFactor)
        origin.b_description.setMinimumWidth(35 * self.core.uiScaleFactor)
        origin.b_description.setMaximumWidth(35 * self.core.uiScaleFactor)
        origin.b_preview.setMinimumWidth(35 * self.core.uiScaleFactor)
        origin.b_preview.setMaximumWidth(35 * self.core.uiScaleFactor)

        #	Remove Import Export and Playblast buttons
        origin.b_createImport.deleteLater()
        origin.b_createExport.deleteLater()
        origin.b_createPlayblast.deleteLater()
        origin.b_shotCam.deleteLater()


        #	Create New Scene Button
        origin.b_createShot = QPushButton(origin.w_CreateImports)
        origin.b_createShot.setObjectName("b_createShot")
        origin.b_createShot.setText("Create New Scene")
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
        origin.b_addMesh.setText("Add Mesh")
        origin.horizontalLayout_3.insertWidget(2, origin.b_addMesh)
        origin.b_addMesh.clicked.connect(lambda: origin.createState("Synth_ImportMesh"))

        # Export Scene Button
        origin.b_exportScene = QPushButton(origin.w_CreateExports)
        origin.b_exportScene.setObjectName("b_exportScene")
        origin.b_exportScene.setText("Export Scene")
        origin.b_exportScene.setMaximumSize(QSize(150, 16777215))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        origin.b_exportScene.setSizePolicy(sizePolicy)
        # index = origin.horizontalLayout_4.indexOf(origin.b_showExportStates)
        # origin.horizontalLayout_4.insertWidget(index - 1, origin.b_exportScene)
        origin.horizontalLayout_4.insertWidget(0, origin.b_exportScene)
        origin.b_exportScene.clicked.connect(lambda: origin.createState("Synth_SceneExport"))

        # origin.createState(appStates["stateType"], parent=parent, setActive=True, **appStates.get("kwargs", {}))

        #   States to Keep in SynthEyes
        keepStates = ["Folder", "Synth_AddShot", "Synth_ImportMesh", "Synth_SceneExport", "Synth_Render_StMap"]

        #   Remove Unused States
        for state in list(origin.stateTypes.keys()):
            if state not in keepStates:
                try:
                    del origin.stateTypes[state]
                except Exception:
                    logger.debug(f"Unable to remove default state: {state}")



        
        # # Add MenuItems
        # origin.actionSortImageLoaders = QAction(origin)
        # origin.actionSortImageLoaders.setObjectName(u"actionSortImageLoaders")
        # origin.actionSortImageLoaders.setText(QCoreApplication.translate("mw_StateManager", u"Sort Image Loaders", None))
        # origin.actionSortImageLoaders.triggered.connect(lambda: self.sortLoaders(comp, getfeedback=True))
        # #.
        # origin.actionSelectImageLoaders = QAction(origin)
        # origin.actionSelectImageLoaders.setObjectName(u"actionSelectImageLoaders")
        # origin.actionSelectImageLoaders.setText(QCoreApplication.translate("mw_StateManager", u"Select Image Loaders", None))
        # origin.actionSelectImageLoaders.triggered.connect(self.selectAllStateLoaders)
        # #.
        # origin.menuAbout.addSeparator()
        # origin.menuAbout.addAction(origin.actionSortImageLoaders)
        # origin.menuAbout.addAction(origin.actionSelectImageLoaders)
        # origin.menuAbout.addSeparator()
        # ##

        # try:
        #     self.core.plugins.monkeyPatch(origin.rclTree, self.rclTree, self, force=True)
        #     self.core.plugins.monkeyPatch(self.core.mediaProducts.getVersionStackContextFromPath,
        #                                     self.getVersionStackContextFromPath,
        #                                     self,
        #                                     force=True)
        #     self.core.plugins.monkeyPatch(origin.importShotCam, self.importShotCam, self, force=True)
        #     self.core.plugins.monkeyPatch(origin.showStateMenu, self.showStateMenu, self, force=True)
        #     self.core.plugins.monkeyPatch(origin.pasteStates, self.pasteStates, self, force=True)
        # except Exception as e:
        #     logger.warning(f"ERROR: Failed to load patched functions:\n{e}")

        # #origin.gb_import.setStyleSheet("margin-top: 20px;")




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
    def exportScene(self):
        self.handle_exportScene()


    @err_catcher(name=__name__)
    def testOne(self):
        # self.core.popup("IN TEST ONE")							#	TESTING

        self.prismMenuTesting()



    @err_catcher(name=__name__)
    def testTwo(self):
        self.core.popup("IN TEST TWO")							#	TESTING

        

        # testPath = r"C:\\Users\\Joshua Breckeen\\Desktop\\TEST_STMAP\\TEST_STMAP_v001.0001.exr"


        # args = [outputName]

        # if stType == "redistort":
        #     if rangeType == "sequence":
        #         stFunct = "WriteRedistortSequence"
        #         args.extend(["exr: <ZIP-scanline>,45", 1, 0, 0])
        #     else:
        #         stFunct = "WriteRedistortImage"

        # elif stType == "undistort":
        #     if rangeType == "sequence":
        #         stFunct = "WriteUndistortSequence"
        #         args.extend(["exr: <ZIP-scanline>,45", 1, 0, 0])
        #     else:
        #         stFunct = "WriteUndistortImage"

    
    #   "exr: <ZIP-scanline>,45"


        # shots = self.synthEyes.Shots()                  #   TODO - ENSURE CORRECT SHOT
        # shot = shots[0]

        # result = shot.Call(stFunct, *args)

        # result = shot.Call("WriteRedistortSequence", "exr: <ZIP-scanline>,45", 1, 1, 1)

        # self.core.popup(f"result:  {result}")							#	TESTING



    @err_catcher(name=__name__)                                                 #   TESTING
    def saveSynthPrefs(self):

        import json
        import os
        from concurrent.futures import ThreadPoolExecutor, TimeoutError

        # Path to JSON output
        jsonPath = r"C:\Users\Joshua Breckeen\Desktop\SynthPrefs.json"


        # Dynamic skip list for problematic prefs
        skip_list = {
            "solvercalib",
            "setAsPrefs",
            "placeAsPrefs",
            "removePrefs",
            "setToPrefs",
            }


        # Read existing JSON to resume if file exists
        if os.path.exists(jsonPath):
            with open(jsonPath, "r", encoding="utf-8") as f:
                try:
                    existing_prefs = json.load(f)
                    start_idx = max(p["index"] for p in existing_prefs) + 1
                except:
                    existing_prefs = []
                    start_idx = 0
        else:
            existing_prefs = []
            start_idx = 0

        print(f"Starting at index {start_idx}")

        # Prepare file for incremental writing
        if not os.path.exists(jsonPath) or start_idx == 0:
            # new file: start JSON array
            with open(jsonPath, "w", encoding="utf-8") as f:
                f.write("[\n")
        else:
            # existing file: continue, remove final ']'
            with open(jsonPath, "rb+") as f:
                f.seek(-2, os.SEEK_END)
                f.truncate()
                f.write(b",\n")

        numPrefs = self.synthEyes.NumPrefs()
        print(f"Total prefs: {numPrefs}")

        self.synthEyes.BeginPref()

        executor = ThreadPoolExecutor(max_workers=1)  # single thread for safety
        first = (start_idx == 0) and (len(existing_prefs) == 0)

        try:
            for idx in range(start_idx, numPrefs):

                name = self.synthEyes.PrefName(idx)
                variable = self.synthEyes.PrefVariable(idx)

                if not variable:
                    continue  # skip headers

                description = self.synthEyes.PrefDescription(idx)

                # Skip known problematic prefs
                if variable in skip_list:
                    print(f"**** Skipped pref {variable}")
                    pref_entry = {
                        "index": idx,
                        "name": name,
                        "variable": variable,
                        "value": None,
                        "description": description
                    }
                else:
                    # Function to safely read value
                    def get_value():
                        try:
                            return self.synthEyes.GetPrefFromIndex(idx)
                        except:
                            return None

                    future = executor.submit(get_value)
                    try:
                        value = future.result(timeout=2.0)  # 2 sec timeout
                        print(f"Pref {variable} = {value}")  # print successful read
                    except TimeoutError:
                        print(f"**** Pref {variable} timed out, skipping")
                        value = None
                        skip_list.add(variable)  # dynamically add to skip list

                    pref_entry = {
                        "index": idx,
                        "name": name,
                        "variable": variable,
                        "value": value,
                        "description": description
                    }

                # Write directly to disk incrementally
                with open(jsonPath, "a", encoding="utf-8") as f:
                    if not first:
                        f.write(",\n")
                    f.write(json.dumps(pref_entry, ensure_ascii=False))
                    first = False

        finally:
            self.synthEyes.AcceptPref()
            executor.shutdown(wait=False)

        # Close JSON array
        with open(jsonPath, "a", encoding="utf-8") as f:
            f.write("\n]")

        print(f"Prefs successfully written to: {jsonPath}")



    @err_catcher(name=__name__)                                                 #   TESTING
    def prismMenuTesting(self):

        self.synthEyes.InitMenu()

        mainMenu = self.synthEyes.MainMenu()
        prismMenu = mainMenu.SubMenuByName("Prism")

        if not prismMenu.Exists():
            prismMenu = mainMenu.AddSubMenu(9, "Prism")

            prismMenu.AddMenuItem(1, "Save Next Version", 1)
            prismMenu.AddMenuItem(2, "Save Version with Comment", 2)
            prismMenu.AddMenuItem(3, "Project Browser", 3)
            prismMenu.AddMenuItem(4, "State Manager", 4)
            prismMenu.AddMenuItem(5, "Prism Settings", 5)
            prismMenu.AddMenuItem(6, "Export Scene", 6)

            # self.synthEyes.ReloadAll()
            self.synthEyes.Redraw()


        # last_id = self.synthEyes.core.Run("MENULAST1")
        # print(f"***  last_id:  {last_id}")								#	TESTING

        # count = prismMenu.Count()

        # for i in range(1, count+1):
        #     name = prismMenu.NameByPos(i)
        #     mid  = prismMenu.IDByPos(i)

        #     print(i, name, mid)
        
        # # print(f"dir prismMenu:  {dir(prismMenu)}")							#	TESTING

        # act_projectB = prismMenu.SubMenuByName("Project Browser")
        # print(f"dir act_projectB:  {dir(act_projectB)}")								#	TESTING

        # print(f"***  act_projectB runcmd:  {act_projectB.runcmd}")								#	TESTING

        # act_save =mainMenu.SubMenuByName("Save")
        # print(f"dir act_save:  {dir(act_save)}")								#	TESTING

        # print(f"***  act_save runcmd:  {act_save.runcmd}")								#	TESTING

        # project_browser_id = prismMenu.IDByName("Project Browser")
        # save_next_id = prismMenu.IDByName("Save Next Version")

        # last_id = self.synthEyes.core.Run("MENULAST1")

        # print(f"***  last_id:  {last_id}")								#	TESTING

        # import time

        # print("Polling for menu selection (Ctrl+C to stop)...")

        # try:
        #     while True:
        #         last_id = self.synthEyes.core.Run("MENULAST1")  # last clicked menu ID
        #         if last_id == project_browser_id:
        #             print("Project Browser menu clicked!")
        #             self.open_ProjectBrowser()
        #         elif last_id == save_next_id:
        #             print("Save Next Version clicked!")
        #             self.saveNextVersion()

        #         time.sleep(0.2)  # poll every 0.2 seconds
        # except KeyboardInterrupt:
        #     print("Polling stopped by user.")

        # print(f"act_projectB.runcmd:  {act_projectB.runcmd}")

        # help(act_projectB.runcmd)

        # print(f"act_projectB.runcmd.__doc__: {act_projectB.runcmd.__doc__}")

        # print(f"type: {type(act_projectB)}")

        # print(f"class: {act_projectB.__class__}")

        # print(f"prismMenu.IDByPos(1): {prismMenu.IDByPos(1)}")

        # print(f"prismMenu.NameByID(1): {prismMenu.NameByID(1)}")

        # print(f"dir core: {dir(self.synthEyes.core)}")

        # self.synthEyes.core.Run(act_projectB.runcmd)

        # actionName = "PRISM.OpenProjectBrowser"
        # self.synthEyes.core.Run(f'REGISTERACTION {actionName}')

        # act_projectB.runcmd = lambda: self.open_ProjectBrowser()

        # print(f"runcmd:  {act_projectB.runcmd}")							#	TESTING

        # Actions = self.synthEyes.Actions()

        # for action in Actions:
        #     print(action)



    ###################################################
    ##                 File Handling                 ##   
    ###################################################

    #   Returns SynthEyes Version
    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        return self.synthEyes.Version()


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
    

    # @err_catcher(name=__name__)
    # def getImportPaths(self, origin):
    #     if "PrismImports" not in bpy.context.scene:
    #         return False
    #     else:
    #         return bpy.context.scene["PrismImports"]


    @err_catcher(name=__name__)
    def getFrameRange(self, origin):
        # return [None, None]                                         #   TODO - FOR TESTING
        try:
            start = (self.synthEyes.AnimStart() + 1)
            end = (self.synthEyes.AnimEnd() +1)
            return[start, end]
        
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Framerange from SynthEyes: {e}")
            return [None, None]


    @err_catcher(name=__name__)
    def getCurrentFrame(self):
        try:
            currentFrame = self.synthEyes.Frame()
            return currentFrame
        except Exception as e:
            logger.warning(f"ERROR: Unable to Get Current Frame from SynthEyes: {e}")
            return None


    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame, endFrame):
        try:
            self.synthEyes.SetAnimStart(startFrame)
            self.synthEyes.SetAnimEnd(endFrame)
            logger.debug("Updated Framerange in SynthEyes")

        except Exception as e:
            logger.warning(f"ERROR: Unable to Set Framerange in SynthEyes: {e}")


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
                    self.synthEyes.Begin()
                    self.synthEyes.Delete(obj)
                    self.synthEyes.Accept(f"Deleted {objType}")
                    break

            return True

        except Exception as e:
            logger.warning(f"ERROR: Unable to delete {objType} - {uuid}")
            return False



    # @err_catcher(name=__name__)
    # def getFPS(self, origin):
    #     intFps = bpy.context.scene.render.fps
    #     baseFps = bpy.context.scene.render.fps_base
    #     return round(intFps / baseFps, 2)


    # @err_catcher(name=__name__)
    # def setFPS(self, origin, fps):
    #     if int(fps) == fps:
    #         bpy.context.scene.render.fps = int(fps)
    #     else:
    #         intFps = math.ceil(fps)
    #         bpy.context.scene.render.fps = intFps
    #         bpy.context.scene.render.fps_base = intFps/fps


    # @err_catcher(name=__name__)
    # def getResolution(self):
    #     width = bpy.context.scene.render.resolution_x
    #     height = bpy.context.scene.render.resolution_y
    #     return [width, height]


    # @err_catcher(name=__name__)
    # def setResolution(self, width=None, height=None):
    #     if width:
    #         bpy.context.scene.render.resolution_x = width
    #     if height:
    #         bpy.context.scene.render.resolution_y = height


    @err_catcher(name=__name__)
    def getCamNodes(self, origin, cur=False):
        return self.synthEyes.Cameras()
    

    @err_catcher(name=__name__)
    def getCamName(self, origin, handle):                           #   TODO - Make Return current or passed Camera
        cams = self.synthEyes.Cameras()
        if cams:
            return cams[0].Name()
        
        return None
    

    # @err_catcher(name=__name__)
    # def selectCam(self, origin):
    #     if self.getObject(origin.curCam):
    #         self.deselectObjects()
    #         self.selectObject(self.getObject(origin.curCam))



    #######################################
    ##               Shots               ##   
    #######################################
   

    @err_catcher(name=__name__)
    def addShot(self, origin, mode):
        if mode == "create":
            question = ("Would you like to Create a New SynthEyes Scene?\n\n"
                        "This will Create a New Clean Scene and Import the Shot")

        elif mode == "add":
            question = ("Would you like to Add an Additional Shot to the\n"
                        "existing Scene?")
        else:
            return False
            
        title = "Create/Add Shot"

        result = self.core.popupQuestion(text=question, title=title)

        if result != "Yes":
            return

        self.addShot_mode = mode
        origin.createState("Synth_AddShot")   


    @err_catcher(name=__name__)
    def sm_addShot(self, origin, mode, shotFilepath, details=None):
        if mode == "create":
            try:
                curr_SniName = self.synthEyes.SNIFileName()

                shot = self.synthEyes.NewSceneAndShot(shotFilepath, asp = 0.0)

                self.synthEyes.SetSNIFileName(curr_SniName)

                camSuffix = "SCENE"

            except Exception as e:
                logger.warning(f"ERROR: Unable to Create Scene Shot: {e}")
                return False
            
        elif mode == "add":
            try:
                shot = self.synthEyes.AddShot(shotFilepath, asp = 0.0)

                camSuffix = "SHOT"

            except Exception as e:
                logger.warning(f"ERROR: Unable to Add Shot: {e}")
                return False

        if details:
            try:
                camName = f"CAMERA_{camSuffix}-{details['identifier']}_{details['version']}"
            
                self.synthEyes.Begin()

                for obj in shot.Objects():
                    if obj.Name().lower().startswith("camera"):
                        obj.SetName(camName)
                        break

                self.synthEyes.Accept("Shot Rename")

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
                
           

    #######################################
    ##           Import Mesh             ##   
    #######################################



    # @err_catcher(name=__name__)
    # def sm_import_startup(self, origin):
    #     origin.f_abcPath.setVisible(True)

    # @err_catcher(name=__name__)
    # def importAlembic(self, importPath, origin=None):
    #     if origin and origin.chb_abcPath.isChecked() and len(origin.nodes) > 0:
    #         cache = None
    #         for i in origin.nodes:
    #             constraints = [
    #                 x
    #                 for x in self.getObject(i).constraints
    #                 if x.type == "TRANSFORM_CACHE"
    #             ]
    #             modifiers = [
    #                 x
    #                 for x in self.getObject(i).modifiers
    #                 if x.type == "MESH_SEQUENCE_CACHE"
    #             ]
    #             if len(constraints) > 0:
    #                 cache = constraints[0].cache_file
    #             elif len(modifiers) > 0:
    #                 cache = modifiers[0].cache_file

    #         if cache is not None:
    #             cache.filepath = importPath
    #             cache.name = os.path.basename(importPath)
    #         #       bpy.context.scene.frame_current += 1        #updates the cache, but leads to crashes
    #         #       bpy.context.scene.frame_current -= 1
    #         else:
    #             self.core.popup("No caches updated.")
    #         return True
    #     else:
    #         if bpy.app.version < (4, 0, 0):
    #             bpy.ops.wm.alembic_import(
    #                 self.getOverrideContext(origin),
    #                 filepath=importPath,
    #                 set_frame_range=False,
    #                 as_background_job=False,
    #             )
    #         else:
    #             with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #                 bpy.ops.wm.alembic_import(
    #                     filepath=importPath,
    #                     set_frame_range=False,
    #                     as_background_job=False,
    #                 )

    # @err_catcher(name=__name__)
    # def importFBX(self, importPath, origin=None):
    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.import_scene.fbx(self.getOverrideContext(origin), filepath=importPath)
    #     else:
    #         with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #             bpy.ops.import_scene.fbx(filepath=importPath)

    # @err_catcher(name=__name__)
    # def importObj(self, importPath, origin=None):
    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.import_scene.obj(self.getOverrideContext(origin), filepath=importPath)
    #     else:
    #         with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #             bpy.ops.wm.obj_import(filepath=importPath)

    # @err_catcher(name=__name__)
    # def importGlb(self, importPath, origin=None):
    #     with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #         bpy.ops.import_scene.gltf(filepath=importPath)

    # @err_catcher(name=__name__)
    # def importUsd(self, filepath, origin=None):
    #     from _bpy import ops as _ops_module
    #     try:
    #         _ops_module.as_string("WM_OT_usd_import")
    #     except:
    #         ext = os.path.splitext(filepath)[1]
    #         msg = "Format \"%s\" is not supported in this synthEyes version. Importing USD requires at least synthEyes 3.0." % ext
    #         self.core.popup(msg)
    #         return False

    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.wm.usd_import(
    #             self.getOverrideContext(origin),
    #             filepath=filepath,
    #             set_frame_range=False,
    #             import_usd_preview=True,
    #         )
    #     else:
    #         with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #             bpy.ops.wm.usd_import(
    #                 filepath=filepath,
    #                 set_frame_range=False,
    #                 import_usd_preview=True,
    #             )

    # @err_catcher(name=__name__)
    # def importFile(self, importPath):
    #     if not importPath:
    #         return

    #     base, ext = os.path.splitext(importPath)
    #     ext = ext.lower()
    #     if ext in self.importHandlers:
    #         return self.importHandlers[ext]["importFunction"](importPath)


    @err_catcher(name=__name__)
    def sm_import_importToApp(self, origin, doImport, update, impFileName, data=None):
        fileName = os.path.splitext(os.path.basename(impFileName))
        ext = fileName[1].lower()

        if ext not in self.importFormats:
            self.core.popup(f"Format {ext} is not supported for SynthEyes Mesh Import.")
            return {"result": False, "doImport": doImport}
        
        else:
            filePath = os.path.normpath(impFileName)

            if data:
                try:
                    meshName = f"{data['product']}_{data['version']}"
                except:
                    pass
            else:
                meshName = fileName[0]

            self.synthEyes.Begin()

            scn = self.synthEyes.Scene()
            meshObj = scn.Call("ReadMesh", filePath)

            if not meshObj:
                self.synthEyes.Accept("Configure Import")
                return {"result": False, "doImport": False}
            
            meshObj.SetName(meshName)

            self.synthEyes.Accept("Configure Import")

            result = meshObj.UniqID()
            doImport = True

            return {"result": result, "doImport": doImport}
        

    @err_catcher(name=__name__)
    def sm_import_preDelete(self, origin, delData:dict):
        try:
            uuid = delData["meshUUID"]
            self.deleteObjByUUID("mesh", uuid)

        except Exception as e:
            logger.warning(e)
        


    #######################################
    ##             Exporting             ##   
    #######################################


    @err_catcher(name=__name__)
    def sm_export_preExecute(self, origin, startFrame, endFrame):
        warnings = []


        return warnings
    

    # @err_catcher(name=__name__)
    # def sm_export_startup(self, origin):
    #     if origin.className == "Export":
    #         origin.w_additionalOptions.setVisible(False)
    

    @err_catcher(name=__name__)
    def sm_sceneExport(self, origin, outputType, outputName, startFrame=None, endFrame=None, details=None):
        try:
            synthFormatType = self.synthFormatNames[outputType]["synthName"]
            exportPath = os.path.normpath(outputName)

            self.synthEyes.Export(synthFormatType, exportPath)

            result = True

        except:
            return False

        if result:
            return outputName


    @err_catcher(name=__name__)
    def sm_export_preDelete(self, origin):
        # try:
        #     self.getGroups().remove(self.getGroups()[origin.getTaskname()], do_unlink=True)
        # except Exception as e:
        #     logger.warning(e)

        pass
    

        







    #######################################
    ##             Rendering             ##   
    #######################################


    @err_catcher(name=__name__)
    def sm_render_stMap_preSubmit(self, origin, rSettings):            #   TODO
        pass


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

    
    #   "exr: <ZIP-scanline>,45"


        shots = self.synthEyes.Shots()                  #   TODO - ENSURE CORRECT SHOT
        shot = shots[0]

        result = shot.Call(stFunct, *args)

  
        return int(result) == 1




    @err_catcher(name=__name__)
    def sm_render_stMap_undoRenderSettings(self, origin, rSettings):            #   TODO
        pass





        

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

        if not note:
            note = self.createIndexNote()

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

        self.synthEyes.Begin()

        index_note = self.getIndexNote()

        old_index = json.loads(index_note.text)
        old_notes = set(old_index.get("notes", []))

        note_numbers = []

        for i, state in enumerate(data["states"]):
            number = 1001 + i
            note_numbers.append(number)

            note = self.getNoteByNumber(number)

            if not note:
                note = self.createStateNote(number)

            note.text = self.compressState(state)

        #   Remove Unused Notes
        new_notes = set(note_numbers)
        to_delete = old_notes - new_notes

        for number in to_delete:
            note = self.getNoteByNumber(number)
            if note:
                self.synthEyes.Delete(note)

        index_note.text = json.dumps({"notes": note_numbers})

        self.synthEyes.Accept("Write Prism States")


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
            index_note = self.createIndexNote()

        index = json.loads(index_note.text)

        for number in index.get("notes", []):

            note = self.getNoteByNumber(number)

            if note:
                self.synthEyes.Delete(note)

        index_note.text = json.dumps({"notes": []})

        self.synthEyes.Accept("Cleared Prism States")







    # @err_catcher(name=__name__)
    # def getValidGroupName(self, groupName):
    #     extension = 1
    #     while groupName in self.getGroups() and extension < 999:
    #         if "%s_%s" % (groupName, extension) not in self.getGroups():
    #             groupName += "_%s" % extension
    #         extension += 1

    #     return groupName

    # @err_catcher(name=__name__)
    # def sm_export_setTaskText(self, origin, prevTaskName, newTaskName):
    #     setName = newTaskName
    #     if prevTaskName and prevTaskName in self.getGroups():
    #         self.getGroups()[prevTaskName].name = setName
    #     else:
    #         self.createGroups(name=setName)

    #     return setName

    # @err_catcher(name=__name__)
    # def sm_export_removeSetItem(self, origin, node):
    #     if origin.getTaskname() not in self.getGroups():
    #         return

    #     obj = self.getObject(node)
    #     if obj.bl_rna.identifier.upper() == "COLLECTION":
    #         self.getGroups()[origin.getTaskname()].children.unlink(obj)
    #     else:
    #         self.getGroups()[origin.getTaskname()].objects.unlink(obj)

    # @err_catcher(name=__name__)
    # def sm_export_clearSet(self, origin):
    #     if origin.getTaskname() not in self.getGroups():
    #         return

    #     for node in self.getGroups()[origin.getTaskname()].objects:
    #         self.getGroups()[origin.getTaskname()].objects.unlink(node)

    #     for node in self.getGroups()[origin.getTaskname()].children:
    #         self.getGroups()[origin.getTaskname()].children.unlink(node)

    # @err_catcher(name=__name__)
    # def sm_export_updateObjects(self, origin):
    #     origin.nodes = []
    #     taskName = origin.getTaskname()
    #     if taskName in self.getGroups():
    #         group = self.getGroups()[taskName]
    #         nodes = []
    #         for obj in group.objects:
    #             if not obj.users_scene:
    #                 group.objects.unlink(obj)
    #                 continue

    #             nodes.append(self.getNode(obj))

    #         for obj in group.children:
    #             nodes.append(self.getNode(obj))

    #         origin.nodes = nodes

    # @err_catcher(name=__name__)
    # def sm_export_exportShotcam(self, origin, startFrame, endFrame, outputName):
    #     self.selectCam(origin)
    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.wm.alembic_export(
    #             self.getOverrideContext(origin),
    #             filepath=(outputName + ".abc"),
    #             start=startFrame,
    #             end=endFrame,
    #             selected=True,
    #             as_background_job=False,
    #         )
    #     else:
    #         with bpy.context.temp_override(**self.getOverrideContext()):
    #             bpy.ops.wm.alembic_export(
    #                 filepath=(outputName + ".abc"),
    #                 start=startFrame,
    #                 end=endFrame,
    #                 selected=True,
    #                 as_background_job=False,
    #             )

    #     self.selectCam(origin)
    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.export_scene.fbx(
    #             self.getOverrideContext(origin),
    #             filepath=(outputName + ".fbx"),
    #             use_selection=True,
    #         )
    #     else:
    #         with bpy.context.temp_override(**self.getOverrideContext()):
    #             bpy.ops.export_scene.fbx(
    #                 filepath=(outputName + ".fbx"),
    #                 use_selection=True,
    #             )

    #     self.deselectObjects()

    # @err_catcher(name=__name__)
    # def exportObj(self, outputName, origin, startFrame, endFrame, expNodes):
    #     for i in range(startFrame, endFrame + 1):
    #         bpy.context.scene.frame_current = i
    #         foutputName = outputName.replace("####", format(i, "04"))
    #         if bpy.app.version < (4, 0, 0):
    #             bpy.ops.export_scene.obj(
    #                 self.getOverrideContext(origin),
    #                 filepath=foutputName,
    #                 use_selection=(not origin.chb_wholeScene.isChecked()),
    #             )
    #         else:
    #             with bpy.context.temp_override(**self.getOverrideContext()):
    #                 bpy.ops.wm.obj_export(
    #                     filepath=foutputName,
    #                     export_selected_objects=(not origin.chb_wholeScene.isChecked()),
    #                 )

    #     outputName = foutputName
    #     return outputName

    # @err_catcher(name=__name__)
    # def exportSelectionToObj(self, outputName):
    #     with bpy.context.temp_override(**self.getOverrideContext()):
    #         bpy.ops.wm.obj_export(
    #             filepath=outputName,
    #             export_selected_objects=True,
    #             export_colors=True,
    #         )

    #     return True

    # @err_catcher(name=__name__)
    # def exportSelectionToFbx(self, outputName):
    #     with bpy.context.temp_override(**self.getOverrideContext()):
    #         bpy.ops.export_scene.fbx(
    #             filepath=outputName,
    #             use_selection=True,
    #             bake_anim=False,
    #             colors_type="LINEAR",
    #             apply_unit_scale=False,
    #             global_scale=0.01,
    #         )

    #     return True

    # @err_catcher(name=__name__)
    # def exportFBX(self, outputName, origin, startFrame, endFrame, expNodes):
    #     useAnim = startFrame != endFrame
    #     if bpy.app.version >= (2, 79, 7):
    #         if bpy.app.version < (4, 0, 0):
    #             bpy.ops.export_scene.fbx(
    #                 self.getOverrideContext(origin),
    #                 filepath=outputName,
    #                 use_selection=(not origin.chb_wholeScene.isChecked()),
    #                 bake_anim=useAnim
    #             )
    #         else:
    #             with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #                 bpy.ops.export_scene.fbx(
    #                     filepath=outputName,
    #                     use_selection=(not origin.chb_wholeScene.isChecked()),
    #                     bake_anim=useAnim
    #                 )
    #     else:
    #         bpy.ops.export_scene.fbx(
    #             self.getOverrideContext(origin),
    #             filepath=outputName,
    #             use_selection=(not origin.chb_wholeScene.isChecked()),
    #             use_anim=useAnim
    #         )
    #     return outputName

    # @err_catcher(name=__name__)
    # def exportAlembic(self, outputName, origin, startFrame, endFrame, expNodes, additionalSettings=None):
    #     if getattr(origin, "additionalSettings", None):
    #         additionalSettings = additionalSettings or {}
    #         for setting in origin.additionalSettings:
    #             if setting["name"] == "abcScale":
    #                 additionalSettings["global_scale"] = setting["value"]

    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.wm.alembic_export(
    #             self.getOverrideContext(origin),
    #             filepath=outputName,
    #             start=startFrame,
    #             end=endFrame,
    #             selected=(not origin.chb_wholeScene.isChecked()),
    #             as_background_job=False,
    #             **additionalSettings,
    #         )
    #     else:
    #         with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #             bpy.ops.wm.alembic_export(
    #                 filepath=outputName,
    #                 start=startFrame,
    #                 end=endFrame,
    #                 selected=(not origin.chb_wholeScene.isChecked()),
    #                 as_background_job=False,
    #                 **additionalSettings,
    #             )

    #     return outputName

    # @err_catcher(name=__name__)
    # def exportGLB(self, outputName, origin, startFrame, endFrame, expNodes):
    #     with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #         bpy.ops.export_scene.gltf(
    #             filepath=outputName,
    #             use_selection=(not origin.chb_wholeScene.isChecked()),
    #             export_format="GLB",
    #         )

    #     return outputName

    # @err_catcher(name=__name__)
    # def exportBlend(self, outputName, origin, startFrame, endFrame, expNodes):
    #     if origin.chb_wholeScene.isChecked():
    #         shutil.copyfile(self.core.getCurrentFileName(), outputName)
    #     else:
    #         origin.setLastPath(outputName)
    #         self.core.saveScene(prismReq=False)
    #         expObjects = [self.getObject(x) for x in expNodes]
    #         for expObject in expObjects:
    #             if expObject.bl_rna.identifier.upper() == "COLLECTION":
    #                 for obj in expObject.all_objects:
    #                     if obj not in expObjects:
    #                         expObjects.append(obj)

    #         for object_ in bpy.data.objects:
    #             if object_ not in expObjects:
    #                 bpy.data.objects.remove(object_, do_unlink=True)

    #         bpy.ops.wm.save_as_mainfile(filepath=outputName, copy=True)
    #         bpy.ops.wm.revert_mainfile()
    #         self.core.stateManager()

    #     return outputName

    # @err_catcher(name=__name__)
    # def exportUsd(self, outputName, origin, startFrame, endFrame, expNodes, catchError=True, additionalSettings=None):
    #     from _bpy import ops as _ops_module
    #     additionalSettings = additionalSettings or {}
    #     try:
    #         _ops_module.as_string("WM_OT_usd_export")
    #     except:
    #         ext = os.path.splitext(outputName)[1]
    #         msg = "Format \"%s\" is not supported in this synthEyes version. Exporting USD requires at least synthEyes 2.82" % ext
    #         self.core.popup(msg)
    #         return False

    #     self.setFrameRange(origin, startFrame, endFrame)
    #     try:
    #         if bpy.app.version < (4, 0, 0):
    #             bpy.ops.wm.usd_export(
    #                 self.getOverrideContext(origin),
    #                 filepath=outputName,
    #                 export_animation=startFrame != endFrame,
    #                 selected_objects_only=(not origin.chb_wholeScene.isChecked()),
    #                 **additionalSettings,
    #             )
    #         else:
    #             with bpy.context.temp_override(**self.getOverrideContext(origin)):
    #                 bpy.ops.wm.usd_export(
    #                     filepath=outputName,
    #                     export_animation=startFrame != endFrame,
    #                     selected_objects_only=(not origin.chb_wholeScene.isChecked()),
    #                     **additionalSettings,
    #                 )
    #     except:
    #         if catchError:
    #             return False
    #         else:
    #             raise

    #     return outputName

    # @err_catcher(name=__name__)
    # def sm_export_exportAppObjects(
    #     self,
    #     origin,
    #     startFrame,
    #     endFrame,
    #     outputName,
    #     additionalSettings=None
    # ):
    #     expNodes = origin.nodes
    #     ctx = self.getOverrideContext(origin)
    #     if bpy.app.version >= (2, 80, 0):
    #         ctx.pop("screen")
    #         ctx.pop("area")

    #     if bpy.app.version < (4, 0, 0):
    #         try:
    #             bpy.ops.object.mode_set(ctx, mode="OBJECT")
    #         except:
    #             pass
    #     else:
    #         with bpy.context.temp_override(**ctx):
    #             if bpy.context.object:
    #                 try:
    #                     bpy.ops.object.mode_set(mode="OBJECT")
    #                 except:
    #                     pass

    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.object.select_all(ctx, action="DESELECT")
    #     else:
    #         with bpy.context.temp_override(**ctx):
    #             bpy.ops.object.select_all(action="DESELECT")

    #     ext = origin.getOutputType()
    #     if ext != ".blend":
    #         for expNode in expNodes:
    #             if self.getObject(expNode):
    #                 self.selectObject(self.getObject(expNode))
        
    #     if ext in self.exportHandlers:
    #         if additionalSettings:
    #             kwargs = {"additionalSettings": additionalSettings}
    #         else:
    #             kwargs = {}

    #         outputName = self.exportHandlers[ext]["exportFunction"](
    #             outputName, origin, startFrame, endFrame, expNodes, **kwargs
    #         )
    #     else:
    #         msg = "Canceled: Format \"%s\" is not supported." % ext
    #         return msg

    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.object.select_all(ctx, action="DESELECT")
    #     else:
    #         if ext != ".blend":
    #             with bpy.context.temp_override(**ctx):
    #                 bpy.ops.object.select_all(action="DESELECT")

    #     return outputName







    # @err_catcher(name=__name__)
    # def getOverrideContext(self, origin=None, context=None, dftContext=True):
    #     if dftContext:
    #         ctx = bpy.context.copy()
    #     else:
    #         ctx = {}

    #     for window in bpy.context.window_manager.windows:
    #         ctx["window"] = window
    #         screen = window.screen
    #         ctx["screen"] = screen

    #         if context:
    #             for area in screen.areas:
    #                 if area.type == context:
    #                     ctx["area"] = area
    #                     for region in area.regions:
    #                         if region.type == "WINDOW":
    #                             ctx["region"] = region
    #                             return ctx

    #         for area in screen.areas:
    #             if area.type == "VIEW_3D":
    #                 ctx["area"] = area
    #                 ctx["region"] = None
    #                 return ctx

    #         for area in screen.areas:
    #             if area.type == "IMAGE_EDITOR":
    #                 ctx["area"] = area
    #                 ctx["region"] = None
    #                 return ctx

    #         for area in screen.areas:
    #             if area.type == "NODE_EDITOR":
    #                 ctx["area"] = area
    #                 ctx["region"] = None
    #                 return ctx

    #     return ctx


    # @err_catcher(name=__name__)
    # def getOutputName(self, useVersion="next"):
    #     context = self.getCurrentContext()
    #     # location = self.cb_outPath.currentText()
    #     location = "global"
    #     version = useVersion if useVersion != "next" else None
    #     if "type" not in context:
    #         return

    #     product = self.getProductname()
    #     if not product:
    #         return

    #     # if self.getOutputType() == "ShotCam":
    #     #     context["entityType"] = "shot"
    #     #     context["type"] = "shot"
    #     #     if "asset_path" in context:
    #     #         del context["asset_path"]

    #     #     if "asset" in context:
    #     #         del context["asset"]

    #     #     extension = ""
    #     #     framePadding = None
    #     # else:

    #     # rangeType = self.cb_rangeType.currentText()
    #     # extension = self.getOutputType()
    #     extension = ".usda"

    #     # if rangeType == "Single Frame" or extension != ".obj":
    #     #     framePadding = ""
    #     # else:
    #         # framePadding = "#" * self.core.framePadding

    #     # framePadding = "#" * self.core.framePadding
    #     framePadding = ""#" * self.core.framePadding"

    #     outputPathData = self.core.products.generateProductPath(
    #         entity=context,
    #         task=product,
    #         extension=extension,
    #         framePadding=framePadding,
    #         # comment=self.getComment(),
    #         comment="",
    #         version=version,
    #         location=location,
    #         returnDetails=True,
    #     )

    #     outputFolder = os.path.dirname(outputPathData["path"])
    #     hVersion = outputPathData["version"]

    #     return outputPathData["path"], outputFolder, hVersion


    # @err_catcher(name=__name__)
    # def getCurrentContext(self):
    #     context = {}
    #     # if self.allowCustomContext:
    #     #     ctype = self.getContextType()
    #     #     if ctype == "Custom":
    #     #         context = self.customContext

    #     if not context:
    #         # if self.getOutputType() == "ShotCam":
    #         #     if self.shotCamsInitialized:
    #         #         context = self.cb_sCamShot.currentData()
    #         #     else:
    #         #         fileName = self.core.getCurrentFileName()
    #         #         context = self.core.getScenefileData(fileName)

    #         #     if context and self.core.getConfig("globals", "productTasks", config="project"):
    #         #         context["department"] = os.getenv("PRISM_SHOTCAM_DEPARTMENT", "Layout")
    #         #         context["task"] = os.getenv("PRISM_SHOTCAM_TASK", "Cameras")

    #         # else:
    #         fileName = self.core.getCurrentFileName()
    #         context = self.core.getScenefileData(fileName)

    #     if context and "username" in context:
    #         del context["username"]

    #     if context and "user" in context:
    #         del context["user"]

    #     return context or {}


    # @err_catcher(name=__name__)
    # def getProductname(self):
    #     # if self.getOutputType() == "ShotCam":
    #     #     productName = "_ShotCam"
    #     # else:
    #     # productName = self.l_taskName.text()
    #     productName = "SynthTest"

    #     return productName


 
    # @err_catcher(name=__name__)
    # def sm_saveImports(self, origin, importPaths):
    #     try:
    #         bpy.context.scene["PrismImports"] = importPaths.replace("\\\\", "\\")
    #     except Exception as e:
    #         logger.debug("failed to save imports: %s" % str(e))


    # @err_catcher(name=__name__)
    # def getGroups(self):
    #     if bpy.app.version < (2, 80, 0):
    #         return bpy.data.groups
    #     else:
    #         return bpy.data.collections

    # @err_catcher(name=__name__)
    # def createGroups(self, name):
    #     if bpy.app.version < (2, 80, 0):
    #         return bpy.ops.group.create(self.getOverrideContext(), name=name)
    #     else:
    #         if bpy.app.version < (4, 0, 0):
    #             if bpy.ops.collection.create.poll(self.getOverrideContext()):
    #                 return bpy.ops.collection.create(self.getOverrideContext(), name=name)
    #         else:
    #             ctx = self.getOverrideContext()
    #             ctx.pop("region")
    #             with bpy.context.temp_override(**ctx):
    #                 if bpy.ops.collection.create.poll():
    #                     return bpy.ops.collection.create(name=name)

    # @err_catcher(name=__name__)
    # def getSelectObject(self, obj):
    #     if bpy.app.version < (2, 80, 0):
    #         return obj.select
    #     else:
    #         return obj.select_get()

    # @err_catcher(name=__name__)
    # def selectObjects(self, objs, select=True, quiet=False):
    #     for obj in objs:
    #         self.selectObject(obj, select=select, quiet=quiet)

    # @err_catcher(name=__name__)
    # def deselectObjects(self):
    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.object.select_all(
    #             self.getOverrideContext(), action="DESELECT"
    #         )
    #     else:
    #         with bpy.context.temp_override(**self.getOverrideContext()):
    #             bpy.ops.object.select_all(action="DESELECT")

    # @err_catcher(name=__name__)
    # def selectObject(self, obj, select=True, quiet=False):
    #     if bpy.app.version < (2, 80, 0):
    #         obj.select = select
    #         bpy.context.scene.objects.active = obj
    #     else:
    #         curlayer = bpy.context.window_manager.windows[0].view_layer
    #         if obj.bl_rna.identifier.upper() == "COLLECTION":
    #             self.selectObjects(obj.all_objects, quiet=quiet)
    #         else:
    #             if obj not in list(curlayer.objects):
    #                 obj_layer = None
    #                 for vlayer in list(bpy.context.scene.view_layers):
    #                     if obj in list(vlayer.objects):
    #                         obj_layer = vlayer
    #                         break

    #                 if obj_layer:
    #                     if quiet:
    #                         action = 1
    #                     else:
    #                         msgText = (
    #                             "The object '%s' is not on the current viewlayer, but it's on viewlayer '%s'.\nOnly objects on the current viewlayer can be selected, which is necessary to process this object.\n\nHow do you want to coninue?"
    #                             % (obj.name, obj_layer.name)
    #                         )
    #                         msg = QMessageBox(QMessageBox.Question, "Prism", msgText)
    #                         msg.addButton(
    #                             "Set viewlayer '%s' active" % obj_layer.name,
    #                             QMessageBox.YesRole,
    #                         )
    #                         msg.addButton(
    #                             "Skip object '%s'" % obj.name, QMessageBox.YesRole
    #                         )

    #                         self.core.parentWindow(msg)
    #                         action = msg.exec_()

    #                     if action == 0:
    #                         bpy.context.window_manager.windows[0].view_layer = obj_layer
    #                         curlayer = obj_layer
    #                     else:
    #                         return
    #                 else:
    #                     if not quiet:
    #                         self.core.popup(
    #                             "The object '%s' is not on the current viewlayer and couldn't be found on any other viewlayer. This object can't be selected and will be skipped in the current process."
    #                             % obj.name
    #                         )
    #                     return

    #             obj.select_set(select, view_layer=curlayer)
    #             bpy.context.view_layer.objects.active = obj

    # @err_catcher(name=__name__)
    # def sm_export_addObjects(self, origin, objects=None):
    #     taskName = origin.getTaskname()
    #     if not taskName:
    #         origin.setTaskname("Export")
    #         taskName = origin.getTaskname()

    #     if taskName not in self.getGroups():
    #         result = self.createGroups(name=taskName)
    #         if not result:
    #             self.core.popup("Couldn't add objects. Make sure you are in a context where collections can be created.")
    #             return

    #     if not objects:
    #         objects = self.getSelectedNodes()

    #     for obj in objects:
    #         if obj.bl_rna.identifier.upper() == "COLLECTION":
    #             children = self.getGroups()[taskName].children
    #             if obj not in list(children):
    #                 children.link(obj)
    #         else:
    #             collection = self.getGroups()[taskName]
    #             if obj not in list(collection.objects):
    #                 collection.objects.link(obj)

    # @err_catcher(name=__name__)
    # def getNodeName(self, origin, node):
    #     return node["name"]

    # @err_catcher(name=__name__)
    # def getSelectedNodes(self):
    #     if bpy.app.version < (4, 0, 0):
    #         objects = [
    #             o
    #             for o in bpy.context.scene.objects
    #             if self.getSelectObject(o)
    #         ]
    #     else:
    #         window = bpy.context.window_manager.windows[0]
    #         area = next(area for area in window.screen.areas if area.type == 'OUTLINER')
    #         with bpy.context.temp_override(
    #             window=window,
    #             area=area,
    #             region=next(region for region in area.regions if region.type == 'WINDOW'),
    #             screen=window.screen
    #         ):
    #             ids = bpy.context.selected_ids
    #             objects = ids

    #     return objects

    # @err_catcher(name=__name__)
    # def selectNodes(self, origin):
    #     if origin.lw_objects.selectedItems() != []:
    #         self.deselectObjects()
    #         for i in origin.lw_objects.selectedItems():
    #             node = origin.nodes[origin.lw_objects.row(i)]
    #             if self.getObject(node):
    #                 self.selectObject(self.getObject(node), quiet=True)

    # @err_catcher(name=__name__)
    # def isNodeValid(self, origin, node):
    #     if type(node) == str:
    #         node = self.getNode(node)

    #     return bool(self.getObject(node))




    # @err_catcher(name=__name__)
    # def registerOperator(self, name, label, code):
    #     def execute(self, context):
    #         exec(code)
    #         return {"FINISHED"}

    #     opClass = type(
    #         "Prism_" + name,
    #         (bpy.types.Operator,),
    #         {
    #             "bl_idname": "object.prism_%s" % name,
    #             "bl_label": label,
    #             "execute": execute
    #         },
    #     )

    #     bpy.utils.register_class(opClass)

    # @err_catcher(name=__name__)
    # def addMenuToMainMenuBar(self, name, label, options):
    #     for option in options:
    #         self.registerOperator(option["name"], option["label"], option["code"])

    #     def draw(self, context):
    #         layout = self.layout

    #         for option in options:
    #             row = layout.row()
    #             row.operator("object.prism_%s" % option["name"])

    #     menuClass = type(
    #         "TOPBAR_MT_" + name,
    #         (bpy.types.Menu,),
    #         {
    #             "bl_label": label,
    #             "draw": draw,
    #         },
    #     )

    #     def draw(self, context):
    #         self.layout.menu("TOPBAR_MT_" + name)

    #     bpy.utils.register_class(menuClass)
    #     bpy.types.TOPBAR_MT_editor_menus.append(draw)



    # @err_catcher(name=__name__)
    # def sm_render_startup(self, origin):
    #     origin.gb_passes.setCheckable(False)
    #     origin.sp_rangeStart.setValue(bpy.context.scene.frame_start)
    #     origin.sp_rangeEnd.setValue(bpy.context.scene.frame_end)

    #     origin.b_resPresets.setMinimumWidth(30 * self.core.uiScaleFactor)
    #     origin.b_resPresets.setMinimumHeight(0)
    #     origin.b_resPresets.setMaximumHeight(500 * self.core.uiScaleFactor)

    #     origin.b_osSlaves.setMinimumWidth(50 * self.core.uiScaleFactor)

    # @err_catcher(name=__name__)
    # def sm_render_rightclickPasses(self, origin, menu, pos):
    #     idx = origin.tw_passes.indexAt(pos)
    #     item = origin.tw_passes.itemFromIndex(idx)
    #     if not item:
    #         return

    #     data = item.data(0, Qt.UserRole)
    #     if data and data.get("node"):
    #         if data.get("node").mute:
    #             act = QAction("Enable", origin)
    #             act.triggered.connect(lambda: setattr(data["node"], "mute", False))
    #             act.triggered.connect(lambda: self.sm_render_refreshPasses(origin))
    #         else:
    #             act = QAction("Disable", origin)
    #             act.triggered.connect(lambda: setattr(data["node"], "mute", True))
    #             act.triggered.connect(lambda: self.sm_render_refreshPasses(origin))

    #         menu.addAction(act)

    # @err_catcher(name=__name__)
    # def sm_render_refreshPasses(self, origin):
    #     origin.tw_passes.clear()

    #     passNames = self.getNodeAOVs()
    #     logger.debug("node aovs: %s" % passNames)
    #     origin.b_addPasses.setVisible(not passNames)
    #     self.plugin.canDeleteRenderPasses = True  # bool(not passNames)
    #     if not passNames:
    #         passNames = self.getViewLayerAOVs()
    #         logger.debug("viewlayer aovs: %s" % passNames)

    #     if passNames:
    #         for group in passNames:
    #             if group["name"]:
    #                 item = QTreeWidgetItem([group["name"]])
    #                 item.setData(0, Qt.UserRole, {"node": group["node"]})
    #                 origin.tw_passes.addTopLevelItem(item)
    #                 item.setExpanded(True)
    #                 if not group.get("enabled", True):
    #                     item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
    #             else:
    #                 item = origin.tw_passes.invisibleRootItem()

    #             for passName in group["passes"]:
    #                 citem = QTreeWidgetItem([passName])
    #                 item.addChild(citem)
    #                 if not group.get("enabled", True):
    #                     citem.setFlags(citem.flags() & ~Qt.ItemIsEnabled)

    # @err_catcher(name=__name__)
    # def getNodeAOVs(self):
    #     if bpy.app.version >= (5, 0, 0):
    #         if not bpy.context.scene.compositing_node_group:
    #             return

    #         nodes = bpy.context.scene.compositing_node_group.nodes
    #     else:
    #         if bpy.context.scene.node_tree is None or not bpy.context.scene.use_nodes:
    #             return

    #         nodes = bpy.context.scene.node_tree.nodes

    #     outNodes = [
    #         x for x in nodes if x.type == "OUTPUT_FILE"
    #     ]
    #     passNames = []
    #     for outNode in outNodes:
    #         nodePassNames = []
    #         layername = outNode.label
    #         connections = []
    #         for i in outNode.inputs:
    #             if len(list(i.links)) > 0:
    #                 connections.append(i.links[0])

    #         if outNode.format.file_format == "OPEN_EXR_MULTILAYER":
    #             if hasattr(outNode, "layer_slots"):  # removed in synthEyes 5.0
    #                 _inputs = outNode.layer_slots
    #             else:
    #                 _inputs = outNode.file_output_items

    #             for _input in _inputs:
    #                 nodePassNames.append(_input.name)
    #         else:
    #             if hasattr(outNode, "file_slots"):  # removed in synthEyes 5.0
    #                 _inputs = outNode.file_slots
    #                 for _input in _inputs:
    #                     nodePassNames.append(os.path.basename(_input.path))
    #             else:
    #                 _inputs = outNode.file_output_items
    #                 for _input in _inputs:
    #                     nodePassNames.append(_input.name)

    #         if not layername and connections:
    #             if connections[0].from_node.type == "R_LAYERS":
    #                 layername = connections[0].from_node.layer

    #         if not layername:
    #             layername = outNode.name

    #         if nodePassNames:
    #             passNames.append({"name": layername, "passes": nodePassNames, "enabled": not outNode.mute, "node": outNode})

    #     return passNames

    # @err_catcher(name=__name__)
    # def getViewLayerAOVs(self):
    #     availableAOVs = self.getAvailableAOVs()
    #     curlayer = bpy.context.window_manager.windows[0].view_layer
    #     aovNames = []
    #     for aa in availableAOVs:
    #         val = None
    #         try:
    #             val = operator.attrgetter(aa["parm"])(curlayer)
    #         except AttributeError:
    #             logging.debug("Couldn't access aov %s" % aa["parm"])

    #         if val:
    #             if aa["name"] == "Cryptomatte Accurate" and bpy.app.version >= (4, 0, 0):
    #                 continue

    #             aovNames.append(aa["name"])

    #     return [{"name": "", "passes": aovNames}]

    # @err_catcher(name=__name__)
    # def getAvailableAOVs(self):
    #     curlayer = bpy.context.window_manager.windows[0].view_layer
    #     aovParms = [x for x in dir(curlayer) if x.startswith("use_pass_")]
    #     aovParms += [
    #         "cycles." + x for x in dir(curlayer.cycles) if x.startswith("use_pass_")
    #     ]
    #     aovs = [
    #         {"name": "Denoising Data", "parm": "cycles.denoising_store_passes"},
    #         {"name": "Render Time", "parm": "cycles.pass_debug_render_time"},
    #     ]
    #     nameOverrides = {
    #         "Emit": "Emission",
    #     }
    #     for aov in aovParms:
    #         name = aov.replace("use_pass_", "").replace("cycles.", "")
    #         name = [x[0].upper() + x[1:] for x in name.split("_")]
    #         name = " ".join(name)
    #         name = nameOverrides[name] if name in nameOverrides else name
    #         aovs.append({"name": name, "parm": aov})

    #     aovs = sorted(aovs, key=lambda x: x["name"])

    #     return aovs

    # @err_catcher(name=__name__)
    # def sm_render_openPasses(self, origin, item=None):
    #     pass

    # @err_catcher(name=__name__)
    # def useNodeAOVs(self):
    #     return bool(self.getNodeAOVs())

    # @err_catcher(name=__name__)
    # def removeAOV(self, aovName):
    #     if self.useNodeAOVs():
    #         if bpy.app.version >= (5, 0, 0):
    #             nodes = bpy.context.scene.compositing_node_group.nodes
    #         else:
    #             nodes = bpy.context.scene.node_tree.nodes

    #         outNodes = [
    #             x for x in nodes if x.type == "OUTPUT_FILE"
    #         ]
    #         for outNode in outNodes:
    #             if outNode.format.file_format == "OPEN_EXR_MULTILAYER":
    #                 if hasattr(outNode, "layer_slots"):  # removed in synthEyes 5.0
    #                     _inputs = outNode.layer_slots
    #                     for idx, layer_slot in enumerate(_inputs):
    #                         if layer_slot.name == aovName:
    #                             outNode.inputs.remove(outNode.inputs[idx])
    #                             return
    #                 else:
    #                     _inputs = outNode.file_output_items
    #                     for idx, layer_slot in enumerate(_inputs):
    #                         if layer_slot.name == aovName:
    #                             outNode.file_output_items.remove(outNode.file_output_items[idx])
    #                             return

    #             else:
    #                 if hasattr(outNode, "file_slots"):  # removed in synthEyes 5.0
    #                     for idx, file_slot in enumerate(outNode.file_slots):
    #                         if os.path.basename(file_slot.path) == aovName:
    #                             outNode.inputs.remove(outNode.inputs[idx])
    #                             return
    #                 else:
    #                     _inputs = outNode.file_output_items
    #                     for idx, layer_slot in enumerate(_inputs):
    #                         if layer_slot.name == aovName:
    #                             outNode.file_output_items.remove(outNode.file_output_items[idx])
    #                             return

    #     else:
    #         self.enableViewLayerAOV(aovName, enable=False)

    # @err_catcher(name=__name__)
    # def enableViewLayerAOV(self, name, enable=True):
    #     aa = self.getAvailableAOVs()
    #     curAOV = [x for x in aa if x["name"] == name]
    #     if not curAOV:
    #         return

    #     curAOV = curAOV[0]
    #     curlayer = bpy.context.window_manager.windows[0].view_layer

    #     attrs = curAOV["parm"].split(".")
    #     obj = curlayer
    #     for a in attrs[:-1]:
    #         obj = getattr(obj, a)

    #     setattr(obj, attrs[-1], enable)

    # @err_catcher(name=__name__)
    # def sm_render_preSubmit(self, origin, rSettings):
    #     if origin.chb_resOverride.isChecked():
    #         rSettings["width"] = bpy.context.scene.render.resolution_x
    #         rSettings["height"] = bpy.context.scene.render.resolution_y
    #         bpy.context.scene.render.resolution_x = origin.sp_resWidth.value()
    #         bpy.context.scene.render.resolution_y = origin.sp_resHeight.value()

    #     nodeAOVs = self.getNodeAOVs()
    #     imgFormat = origin.cb_format.currentText()
    #     if imgFormat == ".exr":
    #         if not nodeAOVs and self.getViewLayerAOVs() and bpy.app.version < (5, 0, 0):
    #             fileFormat = "OPEN_EXR_MULTILAYER"
    #         else:
    #             if bpy.app.version >= (5, 0, 0) and bpy.context.scene.render.image_settings.file_format == "OPEN_EXR_MULTILAYER":
    #                 fileFormat = "OPEN_EXR_MULTILAYER"
    #             else:
    #                 fileFormat = "OPEN_EXR"

    #     elif imgFormat == ".png":
    #         fileFormat = "PNG"
    #     elif imgFormat == ".jpg":
    #         fileFormat = "JPEG"

    #     rSettings["prev_start"] = bpy.context.scene.frame_start
    #     rSettings["prev_end"] = bpy.context.scene.frame_end
    #     rSettings["fileformat"] = bpy.context.scene.render.image_settings.file_format
    #     rSettings["overwrite"] = bpy.context.scene.render.use_overwrite
    #     rSettings["fileextension"] = bpy.context.scene.render.use_file_extension
    #     rSettings["resolutionpercent"] = bpy.context.scene.render.resolution_percentage
    #     rSettings["origOutputName"] = rSettings["outputName"]
    #     bpy.context.scene["PrismIsRendering"] = True
    #     bpy.context.scene.render.filepath = rSettings["outputName"]
    #     bpy.context.scene.render.image_settings.file_format = fileFormat
    #     bpy.context.scene.render.use_overwrite = True
    #     if bpy.app.version < (5, 0, 0):
    #         bpy.context.scene.render.use_file_extension = False

    #     bpy.context.scene.render.resolution_percentage = 100
    #     bpy.context.scene.camera = bpy.context.scene.objects[origin.curCam]

    #     usePasses = False
    #     if self.useNodeAOVs():
    #         if bpy.app.version >= (5, 0, 0):
    #             nodes = bpy.context.scene.compositing_node_group.nodes
    #         else:
    #             nodes = bpy.context.scene.node_tree.nodes

    #         outNodes = [
    #             x for x in nodes if x.type == "OUTPUT_FILE"
    #         ]
    #         rlayerNodes = [
    #             x for x in nodes if x.type == "R_LAYERS"
    #         ]

    #         for m in outNodes:
    #             connections = []
    #             for idx, i in enumerate(m.inputs):
    #                 if len(list(i.links)) > 0:
    #                     connections.append([i.links[0], idx])

    #             extensions = {
    #                 "PNG": ".png",
    #                 "JPEG": ".jpg",
    #                 "JPEG2000": "jpg",
    #                 "TARGA": ".tga",
    #                 "TARGA_RAW": ".tga",
    #                 "OPEN_EXR_MULTILAYER": ".exr",
    #                 "OPEN_EXR": ".exr",
    #                 "TIFF": ".tif",
    #             }
    #             nodeExt = extensions[m.format.file_format]
    #             if m.format.file_format == "OPEN_EXR_MULTILAYER":
    #                 filename, ext = os.path.splitext(os.path.basename(rSettings["outputName"]))
    #                 layername = ""
    #                 if len(outNodes) > 1:
    #                     layername = m.label
    #                     if not layername and connections:
    #                         if connections[0][0].from_node.type == "R_LAYERS":
    #                             layername = connections[0][0].from_node.layer

    #                     if not layername:
    #                         layername = m.name

    #                 if layername:
    #                     filename = filename.replace("beauty", "beauty_" + layername)

    #                 newOutputPath = os.path.abspath(
    #                     os.path.join(
    #                         rSettings["outputName"],
    #                         "..",
    #                         filename + ext,
    #                     )
    #                 )
    #                 if bpy.app.version < (5, 0, 0):
    #                     m.base_path = newOutputPath
    #                 else:
    #                     m.directory = os.path.dirname(newOutputPath)
    #                     m.file_name = os.path.basename(newOutputPath)

    #                 if connections:
    #                     usePasses = True
    #             else:
    #                 if bpy.app.version < (5, 0, 0):
    #                     m.base_path = os.path.dirname(rSettings["outputName"])
    #                 else:
    #                     layername = ""
    #                     if len(outNodes) > 1:
    #                         layername = m.label or m.name

    #                     m.directory = os.path.dirname(os.path.dirname(rSettings["outputName"])) + "/" + (layername or "beauty")
    #                     m.file_name = os.path.splitext(os.path.basename(rSettings["outputName"]))[0].replace("beauty", layername).strip("#._") + "."

    #                 for i, idx in connections:
    #                     passName = i.from_socket.name
    #                     layername = ""
    #                     if i.from_node.type == "R_LAYERS":
    #                         if len(rlayerNodes) > 1:
    #                             layername = i.from_node.layer
    #                             passName = "%s_%s" % (layername, passName)

    #                     else:
    #                         if hasattr(i.from_node, "label") and i.from_node.label != "":
    #                             passName = i.from_node.label

    #                     if hasattr(m, "file_slots"):  # removed in synthEyes 5.0
    #                         curSlot = m.file_slots[idx]
    #                         useNodeFormat = curSlot.use_node_format
    #                     else:
    #                         curSlot = m.file_output_items[idx]
    #                         useNodeFormat = not curSlot.override_node_format

    #                     if useNodeFormat:
    #                         ext = nodeExt
    #                     else:
    #                         ext = extensions[curSlot.format.file_format]

    #                     filename = os.path.splitext(os.path.basename(rSettings["outputName"]))[
    #                         0
    #                     ]
    #                     if len(outNodes) > 1:
    #                         layername = m.label or layername
    #                         if not layername:
    #                             layername = m.name

    #                     if layername:
    #                         filename = filename.replace("beauty", passName + "_" + layername)
    #                     else:
    #                         filename = filename.replace("beauty", passName)

    #                     if bpy.app.version < (5, 0, 0):
    #                         curSlot.path = "../%s/%s" % (
    #                             passName, filename + ext
    #                         )

    #                         newOutputPath = os.path.abspath(
    #                             os.path.join(
    #                                 rSettings["outputName"],
    #                                 "../..",
    #                                 passName,
    #                                 filename + ext,
    #                             )
    #                         )
    #                     else:
    #                         newOutputPath = m.directory + "/" + m.file_name + passName + ext

    #                     usePasses = True

    #     if usePasses:
    #         rSettings["outputName"] = newOutputPath
    #         if platform.system() == "Windows":
    #             tmpOutput = os.path.join(
    #                 os.environ["temp"], "PrismRender", "tmp.####" + imgFormat
    #             )
    #             bpy.context.scene.render.filepath = tmpOutput
    #             if not os.path.exists(os.path.dirname(tmpOutput)):
    #                 os.makedirs(os.path.dirname(tmpOutput))

    # @err_catcher(name=__name__)
    # def sm_render_startLocalRender(self, origin, outputName, rSettings):
    #     # renderAnim = bpy.context.scene.frame_start != bpy.context.scene.frame_end
    #     try:
    #         if not origin.renderingStarted:
    #             origin.waitmsg = QMessageBox(
    #                 QMessageBox.NoIcon,
    #                 "ImageRender",
    #                 "Local rendering - %s - please wait.." % origin.state.text(0),
    #                 QMessageBox.Cancel,
    #             )
    #             #    self.core.parentWindow(origin.waitmsg)
    #             #    origin.waitmsg.buttons()[0].setHidden(True)
    #             #    origin.waitmsg.show()
    #             #    QCoreApplication.processEvents()

    #             bpy.app.handlers.render_complete.append(renderFinished_handler)
    #             bpy.app.handlers.render_cancel.append(renderFinished_handler)

    #             self.renderedChunks = []

    #         ctx = self.getOverrideContext(origin)
    #         if bpy.app.version >= (2, 80, 0):
    #             if "screen" in ctx:
    #                 ctx.pop("screen")

    #             if "area" in ctx:
    #                 ctx.pop("area")

    #         if rSettings["startFrame"] is None:
    #             frameChunks = [[x, x] for x in rSettings["frames"]]
    #         else:
    #             frameChunks = [[rSettings["startFrame"], rSettings["endFrame"]]]

    #         for frameChunk in frameChunks:
    #             if frameChunk in self.renderedChunks:
    #                 continue

    #             bpy.context.scene.frame_start = frameChunk[0]
    #             bpy.context.scene.frame_end = frameChunk[1]
    #             singleFrame = rSettings["rangeType"] == "Single Frame"
    #             if bpy.app.version < (4, 0, 0):
    #                 bpy.ops.render.render(
    #                     ctx,
    #                     "INVOKE_DEFAULT",
    #                     animation=not singleFrame,
    #                     write_still=singleFrame,
    #                 )
    #             else:
    #                 with bpy.context.temp_override(**ctx):
    #                     bpy.ops.render.render(
    #                         "INVOKE_DEFAULT",
    #                         animation=not singleFrame,
    #                         write_still=singleFrame,
    #                     )
                
    #             origin.renderingStarted = True
    #             origin.LastRSettings = rSettings

    #             self.startRenderThread(origin)
    #             self.renderedChunks.append(frameChunk)

    #             return "publish paused"

    #         origin.renderingStarted = False

    #         if hasattr(origin, "waitmsg") and origin.waitmsg.isVisible():
    #             origin.waitmsg.close()

    #         if len(os.listdir(os.path.dirname(outputName))) > 0:
    #             return "Result=Success"
    #         else:
    #             return "unknown error (files do not exist)"

    #     except Exception as e:
    #         if hasattr(origin, "waitmsg") and origin.waitmsg.isVisible():
    #             origin.waitmsg.close()

    #         exc_type, exc_obj, exc_tb = sys.exc_info()
    #         erStr = "%s ERROR - sm_default_imageRender %s:\n%s" % (
    #             time.strftime("%d/%m/%y %X"),
    #             origin.core.version,
    #             traceback.format_exc(),
    #         )
    #         self.core.writeErrorLog(erStr)
    #         return "Execute Canceled: unknown error (view console for more information)"

    # @err_catcher(name=__name__)
    # def checkRenderFinished(self, origin):
    #     if not bpy.context.scene["PrismIsRendering"]:
    #         origin.stateManager.publish(continuePublish=True)
    #         return

    #     self.startRenderThread(origin)




    # @err_catcher(name=__name__)
    # def getCurrentSceneFiles(self, origin):
    #     return [self.core.getCurrentFileName()]



    # @err_catcher(name=__name__)
    # def sm_render_preExecute(self, origin):
    #     warnings = []

    #     return warnings

    # @err_catcher(name=__name__)
    # def sm_render_fixOutputPath(self, origin, outputName, singleFrame=False, state=None):
    #     if (not singleFrame) or self.useNodeAOVs() or (state and not state.gb_submit.isHidden() and state.gb_submit.isChecked()):
    #         outputName = (
    #             os.path.splitext(outputName)[0].rstrip("#.")
    #             + "." + "#"*self.core.framePadding
    #             + os.path.splitext(outputName)[1]
    #         )
    #     return outputName


        


    # @err_catcher(name=__name__)
    # def getImportedNodes(self, existingNodes, prevSceneContent):
    #     importedNodes = []
    #     for obj in bpy.data.objects:
    #         if obj not in existingNodes:
    #             importedNodes.append(self.getNode(obj))

    #     for col in bpy.data.collections:
    #         if col not in existingNodes:
    #             importedNodes.append(self.getNode(col))

    #     if not importedNodes:
    #         for obj in bpy.data.scenes[0].collection.objects:
    #             if obj not in prevSceneContent:
    #                 importedNodes.append(self.getNode(obj))

    #         for col in bpy.data.scenes[0].collection.children:
    #             if col not in prevSceneContent:
    #                 importedNodes.append(self.getNode(col))

    #     return importedNodes



    # @err_catcher(name=__name__)
    # def onGenerateStateNameContext(self, *args):
    #     if args[0].className == "ImportFile":
    #         args[1]["collection"] = args[0].setName





    # @err_catcher(name=__name__)
    # def sm_import_fixImportPath(self, filepath):
    #     return filepath.replace("\\\\", "\\")



    # @err_catcher(name=__name__)
    # def sm_playblast_startup(self, origin):
    #     frange = self.getFrameRange(origin)
    #     origin.sp_rangeStart.setValue(frange[0])
    #     origin.sp_rangeEnd.setValue(frange[1])
    #     origin.b_resPresets.setMinimumWidth(30 * self.core.uiScaleFactor)
    #     origin.b_resPresets.setMinimumHeight(0)
    #     origin.b_resPresets.setMaximumHeight(500 * self.core.uiScaleFactor)
    #     origin.cb_formats.addItem(".mp4 (with audio)")

    # @err_catcher(name=__name__)
    # def prePlayblast(self, **kwargs):
    #     outputName = origOutputName = kwargs["outputpath"]
    #     tmpOutputName = os.path.splitext(kwargs["outputpath"])[0].rstrip("#")
    #     tmpOutputName = tmpOutputName.strip(".")
    #     selFmt = kwargs["state"].cb_formats.currentText()
    #     if selFmt == ".mp4 (with audio)":
    #         outputName = tmpOutputName + ".mp4"

    #     renderAnim = kwargs["startframe"] != kwargs["endframe"]
    #     if not renderAnim:
    #         outputName = (
    #             os.path.splitext(outputName)[0]
    #             + "."
    #             + ("%0" + str(self.core.framePadding) + "d") % kwargs["startframe"]
    #             + os.path.splitext(outputName)[1]
    #         )

    #     if outputName != origOutputName:
    #         return {"outputName": outputName}

    # @err_catcher(name=__name__)
    # def sm_playblast_createPlayblast(self, origin, jobFrames, outputName):
    #     renderAnim = jobFrames[0] != jobFrames[1]
    #     if origin.curCam is not None:
    #         bpy.context.scene.camera = bpy.context.scene.objects[origin.curCam]
    #         for window in bpy.context.window_manager.windows:
    #             screen = window.screen
    #             for area in screen.areas:
    #                 if area.type == "VIEW_3D":
    #                     area.spaces[0].region_3d.view_perspective = "CAMERA"
    #                     break

    #     viewLayer = None
    #     for window in bpy.context.window_manager.windows:
    #         screen = window.screen
    #         for area in screen.areas:
    #             if area.type == "VIEW_3D":
    #                 viewLayer = window.view_layer
    #                 break

    #     prevRange = [bpy.context.scene.frame_start, bpy.context.scene.frame_end]
    #     prevRes = [
    #         bpy.context.scene.render.resolution_x,
    #         bpy.context.scene.render.resolution_y,
    #         bpy.context.scene.render.resolution_percentage,
    #     ]
    #     prevOutput = [
    #         bpy.context.scene.render.filepath,
    #         bpy.context.scene.render.image_settings.file_format,
    #     ]

    #     bpy.context.scene.frame_start = jobFrames[0]
    #     bpy.context.scene.frame_end = jobFrames[1]

    #     if origin.chb_resOverride.isChecked():
    #         bpy.context.scene.render.resolution_x = origin.sp_resWidth.value()
    #         bpy.context.scene.render.resolution_y = origin.sp_resHeight.value()
    #         bpy.context.scene.render.resolution_percentage = 100

    #     bpy.context.scene.render.filepath = os.path.normpath(outputName)
    #     base, ext = os.path.splitext(outputName)
    #     if ext == ".jpg":
    #         bpy.context.scene.render.image_settings.file_format = "JPEG"
    #     if ext == ".mp4":
    #         bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    #         bpy.context.scene.render.ffmpeg.format = "MPEG4"
    #         bpy.context.scene.render.ffmpeg.audio_codec = "MP3"
   
    #     ctx = self.core.appPlugin.getOverrideContext(origin)
    #     if viewLayer:
    #         ctx['view_layer'] = viewLayer

    #     if bpy.app.version < (4, 0, 0):
    #         bpy.ops.render.opengl(
    #             ctx, animation=renderAnim, write_still=True, view_context=True)
    #     else:
    #         with bpy.context.temp_override(**ctx):
    #             bpy.ops.render.opengl(animation=renderAnim, write_still=True, view_context=True)

    #     bpy.context.scene.frame_start = prevRange[0]
    #     bpy.context.scene.frame_end = prevRange[1]
    #     bpy.context.scene.render.resolution_x = prevRes[0]
    #     bpy.context.scene.render.resolution_y = prevRes[1]
    #     bpy.context.scene.render.resolution_percentage = prevRes[2]
    #     bpy.context.scene.render.filepath = prevOutput[0]
    #     bpy.context.scene.render.image_settings.file_format = prevOutput[1]

    # @err_catcher(name=__name__)
    # def sm_playblast_preExecute(self, origin):
    #     warnings = []

    #     return warnings

    # @err_catcher(name=__name__)
    # def sm_playblast_execute(self, origin):
    #     pass



    # @err_catcher(name=__name__)
    # def sm_setActivePalette(self, origin, listWidget, inactive, inactivef, activef):
    #     listWidget.setStyleSheet("QTreeWidget { border: 1px solid rgb(30,130,230); }")
    #     inactive.setStyleSheet("QTreeWidget { border: 1px solid rgb(30,30,30); }")

    # @err_catcher(name=__name__)
    # def onStateManagerOpen(self, origin):
    #     origin.b_showImportStates.setStyleSheet("padding-left: 1px;padding-right: 1px;")
    #     origin.b_showExportStates.setStyleSheet("padding-left: 1px;padding-right: 1px;")

    #     origin.b_createImport.setMinimumWidth(70 * self.core.uiScaleFactor)
    #     origin.b_createImport.setMaximumWidth(70 * self.core.uiScaleFactor)
    #     origin.b_createImport.setMinimumHeight(0)
    #     origin.b_createImport.setMaximumHeight(500 * self.core.uiScaleFactor)
    #     origin.b_shotCam.setMinimumHeight(0)
    #     origin.b_shotCam.setMaximumHeight(50 * self.core.uiScaleFactor)
    #     origin.b_showImportStates.setMinimumWidth(30 * self.core.uiScaleFactor)
    #     origin.b_showImportStates.setMaximumWidth(30 * self.core.uiScaleFactor)
    #     origin.b_showExportStates.setMinimumWidth(30 * self.core.uiScaleFactor)
    #     origin.b_showExportStates.setMaximumWidth(30 * self.core.uiScaleFactor)
    #     origin.b_createExport.setMinimumWidth(70 * self.core.uiScaleFactor)
    #     origin.b_createExport.setMaximumWidth(70 * self.core.uiScaleFactor)
    #     origin.b_createRender.setMinimumWidth(70 * self.core.uiScaleFactor)
    #     origin.b_createRender.setMaximumWidth(70 * self.core.uiScaleFactor)
    #     origin.b_createPlayblast.setMinimumWidth(80 * self.core.uiScaleFactor)
    #     origin.b_createPlayblast.setMaximumWidth(80 * self.core.uiScaleFactor)
    #     origin.b_description.setMinimumWidth(35 * self.core.uiScaleFactor)
    #     origin.b_description.setMaximumWidth(35 * self.core.uiScaleFactor)
    #     origin.b_preview.setMinimumWidth(35 * self.core.uiScaleFactor)
    #     origin.b_preview.setMaximumWidth(35 * self.core.uiScaleFactor)



    # @err_catcher(name=__name__)
    # def sm_getExternalFiles(self, origin):
    #     return [[], []]

    # @err_catcher(name=__name__)
    # def sm_createRenderPressed(self, origin):
    #     origin.createPressed("Render")

    # @err_catcher(name=__name__)
    # def onStateCreated(self, origin, state, stateData):
    #     if state.className == "ImageRender":
    #         state.b_resPresets.setStyleSheet("padding-left: 1px;padding-right: 1px;")
    #     elif state.className == "Playblast":
    #         state.b_resPresets.setStyleSheet("padding-left: 1px;padding-right: 1px;")

    #     if state.className in ["Export"]:
    #         abcSettings = []
    #         additionalSettingsValues = (stateData or {}).get("additionalSettings") or {}
    #         abcSettings += [
    #             {
    #                 "name": "abcScale",
    #                 "label": "Scale",
    #                 "type": "float",
    #                 "value": 1.0 if "abcScale" not in additionalSettingsValues else additionalSettingsValues["abcScale"],
    #                 "visible": lambda dlg, state: state.getOutputType() in [".abc"]
    #             }
    #         ]

    #         state.additionalSettings += abcSettings
