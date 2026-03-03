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

import SyPy3


print("Prism Test")                                 #   TESTING


if "PRISM_ROOT" in os.environ:
    PRISMROOT = os.environ["PRISM_ROOT"]

    print(f"PRISM ROOT IN ENVIRON: {PRISMROOT}")
    if not PRISMROOT:
        print("PRISM_ROOT is not set")
    
#   Gets set during Integration installation
else:
    print("PRISM_ROOT is not set")
    PRISMROOT = r@PRISMROOTREPLACE@

print(f"*** PRISMROOT:  {PRISMROOT}")                #   TESTING

PLUGINROOT = r@PLUGINROOTREPLACE@

print(f"*** PLUGINROOT: {PLUGINROOT}")               #    TESTING

input("Press Enter to exit...")









# hlev = SyPy.SyLevel()
# hlev.OpenExisting()

