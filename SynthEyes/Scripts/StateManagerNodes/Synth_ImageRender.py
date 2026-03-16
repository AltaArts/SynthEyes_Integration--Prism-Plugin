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
import sys
import time
import platform
import logging

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher

from Synth_Formats import (SynthExrCompress,
                           SynthMovCodecs,
                           SynthMP4Codecs,
                           SynthMP4Qual,
                           SynthHasAlpha)

logger = logging.getLogger(__name__)


class Synth_ImageRenderClass(object):
    className = "Synth_ImageRender"
    listType = "Export"
    stateCategories = {"Render": [{"label": className, "stateType": className}]}


    @err_catcher(name=__name__)
    def setup(self, state, core, stateManager, node=None, stateData=None):
        self.state = state
        self.core = core
        self.stateManager = stateManager
        self.canSetVersion = True
        self.customContext = None
        self.allowCustomContext = False
        self.cb_context.addItems(["From scenefile", "Custom"])

        self.renderingStarted = False
        self.cleanOutputdir = True

        self.e_name.setText(state.text(0) + " - {identifier}")

        self.rangeTypes = [
            "Scene",
            "Shot",
            "Shot + 1",
            "Single Frame",
            "Custom",
            ]
        self.cb_rangeType.addItems(self.rangeTypes)
        for idx, rtype in enumerate(self.rangeTypes):
            self.cb_rangeType.setItemData(
                idx, self.stateManager.getFrameRangeTypeToolTip(rtype), Qt.ToolTipRole
            )

        self.curCam = None
        self.refreshCameras()

        self.renderPresets = (
            self.stateManager.stateTypes["RenderSettings"].getPresets(self.core)
            if "RenderSettings" in self.stateManager.stateTypes
            else {}
            )
        if self.renderPresets:
            self.cb_renderPreset.addItems(self.renderPresets.keys())
        else:
            self.w_renderPreset.setVisible(False)

        self.l_name.setVisible(False)
        self.e_name.setVisible(False)

        getattr(self.core.appPlugin, "sm_render_startup", lambda x: None)(self)

        masterItems = ["Set as master", "Add to master", "Don't update master"]
        self.cb_master.addItems(masterItems)
        self.product_paths = self.core.paths.getRenderProductBasePaths()
        self.cb_outPath.addItems(list(self.product_paths.keys()))
        if len(self.product_paths) < 2:
            self.w_outPath.setVisible(False)

        self.mediaType = "2drenders"
        self.tasknameRequired = True
        
        self.outputFormats = [
            ".exr",
            ".mov",
            ".mp4",
            ".png",
            ]

        self.cb_format.addItems(self.outputFormats)

        self.setupFormatOptions()
        self.configFormatUI()

        self.resolutionPresets = self.core.projects.getResolutionPresets()
        if "Get from rendersettings" not in self.resolutionPresets:
            self.resolutionPresets.append("Get from rendersettings")

        self.loadDefaults()
        self.connectEvents()

        self.oldPalette = self.b_changeTask.palette()
        self.warnPalette = QPalette()
        self.warnPalette.setColor(QPalette.Button, QColor(200, 0, 0))
        self.warnPalette.setColor(QPalette.ButtonText, QColor(255, 255, 255))

        self.setTaskWarn(True)
        self.nameChanged(state.text(0))

        self.core.callback("onStateStartup", self)

        self.onVersionOverrideChanged(self.chb_version.isChecked())

        if stateData is not None:
            self.loadData(stateData)
        else:
            self.initializeContextBasedSettings()


    @err_catcher(name=__name__)
    def loadDefaults(self):
        self.cb_format.setCurrentIndex(0)

        idx = self.cb_exrCompression.findText("DWAA")
        if idx != -1:
            self.cb_exrCompression.setCurrentIndex(idx)

        self.chb_include_RGB.setChecked(True)
        self.chb_include_Alpha.setChecked(False)
        self.chb_include_Mesh.setChecked(True)
        self.chb_include_Burnin.setChecked(False)


    @err_catcher(name=__name__)
    def loadData(self, data):
        if "contextType" in data:
            self.setContextType(data["contextType"])
        if "customContext" in data:
            self.customContext = data["customContext"]
        if "taskname" in data:
            self.setIdentifier(data["taskname"])
        if "identifier" in data:
            self.setIdentifier(data["identifier"])

        self.updateUi()

        if "stateName" in data:
            self.e_name.setText(data["stateName"])
        elif "statename" in data:
            self.e_name.setText(data["statename"] + " - {identifier}")
        if "renderpresetoverride" in data:
            res = eval(data["renderpresetoverride"])
            self.chb_renderPreset.setChecked(res)
        if "currentrenderpreset" in data:
            idx = self.cb_renderPreset.findText(data["currentrenderpreset"])
            if idx != -1:
                self.cb_renderPreset.setCurrentIndex(idx)
                self.stateManager.saveStatesToScene()
        if "rangeType" in data:
            idx = self.cb_rangeType.findText(data["rangeType"])
            if idx != -1:
                self.cb_rangeType.setCurrentIndex(idx)
                self.updateRange()
        if "startframe" in data:
            self.sp_rangeStart.setValue(int(data["startframe"]))
        if "endframe" in data:
            self.sp_rangeEnd.setValue(int(data["endframe"]))
        if "currentCam" in data:
            self.curCam = data["currentCam"]
        if "resoverride" in data:
            res = eval(data["resoverride"])
            self.chb_resOverride.setChecked(res[0])
            self.sp_resWidth.setValue(res[1])
            self.sp_resHeight.setValue(res[2])
        if "masterVersion" in data:
            idx = self.cb_master.findText(data["masterVersion"])
            if idx != -1:
                self.cb_master.setCurrentIndex(idx)
        if "curoutputpath" in data:
            idx = self.cb_outPath.findText(data["curoutputpath"])
            if idx != -1:
                self.cb_outPath.setCurrentIndex(idx)
        if "useVersionOverride" in data:
            self.chb_version.setChecked(data["useVersionOverride"])
        if "versionOverride" in data:
            self.sp_version.setValue(data["versionOverride"])
        if "outputFormat" in data:
            idx = self.cb_format.findText(data["outputFormat"])
            if idx != -1:
                self.cb_format.setCurrentIndex(idx)
        if "exrCompress" in data:
            idx = self.cb_exrCompression.findText(data["exrCompress"])
            if idx != -1:
                self.cb_exrCompression.setCurrentIndex(idx)
        if "movCodec" in data:
            idx = self.cb_movCodec.findText(data["movCodec"])
            if idx != -1:
                self.cb_movCodec.setCurrentIndex(idx)
        if "mp4Codec" in data:
            idx = self.cb_mp4Codec.findText(data["mp4Codec"])
            if idx != -1:
                self.cb_mp4Codec.setCurrentIndex(idx)
        if "mp4Qual" in data:
            idx = self.cb_mp4Qual.findText(data["mp4Qual"])
            if idx != -1:
                self.cb_mp4Qual.setCurrentIndex(idx)
        if "include_RGB" in data:
            self.chb_include_RGB.setChecked(data["include_RGB"])
        if "include_Alpha" in data:
            self.chb_include_Alpha.setChecked(data["include_Alpha"])
        if "include_Mesh" in data:
            self.chb_include_Mesh.setChecked(data["include_Mesh"])
        if "include_Burnin" in data:
            self.chb_include_Burnin.setChecked(data["include_Burnin"])

        if "lastexportpath" in data:
            lePath = self.core.fixPath(data["lastexportpath"])
            self.l_pathLast.setText(lePath)
            self.l_pathLast.setToolTip(lePath)
        if "stateenabled" in data:
            if type(data["stateenabled"]) == int:
                self.state.setCheckState(
                    0, Qt.CheckState(data["stateenabled"]),
                )

        self.configFormatUI()

        self.core.callback("onStateSettingsLoaded", self, data)


    @err_catcher(name=__name__)
    def connectEvents(self):
        self.e_name.textChanged.connect(self.nameChanged)
        self.e_name.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.cb_context.activated.connect(self.onContextTypeChanged)
        self.b_context.clicked.connect(self.selectContextClicked)
        self.b_changeTask.clicked.connect(self.changeTask)
        self.chb_renderPreset.stateChanged.connect(self.presetOverrideChanged)
        self.cb_renderPreset.activated.connect(self.stateManager.saveStatesToScene)
        self.cb_rangeType.activated.connect(self.rangeTypeChanged)
        self.sp_rangeStart.editingFinished.connect(self.startChanged)
        self.sp_rangeEnd.editingFinished.connect(self.endChanged)
        self.cb_cam.activated.connect(self.setCam)
        self.chb_resOverride.stateChanged.connect(self.resOverrideChanged)
        self.sp_resWidth.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.sp_resHeight.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.b_resPresets.clicked.connect(self.showResPresets)
        self.cb_master.activated.connect(self.stateManager.saveStatesToScene)
        self.cb_outPath.activated.connect(self.stateManager.saveStatesToScene)
        self.chb_version.stateChanged.connect(self.onVersionOverrideChanged)
        self.sp_version.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.b_version.clicked.connect(self.onVersionOverrideClicked)
        self.cb_format.activated.connect(self.configFormatUI)
        self.cb_exrCompression.activated.connect(self.stateManager.saveStatesToScene)
        self.cb_movCodec.activated.connect(self.configFormatUI)
        self.cb_mp4Codec.activated.connect(self.stateManager.saveStatesToScene)
        self.cb_mp4Qual.activated.connect(self.stateManager.saveStatesToScene)
        self.chb_include_RGB.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.chb_include_Alpha.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.chb_include_Mesh.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.chb_include_Burnin.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.b_pathLast.clicked.connect(lambda: self.stateManager.showLastPathMenu(self))


    @err_catcher(name=__name__)
    def initializeContextBasedSettings(self):
        context = self.getCurrentContext()
        if context.get("type") == "asset":
            self.setRangeType("Single Frame")
        elif context.get("type") == "shot":
            self.setRangeType("Shot")
        elif self.stateManager.standalone:
            self.setRangeType("Custom")
        else:
            self.setRangeType("Scene")

        start, end = self.getFrameRange("Scene")
        if start is not None:
            self.sp_rangeStart.setValue(start)

        if end is not None:
            self.sp_rangeEnd.setValue(end)

        if context.get("task"):
            self.setIdentifier(context.get("task"))

        self.updateUi()

    @err_catcher(name=__name__)
    def getLastPathOptions(self):
        path = self.l_pathLast.text()
        if path == "None":
            return

        options = [
            {
                "label": "Play...",
                "callback": lambda: self.core.media.playMediaInExternalPlayer(path)
            },
            {
                "label": "Open in Media Browser...",
                "callback": lambda: self.openInMediaBrowser(path)
            },
            {
                "label": "Open in Explorer...",
                "callback": lambda: self.core.openFolder(path)
            },
        ]
        if os.getenv("PRISM_COPY_FILE_CONTENT", "0") == "1":
            options.append({
                "label": "Copy",
                "callback": lambda: self.core.copyToClipboard(path, file=True)
            })
        else:
            options.append({
                "label": "Copy Path",
                "callback": lambda: self.core.copyToClipboard(path, file=False)
            })

        return options

    @err_catcher(name=__name__)
    def openInMediaBrowser(self, path):
        self.core.projectBrowser()
        self.core.pb.showTab("Media")
        data = self.core.paths.getRenderProductData(path)
        self.core.pb.mediaBrowser.showRender(entity=data, identifier=data.get("identifier"), version=data.get("version"))


    @err_catcher(name=__name__)
    def selectContextClicked(self, state=None):
        self.dlg_entity = self.stateManager.entityDlg(self)
        data = self.getCurrentContext()
        self.dlg_entity.w_entities.navigate(data)
        self.dlg_entity.entitySelected.connect(lambda x: self.setCustomContext(x))
        self.dlg_entity.show()


    @err_catcher(name=__name__)
    def setCustomContext(self, context):
        self.customContext = context
        self.refreshContext()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def onContextTypeChanged(self, state):
        self.refreshContext()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def rangeTypeChanged(self, state):
        self.updateUi()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def startChanged(self):
        if self.sp_rangeStart.value() > self.sp_rangeEnd.value():
            self.sp_rangeEnd.setValue(self.sp_rangeStart.value())

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def endChanged(self):
        if self.sp_rangeEnd.value() < self.sp_rangeStart.value():
            self.sp_rangeStart.setValue(self.sp_rangeEnd.value())

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def nameChanged(self, text):
        text = self.e_name.text()
        context = {}
        context["identifier"] = self.getIdentifier() or "None"
        num = 0
        try:
            if "{#}" in text:
                while True:
                    context["#"] = num or ""
                    name = text.format(**context)
                    for state in self.stateManager.states:
                        if state.ui.listType != "Export":
                            continue

                        if state is self.state:
                            continue

                        if state.text(0) == name:
                            num += 1
                            break
                    else:
                        break
            else:
                name = text.format(**context)
        except Exception:
            name = text

        if self.state.text(0).endswith(" - disabled"):
            name += " - disabled"

        self.state.setText(0, name)


    @err_catcher(name=__name__)
    def getFormat(self):
        return self.cb_format.currentText()


    @err_catcher(name=__name__)
    def setFormat(self, fmt):
        idx = self.cb_format.findText(fmt)
        if idx != -1:
            self.cb_format.setCurrentIndex(idx)
            self.stateManager.saveStatesToScene()
            return True

        return False
    

    #   Populate Various Format Combos
    @err_catcher(name=__name__)
    def setupFormatOptions(self):
        exrCompress = SynthExrCompress.keys()
        self.cb_exrCompression.addItems(exrCompress)

        movCodecs = SynthMovCodecs.keys()
        self.cb_movCodec.addItems(movCodecs)

        mp4Codecs = SynthMP4Codecs.keys()
        self.cb_mp4Codec.addItems(mp4Codecs)

        mp4Qual = SynthMP4Qual.keys()
        self.cb_mp4Qual.addItems(mp4Qual)


    #   Show/Hide Format UI
    @err_catcher(name=__name__)
    def configFormatUI(self, format=None):
        ##  Option Widgets
        #   Hide All Codec Option Widgets
        for w in self.findChildren(QWidget):
            if w.objectName().startswith("f_codecOptions_"):
                w.hide()

        #   Find Widget Name for Format
        fmt = self.cb_format.currentText().upper().replace(".", "")
        targetWidget = f"f_codecOptions_{fmt}"

        #   Show the Matching Format Widget
        widget = getattr(self, targetWidget, None)
        if widget:
            widget.show()

        ##  Alpha Checkbox
        hasAlpha = False

        #   Check Format
        if fmt in SynthHasAlpha:
            hasAlpha = True

        else:
            #   Find Codec Combo by Matching Format Name
            codecCombo = None
            for child in widget.findChildren(QWidget):               
                if child.objectName().startswith("cb_"):
                    codecCombo = child
                    break

            #   Check if Codec is Alpha Supported
            if codecCombo:
                codec = codecCombo.currentText()
                hasAlpha = codec in SynthHasAlpha

        #   Configure Alpha Checkbox
        if not hasAlpha:
            self.chb_include_Alpha.setChecked(False)
            self.chb_include_Alpha.setDisabled(True)
        else:
            self.chb_include_Alpha.setDisabled(False)
        
        self.stateManager.saveStatesToScene

    
    #   Returns Dict of format Options Based on Selected format
    @err_catcher(name=__name__)
    def getFormatOptions(self):
        fmt = self.getFormat().lower()

        if fmt == ".exr":
            return {"exrCompress": self.cb_exrCompression.currentText()}
        
        elif fmt == ".mov":
            return {"movCodec": self.cb_movCodec.currentText()}
        
        elif fmt == ".mp4":
            return {"mp4Codec": self.cb_mp4Codec.currentText(),
                    "mp4Qual": self.cb_mp4Qual.currentText()}
        else:
            return {}
        

    @err_catcher(name=__name__)
    def getContextType(self):
        contextType = self.cb_context.currentText()
        return contextType


    @err_catcher(name=__name__)
    def setContextType(self, contextType):
        idx = self.cb_context.findText(contextType)
        if idx != -1:
            self.cb_context.setCurrentIndex(idx)
            self.refreshContext()
            return True

        return False


    @err_catcher(name=__name__)
    def getIdentifier(self):
        identifier = self.l_taskName.text()
        return identifier


    @err_catcher(name=__name__)
    def getTaskname(self):
        return self.getIdentifier()


    @err_catcher(name=__name__)
    def setIdentifier(self, identifier):
        self.l_taskName.setText(identifier)
        self.setTaskWarn(not bool(identifier))
        self.updateUi()


    @err_catcher(name=__name__)
    def setTaskname(self, taskname):
        self.setIdentifier(taskname)


    @err_catcher(name=__name__)
    def getSortKey(self):
        return self.getIdentifier()


    @err_catcher(name=__name__)
    def changeTask(self):
        from PrismUtils import PrismWidgets
        self.nameWin = PrismWidgets.CreateItem(
            startText=self.getIdentifier(),
            showTasks=True,
            taskType="3d",
            core=self.core,
        )
        self.core.parentWindow(self.nameWin)
        self.nameWin.setWindowTitle("Change Identifier")
        self.nameWin.l_item.setText("Identifier:")
        self.nameWin.buttonBox.buttons()[0].setText("Ok")
        self.nameWin.e_item.selectAll()
        result = self.nameWin.exec_()

        if result == 1:
            self.setIdentifier(self.nameWin.e_item.text())
            self.nameChanged(self.e_name.text())
            self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def presetOverrideChanged(self, checked):
        self.cb_renderPreset.setEnabled(checked)
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def resOverrideChanged(self, checked):
        self.sp_resWidth.setEnabled(checked)
        self.sp_resHeight.setEnabled(checked)
        self.b_resPresets.setEnabled(checked)

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def showResPresets(self):
        pmenu = QMenu(self)

        for preset in self.resolutionPresets:
            pAct = QAction(preset, self)
            res = self.getResolution(preset)
            if not res:
                continue

            pwidth, pheight = res

            pAct.triggered.connect(
                lambda x=None, v=pwidth: self.sp_resWidth.setValue(v)
            )
            pAct.triggered.connect(
                lambda x=None, v=pheight: self.sp_resHeight.setValue(v)
            )
            pAct.triggered.connect(lambda: self.stateManager.saveStatesToScene())
            pmenu.addAction(pAct)

        pmenu.exec_(QCursor.pos())


    @err_catcher(name=__name__)
    def onVersionOverrideChanged(self, checked):
        self.sp_version.setEnabled(checked)
        self.sp_version.lineEdit().setHidden(not checked)
        self.b_version.setEnabled(checked)
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def onVersionOverrideClicked(self):
        pmenu = QMenu(self)

        outPath = self.getOutputName()
        if not outPath:
            return

        existingVersions = self.core.mediaProducts.getVersionsFromSameVersionStack(
            outPath[0]
        )
        for version in sorted(
            existingVersions, key=lambda x: x["version"], reverse=True
        ):
            name = version["version"]
            intVersion = self.core.products.getIntVersionFromVersionName(name)
            if intVersion is None:
                continue

            actV = QAction(name, self)
            actV.triggered.connect(
                lambda y=None, v=intVersion: self.sp_version.setValue(v)
            )
            actV.triggered.connect(lambda: self.stateManager.saveStatesToScene())
            pmenu.addAction(actV)

        if existingVersions:
            pmenu.exec_(QCursor.pos())
        else:
            self.core.popup("No versions exists in the current context.", severity="info")


    @err_catcher(name=__name__)
    def getRangeType(self):
        return self.cb_rangeType.currentText()


    @err_catcher(name=__name__)
    def setRangeType(self, rangeType):
        idx = self.cb_rangeType.findText(rangeType)
        if idx != -1:
            self.cb_rangeType.setCurrentIndex(idx)
            self.updateRange()
            return True

        return False


    @err_catcher(name=__name__)
    def getResolution(self, resolution):
        res = None
        if resolution == "Get from rendersettings":
            if hasattr(self.core.appPlugin, "getResolution"):
                res = self.core.appPlugin.getResolution()
            else:
                res = [1920, 1080]
        elif resolution.startswith("Project ("):
            res = resolution[9:-1].split("x")
            res = [int(r) for r in res]
        else:
            try:
                pwidth = int(resolution.split("x")[0])
                pheight = int(resolution.split("x")[1])
                res = [pwidth, pheight]
            except:
                res = getattr(
                    self.core.appPlugin, "evaluateResolution", lambda x: None
                )(resolution)

        return res


    @err_catcher(name=__name__)
    def getMasterVersion(self):
        return self.cb_master.currentText()


    @err_catcher(name=__name__)
    def setMasterVersion(self, master):
        idx = self.cb_master.findText(master)
        if idx != -1:
            self.cb_master.setCurrentIndex(idx)
            self.stateManager.saveStatesToScene()
            return True

        return False


    @err_catcher(name=__name__)
    def getLocation(self):
        return self.cb_outPath.currentText()


    @err_catcher(name=__name__)
    def setLocation(self, location):
        idx = self.cb_outPath.findText(location)
        if idx != -1:
            self.cb_outPath.setCurrentIndex(idx)
            self.stateManager.saveStatesToScene()
            return True

        return False
    

    @err_catcher(name=__name__)
    def setCam(self, cameraIdx): 
        self.curCam = self.cb_cam.currentText()

        self.refreshCameras()


    @err_catcher(name=__name__)
    def refreshCameras(self):
        self.cb_cam.clear()
        self.camlist = []

        if not self.stateManager.standalone:
            camObjs = self.core.appPlugin.getCamNodes(self, cur=True)
            self.camlist = [self.core.appPlugin.getCamName(self, i) for i in camObjs]

        self.cb_cam.addItems(self.camlist)

        if self.curCam in self.camlist:
            idx = self.cb_cam.findText(self.curCam)
            if idx != -1:
                self.cb_cam.setCurrentIndex(idx)
        else:
            self.cb_cam.setCurrentIndex(0)
            if len(self.camlist) > 0:
                self.curCam = self.camlist[0]
            else:
                self.curCam = None

        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def updateUi(self):
        self.w_context.setHidden(not self.allowCustomContext)
        self.w_comment.setHidden(not self.stateManager.useStateComments())
 
        if not self.core.mediaProducts.getUseMaster():
            self.w_master.setVisible(False)

        self.refreshContext()
        self.refreshCameras()
        self.updateRange()

        self.nameChanged(self.e_name.text())
        getattr(self.core.appPlugin, "sm_render_updateUi", lambda x: None)(self)

        return True


    @err_catcher(name=__name__)
    def refreshContext(self):
        context = self.getCurrentContext()
        contextStr = self.getContextStrFromEntity(context)
        self.l_context.setText(contextStr)


    @err_catcher(name=__name__)
    def getCurrentContext(self):
        context = None
        if self.allowCustomContext:
            ctype = self.getContextType()
            if ctype == "Custom":
                context = self.customContext

        if not context:
            fileName = self.core.getCurrentFileName()
            context = self.core.getScenefileData(fileName)
        
        if "username" in context:
            del context["username"]

        if "user" in context:
            del context["user"]

        return context


    @err_catcher(name=__name__)
    def updateRange(self):
        rangeType = self.cb_rangeType.currentText()
        isCustom = rangeType == "Custom"
        self.l_rangeStart.setVisible(not isCustom)
        self.l_rangeEnd.setVisible(not isCustom)
        self.sp_rangeStart.setVisible(isCustom)
        self.sp_rangeEnd.setVisible(isCustom)
        self.w_frameRangeValues.setVisible(True)

        if not isCustom:
            frange = self.getFrameRange(rangeType=rangeType)
            start = str(int(frange[0])) if frange[0] is not None else "-"
            end = str(int(frange[1])) if frange[1] is not None else "-"
            self.l_rangeStart.setText(start)
            self.l_rangeEnd.setText(end)


    @err_catcher(name=__name__)
    def getFrameRange(self, rangeType):
        startFrame = None
        endFrame = None
        if rangeType == "Scene":
            if hasattr(self.core.appPlugin, "getFrameRange"):
                startFrame, endFrame = self.core.appPlugin.getFrameRange(self)
                startFrame = int(startFrame)
                endFrame = int(endFrame)
            else:
                startFrame = 1001
                endFrame = 1100
        elif rangeType == "Shot":
            context = self.getCurrentContext()
            if context.get("type") == "shot" and "sequence" in context:
                frange = self.core.entities.getShotRange(context)
                if frange:
                    startFrame, endFrame = frange
        elif rangeType == "Shot + 1":
            context = self.getCurrentContext()
            if context.get("type") == "shot" and "sequence" in context:
                frange = self.core.entities.getShotRange(context)
                if frange and frange[0] is not None and frange[1] is not None:
                    startFrame, endFrame = frange
                    startFrame -= 1
                    endFrame += 1
        elif rangeType == "Single Frame":
            if hasattr(self.core.appPlugin, "getCurrentFrame"):
                startFrame = int(self.core.appPlugin.getCurrentFrame())
            else:
                startFrame = 1001
        elif rangeType == "Custom":
            startFrame = self.sp_rangeStart.value()
            endFrame = self.sp_rangeEnd.value()
        elif rangeType == "Expression":
            return self.core.resolveFrameExpression(self.le_frameExpression.text())

        if startFrame == "":
            startFrame = None

        if endFrame == "":
            endFrame = None

        if startFrame is not None:
            startFrame = int(startFrame)

        if endFrame is not None:
            endFrame = int(endFrame)

        return startFrame, endFrame


    @err_catcher(name=__name__)
    def getContextStrFromEntity(self, entity):
        if not entity:
            return ""

        entityType = entity.get("type", "")
        if entityType == "asset":
            entityName = entity.get("asset_path", "").replace("\\", "/")
        elif entityType == "shot":
            entityName = self.core.entities.getShotName(entity)
        else:
            return ""

        context = "%s - %s" % (entityType.capitalize(), entityName)
        return context


    @err_catcher(name=__name__)
    def preExecuteState(self):
        warnings = []

        self.updateUi()

        rData = {}

        rData["currentCam"] = self.cb_cam.currentText()

        rangeType = self.cb_rangeType.currentText()
        startFrame, endFrame = self.getFrameRange(rangeType)

        if startFrame is None:
            warnings.append(["Framerange is invalid.", "", 3])

        warnings += self.core.appPlugin.sm_render_preExecute(self, rData)

        return [self.state.text(0), warnings]
    

    @err_catcher(name=__name__)
    def getOutputName(self, useVersion="next", identifier=None):
        if self.tasknameRequired and not identifier:
            return

        context = self.getCurrentContext()

        if "type" not in context:
            return
        
        extension = self.cb_format.currentText().lower()
        padding = ""
        if extension not in self.core.media.videoFormats:
            padding = ("#" * self.core.framePadding)

        location = self.cb_outPath.currentText()

        if self.chb_version.isChecked():
            version = self.core.versionFormat % self.sp_version.value()
        else:
            version = useVersion if useVersion != "next" else None

        outputPathData = self.core.mediaProducts.generateMediaProductPath(
            entity=context,
            task=identifier,
            extension=extension,
            framePadding=padding,
            comment=self.getComment(),
            version=version,
            location=location,
            singleFrame=False,
            returnDetails=True,
            mediaType=self.mediaType,
            state=self,
        )

        outputPath = outputPathData["path"]
        outputFolder = os.path.dirname(outputPathData["path"])
        if not os.path.exists(outputFolder):
            os.makedirs(outputFolder)

        hVersion = outputPathData["version"]
        return outputPath, outputFolder, hVersion


    @err_catcher(name=__name__)
    def getComment(self):
        if self.stateManager.useStateComments():
            comment = self.e_comment.text() or self.stateManager.publishComment
        else:
            comment = self.stateManager.publishComment

        return comment


    @err_catcher(name=__name__)
    def executeState(self, parent, useVersion="next"):
        rangeType = self.cb_rangeType.currentText()
        frames = self.getFrameRange(rangeType)
        startFrame = frames[0]
        endFrame = frames[1]

        if frames is None or frames == [] or frames[0] is None:
            return [self.state.text(0) + ": error - Framerange is invalid"]

        if rangeType == "Single Frame":
            endFrame = startFrame

        fileName = self.core.getCurrentFileName()
        context = self.getCurrentContext()

        idf = self.getIdentifier()

        outputName, outputPath, hVersion = self.getOutputName(useVersion="next", identifier=idf)
        expandedOutputPath = self.expandvars(outputPath)

        #   Change Prism "###"'s to ".001"'s
        extension = self.cb_format.currentText().lower()
        if extension not in self.core.media.videoFormats:
            paddingNum = self.core.framePadding
            framePadding = "#" * paddingNum
            paddedFrame = str(startFrame).zfill(paddingNum)
            outputName = outputName.replace(framePadding, paddedFrame)

        outLength = len(expandedOutputPath)
        if platform.system() == "Windows" and os.getenv("PRISM_IGNORE_PATH_LENGTH") != "1" and outLength > 255:
            return [
                self.state.text(0)
                + " - error - The outputpath is longer than 255 characters (%s), which is not supported on Windows. Please shorten the outputpath by changing the comment, identifier or projectpath."
                % outLength
            ]

        if not os.path.exists(os.path.dirname(expandedOutputPath)):
            os.makedirs(os.path.dirname(expandedOutputPath))

        useVersion = hVersion if useVersion == "next" or (self.core.compareVersions(hVersion, useVersion) == "higher") else useVersion

        rSettings = {
            "outputName": outputName,
            "startFrame": startFrame,
            "endFrame": endFrame,
            "frames": frames,
            "identifier": idf,
            "currentCam": self.cb_cam.currentText(),
            "format": extension,
            "include_RGB": self.chb_include_RGB.isChecked(),
            "include_Alpha": self.chb_include_Alpha.isChecked(),
            "include_Mesh": self.chb_include_Mesh.isChecked(),
            "include_Burnin": self.chb_include_Burnin.isChecked(),
            }
        
        #   Add Format Specific Options
        rSettings.update(self.getFormatOptions())

        errors = []

        result = self.core.appPlugin.sm_render_Sequence(self, self.stateManager, rSettings["outputName"], rSettings, context)

        if result:
            try:
                details = context.copy()
                if "filename" in details:
                    del details["filename"]

                if "extension" in details:
                    del details["extension"]

                details["version"] = hVersion
                details["sourceScene"] = fileName
                details["identifier"] = idf
                details["comment"] = self.getComment()
                details["startframe"] = startFrame
                details["endframe"] = endFrame
                details["path"] = expandedOutputPath
                details["mediaType"] = self.mediaType
                details["include_RGB"] = self.chb_include_RGB.isChecked()
                details["include_Alpha"] = self.chb_include_Alpha.isChecked()
                details["include_Mesh"] = self.chb_include_Mesh.isChecked()
                details["include_Burnin"] = self.chb_include_Burnin.isChecked()

                self.core.saveVersionInfo(filepath=expandedOutputPath, details=details)
            except:
                errors.append(f"{idf}: VersionInfo Error")

            try:
                self.handleMasterVersion(outputName, details)
            except:
                errors.append(f"{idf}: Master Error")
        else:
            errors.append(f"{idf}: Render Error")

        if not errors:
            kwargs = {
                "state": self,
                "scenefile": fileName,
                "settings": rSettings,
                "result": result,
            }

            self.core.callback("postRender", **kwargs)

            return [self.state.text(0) + " - success"]

        else:
            erStr = "%s ERROR - sm_default_imageRenderPublish %s:\n%s" % (
                time.strftime("%d/%m/%y %X"),
                self.core.version,
                errors,
                )
            
            if not result.startswith("Execute Canceled: "):
                if result == "unknown error (files do not exist)":
                    msg = "No files were created during the rendering. If you think this is a Prism bug please report it on our Discord server:\nwww.prism-pipeline.com/discord\nor write a mail to contact@prism-pipeline.com"
                    self.core.popup(msg)

                else:
                    self.core.writeErrorLog(erStr)

            return [self.state.text(0) + " - error - " + result]


    @err_catcher(name=__name__)
    def expandvars(self, path):
        if hasattr(self.core.appPlugin, "expandEnvVarsInFilepath"):
            expandedPath = self.core.appPlugin.expandEnvVarsInFilepath(path)
        else:
            expandedPath = os.path.expandvars(path)

        return expandedPath


    @err_catcher(name=__name__)
    def isUsingMasterVersion(self):
        useMaster = self.core.mediaProducts.getUseMaster()
        if not useMaster:
            return False

        masterAction = self.cb_master.currentText()
        if masterAction == "Don't update master":
            return False

        return True


    @err_catcher(name=__name__)
    def handleMasterVersion(self, outputName, context):
        if not self.isUsingMasterVersion():
            return

        masterAction = self.cb_master.currentText()
        if masterAction == "Set as master":
            self.core.mediaProducts.updateMasterVersion(outputName, context=context)
        elif masterAction == "Add to master":
            self.core.mediaProducts.addToMasterVersion(outputName, context=context)


    @err_catcher(name=__name__)
    def setTaskWarn(self, warn):
        useSS = getattr(self.core.appPlugin, "colorButtonWithStyleSheet", False)
        if warn and self.f_taskname.isEnabled():
            if useSS:
                self.b_changeTask.setStyleSheet(
                    "QPushButton { background-color: rgb(200,0,0); }"
                )
            else:
                self.b_changeTask.setPalette(self.warnPalette)
        else:
            if useSS:
                self.b_changeTask.setStyleSheet("")
            else:
                self.b_changeTask.setPalette(self.oldPalette)


    @err_catcher(name=__name__)
    def getStateProps(self):
        stateProps = {
            "stateName": self.e_name.text(),
            "contextType": self.getContextType(),
            "customContext": self.customContext,
            "identifier": self.getIdentifier(),
            "renderpresetoverride": str(self.chb_renderPreset.isChecked()),
            "currentrenderpreset": self.cb_renderPreset.currentText(),
            "rangeType": str(self.cb_rangeType.currentText()),
            "startframe": self.sp_rangeStart.value(),
            "endframe": self.sp_rangeEnd.value(),
            "currentCam": self.cb_cam.currentText(),
            "resoverride": str(
                [
                    self.chb_resOverride.isChecked(),
                    self.sp_resWidth.value(),
                    self.sp_resHeight.value(),
                ]
            ),
            "masterVersion": self.cb_master.currentText(),
            "curoutputpath": self.cb_outPath.currentText(),
            "useVersionOverride": self.chb_version.isChecked(),
            "versionOverride": self.sp_version.value(),
            "outputFormat": self.getFormat(),
            "exrCompress": self.cb_exrCompression.currentText(),
            "movCodec": self.cb_movCodec.currentText(),
            "mp4Codec": self.cb_mp4Codec.currentText(),
            "mp4Qual": self.cb_mp4Qual.currentText(),
            "include_RGB": self.chb_include_RGB.isChecked(),
            "include_Alpha": self.chb_include_Alpha.isChecked(),
            "include_Mesh": self.chb_include_Mesh.isChecked(),
            "include_Burnin": self.chb_include_Burnin.isChecked(),
            "lastexportpath": self.l_pathLast.text().replace("\\", "/"),
            "stateenabled": self.core.getCheckStateValue(self.state.checkState(0)),
        }

        self.core.callback("onStateGetSettings", self, stateProps)

        return stateProps
