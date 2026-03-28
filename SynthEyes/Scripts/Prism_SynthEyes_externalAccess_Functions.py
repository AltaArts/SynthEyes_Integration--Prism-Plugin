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

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


logger = logging.getLogger(__name__)


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
        #   Options Groupbox
        origin.gb_synthOptions = QGroupBox("SynthEyes Options")
        origin.gb_synthOptions.setCheckable(False)
        origin.gb_synthOptions.setChecked(True)

        #   Grid Layout
        grid = QGridLayout()
        grid.setContentsMargins(30, 10, 30, 10)
        grid.setHorizontalSpacing(20)
        origin.gb_synthOptions.setLayout(grid)

        #   Auto-start
        l_autoStart = QLabel("Click to Set Prism Auto-start:")
        l_autoStart.setFixedWidth(280)
        origin.b_autoStart = QPushButton("Add")
        origin.b_autoStart.setFixedWidth(100)
        grid.addWidget(l_autoStart, 0, 0, alignment=Qt.AlignLeft)
        grid.addWidget(origin.b_autoStart, 0, 1, alignment=Qt.AlignLeft)

        #   Comms Port
        l_port = QLabel("SynthEyes Communications Socket Port:")
        l_port.setFixedWidth(280)
        origin.sp_port = QSpinBox()
        origin.sp_port.setFixedWidth(150)
        origin.sp_port.setRange(49152, 65535)
        origin.sp_port.setValue(50555)
        grid.addWidget(l_port, 1, 0, alignment=Qt.AlignLeft)
        grid.addWidget(origin.sp_port, 1, 1, alignment=Qt.AlignLeft)

        #   Add Options to DCC Tab
        tab.layout().addWidget(origin.gb_synthOptions)

        #   Add Signal to Button and Pass the DCC Settings UI Objects
        origin.b_autoStart.clicked.connect(
            lambda: self.onAutostartClicked(
                origin.exOverridePlugins["SynthEyes"]["chb"],
                origin.exOverridePlugins["SynthEyes"]["le"]
                )
            )

        tip = ("Adds a .bat file to the 'Executable Override' (above).\n\n"
               "This .bat file will allow Prism to automatically\n"
               "start in SynthEyes.  To disable, just un-check the\n"
               "enabled checkbox above.")
        l_autoStart.setToolTip(tip)
        origin.b_autoStart.setToolTip(tip)

        tip = ("The port that the SynthEyes Prism integration uses\n"
               "for socket communications between the Prism menu\n"
               "in SynthEyes and Prism Core.")
        l_port.setToolTip(tip)
        origin.sp_port.setToolTip(tip)


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


    #   Sets the Executable Override for the Autostart
    @err_catcher(name=__name__)
    def onAutostartClicked(self, chb_ovr, le_ovr):
        #   Get SynthEyes Intergration
        integrations = self.core.integration.getIntegrations()
        synthData = integrations.get("SynthEyes")

        if not synthData:
            logger.warning("ERROR: Unable to Set Auto-start - SynthEyes integration not found.")
            self.core.popup("ERROR:\n\n"
                            "Unable to Set Auto-start - SynthEyes integration not found.")
            return

        #   Make Autostart Path
        synthPath = synthData[0]
        autostartPath = os.path.join(synthPath, "SynthEyes-Prism.bat")

        if not os.path.isfile(autostartPath):
            logger.warning("ERROR: Unable to Set Auto-start - 'SynthEyes-Prism.bat' not found.")
            self.core.popup("ERROR:\n\n"
                                      "Unable to Set Auto-start - 'SynthEyes-Prism.bat' not found.")
            return

        #   Set the Executable Override Path
        chb_ovr.setChecked(True)
        le_ovr.setText(autostartPath)