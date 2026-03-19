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


import os
import logging

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher


logger = logging.getLogger(__name__)

#   Icon to be used for State
scriptDir = os.path.dirname(os.path.dirname(__file__))
STATE_ICON = os.path.join(scriptDir, "Icons", "Geo.png")


class Synth_ImportMeshClass(object):
    className = "Synth_ImportMesh"
    listType = "Import"

    @err_catcher(name=__name__)
    def setup(
        self,
        state,
        core,
        stateManager,
        node=None,
        importPath=None,
        stateData=None,
        openProductsBrowser=True,
        settings=None,
    ):
        
        #   Checks if the ATTR Already Exists and Assigns if Not
        self.core = getattr(self, "core", core)
        self.state = getattr(self, "state", state)
        self.stateManager = getattr(self, "stateManager", stateManager)
        self.synthFuncts = getattr(self, "synthFuncts", self.core.appPlugin)
        self.synthEyes = self.synthFuncts.synthEyes

        self.state = state
        self.stateMode = "Synth_ImportMesh"

        self.core = core
        self.stateManager = stateManager
        self.taskName = ""
        self.setName = ""
        self.meshUUID = None

        stateNameTemplate = "{entity}_{product}_{version}"
        self.stateNameTemplate = self.core.getConfig(
            "globals",
            "defaultImportStateName",
            configPath=self.core.prismIni,
        ) or stateNameTemplate
        self.e_name.setText(self.stateNameTemplate)
        self.l_name.setVisible(False)
        self.e_name.setVisible(False)

        # self.f_abcPath.setVisible(False)
        # self.f_keepRefEdits.setVisible(False)

        self.oldPalette = self.b_importLatest.palette()
        self.updatePalette = QPalette()
        self.updatePalette.setColor(QPalette.Button, QColor(200, 100, 0))
        self.updatePalette.setColor(QPalette.ButtonText, QColor(255, 255, 255))

        createEmptyState = (
            QApplication.keyboardModifiers() == Qt.ControlModifier
            or not self.core.uiAvailable
        ) or not openProductsBrowser

        if (
            importPath is None
            and stateData is None
            and not createEmptyState
            and not self.stateManager.standalone
        ):
            importPaths = self.requestImportPaths()
           
            if importPaths:
                importPath = importPaths[-1]
                if len(importPaths) > 1:
                    for impPath in importPaths[:-1]:
                        stateManager.importFile(impPath)

        if importPath:
            self.setImportPath(importPath)
            result = self.importObject(settings=settings)

            if not result:
                return False
        elif (
            stateData is None
            and not createEmptyState
            and not self.stateManager.standalone
        ):
            return False

        getattr(self.core.appPlugin, "sm_import_startup", lambda x: None)(self)
        self.connectEvents()

        if stateData is not None:
            self.loadData(stateData)

        self.nameChanged()
        self.updateUi()


    @err_catcher(name=__name__)
    def setStateMode(self, stateMode):
        self.stateMode = stateMode
        self.l_class.setText(stateMode)


    @err_catcher(name=__name__)
    def requestImportPaths(self):
        #####################################################
        ### DISABLED AS IT DISPLAYS BEHIND STATEMANAGER   ###

        # result = self.core.callback("requestImportPath", self.stateManager)
        # for res in result:
        #     if isinstance(res, dict) and res.get("importPaths") is not None:
        #         return res["importPaths"]

        #####################################################

        import ProductBrowser
        ts = ProductBrowser.ProductBrowser(core=self.core, importState=self)
        self.core.parentWindow(ts)

        ts.exec_()
        importPath = [ts.productPath]
        return importPath


    @err_catcher(name=__name__)
    def loadData(self, data):
        if "statename" in data:
            self.e_name.setText(data["statename"])
        if "statemode" in data:
            self.setStateMode(data["statemode"])
        if "meshUUID" in data:
            self.meshUUID = data["meshUUID"]
        if "filepath" in data:
            data["filepath"] = getattr(
                self.core.appPlugin, "sm_import_fixImportPath", lambda x: x
            )(data["filepath"])
            self.setImportPath(data["filepath"])
        if "taskname" in data:
            self.taskName = data["taskname"]
        if "setname" in data:
            self.setName = data["setname"]
        if "autoUpdate" in data:
            self.chb_autoUpdate.setChecked(eval(data["autoUpdate"]))

        self.core.callback("onStateSettingsLoaded", self, data)


    @err_catcher(name=__name__)
    def connectEvents(self):
        self.e_name.textChanged.connect(self.nameChanged)
        self.e_name.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.b_browse.clicked.connect(self.browse)
        self.b_browse.customContextMenuRequested.connect(self.openFolder)
        self.b_import.clicked.connect(lambda: self.importObject(update=True))
        self.b_importLatest.clicked.connect(self.importLatest)
        self.chb_autoUpdate.stateChanged.connect(self.autoUpdateChanged)
        self.e_meshName.editingFinished.connect(
            lambda: self.updateMeshName(self.e_meshName.text())
            )


    #   Set State Name and Icon
    @err_catcher(name=__name__)
    def nameChanged(self, text=None):
        name = self.e_name.text()

        if text:
            name = text
        else:
            try:
                impFileName = self.getImportPath()
                impFileName = os.path.normpath(impFileName)
                productData = self.core.products.getProductDataFromFilepath(impFileName)
                name = productData['product']

            except Exception as e:
                name = text

        #   Set the name for the State list
        self.e_name.setText(name)
        self.state.setText(0, name)

        #   Add icon to State name
        self.state.setIcon(0, QIcon(STATE_ICON))

        self.stateManager.saveImports()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def getSortKey(self):
        cacheData = self.core.paths.getCachePathData(self.getImportPath())
        return cacheData.get("product")


    @err_catcher(name=__name__)
    def browse(self):
        import ProductBrowser

        ts = ProductBrowser.ProductBrowser(core=self.core, importState=self)
        self.core.parentWindow(ts)
        ts.exec_()
        importPath = ts.productPath

        if importPath:
            result = self.importObject(update=True, path=importPath)
            if result:
                self.setImportPath(importPath)
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
        self.w_currentVersion.setToolTip(path)
        self.stateManager.saveImports()
        self.stateManager.saveStatesToScene()
        self.updateUi()


    @err_catcher(name=__name__)
    def isShotCam(self, path=None):
        if not path:
            path = self.getImportPath()
        return path.endswith(".abc") and "/_ShotCam/" in path


    @err_catcher(name=__name__)
    def autoUpdateChanged(self, checked):
        self.w_latestVersion.setVisible(not checked)
        self.w_importLatest.setVisible(not checked)

        if checked:
            curVersion, latestVersion = self.checkLatestVersion()
            if self.chb_autoUpdate.isChecked():
                if curVersion.get("version") and latestVersion.get("version") and curVersion["version"] != latestVersion["version"]:
                    self.importLatest()

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def autoNameSpaceChanged(self, checked):
        self.b_nameSpaces.setEnabled(not checked)
        if not self.stateManager.standalone:
            self.core.appPlugin.sm_import_removeNameSpaces(self)
            self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def runSanityChecks(self, cachePath, settings=None):
        result = True

        if getattr(self.core.appPlugin, "hasFrameRange", True):
            result = self.checkFrameRange(cachePath, settings=settings)

        if not result:
            return False

        return True


    @err_catcher(name=__name__)
    def checkFrameRange(self, cachePath, settings=None):
        versionInfoPath = self.core.getVersioninfoPath(
            self.core.products.getVersionInfoPathFromProductFilepath(cachePath)
        )

        impFPS = self.core.getConfig("fps", configPath=versionInfoPath)
        curFPS = self.core.getFPS()
        if not impFPS or not curFPS or impFPS == curFPS:
            return True

        fString = (
            "The FPS of the import doesn't match the FPS of the current scene:\n\nCurrent scene FPS:\t%s\nImport FPS:\t\t%s"
            % (curFPS, impFPS)
        )

        if not settings or not settings.get("quiet", False):
            result = self.core.popupQuestion(
                fString,
                title="FPS mismatch",
                buttons=["Continue", "Cancel"],
                icon=QMessageBox.Warning,
            )
        else:
            logger.warning(fString)
            result = "Continue"

        if result == "Cancel":
            return False

        return True


    @err_catcher(name=__name__)
    def importObject(self, update=False, path=None, settings=None):
        result = True

        if self.stateManager.standalone:
            return result
        
        fileName = self.core.getCurrentFileName()
        impFileName = path or self.getImportPath()
        impFileName = os.path.normpath(impFileName)

        productData = self.core.products.getProductDataFromFilepath(impFileName)
        productData["meshUUID"] = self.meshUUID

        kwargs = {
            "state": self,
            "scenefile": fileName,
            "importfile": impFileName,
            "productData": productData
        }

        result = self.core.callback("preImport", **kwargs)
        for res in result:
            if isinstance(res, dict) and res.get("cancel", False):
                return

            if res and "importfile" in res:
                impFileName = res["importfile"]
                if not impFileName:
                    return

        if not impFileName:
            self.core.popup("Invalid Import Path:\n\n%s" % impFileName)
            return

        if not hasattr(self.core.appPlugin, "sm_import_importToApp"):
            self.core.popup("Import into %s is not supported." % self.core.appPlugin.pluginName)
            return

        result = self.runSanityChecks(impFileName, settings=settings)
        if not result:
            return

        cacheData = self.core.paths.getCachePathData(impFileName)
        self.taskName = cacheData.get("task")
        doImport = True

        importResult = self.core.appPlugin.sm_import_importToApp(
            self, doImport=doImport, update=update, impFileName=impFileName, data=productData)

        if not importResult:
            result = None
            doImport = False
        else:
            result = self.meshUUID = importResult["result"]
            doImport = importResult["doImport"]
            if result and "mode" in importResult:
                self.setStateMode(importResult["mode"])

        if doImport:
            if result == "canceled":
                return

            if not result:
                msgStr = "Import failed: %s" % impFileName
                self.core.popup(msgStr, title="ImportFile")

        kwargs = {
            "state": self,
            "scenefile": fileName,
            "importfile": impFileName,
        }

        self.core.callback("postImport", **kwargs)

        self.setImportPath(impFileName)
        self.stateManager.saveImports()
        self.updateUi()
        self.stateManager.saveStatesToScene()

        return result


    @err_catcher(name=__name__)
    def importLatest(self, refreshUi=True, selectedStates=True):
        if refreshUi:
            self.updateUi()

        latestVersion = self.core.products.getLatestVersionFromPath(
            self.getImportPath()
        )
        filepath = self.core.products.getPreferredFileFromVersion(latestVersion)
        if not filepath:
            if not self.chb_autoUpdate.isChecked():
                self.core.popup("Couldn't get latest version.")
            return

        prevState = self.stateManager.applyChangesToSelection
        self.stateManager.applyChangesToSelection = False
        self.setImportPath(filepath)
        self.importObject(update=True)
        if selectedStates:
            selStates = self.stateManager.getSelectedStates()
            for state in selStates:
                if state.__hash__() == self.state.__hash__():
                    continue

                if hasattr(state.ui, "importLatest"):
                    state.ui.importLatest(refreshUi=refreshUi, selectedStates=False)

        self.stateManager.applyChangesToSelection = prevState


    @err_catcher(name=__name__)
    def checkLatestVersion(self):
        path = self.getImportPath()
        curVersionName = self.core.products.getVersionFromFilepath(path) or ""
        curVersionData = {"version": curVersionName, "path": path}
        latestVersion = self.core.products.getLatestVersionFromPath(path)
        if latestVersion:
            latestVersionData = {"version": latestVersion["version"], "path": latestVersion["path"]}
        else:
            latestVersionData = {}

        return curVersionData, latestVersionData


    @err_catcher(name=__name__)
    def updateMeshName(self, meshName=None):
        #   Get Shot Camera Object
        meshObj = self.synthFuncts.getObjByUUID("mesh", self.meshUUID)

        if not meshObj:
            return
        
        #   If Passed a New Name, Change it
        if meshName:
            with self.synthFuncts.UNDO_BLOCK("Rename Mesh"):
                self.synthFuncts.setObjName(meshObj, meshName)

        #   Get the Camera Name and Set it in the UI
        meshName = self.synthFuncts.getObjName(self, meshObj)
        self.e_meshName.setText(meshName)




    @err_catcher(name=__name__)
    def setStateColor(self, status):
        if status == "ok":
            statusColor = QColor(0, 130, 0)
        elif status == "warning":
            statusColor = QColor(200, 100, 0)
        elif status == "error":
            statusColor = QColor(130, 0, 0)
        else:
            statusColor = QColor(0, 0, 0, 0)

        self.statusColor = statusColor
        self.stateManager.tw_import.repaint()


    @err_catcher(name=__name__)
    def updateUi(self):
        self.updateMeshName()

        versions = self.checkLatestVersion()
        if versions:
            curVersion, latestVersion = versions
        else:
            curVersion = latestVersion = ""

        if curVersion.get("version") == "master":
            filepath = self.getImportPath()
            curVersionName = self.core.products.getMasterVersionLabel(filepath)
        else:
            curVersionName = curVersion.get("version")

        if latestVersion.get("version") == "master":
            filepath = latestVersion["path"]
            latestVersionName = self.core.products.getMasterVersionLabel(filepath)
        else:
            latestVersionName = latestVersion.get("version")

        self.l_curVersion.setText(curVersionName or "-")
        self.l_latestVersion.setText(latestVersionName or "-")

        status = "error"
        if self.chb_autoUpdate.isChecked():
            if curVersionName and latestVersionName and curVersionName != latestVersionName:
                self.importLatest(refreshUi=False)

            if latestVersionName:
                status = "ok"
        else:
            useSS = getattr(self.core.appPlugin, "colorButtonWithStyleSheet", False)
            if (
                curVersionName
                and latestVersionName
                and curVersionName != latestVersionName
                and not curVersionName.startswith("master")
            ):
                status = "warning"
                if useSS:
                    self.b_importLatest.setStyleSheet(
                        "QPushButton { background-color: rgb(200,100,0); }"
                    )
                else:
                    self.b_importLatest.setPalette(self.updatePalette)
            else:
                if curVersionName and latestVersionName:
                    status = "ok"
                elif self.nodes:
                    status = "ok"

                if useSS:
                    self.b_importLatest.setStyleSheet("")
                else:
                    self.b_importLatest.setPalette(self.oldPalette)

        self.nameChanged()
        self.setStateColor(status)
        getattr(self.core.appPlugin, "sm_import_updateUi", lambda x: None)(self)


    @err_catcher(name=__name__)
    def setToolTips(self):
        tip = "Product Name of Imported Mesh"
        self.e_name.setToolTip(tip)

        tip = "Opens the Product Browser to select a specific version"
        self.b_browse.setToolTip(tip)

        tip = "Will import the latest version of the Mesh."
        self.b_importLatest.setToolTip(tip)

        # tip = ("Enables Auto-update function.\n\n"
        #        "This will automatically import/update to\n"
        #        "the most recent version of the media.")
        # self.w_autoUpdate.setToolTip(tip)

        tip = ("Name of SynthEyes Mesh for the Import.\n\n"
               "You may change the name and it will be\n"
               "reflected in SynthEyes.  Also the version\n"
               "number (if any) will be updated with changes\n"
               " to the selected version.")
        self.l_meshName.setToolTip(tip)
        self.e_meshName.setToolTip(tip)




    @err_catcher(name=__name__)
    def preDelete(
        self,
        item=None,
        baseText="Do you also want to delete the SynthEyes Mesh?\n\n",
    ):

        if not self.core.uiAvailable:
            action = "Yes"
        else:
            action = self.core.popupQuestion(baseText, title="Delete State", parent=self.stateManager)

        if action == "Yes":
            logger.debug("Deleting SynthEyes Mesh")
            delData = {
                "meshUUID": self.meshUUID
            }

            getattr(self.core.appPlugin, "sm_import_preDelete", lambda *x: None)(
                self, delData
            )



    @err_catcher(name=__name__)
    def getStateProps(self):
        return {
            "statename": self.e_name.text(),
            "statemode": self.stateMode,
            "meshUUID": self.meshUUID,
            "filepath": self.getImportPath(),
            "autoUpdate": str(self.chb_autoUpdate.isChecked()),
            "taskname": self.taskName,
            "setname": self.setName,
        }
