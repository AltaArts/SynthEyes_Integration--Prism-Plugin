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


class Prism_SynthEyes_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v1.0"
        self.pluginName = "SynthEyes"
        self.pluginType = "App"
        self.appShortName = "syntheyes"
        self.appType = "3d"
        self.hasQtParent = False
        self.sceneFormats = [".sni"]
        self.appSpecificFormats = self.sceneFormats
        self.importFormats = ["usd", "usdc", ".usda", ".obj", ".fbx", "glb"]
        self.outputFormats = [".usda", ".abc", ".obj", ".fbx", ".comp", ".blend", "ShotCam"]
        self.appColor = [200, 180, 0]
        self.canDeleteRenderPasses = False
        self.colorButtonWithStyleSheet = True
        self.platforms = ["Windows", "Linux", "Darwin"]
        self.pluginDirectory = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        self.appIcon = os.path.join(self.pluginDirectory, "UserInterfaces", "SynthEyes.ico")
        self.prismAppIcon = os.path.join(self.pluginDirectory, "UserInterfaces", "SynthEyes.ico")
        self.synthStates = [
            "Folder",
            "AddShot",
            "ImportMesh",
            "SceneExport",
            "RenderShot",
            "StMap",
            "Playblast"
            ]
        
        self.synthMenuData = [
            {
                "menuName": "Save Next Version",
                "menuPos": 1,
                "scriptName": "Prism - Save Version",
                "actionID": None,
            },
            {
                "menuName": "Save Version with Comment",
                "menuPos": 2,
                "scriptName": "Prism - Save Comment",
                "actionID": None,
            },
            {
                "menuName": "Project Browser",
                "menuPos": 3,
                "scriptName": "Prism - Open Project Browser",
                "actionID": None,
            },
            {
                "menuName": "State Manager",
                "menuPos": 4,
                "scriptName": "Prism - Open State Manager",
                "actionID": None,
            },
            {
                "menuName": "Prism Settings",
                "menuPos": 5,
                "scriptName": "Prism - Open Prism Settings",
                "actionID": None,
            },
            {
                "menuName": "Reset Prism",
                "menuPos": 6,
                "scriptName": "Launch Prism",
                "actionID": None,
            },
        ]