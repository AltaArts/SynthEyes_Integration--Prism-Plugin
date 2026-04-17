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


###########################################################################
##                                                                       ##
##      This launches a Listener Thread to receive commands from the     ##
##      Prism Scripts in SynthEyes (called from the Prism Menu), and     ##
##      sends a signal to Prism_SynthEyes_Functions.                     ##
##                                                                       ##


import socket
import threading
import logging
import json
from typing import TYPE_CHECKING

from qtpy.QtCore import QObject, Signal

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from PrismCore import PrismCore
    from Prism_SynthEyes_Functions import Prism_SynthEyes_Functions


#   Signals for Prism_SynthEyes_Functions to Receive
class PrismSignalBridge(QObject):
    commandReceived = Signal(dict)



#   Listener Thread
class PrismCommsListener:
    def __init__(self, origin, host, port):
        self.synthFucnts:Prism_SynthEyes_Functions = origin
        self.core:PrismCore = origin.core

        self.host:str = host
        self.port:int = port
        self.bridge = PrismSignalBridge()


    def start(self):
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()


    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server.bind((self.host, self.port))
        server.listen(5)

        while True:
            client, addr = server.accept()
            data = client.recv(4096).decode("utf-8")

            if data:
                self.handleMessage(data)

            client.close()


    def handleMessage(self, data):
        logger.debug(f"[SynthListener]  Received: {data}")

        msg = json.loads(data)

        #   Send Signal to Main Qt Thread
        self.bridge.commandReceived.emit(msg)

