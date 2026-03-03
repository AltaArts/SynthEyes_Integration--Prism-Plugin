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

import bpy

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher as err_catcher


class Import_SceneData(QDialog):
    def __init__(self, core, plugin):
        super(Import_SceneData, self).__init__()
        self.core = core
        self.plugin = plugin
        self.mode = None
        self.importedNodes = []

    @err_catcher(name=__name__)
    def importScene(self, scenepath, update, state):
        self.scenepath = scenepath
        self.state = state
        self.updated = False

        validNodes = [
            x for x in self.state.nodes if self.plugin.isNodeValid(self.state, x)
        ]
        if update and validNodes:
            self.updated = self.updateData(validNodes)
            if self.updated:
                return

        self.setupUI()
        self.connectEvents()
        self.refreshTree()
        action = self.exec_()
        return {"result": action, "mode": self.mode, "importedNodes": self.importedNodes}

    @err_catcher(name=__name__)
    def setupUI(self):
        self.core.parentWindow(self)
        self.setWindowTitle(os.path.basename(self.scenepath))
        self.lo_main = QVBoxLayout()
        self.tw_scenedata = QTreeWidget()
        self.tw_scenedata.header().setVisible(False)

        self.tw_scenedata.setColumnCount(1)
        self.tw_scenedata.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tw_scenedata.setSortingEnabled(False)
        self.tw_scenedata.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_scenedata.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_scenedata.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_scenedata.itemClicked.connect(self.selectionChanged)

        self.rb_append = QRadioButton("Append")
        self.rb_append.setChecked(True)
        self.chb_override = QCheckBox("Create Library Override")
        self.chb_override.setChecked(True)
        self.rb_link = QRadioButton("Link")
        self.rb_append.toggled.connect(self.onModeChanged)
        self.rb_link.toggled.connect(self.onModeChanged)
        self.onModeChanged()

        self.bb_main = QDialogButtonBox(QDialogButtonBox.Cancel)
        b_accept = self.bb_main.addButton("Accept", QDialogButtonBox.AcceptRole)
        b_accept.clicked.connect(self.importData)
        self.bb_main.rejected.connect(self.reject)

        self.w_footer = QWidget()
        self.lo_footer = QGridLayout(self.w_footer)
        self.spacer = QWidget()
        policy = QSizePolicy()
        policy.setHorizontalPolicy(QSizePolicy.Expanding)
        policy.setHorizontalStretch(50)
        self.spacer.setSizePolicy(policy)
        self.lo_footer.addWidget(self.spacer, 0, 0)
        self.lo_footer.addWidget(self.rb_append, 0, 1)
        self.lo_footer.addWidget(self.rb_link, 1, 1)
        self.lo_footer.addWidget(self.chb_override, 1, 2)

        self.lo_main.addWidget(self.tw_scenedata)
        self.lo_main.addWidget(self.w_footer)
        self.lo_main.addWidget(self.bb_main)
        self.setLayout(self.lo_main)

        self.resize(800 * self.core.uiScaleFactor, 600 * self.core.uiScaleFactor)

    @err_catcher(name=__name__)
    def connectEvents(self):
        self.tw_scenedata.doubleClicked.connect(self.accept)
        self.tw_scenedata.doubleClicked.connect(lambda: self.importData())

    @err_catcher(name=__name__)
    def onModeChanged(self, state=None):
        self.chb_override.setEnabled(self.rb_link.isChecked())

    @err_catcher(name=__name__)
    def selectionChanged(self, item, column):
        for cIdx in range(item.childCount()):
            item.child(cIdx).setSelected(item.isSelected())

    @err_catcher(name=__name__)
    def refreshTree(self):
        with bpy.data.libraries.load(self.scenepath, link=False) as (
            data_from,
            data_to,
        ):
            pass

        self.tw_scenedata.clear()

        cats = ["Collections", "Objects"]

        for cat in cats:
            parentItem = QTreeWidgetItem([cat])
            self.tw_scenedata.addTopLevelItem(parentItem)
            parentItem.setExpanded(True)

            for obj in getattr(data_from, cat.lower()):
                item = QTreeWidgetItem([obj])
                parentItem.addChild(item)

    @err_catcher(name=__name__)
    def getSelectedData(self):
        data = {}
        for iIdx in range(self.tw_scenedata.topLevelItemCount()):
            tItem = self.tw_scenedata.topLevelItem(iIdx)
            data[tItem.text(0).lower()] = []

        for sItem in self.tw_scenedata.selectedItems():
            if not sItem.parent():
                continue

            data[sItem.parent().text(0).lower()].append({"name": sItem.text(0)})

        return data

    @err_catcher(name=__name__)
    def updateData(self, validNodes):
        updated = False
        libs = []
        if validNodes:
            for i in validNodes:
                obj = self.plugin.getObject(i)
                if obj.library and obj.library not in libs:
                    updated = True
                    oldLib = obj.library.filepath
                    obj.library.filepath = self.scenepath
                    libs.append(obj.library)
                    for node in self.state.nodes:
                        if node["library"] == oldLib:
                            node["library"] = self.scenepath

                elif obj.override_library and obj.override_library.reference:
                    lib = obj.override_library.reference.library
                    if lib:
                        updated = True
                        oldLib = lib.filepath
                        libs.append(lib)
                        lib.filepath = self.scenepath
                        for node in self.state.nodes:
                            if node["library"] == oldLib:
                                node["library"] = self.scenepath

            for lib in libs:
                lib.reload()
        
        return updated

    @err_catcher(name=__name__)
    def importData(self):
        link = self.rb_link.isChecked()
        self.state.preDelete(
            baseText="Do you want to delete the currently connected objects?\n\n"
        )

        if bpy.app.version >= (2, 80, 0):
            self.existingNodes = list(bpy.data.objects) + list(bpy.data.collections)
        else:
            self.existingNodes = list(bpy.context.scene.objects) + list(bpy.data.collections)

        data = self.getSelectedData()
        if not data["collections"] and not data["objects"]:
            self.core.popup("Nothing selected to import.")
            return

        ctx = self.plugin.getOverrideContext(self)
        self.hide()
        importedNodes = []
        self.mode = "link" if link else "append"
        # bpy.context.collection.children.link creates collections, which can't have library overrides so we have to use bpy.ops
        if link:
            if data["collections"]:
                with bpy.data.libraries.load(self.scenepath, link=True) as (data_from, data_to):
                    colNames = [c["name"] for c in data["collections"]]
                    data_to.collections = [c for c in data_from.collections if c in colNames]

                scene = bpy.context.scene
                vlayer = bpy.context.view_layer
                for col in data_to.collections:
                    if self.chb_override.isChecked():
                        col = col.override_hierarchy_create(scene, vlayer, do_fully_editable=True)
                    else:
                        try:
                            bpy.context.scene.collection.children.link(col)
                        except Exception as e:
                            if "already in collection " in str(e):
                                msg = "Collection \"%s\" is already linked to the current viewlayer. You can link it with an override to get a second instance." % (col.name)
                                result = self.core.popupQuestion(msg, buttons=["Create Override", "Cancel"])
                                if result == "Create Override":
                                    col = col.override_hierarchy_create(scene, vlayer, do_fully_editable=True)
                                else:
                                    self.reject()
                                    return
                            else:
                                raise

                    importedNodes.append(col)

            if data["objects"]:
                with bpy.data.libraries.load(self.scenepath, link=True) as (data_from, data_to):
                    objNames = [c["name"] for c in data["objects"]]
                    data_to.objects = [c for c in data_from.objects if c in objNames]

                scene = bpy.context.scene
                vlayer = bpy.context.view_layer
                for obj in data_to.objects:
                    if self.chb_override.isChecked():
                        obj = obj.override_hierarchy_create(scene, vlayer, do_fully_editable=True)
                    else:
                        try:
                            bpy.context.scene.collection.objects.link(obj)
                        except Exception as e:
                            if "already in collection " in str(e):
                                msg = "Collection \"%s\" is already linked to the current viewlayer. You can link it with an override to get a second instance." % (obj.name)
                                result = self.core.popupQuestion(msg, buttons=["Create Override", "Cancel"])
                                if result == "Create Override":
                                    obj = obj.override_hierarchy_create(scene, vlayer, do_fully_editable=True)
                                else:
                                    self.reject()
                                    return
                            else:
                                raise

                    importedNodes.append(obj)

            self.importedNodes = [self.plugin.getNode(obj) for obj in importedNodes]
        else:
            if data["collections"]:
                if bpy.app.version < (4, 0, 0):
                    bpy.ops.wm.append(
                        ctx,
                        directory=self.scenepath + "/Collection/",
                        files=data["collections"],
                    )
                else:
                    with bpy.context.temp_override(**ctx):
                        bpy.ops.wm.append(
                            directory=self.scenepath + "/Collection/",
                            files=data["collections"],
                        )
            if data["objects"]:
                if bpy.app.version < (4, 0, 0):
                    bpy.ops.wm.append(
                        ctx, directory=self.scenepath + "/Object/", files=data["objects"]
                    )
                else:
                    with bpy.context.temp_override(**ctx):
                        bpy.ops.wm.append(
                            directory=self.scenepath + "/Object/", files=data["objects"]
                        )

        self.accept()
