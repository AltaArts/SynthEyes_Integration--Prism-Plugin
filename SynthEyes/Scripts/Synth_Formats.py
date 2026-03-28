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
##      This is a collection of SynthEyes settings names for             ##
##      use in various SynthEyes API calls.                              ##



## SynthEyes Format Naming and Settings Options
SynthFormatNames: dict = {
    "USD  (.usda)": {
        "synthName": "USD ASCII Scene",
        "format": ".usda",
        "exportSettings": {
            "workArea": {
                "name": "Timeline Setup",
                "widgetType": "combo",
                "comboItems": [("Active part", "0"), ("Entire shot", "1"), ("Match frames", "2")],
                "factoryDefault": "2",
                "toolTip": "Controls which portion of the shot is placed at the Starting frame#.\nMatch Frames makes the placement match the image sequence's frame numbers;\nequivalent to Entire shot for movies."
            },
            "userStart": {
                "name": "Starting Frame",
                "widgetType": "spin",
                "range": [0, 1000000],
                "step": 1,
                "factoryDefault": 1,
                "toolTip": "The first frame of the selected part of the shot will be put at this frame number in the export.\nNot used when Match frames is selected unless the shot is a movie."
            },
            "units": {
                "name": "Interpret SynthEyes Units as",
                "widgetType": "combo",
                "comboItems": [("Use scene settings", "scene"), ("None", ""), ("Millimeters", "mm"), ("Centimeters", "cm"), ("Meters", "m"), ("Kilometers", "km"), ("Inches", "in"), ("Feet", "ft"), ("Yards", "yd"), ("Miles", "mi")],
                "factoryDefault": "ft",
                "toolTip": "This sets metersPerUnit in the USD scene."
            },
            "buildRigs": {
                "name": "Deform with Rigs",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set, a rig will be exported for Geometric Hierarchy Tracking rigs.\nWhen off, deformed meshes will be exported via a vertex cache."
            },
            "fixAD": {
                "name": "Fix Anamorphic Distance",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When on and an anamorphic distance is present,\neach mesh has a vertex cache, and tracker positions are compensated..."
            },
            "doScreen": {
                "name": "Projection Screens",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Generate a projection screen to hold the shot imagery..."
            },
            "usePreprocessor": {
                "name": "Based On",
                "widgetType": "combo",
                "comboItems": [("Solver distortion", "0"), ("Image Preprocessor (normal)", "1")],
                "factoryDefault": "1",
                "toolTip": "Where to look for lens distortion information..."
            },
            "uvScreenMode": {
                "name": "UV Screen Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("If a UVmap is present", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "Controls when UV projection mode is used."
            },
            "nomgrid": {
                "name": "Horizontal Grids",
                "widgetType": "spin",
                "range": [12, 256],
                "step": 1,
                "factoryDefault": 64,
                "toolTip": "Number of horizontal grids for a projection screen."
            },
            "relScreenDis": {
                "name": "Screen Relative Distance",
                "widgetType": "spin",
                "range": [0, 20],
                "step": 1,
                "factoryDefault": 5,
                "toolTip": "Distance from camera to projection screen..."
            },
            "rotOrder": {
                "name": "Rotation Order",
                "widgetType": "combo",
                "comboItems": [("XYZ", "0"), ("ZXY", "1")],
                "factoryDefault": "1",
                "toolTip": "Use this rotation order."
            },
            "relTrkSize": {
                "name": "Relative Tracker Size",
                "widgetType": "doubleSpin",
                "range": [0.001, 10],
                "precision": 3,
                "step": .001,
                "factoryDefault": 0.001,
                "toolTip": "Tracker marker size as fraction of world size."
            },
            "relLidarSize": {
                "name": "Relative Lidar Size",
                "widgetType": "doubleSpin",
                "range": [0.0001, 10],
                "precision": 4,
                "step": .0001,
                "factoryDefault": 0.0002,
                "toolTip": "Lidar point size as fraction of world size."
            },
            "relFarClip": {
                "name": "Far Clipping Plane Multiple",
                "widgetType": "spin",
                "range": [1, 50],
                "step": 1,
                "factoryDefault": 10,
                "toolTip": "Far clipping plane distance."
            },
            "miscOpacity": {
                "name": "Gnomon/Tracker Opacity",
                "widgetType": "doubleSpin",
                "range": [0, 1],
                "precision": 2,
                "step": .01,
                "factoryDefault": 1,
                "toolTip": "Opacity setting for helper visuals."
            },
            "doFrustrum": {
                "name": "Camera Frustrums",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Show camera viewing frustrum."
            },
            "doGnomon": {
                "name": "Object Gnomons",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Include gnomon mesh."
            },
            "doChisel": {
                "name": "Tracker Chisels",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Include chisel mesh."
            },
            "geoPrimitives": {
                "name": "Use USD Primitives",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Use USD primitive types where possible."
            },
            "silentMovies": {
                "name": "Silence Movie Warnings",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Silence warnings for movie imagery."
            }
        }
    },
    "FBX  (.fbx)": {
        "synthName": "Filmbox FBX",
        "format": ".fbx"
    },
    "Alembic  (.abc)": {
        "synthName": "Alembic 1.5+",
        "format": ".abc"
    },
    "Blender  (.py)": {
        "synthName": "Blender (Python)",
        "format": ".py"
    },
    "Maya  (.ma)": {
        "synthName": "Maya ASCII Updated",
        "format": ".ma"
    },
    "BMD Fusion  (.comp)": {
        "synthName": "Fusion Composition",
        "format": ".comp"
    },
    "Nuke  (.nk)": {
        "synthName": "Nuke (Current)",
        "format": ".nk"
    },
}





