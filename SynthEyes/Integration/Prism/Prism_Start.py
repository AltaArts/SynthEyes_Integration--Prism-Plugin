# ; Start Prism

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
import socket
import json
import tempfile


if "PRISM_ROOT" in os.environ:
    PRISMROOT = os.environ["PRISM_ROOT"]
else:
    PRISMROOT = r@PRISMROOTREPLACE@

PLUGINROOT = r@PLUGINROOTREPLACE@

sys.path.append(PRISMROOT)
sys.path.insert(0, os.path.join(PRISMROOT, "Scripts"))
sys.path.append(os.path.join(PRISMROOT, "PythonLibs", "Python3"))


import PrismCore
import psutil

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *



#   Socket Communication
#   Imported to Each Prism Menu Script
def sendToPrism(command, payload=None):
    msg = {"command": command, "data": payload or {}}

    try:
        #   Get Port from Saved Temp File
        portFile = os.path.join(tempfile.gettempdir(), "prism_synth_port.txt")
        with open(portFile) as f:
            commsPort = int(f.read().strip())

        if not commsPort:
            raise Exception
        
    #   Use Default
    except:
        commsPort = 50555

    try:
        #   Start Listener Bridge
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect(("127.0.0.1", commsPort))

        s.send(json.dumps(msg).encode("utf-8"))
        s.close()

    except Exception as e:
        print("[Script_SaveVersion]  ERROR: Could not connect to Prism listener:", e)


#   Prism Tools Persistent Object
class PrismToolsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.core = None
        self.synthFuncts = None

        self.parent_pid = os.getppid()

        self.getPrismCore()
        self.getSynthFuncts()
        self.setupUI()
        self.loadStylesheet()
        self.connections()
        self.startSyntheyesMonitor()


    #   Creates Prism Instance
    def getPrismCore(self):
        self.core = PrismCore.create(app="SynthEyes", prismArgs=["noProjectBrowser", "splash"])


    #   Assigns the Plugin Functions Object
    def getSynthFuncts(self):
        self.synthFuncts = self.core.getPlugin("SynthEyes")


    #   Prism Tools UI Setup
    def setupUI(self):
        #   Main Tools Window
        self.setObjectName("MainWindow")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowTitle("Prism Tools")
        self.setGeometry(100, 100, 250, 250)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        #   Buttons Widget
        w_central = QWidget()
        self.setCentralWidget(w_central)
        lo_buttons = QVBoxLayout(w_central)

        #   Buttons Listing
        self.buttonDict = {
            "saveVersion": "Save Version",
            "saveComment": "Save Version with Comment",
            "openProjectBrowser": "Project Browser",
            "openStateManager": "State Manager",
            "openPrismSettings": "Prism Settings",
            "testOne": "Test 1",        #   TESTING
            "testTwo": "Test 2"         #   TESTING
        }

        #   Itterate Over Buttons and Create Objects
        for key, label in self.buttonDict.items():
            btn = QPushButton(label)
            btn.setObjectName(f"b_{key}")
            btn.setFixedHeight(40)

            #   Add Button to Class Self
            setattr(self, f"b_{key}", btn)

            lo_buttons.addWidget(btn)


    #   Style Sheet
    def loadStylesheet(self):
        #   Get SynthEyes Stylesheet from Plugin Dir
        qss_path = os.path.join(
            PLUGINROOT,
            "UserInterfaces",
            "SynthEyesStyleSheet",
            "SynthEyes.qss"
        )

        #   Read Stylesheet
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                qss = f.read()

            #   Fix Relative Image Paths if needed
            style_dir = os.path.dirname(qss_path)
            qss = qss.replace("url(images/", f"url({style_dir}/images/")

            QApplication.instance().setStyleSheet(qss)


    def connections(self):
        self.b_saveVersion.clicked.connect(self.saveVersion)
        self.b_saveComment.clicked.connect(self.saveComment)
        self.b_openProjectBrowser.clicked.connect(self.open_ProjectBrowser)
        self.b_openStateManager.clicked.connect(self.open_StateManager)
        self.b_openPrismSettings.clicked.connect(self.open_PrismSettings)

        self.b_testOne.clicked.connect(self.testOne)                        #   TESTING
        self.b_testTwo.clicked.connect(self.testTwo)                        #   TESTING


    #   Periodically Checks if SynthEyes is Still Running
    def startSyntheyesMonitor(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.checkSyntheyesRunning)
        self.timer.start(1000)


    #   Checks if SynthEyes is Still Running and Quit Prism if Not
    def checkSyntheyesRunning(self):
        try:
            parent = psutil.Process(self.parent_pid)
            if not parent.is_running():
                QApplication.quit()

        except psutil.NoSuchProcess:
            QApplication.quit()


    #   Calls from Prism Tools Buttons
    def saveVersion(self):
        self.synthFuncts.saveVersion()

    def saveComment(self):
        self.synthFuncts.saveComment()

    def open_ProjectBrowser(self):
        self.synthFuncts.open_ProjectBrowser()

    def open_StateManager(self):
        self.synthFuncts.open_StateManager()

    def open_PrismSettings(self):
        self.synthFuncts.open_PrismSettings()


    def testOne(self):                          #   TESTING
        self.synthFuncts.testOne()
        
    def testTwo(self):                          #   TESTING
        self.synthFuncts.testTwo()


#   Entry Point
def main():
    app = QApplication(sys.argv)

    #   Ensures Prism Tools Window Stays Persistent
    app.setQuitOnLastWindowClosed(False)

    #   Creates Hidden Prism Tools Window
    window = PrismToolsWindow()
    # window.show() #   Uncomment to Display Window

    sys.exit(app.exec_())


#   Auto Run
if __name__ == "__main__":
    main()