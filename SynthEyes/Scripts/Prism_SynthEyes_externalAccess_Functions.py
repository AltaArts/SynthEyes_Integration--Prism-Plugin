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

        self.core.registerCallback("userSettings_saveSettings", self.userSettings_saveSettings, plugin=self.plugin)
        self.core.registerCallback("userSettings_loadSettings", self.userSettings_loadSettings, plugin=self.plugin)
        self.core.registerCallback("getPresetScenes", self.getPresetScenes, plugin=self.plugin)

        ssheetPath = os.path.join(self.pluginDirectory, "UserInterfaces", "SynthEyesStyleSheet")
        self.core.registerStyleSheet(ssheetPath)


    @err_catcher(name=__name__)
    def userSettings_loadUI(self, origin, tab):
        #   Options Groupbox
        origin.gb_synthOptions = QGroupBox("Options")
        origin.gb_synthOptions.setCheckable(False)
        origin.gb_synthOptions.setChecked(True)

        #   Grid Layout
        lo_synthOptions = QGridLayout()
        lo_synthOptions.setContentsMargins(30, 10, 30, 10)
        lo_synthOptions.setHorizontalSpacing(20)
        origin.gb_synthOptions.setLayout(lo_synthOptions)

        #   Auto-start
        l_autoStart = QLabel("Click to Set Prism Auto-start:")
        l_autoStart.setFixedWidth(280)
        origin.b_autoStart = QPushButton("Add")
        origin.b_autoStart.setFixedWidth(100)
        lo_synthOptions.addWidget(l_autoStart, 0, 0, alignment=Qt.AlignLeft)
        lo_synthOptions.addWidget(origin.b_autoStart, 0, 1, alignment=Qt.AlignLeft)

        #   Comms Port
        l_port = QLabel("SynthEyes Communications Socket Port:")
        l_port.setFixedWidth(280)
        origin.sp_port = QSpinBox()
        origin.sp_port.setFixedWidth(150)
        origin.sp_port.setRange(49152, 65535)
        origin.sp_port.setValue(50555)
        lo_synthOptions.addWidget(l_port, 1, 0, alignment=Qt.AlignLeft)
        lo_synthOptions.addWidget(origin.sp_port, 1, 1, alignment=Qt.AlignLeft)

        #   Add Options to DCC Tab
        tab.layout().addWidget(origin.gb_synthOptions)

        #   Defaults Groupbox
        origin.gb_synthDefaults = QGroupBox("Defaults")
        origin.gb_synthDefaults.setCheckable(False)
        origin.gb_synthDefaults.setChecked(True)

        #   Grid Layout
        lo_synthDefaults = QGridLayout()
        lo_synthDefaults.setContentsMargins(30, 10, 30, 10)
        lo_synthDefaults.setHorizontalSpacing(20)
        origin.gb_synthDefaults.setLayout(lo_synthDefaults)

        #   Scene Camera Prefix
        l_sceneCam = QLabel("Scene Camera Prefix:")
        l_sceneCam.setFixedWidth(280)
        origin.le_sceneCam = QLineEdit()
        origin.le_sceneCam.setObjectName("synth_LineEdit_Wide")
        lo_synthDefaults.addWidget(l_sceneCam, 0, 0)
        lo_synthDefaults.addWidget(origin.le_sceneCam, 0, 1)

        #   Shot Camera Prefix
        l_shotCam = QLabel("Shot Camera Prefix:")
        l_shotCam.setFixedWidth(280)
        origin.le_shotCam = QLineEdit()
        origin.le_shotCam.setObjectName("synth_LineEdit_Wide")
        lo_synthDefaults.addWidget(l_shotCam, 1, 0)
        lo_synthDefaults.addWidget(origin.le_shotCam, 1, 1)

        #   UnDistort Suffix
        l_unDistort = QLabel("UnDistort Suffix:")
        l_unDistort.setFixedWidth(280)
        origin.le_unDistort = QLineEdit()
        origin.le_unDistort.setObjectName("synth_LineEdit_Wide")
        lo_synthDefaults.addWidget(l_unDistort, 2, 0)
        lo_synthDefaults.addWidget(origin.le_unDistort, 2, 1)

        #   ReDistort Suffix
        l_reDistort = QLabel("ReDistort Suffix:")
        l_reDistort.setFixedWidth(280)
        origin.le_reDistort = QLineEdit()
        origin.le_reDistort.setObjectName("synth_LineEdit_Wide")
        lo_synthDefaults.addWidget(l_reDistort, 3, 0)
        lo_synthDefaults.addWidget(origin.le_reDistort, 3, 1)

        #   Override Line Edit Style for Full Width
        style = """
        QLineEdit#synth_LineEdit_Wide {
            min-width: 300px;
            max-width: 16777215px;
            width: 300px;
        }
        """
        origin.le_sceneCam.setStyleSheet(style)
        origin.le_shotCam.setStyleSheet(style)
        origin.le_unDistort.setStyleSheet(style)
        origin.le_reDistort.setStyleSheet(style)

        #   Add Options to DCC Tab
        tab.layout().addWidget(origin.gb_synthDefaults)

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

        tip = ("This is the prefix that will be automatically added to\n"
               "new Scene Camera names.\n\n"
               "The name can be manually edited in the AddShot state.")
        l_sceneCam.setToolTip(tip)
        origin.le_sceneCam.setToolTip(tip)

        tip = ("This is the prefix that will be automatically added to\n"
               "new additional Shot Camera names.\n\n"
               "The name can be manually edited in the AddShot state.")
        l_shotCam.setToolTip(tip)
        origin.le_shotCam.setToolTip(tip)

        tip = ("This is the suffix that will be automatically added to\n"
               "the STMap Un-Distort file.")
        l_unDistort.setToolTip(tip)
        origin.le_unDistort.setToolTip(tip)

        tip = ("This is the suffix that will be automatically added to\n"
               "the STMap Re-Distort file.")
        l_reDistort.setToolTip(tip)
        origin.le_reDistort.setToolTip(tip)


    @err_catcher(name=__name__)
    def userSettings_saveSettings(self, origin, settings):
        if "SynthEyes" not in settings:
            settings["SynthEyes"] = {}

        if hasattr(origin, "sp_port"):
            settings["SynthEyes"]["commsPort"] = origin.sp_port.value()

        if hasattr(origin, "le_sceneCam"):
            settings["SynthEyes"]["sceneCamPrefix"] = origin.le_sceneCam.text()

        if hasattr(origin, "le_shotCam"):
            settings["SynthEyes"]["shotCamPrefix"] = origin.le_shotCam.text()

        if hasattr(origin, "le_unDistort"):
            settings["SynthEyes"]["unDistortSuffix"] = origin.le_unDistort.text()

        if hasattr(origin, "le_reDistort"):
            settings["SynthEyes"]["reDistortSuffix"] = origin.le_reDistort.text()


    @err_catcher(name=__name__)
    def userSettings_loadSettings(self, origin, settings):
        #   Get Synth Settings from User Settings
        if "SynthEyes" in settings:
            sData = settings["SynthEyes"]
            
        #   Get Defaults from Variables
        else:
            sData = self.synthDefaults

        if "commsPort" in sData:
            origin.sp_port.setValue(sData["commsPort"])

        if "sceneCamPrefix" in sData:
            origin.le_sceneCam.setText(sData["sceneCamPrefix"])

        if "shotCamPrefix" in sData:
            origin.le_shotCam.setText(sData["shotCamPrefix"])

        if "unDistortSuffix" in sData:
            origin.le_unDistort.setText(sData["unDistortSuffix"])

        if "reDistortSuffix" in sData:
            origin.le_reDistort.setText(sData["reDistortSuffix"])


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