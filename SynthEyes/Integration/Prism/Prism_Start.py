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
import platform


if "PRISM_ROOT" in os.environ:
    PRISMROOT = os.environ["PRISM_ROOT"]
    
#   Gets set during Integration installation
else:
    # print("PRISM_ROOT is not set")
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


import SyPy3


# hlev = SyPy.SyLevel()
# hlev.OpenExisting()



class PrismToolsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.core = None

        self.parent_pid = os.getppid()

        self.getPrismCore()
        self.setup_ui()
        self.load_stylesheet()
        self.connections()
        self.start_parent_monitor()


    #   Creates Prism instance
    def getPrismCore(self):
        self.core = PrismCore.create(app="SynthEyes", prismArgs=["noProjectBrowser"])

        if not platform.system() == "Darwin":
            curPrj = self.core.getConfig("globals", "current project")


    #   UI Setup
    def setup_ui(self):
        self.setObjectName("MainWindow")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setWindowTitle("Prism Tools")
        self.setGeometry(100, 100, 250, 250)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)

        central = QWidget()
        self.setCentralWidget(central)

        self.layout = QVBoxLayout(central)

        self.buttons = {
            "saveVersion": "Save Version",
            "saveComment": "Save Version with Comment",
            "openProjectBrowser": "Project Browser",
            "openStateManager": "State Manager",
            "openPrismSettings": "Prism Settings",
        }

        for key, label in self.buttons.items():

            btn = QPushButton(label)
            btn.setObjectName(f"b_{key}")
            btn.setFixedHeight(40)

            # Create attribute like self.b_saveVersion
            setattr(self, f"b_{key}", btn)

            # Connect to a dispatcher
            # btn.clicked.connect(lambda checked, k=key: self.handle_button(k))

            self.layout.addWidget(btn)


    #   Styling
    def load_stylesheet(self):
        qss_path = os.path.join(
            PLUGINROOT,
            "UserInterfaces",
            "SynthEyesStyleSheet",
            "SynthEyes.qss"
        )

        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                qss = f.read()

            # Fix relative image paths if needed
            style_dir = os.path.dirname(qss_path)
            qss = qss.replace("url(images/", f"url({style_dir}/images/")

            QApplication.instance().setStyleSheet(qss)


    def connections(self):
        self.b_saveVersion.clicked.connect(self.saveVersion)
        self.b_saveComment.clicked.connect(self.saveComment)
        self.b_openProjectBrowser.clicked.connect(self.open_ProjectBrowser)
        self.b_openStateManager.clicked.connect(self.open_StateManager)
        self.b_openPrismSettings.clicked.connect(self.open_PrismSettings)



    # Parent Process Monitoring
    def start_parent_monitor(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_parent)
        self.timer.start(1000)

    def check_parent(self):
        try:
            parent = psutil.Process(self.parent_pid)
            if not parent.is_running():
                self.close()
        except psutil.NoSuchProcess:
            self.close()



    def saveVersion(self):
        self.core.popup("PRISM POPUP: SAVE VERSION")


    def saveComment(self):
        self.core.popup("PRISM POPUP: SAVE COMMENT")


    def open_ProjectBrowser(self):
        self.core.projectBrowser()


    def open_StateManager(self):
        self.core.stateManager()


    def open_PrismSettings(self):
        self.core.prismSettings()



#   Entry Point
def main():
    app = QApplication(sys.argv)

    window = PrismToolsWindow()
    window.show()

    sys.exit(app.exec_())


#   Auto Run
if __name__ == "__main__":
    main()