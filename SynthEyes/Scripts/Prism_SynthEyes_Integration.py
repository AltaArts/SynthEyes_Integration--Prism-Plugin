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
import glob

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

if platform.system() == "Windows":
    if sys.version[0] == "3":
        import winreg as _winreg
    else:
        import _winreg

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_SynthEyes_Integration(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        #   Sets Example Path
        if platform.system() == "Windows":
            self.examplePath = self.getSynthEyesPath() or "C:/Program Files/BorisFX/SynthEyes 2025.5"
        elif platform.system() == "Linux":
            self.examplePath = "/usr/local/synthEyes-4.5-linux-glibc219-x86_64/4.5"
        elif platform.system() == "Darwin":
            self.examplePath = os.path.expanduser("~/Library/Application Support/SynthEyes/4.5")


    #   Returns SynthEyes EXE from the Register Key for .SNI Files
    @err_catcher(name=__name__)
    def findSyntheyesFromReg(self):
        key_path = r"SOFTWARE\Classes\snifile\shell\open\command"

        try:
            key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, key_path)
            value, _ = _winreg.QueryValueEx(key, None)

            exe = value.strip().split(' ')[0].strip('"')

            if os.path.exists(exe):
                return exe

        except Exception:
            pass

        return None
    
    
    #   Returns Discovered SynthEyes EXE
    @err_catcher(name=__name__)
    def getExecutable(self):
        exe = self.findSyntheyesFromReg()
        return exe if exe else ""


    #   Returns SynthEyes Dir
    @err_catcher(name=__name__)
    def getSynthEyesPath(self):
        synth_exe = self.findSyntheyesFromReg()

        if synth_exe and os.path.isfile(synth_exe):
            return os.path.dirname(synth_exe)

        return ""
        

    @err_catcher(name=__name__)
    def getSynthEyesPaths(self):
        synthEyesPaths = []
        basepath = os.path.dirname(self.examplePath)

        for path in glob.glob(basepath + "/SynthEyes*"):
            if self.useUserPrefs:
                if os.path.exists(path + "/config"):
                    synthEyesPaths.append(os.path.normpath(path))
            else:
                if os.path.exists(path + "/synthEyes.exe"):
                    synthEyesPaths.append(os.path.normpath(path))

        regPath = self.getSynthEyesPath()
        if regPath and os.path.exists(regPath) and regPath not in synthEyesPaths:
            synthEyesPaths.append(regPath)

        return synthEyesPaths


    def addIntegration(self, installPath):
        try:
            #   Checks is Install Dir is Valid and Contains the EXE
            synthExeExists = os.path.isfile(os.path.join(installPath, "SynthEyes64.exe"))
            scripts_dir = os.path.join(installPath, "scripts")
            
            if not os.path.exists(scripts_dir) or not synthExeExists:
                msgStr = (
                    "Invalid SynthEyes path: %s.\n\nThe path has to be the SynthEyes install folder, which usually looks like this:\n\n%s"
                    % (self.examplePath)
                )
                self.core.popup(msgStr, title="Prism Integration")
                return False

            integrationBase = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Integration")
            integrationBase = os.path.realpath(integrationBase)
            prismScripts_dir = os.path.join(scripts_dir, "Prism")

            cmds = []
            addedFiles = []

            #   Cmd to Remove Prism Script Dir if Exists
            if os.path.exists(prismScripts_dir):
                cmd = {"type": "removeFolder", "args": [prismScripts_dir]}
                cmds.append(cmd)

            #   Cmd to Create the Prism Script Dir
            cmd = {"type": "createFolder", "args": [prismScripts_dir]}
            cmds.append(cmd)

            #   Cmd to Copy Prism Toolbar
            source_toolbar = os.path.abspath(os.path.join(integrationBase, "Prism.tbi"))
            dest_toolbar = os.path.abspath(os.path.join(scripts_dir, "Prism.tbi"))
            cmd = {"type": "copyFile", "args": [source_toolbar, dest_toolbar]}
            cmds.append(cmd)
            addedFiles.append(dest_toolbar)

            #   Cmd to Copy all the Integration Files
            prismInterDir = os.path.join(integrationBase, "Prism")
            for file in os.listdir(prismInterDir):
                source_path = os.path.abspath(os.path.join(prismInterDir, file))
                dest_path = os.path.abspath(os.path.join(prismScripts_dir, file))

                cmd = {"type": "copyFile", "args": [source_path, dest_path]}
                cmds.append(cmd)
                addedFiles.append(dest_path)

            #   Run the Commands
            result = self.core.runFileCommands(cmds)

            if not result:
                return False

            #   Change Owner if Needed
            if platform.system() in ["Linux", "Darwin"]:
                for i in addedFiles:
                    os.chmod(i, 0o777)

            #   Replaces Path Placeholders with Local Install Paths
            result = self.replacePaths(addedFiles)

            if result is True:
                return True
            elif result is False:
                return False
            else:
                raise Exception(result)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msgStr = (
                "Errors occurred during the installation of the SynthEyes integration.\nThe installation is possibly incomplete.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

            QMessageBox.warning(self.core.messageParent, "Prism Integration", msgStr)
            return False


    #   Replaces Path Placeholders with Local Install Paths
    def replacePaths(self, addedFiles):
        prismRoot = os.path.abspath(self.core.prismRoot)
        pluginRoot = os.path.dirname(os.path.dirname(__file__))

        cmds = []

        #   Read Each File and Replace Strings
        for file in addedFiles:
            with open(file, "r") as file_data:
                file_str = file_data.read()

            file_str = file_str.replace("@PRISMROOTREPLACE@", '"%s"' % prismRoot.replace("\\", "/"))
            file_str = file_str.replace("@PLUGINROOTREPLACE@", '"%s"' % pluginRoot.replace("\\", "/"))

            cmd = {"type": "writeToFile", "args": [file, file_str]}
            cmds.append(cmd)

        #   Run Commands
        result = self.core.runFileCommands(cmds)

        return result


    def removeIntegration(self, installPath):
        try:    
            cmds = []
            scripts_dir = os.path.join(installPath, "scripts")
            prismScripts_dir = os.path.join(scripts_dir, "Prism")
            toolbarfile = os.path.join(scripts_dir, "Prism.tbi")
            
            if os.path.isfile(toolbarfile):
                cmd = {"type": "removeFile", "args": [toolbarfile]}
                cmds.append(cmd)

            #   Cmd to Remove Prism Script Dir
            if os.path.exists(prismScripts_dir):
                cmd = {"type": "removeFolder", "args": [prismScripts_dir]}
                cmds.append(cmd)

            #   Run Commands
            result = self.core.runFileCommands(cmds)

            if result is True:
                return True
            elif result is False:
                return False
            else:
                raise Exception(result)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msgStr = (
                "Errors occurred during the removal of the SynthEyes integration.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

            QMessageBox.warning(self.core.messageParent, "Prism Integration", msgStr)
            return False


    def updateInstallerUI(self, userFolders, pItem):
        try:
            synthItem = QTreeWidgetItem(["SynthEyes"])
            synthItem.setCheckState(0, Qt.Checked)
            pItem.addChild(synthItem)

            synthPaths = self.getSynthEyesPaths() or []
            synthCustomItem = QTreeWidgetItem(["Custom"])
            synthCustomItem.setToolTip(0, 'e.g. "%s"' % self.examplePath)
            synthCustomItem.setToolTip(1, 'e.g. "%s"' % self.examplePath)
            synthCustomItem.setText(1, "< doubleclick to browse path >")
            synthCustomItem.setCheckState(0, Qt.Unchecked)
            synthCustomItem.setFlags(synthCustomItem.flags() & ~Qt.ItemIsAutoTristate)
            synthItem.addChild(synthCustomItem)
            synthItem.setExpanded(True)

            activeVersion = False
            for synthPath in synthPaths:
                synthVItem = QTreeWidgetItem([os.path.basename(synthPath).replace("SynthEyes ", "")])
                synthItem.addChild(synthVItem)

                synthVItem.setCheckState(0, Qt.Checked)
                synthVItem.setFlags(synthVItem.flags() & ~Qt.ItemIsAutoTristate)
                synthVItem.setText(1, synthPath)
                synthVItem.setToolTip(0, synthPath)
                synthVItem.setText(1, synthPath)
                activeVersion = True

            if not activeVersion:
                synthItem.setCheckState(0, Qt.Unchecked)
                synthCustomItem.setFlags(~Qt.ItemIsEnabled)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = QMessageBox.warning(
                self.core.messageParent,
                "Prism Installation",
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno),
            )
            return False


    def installerExecute(self, synthItem, result):
        try:
            synthPaths = []
            installLocs = []

            if synthItem.checkState(0) != Qt.Checked:
                return installLocs

            for i in range(synthItem.childCount()):
                item = synthItem.child(i)
                if item.checkState(0) == Qt.Checked and os.path.exists(item.text(1)):
                    synthPaths.append(item.text(1))

            for i in synthPaths:
                result["SynthEyes integration"] = self.core.integration.addIntegration(
                    self.plugin.pluginName, path=i, quiet=True
                )
                if result["SynthEyes integration"]:
                    installLocs.append(i)

            return installLocs
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = QMessageBox.warning(
                self.core.messageParent,
                "Prism Installation",
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno),
            )
            return False
