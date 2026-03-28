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
import sys
import time
import traceback
import platform
import logging
import json

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher

from Synth_Formats import SynthFormatNames


logger = logging.getLogger(__name__)


class Synth_SceneExportClass(object):
    className = "Synth_SceneExport"
    listType = "Export"
    stateCategories = {"Export": [{"label": className, "stateType": className}]}

    @err_catcher(name=__name__)
    def setup(self, state, core, stateManager, node=None, stateData=None):
        self.state = state
        self.core = core
        self.stateManager = stateManager
        self.synthFuncts = self.core.appPlugin

        self.canSetVersion = True
        self.customContext = None
        self.allowCustomContext = False
        self.shotCamsInitialized = False

        self.exportData = None

        self.e_name.setText(state.text(0) + " ({product})")
        self.l_name.setVisible(False)
        self.e_name.setVisible(False)

        self.cb_context.addItems(["From scenefile", "Custom"])

        self.chb_master.setChecked(os.getenv("PRISM_ENABLE_MASTER_DFT", "1") == "1")

        self.oldPalette = self.b_changeTask.palette()
        self.warnPalette = QPalette()
        self.warnPalette.setColor(QPalette.Button, QColor(200, 0, 0))
        self.warnPalette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        self.b_changeTask.setPalette(self.warnPalette)

        self.additionalSettings = []
        self.b_additionalSettings = QPushButton("Additional Settings...")
        self.b_additionalSettings.clicked.connect(self.showAdditionalSettings)

        self.rangeTypes = ["Scene", "Shot", "Shot + 1", "Single Frame", "Custom"]
        self.cb_rangeType.addItems(self.rangeTypes)
        for idx, rtype in enumerate(self.rangeTypes):
            self.cb_rangeType.setItemData(
                idx, self.stateManager.getFrameRangeTypeToolTip(rtype), Qt.ToolTipRole
            )

        outputFormats = SynthFormatNames.keys()
        self.cb_outType.addItems(outputFormats)

        self.export_paths = self.core.paths.getExportProductBasePaths()
        self.cb_outPath.addItems(list(self.export_paths.keys()))
        if len(self.export_paths) < 2:
            self.w_outPath.setVisible(False)

        getattr(self.core.appPlugin, "sm_export_startup", lambda x: None)(self)
        self.nameChanged(state.text(0))

        self.toolTips()
        self.connectEvents()

        #   Set Prism Icon Dir
        iconDir = os.path.join(self.core.prismRoot, "Scripts", "UserInterfacesPrism")
        iconDir = iconDir.replace("\\", "/")

        #   Set Section Icons
        self.chb_exportSettings.setStyleSheet(f"""
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
            }}

            QCheckBox::indicator:unchecked {{
                image: url("{iconDir}/right_arrow_light.png");
            }}

            QCheckBox::indicator:checked {{
                image: url("{iconDir}/down_arrow_light.png");
            }}
            """)
        
        self.chb_sceneHierarchy.setStyleSheet(f"""
            QCheckBox::indicator {{
                width: 15px;
                height: 15px;
            }}

            QCheckBox::indicator:unchecked {{
                image: url("{iconDir}/right_arrow_light.png");
            }}

            QCheckBox::indicator:checked {{
                image: url("{iconDir}/down_arrow_light.png");
            }}
            """)

        #   Close Sections by Default
        self.onSectionToggled("exportSettings", False)
        self.onSectionToggled("sceneH", False)

        #   Set Refresh Icon
        icon_refresh = QIcon(os.path.join(iconDir, "refresh.png"))
        self.b_refreshExports.setIcon(icon_refresh)

        self.chb_customExport.setChecked(False)

        self.core.callback("onStateStartup", self)

        self.setupExportSettings()

        if stateData is not None:
            self.loadData(stateData)
        else:
            self.initializeContextBasedSettings()
            self.loadExportLists()

        self.typeChanged(self.getOutputType())


    @err_catcher(name=__name__)
    def toolTips(self):
        tip = "Image format for the Scene Export."
        self.cb_outType.setToolTip(tip)

        tip = ("Refreshes the Export Items and their current\n"
               "state in the SynthEyes scene.")
        self.b_refreshExports.setToolTip(tip)


    @err_catcher(name=__name__)
    def loadData(self, data):
        if "contextType" in data:
            self.setContextType(data["contextType"])
        if "customContext" in data:
            self.customContext = data["customContext"]
        if "taskname" in data:
            self.setProductname(data["taskname"])
        if "productname" in data:
            self.setProductname(data["productname"])

        self.updateUi()

        if "stateName" in data:
            self.e_name.setText(data["stateName"])
        elif "statename" in data:
            self.e_name.setText(data["statename"] + " ({product})")
        if "rangeType" in data:
            idx = self.cb_rangeType.findText(data["rangeType"])
            if idx != -1:
                self.cb_rangeType.setCurrentIndex(idx)
                self.updateRange()
        if "startframe" in data:
            self.sp_rangeStart.setValue(int(data["startframe"]))
        if "endframe" in data:
            self.sp_rangeEnd.setValue(int(data["endframe"]))
        if "updateMasterVersion" in data:
            self.chb_master.setChecked(data["updateMasterVersion"])
        if "curoutputpath" in data:
            idx = self.cb_outPath.findText(data["curoutputpath"])
            if idx != -1:
                self.cb_outPath.setCurrentIndex(idx)
        if "curoutputtype" in data:
            idx = self.cb_outType.findText(data["curoutputtype"])
            if idx != -1:
                self.cb_outType.setCurrentIndex(idx)
        if "customExport" in data:
            self.chb_customExport.setChecked(data["customExport"])
        if "exportItems" in data:
            self.exportData = json.loads(data["exportItems"])
            self.loadExportLists()
        if "additionaloptions" in data:
            self.chb_additionalOptions.setChecked(eval(data["additionaloptions"]))
        if "lastexportpath" in data:
            lePath = self.core.fixPath(data["lastexportpath"])
            self.setLastPath(lePath)
        if "stateenabled" in data:
            if type(data["stateenabled"]) == int:
                self.state.setCheckState(
                    0, Qt.CheckState(data["stateenabled"]),
                )
        if "additionalSettings" in data:
            for setting in data["additionalSettings"]:
                for asetting in self.additionalSettings:
                    if asetting["name"] == setting:
                        asetting["value"] = data["additionalSettings"][setting]

        getattr(self.core.appPlugin, "sm_export_loadData", lambda x, y: None)(
            self, data
        )
        self.core.callback("onStateSettingsLoaded", self, data)


    @err_catcher(name=__name__)
    def connectEvents(self):
        self.e_name.textChanged.connect(self.nameChanged)
        self.e_name.editingFinished.connect(self.stateManager.saveStatesToScene)
        self.cb_context.activated.connect(self.onContextTypeChanged)
        self.b_context.clicked.connect(self.selectContextClicked)
        self.b_changeTask.clicked.connect(self.changeTask)
        self.cb_rangeType.activated.connect(self.rangeTypeChanged)
        self.sp_rangeStart.editingFinished.connect(self.startChanged)
        self.sp_rangeEnd.editingFinished.connect(self.endChanged)
        self.chb_master.stateChanged.connect(self.stateManager.saveStatesToScene)
        self.cb_outPath.activated.connect(self.stateManager.saveStatesToScene)
        self.cb_outType.activated.connect(lambda x: self.typeChanged(self.getOutputType()))
        self.chb_exportSettings.toggled.connect(lambda checked: self.onSectionToggled("exportSettings", checked))
        self.chb_sceneHierarchy.toggled.connect(lambda checked: self.onSectionToggled("sceneH", checked))
        self.chb_customExport.stateChanged.connect(self.updateExportUI)
        self.b_refreshExports.clicked.connect(self.refreshExportLists)
        self.lw_shots.itemChanged.connect(self.onExportItemChanged)
        self.lw_meshes.itemChanged.connect(self.onExportItemChanged)
        self.b_pathLast.clicked.connect(lambda: self.stateManager.showLastPathMenu(self))


    @err_catcher(name=__name__)
    def initializeContextBasedSettings(self):
        context = self.getCurrentContext()
        startFrame, endFrame = self.getFrameRange("Scene")
        if startFrame is not None:
            self.sp_rangeStart.setValue(startFrame)
        if endFrame is not None:
            self.sp_rangeEnd.setValue(endFrame)
        if context.get("type") == "asset":
            self.setRangeType("Single Frame")
            self.sp_rangeEnd.setValue(startFrame)
        elif context.get("type") == "shot":
            self.setRangeType("Shot")
        elif self.stateManager.standalone:
            self.setRangeType("Custom")
        else:
            self.setRangeType("Scene")

        if context.get("task"):
            self.setProductname(context.get("task"))


    @err_catcher(name=__name__)
    def getLastPathOptions(self):
        path = self.l_pathLast.text()
        if path == "None":
            return

        options = [
            {
                "label": "Open in Product Browser...",
                "callback": lambda: self.openInProductBrowser(path)
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
    def showAdditionalSettings(self):
        self.dlg_additionalSettings = AdditionalSettingsDialog(self)
        self.dlg_additionalSettings.show()


    @err_catcher(name=__name__)
    def openInProductBrowser(self, path):
        self.core.projectBrowser()
        self.core.pb.showTab("Products")
        data = self.core.paths.getCachePathData(path)
        self.core.pb.productBrowser.navigateToVersion(version=data["version"], product=data["product"], entity=data)


    @err_catcher(name=__name__)
    def selectContextClicked(self):
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
        self.updateRange()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def onExportItemChanged(self, item):
        self.getExportItems()
        self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def nameChanged(self, text):
        text = self.e_name.text()
        context = {}
        if self.getOutputType() == "ShotCam":
            context["product"] = "ShotCam - %s" % self.cb_cam.currentText()
        else:
            context["product"] = self.getProductname() or "None"

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
    def getUpdateMasterVersion(self):
        return self.chb_master.isChecked()


    @err_catcher(name=__name__)
    def setUpdateMasterVersion(self, master):
        self.chb_master.setChecked(master)


    @err_catcher(name=__name__)
    def getOutputType(self):
        return self.cb_outType.currentText()


    @err_catcher(name=__name__)
    def setOutputType(self, outType):
        idx = self.cb_outType.findText(outType)
        if idx != -1:
            self.cb_outType.setCurrentIndex(idx)


    @err_catcher(name=__name__)
    def getOutputExt(self):
        try:
            outputType = self.getOutputType()
            return SynthFormatNames[outputType]["format"]
        except:
            return None


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
    def getProductname(self):
        if self.getOutputType() == "ShotCam":
            productName = "_ShotCam"
        else:
            productName = self.l_taskName.text()

        return productName


    @err_catcher(name=__name__)
    def getTaskname(self):
        return self.getProductname()


    @err_catcher(name=__name__)
    def setProductname(self, productname):
        prevProductName = self.getProductname()
        default_func = lambda x1, x2, newTaskName: productname
        productname = getattr(self.core.appPlugin, "sm_export_setTaskText", default_func)(
            self, prevProductName, productname
        )
        self.l_taskName.setText(productname)
        self.updateUi()
        return productname


    @err_catcher(name=__name__)
    def setTaskname(self, taskname):
        return self.setProductname(taskname)


    @err_catcher(name=__name__)
    def getSortKey(self):
        return self.getProductname()


    @err_catcher(name=__name__)
    def changeTask(self):
        from PrismUtils import PrismWidgets
        self.nameWin = PrismWidgets.CreateItem(
            startText=self.getProductname(),
            showTasks=True,
            taskType="export",
            core=self.core,
            )
        
        self.core.parentWindow(self.nameWin)
        self.nameWin.setWindowTitle("Change Productname")
        self.nameWin.l_item.setText("Productname:")
        self.nameWin.buttonBox.buttons()[0].setText("Ok")
        self.nameWin.w_tags = QWidget()
        self.nameWin.lo_tags = QHBoxLayout(self.nameWin.w_tags)
        self.nameWin.lo_tags.setContentsMargins(9, 0, 9, 0)
        self.nameWin.l_tagLabel = QLabel("Tags:               ")
        self.nameWin.e_tags = QLineEdit()
        self.nameWin.b_editTags = QPushButton(u"\u25bc")
        self.nameWin.b_editTags.setToolTip("Recommended Tags")
        self.nameWin.b_editTags.setMaximumSize(QSize(30, 16777215))
        self.nameWin.lo_tags.addWidget(self.nameWin.l_tagLabel)
        self.nameWin.lo_tags.addWidget(self.nameWin.e_tags)
        self.nameWin.lo_tags.addWidget(self.nameWin.b_editTags)
        self.nameWin.layout().insertWidget(2, self.nameWin.w_tags)
        self.nameWin.e_item.textChanged.connect(self.onProductNameChanged)
        self.nameWin.b_editTags.clicked.connect(self.showRecommendedTags)
        self.onProductNameChanged()
        self.nameWin.e_item.selectAll()
        result = self.nameWin.exec_()

        if result == 1:
            product = self.nameWin.e_item.text()
            self.setProductname(product)
            tags = [t.strip() for t in self.nameWin.e_tags.text().split(",")]
            ctx = self.getCurrentContext().copy()
            ctx["product"] = product
            self.core.products.setProductTags(ctx, tags)
            self.stateManager.saveStatesToScene()


    @err_catcher(name=__name__)
    def onProductNameChanged(self, text=None):
        product = self.nameWin.e_item.text()
        ctx = self.getCurrentContext().copy()
        ctx["product"] = product
        tags = self.core.products.getTagsFromProduct(ctx)
        self.nameWin.e_tags.setText(", ".join(tags))


    @err_catcher(name=__name__)
    def showRecommendedTags(self):
        tmenu = QMenu(self)

        tags = self.core.products.getRecommendedTags(self.getCurrentContext())
        for tag in tags:
            tAct = QAction(tag, self)
            tAct.triggered.connect(lambda x=None, t=tag: self.toggleTag(t))
            tmenu.addAction(tAct)

        tmenu.exec_(QCursor.pos())


    @err_catcher(name=__name__)
    def toggleTag(self, tag):
        tags = [t.strip() for t in self.nameWin.e_tags.text().split(",")]
        if tag in tags:
            tags = [t for t in tags if t != tag]
        else:
            tags.append(tag)

        tags = [t for t in tags if t]
        self.nameWin.e_tags.setText(", ".join(tags))


    @err_catcher(name=__name__)
    def preDelete(self, item):
        self.synthFuncts.sm_export_preDelete(self)


    @err_catcher(name=__name__)
    def refreshShotCameras(self):
        curShot = self.cb_sCamShot.currentText()
        self.cb_sCamShot.clear()
        shots = self.core.entities.getShots()
        for shot in sorted(shots, key=lambda s: self.core.entities.getShotName(s).lower()):
            shotData = {"type": "shot", "sequence": shot["sequence"], "shot": shot["shot"]}
            if "episode" in shot:
                shotData["episode"] = shot["episode"]

            shotName = self.core.entities.getShotName(shot)
            self.cb_sCamShot.addItem(shotName, shotData)

        idx = self.cb_sCamShot.findText(curShot)
        if idx != -1:
            self.cb_sCamShot.setCurrentIndex(idx)
        else:
            self.cb_sCamShot.setCurrentIndex(0)
            self.stateManager.saveStatesToScene()

        if not self.shotCamsInitialized:
            context = self.getCurrentContext()
            if (
                context.get("type") == "shot"
                and "sequence" in context
            ):
                shotName = self.core.entities.getShotName(context)
                idx = self.cb_sCamShot.findText(shotName)
                if idx != -1:
                    self.cb_sCamShot.setCurrentIndex(idx)
                    self.stateManager.saveStatesToScene()

            self.shotCamsInitialized = True


    @err_catcher(name=__name__)
    def updateUi(self):
        self.w_context.setHidden(not self.allowCustomContext)
        self.w_comment.setHidden(not self.stateManager.useStateComments())

        if not self.core.products.getUseMaster():
            self.w_master.setVisible(False)

        self.refreshContext()
        self.updateRange()

        if self.getOutputType() == "ShotCam":
            self.refreshShotCameras()

        if self.getProductname():
            self.b_changeTask.setPalette(self.oldPalette)

        showSettings = any([setting.get("visible", lambda dlg, state: True)(None, self) for setting in self.additionalSettings])
        self.b_additionalSettings.setHidden(not showSettings)
        self.nameChanged(self.e_name.text())

        self.updateExportUI()

        self.core.callback("sm_export_updateUi", self)



    @err_catcher(name=__name__)
    def updateExportUI(self, checked=None):
        if checked is None:
            checked = self.chb_customExport.isChecked()

        self.gb_shotList.setEnabled(checked)
        self.gb_meshList.setEnabled(checked)

        self.stateManager.saveStatesToScene()


    #   Toggles Sections Open/Closed
    @err_catcher(name=__name__)
    def onSectionToggled(self, section, checked):
        if section == "exportSettings":
            widget =  self.w_exportSettings

        elif section == "sceneH":
            widget = self.w_sceneHierarchy

        widget.setVisible(checked)


    @err_catcher(name=__name__)
    def refreshContext(self):
        context = self.getCurrentContext()
        contextStr = self.getContextStrFromEntity(context)
        self.l_context.setText(contextStr)
        if contextStr:
            self.b_context.setPalette(self.oldPalette)
        else:
            self.b_context.setPalette(self.warnPalette)


    @err_catcher(name=__name__)
    def getCurrentContext(self):
        context = {}
        if self.allowCustomContext:
            ctype = self.getContextType()
            if ctype == "Custom":
                context = self.customContext

        if not context:
            if self.getOutputType() == "ShotCam":
                if self.shotCamsInitialized:
                    context = self.cb_sCamShot.currentData()
                else:
                    fileName = self.core.getCurrentFileName()
                    context = self.core.getScenefileData(fileName)

                if context and self.core.getConfig("globals", "productTasks", config="project"):
                    context["department"] = os.getenv("PRISM_SHOTCAM_DEPARTMENT", "Layout")
                    context["task"] = os.getenv("PRISM_SHOTCAM_TASK", "Cameras")

            else:
                fileName = self.core.getCurrentFileName()
                context = self.core.getScenefileData(fileName)

        if context and "username" in context:
            del context["username"]

        if context and "user" in context:
            del context["user"]

        return context or {}


    @err_catcher(name=__name__)
    def updateRange(self):
        rangeType = self.cb_rangeType.currentText()
        isCustom = rangeType == "Custom"
        self.l_rangeStart.setVisible(not isCustom)
        self.l_rangeEnd.setVisible(not isCustom)
        self.sp_rangeStart.setVisible(isCustom)
        self.sp_rangeEnd.setVisible(isCustom)

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
                startFrame = self.core.appPlugin.getCurrentFrame()
            else:
                startFrame = 1001
        elif rangeType == "Custom":
            startFrame = self.sp_rangeStart.value()
            endFrame = self.sp_rangeEnd.value()

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
    def typeChanged(self, idx):
        isSCam = idx == "ShotCam"
        self.w_taskname.setVisible(not isSCam)
        getattr(self.core.appPlugin, "sm_export_typeChanged", lambda x, y: None)(
            self, idx
        )

        self.updateUi()
        self.stateManager.saveStatesToScene()


    #   Creates the Exporter Settings Based on Type
    @err_catcher(name=__name__)
    def setupExportSettings(self):
        exportType = self.cb_outType.currentText()
        settingsWindow = self.w_exportSettings
        layout = settingsWindow.layout()

        #   Clear Existing UI
        self.clearLayout(layout)
        self.exportWidgets = {}

        #   Get Exporter Settings from Formats File
        schema = SynthFormatNames.get(exportType, {}).get("exportSettings", {})

        #   Create UI Widgets
        for key, setting in schema.items():
            row = self.createSettingWidget(key, setting, settingsWindow)
            if row:
                layout.addWidget(row)


    #   Removes All Widgets from Layout
    def clearLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clearLayout(item.layout())


    #   Creates Widget Row Based on Settings in Format File
    def createSettingWidget(self, key, setting, parent):
        widgetType = setting["widgetType"]
        name = setting["name"]
        tooltip = setting.get("toolTip", "")

        #   Create Row
        row = QWidget(parent)
        rowLayout = QHBoxLayout(row)
        rowLayout.setContentsMargins(30, 0, 30, 0)

        #   Create Label from Name
        label = QLabel(name, row)
        label.setToolTip(tooltip)
        rowLayout.addWidget(label)

        #   Add Spacing
        rowLayout.addStretch()

        ##  Create Widget by Type

        #   Checkbox
        if widgetType == "checkbox":
            cb = QCheckBox("", row)
            cb.setToolTip(tooltip)

            default = setting.get("factoryDefault", 0)
            cb.setChecked(str(default) in ("1", "True", True, 1))

            self.exportWidgets[key] = cb
            rowLayout.addWidget(cb)

            return row

        #   ComboBox
        elif widgetType == "combo":
            combo = QComboBox(row)
            combo.setToolTip(tooltip)

            for label_text, value in setting.get("comboItems", []):
                combo.addItem(label_text, value)

            default = setting.get("factoryDefault")

            index = 0
            for i in range(combo.count()):
                if combo.itemData(i) == default:
                    index = i
                    break
            combo.setCurrentIndex(index)

            self.exportWidgets[key] = combo
            rowLayout.addWidget(combo)

            return row

        #   SpinBox
        elif widgetType == "spin":
            spin = QSpinBox(row)
            spin.setToolTip(tooltip)

            r = setting.get("range", [0, 100])
            spin.setRange(r[0], r[1])
            spin.setSingleStep(setting.get("step", 1))
            spin.setValue(setting.get("factoryDefault", 0))

            self.exportWidgets[key] = spin
            rowLayout.addWidget(spin)

            return row

        #   Dual SpinBox
        elif widgetType == "doubleSpin":
            spin = QDoubleSpinBox(row)
            spin.setToolTip(tooltip)

            r = setting.get("range", [0.0, 1.0])
            spin.setRange(r[0], r[1])
            spin.setDecimals(setting.get("precision", 3))
            spin.setSingleStep(setting.get("step", 0.01))

            spin.setValue(setting.get("factoryDefault", 0.0))
            self.exportWidgets[key] = spin
            rowLayout.addWidget(spin)

            return row
        
        else:
            return None


    # @err_catcher(name=__name__)
    # def getExportSettings(self):                                        #   TODO - ADD UI
    #     eData = {
    #     "exporter_Type": "USD ASCII Scene",
    #     "exporter_SettingsName": "USD ASCII Scene Settings",
    #     "exporter_Settings":[
    #             ["workArea", "2"],
    #             ["userStart", 1],
    #             ["units", "ft"],
    #             ["buildRigs", 1],
    #             ["fixAD", 1],
    #             ["doScreen", 1],
    #             ["usePreprocessor", "1"],
    #             ["uvScreenMode", "1"],
    #             ["nomgrid", 64],
    #             ["relScreenDis", 5],
    #             ["rotOrder", "1"],
    #             ["relTrkSize", 0.001],
    #             ["relLidarSize", 0.0002],
    #             ["relFarClip", 10],
    #             ["miscOpacity", 1],
    #             ["doFrustrum", 1],
    #             ["doGnomon", 1],
    #             ["doChisel", 1],
    #             ["geoPrimitives", 0],
    #             ["silentMovies", 1]
    #         ]
    #     }

    #     return eData
    

    #   Gets Exporter Settings from UI
    @err_catcher(name=__name__)
    def getExportSettings(self):
        #   Get Settings Format from Format File
        exportTypeUI = self.cb_outType.currentText()
        formatData = SynthFormatNames.get(exportTypeUI, {})

        #   Get the Exporter Settings Names
        exporterType = formatData.get("synthName", "")
        exporterSettingsName = f"{exporterType} Settings"

        settingsList = []

        #   Iterate the Settings Widgets and Get Value by Type
        for key, widget in self.exportWidgets.items():
            try:
                if isinstance(widget, QCheckBox):
                    value = 1 if widget.isChecked() else 0

                elif isinstance(widget, QComboBox):
                    value = widget.currentData()

                elif isinstance(widget, QSpinBox):
                    value = int(widget.value())

                elif isinstance(widget, QDoubleSpinBox):
                    value = float(widget.value())

                else:
                    continue

                #   Make the Settins a List for Sizzle
                settingsList.append([key, value])
                
            except Exception as e:
                logger.warning(f"ERROR: Unable to Get Exporter Setting: {e}")

        #   Build Settings Dict
        eData = {
            "exporter_Type": exporterType,
            "exporter_SettingsName": exporterSettingsName,
            "exporter_Settings": settingsList
        }

        return eData


    #   Called from Refresh Button to Reload Lists from Scene Data
    @err_catcher(name=__name__)
    def refreshExportLists(self):
        self.exportData = None
        self.loadExportLists()

        self.stateManager.saveStatesToScene()


    #   Loads and Sets the Export Lists
    @err_catcher(name=__name__)
    def loadExportLists(self):
        self.loadExportList("shots")
        self.loadExportList("meshes")


    #   Loads the Export Table Based on Passed List Type
    @err_catcher(name=__name__)
    def loadExportList(self, listType: str):
        #   Assign Vars based on Type
        if listType == "shots":
            listWidget = self.lw_shots
            objects = self.synthFuncts.getCamNodes()
            exportKey = "cameraExports"
            getNameFunc = self.synthFuncts.getCamName
            getExportedFunc = self.synthFuncts.getObjExported

        elif listType == "meshes":
            listWidget = self.lw_meshes
            objects = self.synthFuncts.synthEyes.Meshes()
            exportKey = "meshExports"
            getNameFunc = self.synthFuncts.getObjName
            getExportedFunc = self.synthFuncts.getObjExported

        else:
            logger.warning(f"ERROR: Unknown listType: {listType}")
            return

        listWidget.blockSignals(True)
        listWidget.clear()

        #   Build Lookup Dict from ExportData
        lookup = {}
        if self.exportData and exportKey in self.exportData:
            keyName = "cameraName" if exportKey == "cameraExports" else "meshName"
            lookup = {item[keyName]: item["exported"] for item in self.exportData[exportKey]}

        #   Populate List
        for obj in objects:
            name = getNameFunc(self, obj)
            exported = lookup.get(name, getExportedFunc(obj))

            item = QListWidgetItem(name)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked if exported else Qt.Unchecked)

            listWidget.addItem(item)

        listWidget.blockSignals(False)


    #   Builds Export Items from List Items
    @err_catcher(name=__name__)
    def getExportItems(self):
        ##  Camera List
        camExportData = []
        #   Iterate Camera List and Build Dict of Check States
        for i in range(self.lw_shots.count()):
            camItem = self.lw_shots.item(i)
            cData = {
                "cameraName": camItem.text(),
                "exported": camItem.checkState() == Qt.Checked
            }
            camExportData.append(cData)

        ##   Mesh List
        meshExportData = []
        #   Iterate Mesh List and Build Dict of Check States
        for i in range(self.lw_meshes.count()):
            meshItem = self.lw_meshes.item(i)
            mData = {
                "meshName": meshItem.text(),
                "exported": meshItem.checkState() == Qt.Checked
            }
            meshExportData.append(mData)

        eData = {
            "cameraExports": camExportData,
            "meshExports": meshExportData
        }

        self.exportData = eData

        return eData


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
    def setLastPath(self, path):
        self.l_pathLast.setText(path)
        self.l_pathLast.setToolTip(path)
        self.stateManager.saveStatesToScene()


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

        rangeType = self.cb_rangeType.currentText()
        startFrame, endFrame = self.getFrameRange(rangeType)

        if startFrame is None:
            warnings.append(["Framerange is invalid.", "", 3])

        checked = sum(
            1 for i in range(self.lw_shots.count())
            if self.lw_shots.item(i).checkState() == Qt.Checked
            )
        
        if checked < 1:
            warnings.append(["No Cameras are Selected for Export.", "", 2])

        warnings += self.synthFuncts.sm_sceneExport_preExecute(self, startFrame, endFrame)

        return [self.state.text(0), warnings]
    

    @err_catcher(name=__name__)
    def getOutputName(self, useVersion="next"):
        context = self.getCurrentContext()
        location = self.cb_outPath.currentText()
        version = useVersion if useVersion != "next" else None
        if "type" not in context:
            return

        product = self.getProductname()
        if not product:
            return

        if self.getOutputType() == "ShotCam":
            context["entityType"] = "shot"
            context["type"] = "shot"
            if "asset_path" in context:
                del context["asset_path"]

            if "asset" in context:
                del context["asset"]

            extension = ""
            framePadding = None
        else:
            rangeType = self.cb_rangeType.currentText()
            extension = self.getOutputExt()

            if rangeType == "Single Frame" or extension != ".obj":
                framePadding = ""
            else:
                framePadding = "#" * self.core.framePadding

        outputPathData = self.core.products.generateProductPath(
            entity=context,
            task=product,
            extension=extension,
            framePadding=framePadding,
            comment=self.getComment(),
            version=version,
            location=location,
            returnDetails=True,
        )

        outputFolder = os.path.dirname(outputPathData["path"])
        hVersion = outputPathData["version"]

        return outputPathData["path"], outputFolder, hVersion


    @err_catcher(name=__name__)
    def isUsingMasterVersion(self):
        useMaster = self.core.products.getUseMaster()
        if not useMaster:
            return False

        return useMaster and self.getUpdateMasterVersion()


    @err_catcher(name=__name__)
    def handleMasterVersion(self, outputName):
        if not self.isUsingMasterVersion():
            return

        self.core.products.updateMasterVersion(outputName)


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
        startFrame, endFrame = self.getFrameRange(rangeType)
        if startFrame is None:
            return [self.state.text(0) + ": error - Framerange is invalid"]

        if rangeType == "Single Frame":
            endFrame = startFrame

        ##   For ShotCam
        if self.getOutputType() == "ShotCam":
            pass
            # if self.curCam is None:
            #     return [
            #         self.state.text(0)
            #         + ": error - No camera specified. Skipped the activation of this state."
            #     ]

            # if self.cb_sCamShot.currentText() == "":
            #     return [
            #         self.state.text(0)
            #         + ": error - No Shot specified. Skipped the activation of this state."
            #     ]

            fileName = self.core.getCurrentFileName()
            context = self.getCurrentContext()
            outputName, outputPath, hVersion = self.getOutputName(useVersion=useVersion)

            outLength = len(outputName)
            if platform.system() == "Windows" and os.getenv("PRISM_IGNORE_PATH_LENGTH") != "1" and outLength > 255:
                return [
                    self.state.text(0)
                    + " - error - The outputpath is longer than 255 characters (%s), which is not supported on Windows. Please shorten the outputpath by changing the comment, taskname or projectpath."
                    % outLength
                ]

            kwargs = {
                "state": self,
                "scenefile": fileName,
                "startframe": startFrame,
                "endframe": endFrame,
                "outputpath": outputName,
                "version": hVersion,
            }

            result = self.core.callback("preExport", **kwargs)
            for res in result:
                if isinstance(res, dict) and res.get("cancel", False):
                    return [
                        self.state.text(0)
                        + " - error - %s" % res.get("details", "preExport hook returned False")
                    ]

                if res and "outputName" in res:
                    outputName = res["outputName"]

                if res and "version" in res:
                    hVersion = res["version"]

            outputPath = os.path.dirname(outputName)
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            details = context.copy()
            if "filename" in details:
                del details["filename"]

            if "extension" in details:
                del details["extension"]

            details["version"] = hVersion
            details["sourceScene"] = fileName
            details["product"] = self.getProductname()
            details["resolution"] = self.synthFuncts.getResolution()
            details["comment"] = self.getComment()

            details.update(self.cb_sCamShot.currentData())
            details["entityType"] = "shot"
            details["type"] = "shot"
            if "asset_path" in details:
                del details["asset_path"]

            if startFrame != endFrame:
                details["fps"] = self.core.getFPS()

            infoPath = self.core.products.getVersionInfoPathFromProductFilepath(
                outputName
            )
            self.core.saveVersionInfo(filepath=infoPath, details=details)

            self.synthFuncts.sm_export_exportShotcam(
                self, startFrame=startFrame, endFrame=endFrame, outputName=outputName
            )

            outputName += ".abc"

            self.setLastPath(outputName)

            useMaster = self.core.products.getUseMaster()
            if useMaster and self.getUpdateMasterVersion():
                self.core.products.updateMasterVersion(outputName)

            kwargs = {
                "state": self,
                "scenefile": fileName,
                "startframe": startFrame,
                "endframe": endFrame,
                "outputpath": outputName,
            }

            result = self.core.callback("postExport", **kwargs)
            validateOutput = True
            for res in result:
                if isinstance(res, dict) and res.get("cancel", False):
                    return [
                        self.state.text(0)
                        + " - error - %s" % res.get("details", "postExport hook returned False")
                    ]

                if res and "outputName" in res:
                    outputName = res["outputName"]

                if res and "validateOutput" in res:
                    validateOutput = res["validateOutput"]

            self.stateManager.saveStatesToScene()

            if not validateOutput or os.path.exists(outputName):
                return [self.state.text(0) + " - success"]
            else:
                return [self.state.text(0) + " - unknown error"]
        
        ##   For Other Than ShotCam
        else:

            if not self.getProductname():
                return [
                    self.state.text(0)
                    + ": error - No productname is given. Skipped the activation of this state."
                ]

            fileName = self.core.getCurrentFileName()
            context = self.getCurrentContext()
            outputName, outputPath, hVersion = self.getOutputName(useVersion=useVersion)

            outLength = len(outputName)
            if platform.system() == "Windows" and os.getenv("PRISM_IGNORE_PATH_LENGTH") != "1" and outLength > 255:
                return [
                    self.state.text(0)
                    + " - error - The outputpath is longer than 255 characters (%s), which is not supported on Windows. Please shorten the outputpath by changing the comment, taskname or projectpath."
                    % outLength
                ]

            kwargs = {
                "state": self,
                "scenefile": fileName,
                "startframe": startFrame,
                "endframe": endFrame,
                "outputpath": outputName,
            }
            extraVersionInfo = {}

            result = self.core.callback("preExport", **kwargs)
            for res in result:
                if isinstance(res, dict) and res.get("cancel", False):
                    return [
                        self.state.text(0)
                        + " - error - %s" % res.get("details", "preExport hook returned False")
                    ]
                
                if res and "outputName" in res:
                    outputName = res["outputName"]

                if res and "extraVersionInfo" in res:
                    extraVersionInfo.update(res["extraVersionInfo"])

            outputPath = os.path.dirname(outputName)
            if not os.path.exists(outputPath):
                os.makedirs(outputPath)

            details = context.copy()

            if "filename" in details:
                del details["filename"]

            if "extension" in details:
                del details["extension"]

            details["version"] = hVersion
            details["sourceScene"] = fileName
            details["product"] = self.getProductname()
            details["startFrame"] = startFrame
            details["endFrame"] = endFrame
            details["comment"] = self.getComment()

            if startFrame != endFrame:
                details["fps"] = self.core.getFPS()

            details.update(extraVersionInfo)
            infoPath = self.core.products.getVersionInfoPathFromProductFilepath(
                outputName
            )
            self.core.saveVersionInfo(filepath=infoPath, details=details)
            if self.core.products.getUseProductPreviews():
                preview = self.core.products.generateProductPreview()
                if preview:
                    self.core.products.setProductPreview(os.path.dirname(outputName), preview)

            outputType = self.cb_outType.currentText()

            rSettings = details.copy()
            rSettings["customExport"] = self.chb_customExport.isChecked()
            rSettings["exportData"] = self.exportData
            rSettings["exportSettings"] = self.getExportSettings()

            #   Capture Current and Config New Settings
            rSettings = self.synthFuncts.sm_pre_sceneExport(self, rSettings)

            try:
                submitResult = None

                outputName = self.synthFuncts.sm_sceneExport(
                    self,
                    outputType,
                    outputName=outputName,
                    details=rSettings
                )

                if not outputName:
                    return [self.state.text(0) + " - error"]

                if outputName.startswith("Canceled"):
                    return [self.state.text(0) + " - error: %s" % outputName]

                #   Restore Orignial Settings
                self.synthFuncts.sm_post_sceneExport(self, rSettings)

                logger.debug("exported to: %s" % outputName)
                self.setLastPath(outputName)
                self.stateManager.saveStatesToScene()

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                erStr = "%s ERROR - sm_default_export %s:\n%s" % (
                    time.strftime("%d/%m/%y %X"),
                    self.core.version,
                    traceback.format_exc(),
                )
                self.core.writeErrorLog(erStr)
                return [
                    self.state.text(0)
                    + " - unknown error (view console for more information)"
                ]

            useMaster = self.core.products.getUseMaster()
            if useMaster and self.getUpdateMasterVersion():
                self.handleMasterVersion(outputName)

            kwargs = {
                "state": self,
                "scenefile": fileName,
                "startframe": startFrame,
                "endframe": endFrame,
                "outputpath": outputName,
                "result": submitResult,
            }

            result = self.core.callback("postExport", **kwargs)
            validateOutput = True
            for res in result:
                if res:
                    if res and "outputName" in res:
                        outputName = res["outputName"]

                    if res and "validateOutput" in res:
                        validateOutput = res["validateOutput"]

            if os.path.exists(outputName) or self.core.media.getFilesFromSequence(outputName) or not validateOutput:
                return [self.state.text(0) + " - success"]
            else:
                return [self.state.text(0) + " - unknown error (files do not exist)"]


    @err_catcher(name=__name__)
    def getStateProps(self):
        stateProps = {}

        stateProps.update(
            {
                "stateName": self.e_name.text(),
                "contextType": self.getContextType(),
                "customContext": self.customContext,
                "productname": self.getProductname(),
                "rangeType": str(self.cb_rangeType.currentText()),
                "startframe": self.sp_rangeStart.value(),
                "endframe": self.sp_rangeEnd.value(),
                "updateMasterVersion": self.chb_master.isChecked(),
                "curoutputpath": self.cb_outPath.currentText(),
                "curoutputtype": self.getOutputType(),
                # "currentcam": self.cb_cam.currentText(),
                # "currentscamshot": self.cb_sCamShot.currentText(),
                "customExport": self.chb_customExport.isChecked(),

                "exportItems": json.dumps(self.getExportItems()),

                "lastexportpath": self.l_pathLast.text().replace("\\", "/"),
                "stateenabled": self.core.getCheckStateValue(self.state.checkState(0)),
                "additionalSettings": {s["name"]: s["value"] for s in self.additionalSettings}
            }
        )

        getattr(self.core.appPlugin, "sm_export_getStateProps", lambda x, y: None)(
            self, stateProps
        )

        self.core.callback("onStateGetSettings", self, stateProps)
        
        return stateProps



class AdditionalSettingsDialog(QDialog):
    def __init__(self, state):
        super(AdditionalSettingsDialog, self).__init__()
        self.state = state
        self.core = self.state.core
        self.core.parentWindow(self, parent=self.state)
        self.widgets = []
        self.loadLayout()


    @err_catcher(name=__name__)
    def loadLayout(self):
        self.setWindowTitle("Additional Settings")
        self.lo_main = QVBoxLayout(self)

        for setting in self.state.additionalSettings:
            widgets = {}
            w = QWidget()
            lo = QHBoxLayout(w)
            lo.setContentsMargins(9, 0, 9, 0)
            l = QLabel(setting["label"] + ":")
            lo.addWidget(l)
            lo.addStretch()
            setattr(self, "l_" + setting["name"], l)
            setattr(self, "w_" + setting["name"], w)
            setattr(self, "lo_" + setting["name"], lo)
            self.lo_main.addWidget(w)
            widgets = {"widget": w, "label": l, "type": setting["type"]}

            if setting["type"] == "checkbox":
                chb = QCheckBox()
                lo.addWidget(chb)
                setattr(self, "chb_" + setting["name"], chb)
                widgets["checkbox"] = chb
                chb.setChecked(setting["value"])
                chb.toggled.connect(lambda x: self.refreshVisibility())
            elif setting["type"] == "combobox":
                cb = QComboBox()
                lo.addWidget(cb)
                setattr(self, "cb_" + setting["name"], cb)
                widgets["combobox"] = cb
                cb.addItems(setting["items"])
                cb.setCurrentText(setting["value"])
                cb.currentIndexChanged.connect(lambda x: self.refreshVisibility())
            elif setting["type"] == "float":
                sp = QDoubleSpinBox()
                lo.addWidget(sp)
                setattr(self, "sp_" + setting["name"], sp)
                widgets["spinbox"] = sp
                sp.setValue(setting["value"])

            if not setting.get("visible", lambda dlg, state: True)(self, self.state):
                w.setHidden(True)

            self.widgets.append(widgets)

        self.lo_main.addStretch()
        self.bb_main = QDialogButtonBox()
        self.bb_main.addButton("Accept", QDialogButtonBox.AcceptRole)
        self.bb_main.addButton("Cancel", QDialogButtonBox.RejectRole)
        self.bb_main.accepted.connect(self.onAccept)
        self.bb_main.rejected.connect(self.reject)
        self.lo_main.addWidget(self.bb_main)


    @err_catcher(name=__name__)
    def refreshVisibility(self):
        for idx, setting in enumerate(self.state.additionalSettings):
            self.widgets[idx]["widget"].setHidden(not setting.get("visible", lambda dlg, state: True)(self, self.state))


    @err_catcher(name=__name__)
    def onAccept(self):
        for idx, setting in enumerate(self.state.additionalSettings):
            val = self.getValueFromWidget(self.widgets[idx])
            setting["value"] = val

        self.state.stateManager.saveStatesToScene()
        self.accept()


    @err_catcher(name=__name__)
    def getValueFromWidget(self, widget):
        if widget["type"] == "checkbox":
            return widget["checkbox"].isChecked()
        elif widget["type"] == "combobox":
            return widget["combobox"].currentText()
        elif widget["type"] == "float":
            return widget["spinbox"].value()