## SynthEyes EXR 'Compression' Strings
SynthExrCompress:dict = {
    "NONE": "exr: <None>,45",
    "ZIP":"exr: <ZIP-block>,45",
    "ZIPS": "exr: <ZIP-scanline>,45",
    "DWAA": "exr: <DWAA32 Lossy>,45",
    "DWAB": "exr: <DWAB256 Lossy>,45",
    "RLE": "exr: <Run-length>,45",
    "PXR24": "exr: <PXR Lossy>,45"
    }

## SynthEyes MOV 'Compression' Strings
SynthMovCodecs:dict = {
    "ProRes 422": "prores: <prores422>,0",
    "ProRes LT": "prores: <prores422lt>,0",
    "ProRes Proxy": "prores: <prores422proxy>,0",
    "ProRes 4444": "prores: <prores4444>,0",
    "ProRes 4444XQ": "prores: <prores4444xq>,0",
    }

## SynthEyes MP4 'Compression' Strings
#      The first part
SynthMP4Codecs:dict = {
    "H264": "WMFC: 'H264' K:0 Q:0",
    "H265": "WMFC: 'HEVC' K:0 Q:0",
    }

## SynthEyes MP4 'Compression' Strings
#       the second part
SynthMP4Qual:dict = {
    "High (30 Mb/s)": "B:30000000",
    "Good (15 Mb/s)": "B:15000000",
    "Med (8 Mb/s)": "B:8000000",
    "Low (4 Mb/s)": "B:4000000",
    "Preview (2 Mb/s)": "B:2000000",
    }

## SynthEyes Alpha Supported Formats
SynthHasAlpha:list = [
    "ProRes 4444",
    "ProRes 4444XQ",
    "EXR",
    "PNG"
] 

## SynthEyes Image PreProcessor Subsampling Ints
SynthSubSample:dict = {
    "100%": 1.0,
    "50%": 2.0,
    "25%": 4.0
}

## SynthEyes Image PreProcessor Subsampling Filters
SynthInterp:dict = {
    "Low (Bi-Linear)": 0.0,
    "Med (Lanczos 2)": 1.0,
    "Good (Mitchell)": 3.0,
    "High (Lanczos 3)": 2.0
}

