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

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_SynthEyes_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.core.registerCallback(
            "userSettings_saveSettings",
            self.userSettings_saveSettings,
            plugin=self.plugin,
            )
        
        self.core.registerCallback(
            "userSettings_loadSettings",
            self.userSettings_loadSettings,
            plugin=self.plugin,
            )
        
        self.core.registerCallback("getPresetScenes", self.getPresetScenes, plugin=self.plugin)

        ssheetPath = os.path.join(self.pluginDirectory, "UserInterfaces", "SynthEyesStyleSheet")
        self.core.registerStyleSheet(ssheetPath)


    @err_catcher(name=__name__)
    def userSettings_loadUI(self, origin, tab):
        origin.gb_options = QGroupBox("SynthEyes Socket Communications")
        lo_comms = QVBoxLayout()
        origin.gb_options.setLayout(lo_comms)
        origin.gb_options.setCheckable(False)
        origin.gb_options.setChecked(True)

        w_bldAutoSavePath = QWidget()
        lo_socketPort = QHBoxLayout()

        l_port = QLabel("Socket Port:   ")
        lo_socketPort.addWidget(l_port)

        origin.sp_port = QSpinBox()
        origin.sp_port.setRange(49152, 65535)
        origin.sp_port.setValue(50555)
        lo_socketPort.addWidget(origin.sp_port)

        lo_socketPort.setContentsMargins(20, 0, 0, 20)
        w_bldAutoSavePath.setLayout(lo_socketPort)

        lo_comms.addWidget(w_bldAutoSavePath)
        tab.layout().addWidget(origin.gb_options)


    @err_catcher(name=__name__)
    def userSettings_saveSettings(self, origin, settings):
        if "SynthEyes" not in settings:
            settings["SynthEyes"] = {}

        if hasattr(origin, "sp_port"):
            settings["SynthEyes"]["commsPort"] = origin.sp_port.value()


    @err_catcher(name=__name__)
    def userSettings_loadSettings(self, origin, settings):
        if "SynthEyes" in settings:
            if "commsPort" in settings["SynthEyes"]:
                origin.sp_port.setValue(settings["SynthEyes"]["commsPort"])


    @err_catcher(name=__name__)
    def getPresetScenes(self, presetScenes):
        if os.getenv("PRISM_SHOW_DEFAULT_SCENEFILE_PRESETS", "1") != "1":
            return

        presetDir = os.path.join(self.pluginDirectory, "Presets")
        scenes = self.core.entities.getPresetScenesFromFolder(presetDir)
        presetScenes += scenes
