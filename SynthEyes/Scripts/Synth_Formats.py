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
                "toolTip": "When on and an anamorphic distance is present, each mesh is exported with a vertex cache,\nand tracker positions are compensated, so that the shot lines up\n(as seen only from *this* current active camera) in non-savvy downstream applications.\nWon't fix meshes with rigs or pre-existing vertex caches."
            },
            "doScreen": {
                "name": "Projection Screens",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Generate a projection screen to hold the shot imagery, and possibly distort it to mimic the image preprocessor."
            },
            "usePreprocessor": {
                "name": "Based On",
                "widgetType": "combo",
                "comboItems": [("Solver distortion", "0"), ("Image Preprocessor (normal)", "1")],
                "factoryDefault": "1",
                "toolTip": "Where to look for lens distortion information. Normally, this should be the Image preprocessor,\nafter running the Lens Workflow script.\nThe solver's distortion can also be selected, though this is not recommended."
            },
            "uvScreenMode": {
                "name": "UV Screen Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("If a UVmap is present", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "With a UVmap, a projection screen using texture coordinates will work better than a vertex-positioning screen,\nalthough animated distortion can't be handled. This controls when the alternate version is used."
            },
            "nomgrid": {
                "name": "Horizontal Grids",
                "widgetType": "spin",
                "range": [12, 256],
                "step": 1,
                "factoryDefault": 64,
                "toolTip": "Number of horizontal grids for a projection screen. The vertical count is determined from the aspect ratio."
            },
            "relScreenDis": {
                "name": "Screen Relative Distance",
                "widgetType": "spin",
                "range": [0, 20],
                "step": 1,
                "factoryDefault": 5,
                "toolTip": "Distance from camera to projection screen for shot, as a multiple of the solver panel's world size"
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
                "toolTip": "The tracker marker size will be this fraction of the camera's world size.\nA good world size minimizes the need to adjust this."
            },
            "relLidarSize": {
                "name": "Relative Lidar Size",
                "widgetType": "doubleSpin",
                "range": [0.0001, 10],
                "precision": 4,
                "step": .0001,
                "factoryDefault": 0.0002,
                "toolTip": "The lidar point size will be this fraction of the camera's world size.\nA good world size minimizes the need to adjust this."
            },
            "relFarClip": {
                "name": "Far Clipping Plane Multiple",
                "widgetType": "spin",
                "range": [1, 50],
                "step": 1,
                "factoryDefault": 10,
                "toolTip": "Far clipping plane distance, as a multiple of the world size."
            },
            "miscOpacity": {
                "name": "Gnomon/Tracker Opacity",
                "widgetType": "doubleSpin",
                "range": [0, 1],
                "precision": 2,
                "step": .01,
                "factoryDefault": 1,
                "toolTip": "Opacity setting for object gnomons and tracker chisels.\nA reduced opacity may help you better assess placement against the background image."
            },
            "doFrustrum": {
                "name": "Camera Frustrums",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Show each camera's viewing frustrum as lines."
            },
            "doGnomon": {
                "name": "Object Gnomons",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Include a visible 'gnomon' mesh for each moving object, in addition to the transform."
            },
            "doChisel": {
                "name": "Tracker Chisels",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Include a visible 'chisel' mesh for each tracker, in addition to the transform."
            },
            "geoPrimitives": {
                "name": "Use USD Primitives",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "If set, use USD primitive types for sphere, cylinder, cone, and box representations.\nOnly for simple cases, don't use if primitives have textures or advanced SynthEyes settings."
            },
            "silentMovies": {
                "name": "Silence Movie Warnings",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "USDA can only output image sequences for shots, and warns if movie imagery is present. This checkbox silences that warning."
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
        "format": ".py",
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
                "toolTip": "The first frame of the selected part of the shot will\nbe put at this frame number in the export.\nNot used when Match frames is selected unless\nthe shot is a movie."
            },
            "version": {
                "name": "Blender Version",
                "widgetType": "combo",
                "comboItems": [("4.0+", "4.0"), ("3.2+", "3.02"), ("2.80+", "2.80")],
                "factoryDefault": "4.0",
                "toolTip": "Select your Blender version, or the most-recent version earlier than yours."
            },
            "hexData": {
                "name": "Hex Mesh Workaround",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Use hexadecimal binary data as a workaround for broken python in blender 3.2x.\nFiles are 2x larger and somewhat slower to write,\nbut blender can execute them substantially faster."
            },
            "mode": {
                "name": "Scene Mode",
                "widgetType": "radioGroup",
                "options": [
                    ("Create New Scene", "create"),
                    ("Update Existing Scene", "update"),
                ],
                "factoryDefault": "create",
                "toolTip": "Either Create New Empty Blender Scene, or Minimally update a .blend file\nfrom an earlier export of this scene: only camera and object path data and tracker positions."
            },
            "buildRigs": {
                "name": "Create Armatures",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "2.80+! When set, an armature will be built for Geometric Hierarchy Tracking rigs.\nOtherwise, deformed meshes will be exported by a vertex cache."
            },
            "updateMeshCaches": {
                "name": "Update Mesh Caches",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Relevant when updating scenes with 'Update existing scene' exports,\nexporting rigs as vertex caches,\nie Create armatures is OFF. When this checkbox is ON,\ndeformed caches will have a new vertex cache written for each update.\nWhen it is OFF, no updated cache is written (to save time), and the old animation will persist.\nThe mesh must not have been edited, and any anamorphic distance must not have changed!"
            },
            "doQuads": {
                "name": "Use Quads",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set, meshes will be output using quads, if possible.\nOtherwise, meshes will be output using only triangles."
            },
            "fixAD": {
                "name": "Fix Anamorphic Distance",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When on and an anamorphic distance is present, each mesh is exported with a vertex cache,\nand tracker positions are compensated, so that the shot lines up\n(as seen only from *this* current active camera) in non-savvy downstream applications.\nWon't fix meshes with rigs or pre-existing vertex caches."
            },
            "uscl": {
                "name": "Rescale Scene",
                "widgetType": "doubleSpin",
                "range": [0.01, 100.00],
                "precision": 2,
                "step": 0.01,
                "factoryDefault": 0.33,
                "toolTip": "Scaling factor applied to SynthEyes values."
            },
            "tksz": {
                "name": "Tracker Size",
                "widgetType": "spin",
                "range": [1, 10],
                "step": 1,
                "factoryDefault": 1,
                "toolTip": "Size of the tracker empty object, before the scaling factor"
            },
            "useBackground": {
                "name": "Use Camera Background",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "The camera background is available only in Blender 2.80 or later.\nIf unchecked, or distortion is present, a projection screen is generated."
            },
            "uvScreenMode": {
                "name": "UV Screen Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("If UV present", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "With a UVmap, a projection screen using texture coordinates will work better than a vertex-positioning screen, \nAlthough animated distortion can't be handled. This controls when the alternate version is used."
            },
            "hgrid": {
                "name": "Horizontal Grids",
                "widgetType": "spin",
                "range": [1, 256],
                "step": 1,
                "factoryDefault": 64,
                "toolTip": "Number of horizontal grids for a projection screen. The vertical count is determined from the aspect ratio."
            },
            "scnDis": {
                "name": "Screen Relative Distance",
                "widgetType": "spin",
                "range": [0, 20],
                "step": 1,
                "factoryDefault": 3,
                "toolTip": "Distance from camera to projection screen for shot, as a multiple of the solver panel's world size."
            },
            "clip": {
                "name": "Clipping Relative Distance",
                "widgetType": "spin",
                "range": [1, 50],
                "step": 1,
                "factoryDefault": 4,
                "toolTip": "Clipping distance in blender, as a multiple of the solver panel's world size."
            },
            "cube": {
                "name": "Delete Pre-Existing Meshes",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "If set, the blender scene's default cube will be deleted."
            },
            "from_prefix": {
                "name": "Remove Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "The remove-prefix is removed from file names in the exported file,\nand replaced with the add-prefix, to make it easier to output files for a different machine."
            },
            "to_prefix": {
                "name": "Add Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "The remove-prefix is removed from file names in the exported file,\nand replaced with the add-prefix, to make it easier to output files for a different machine."
            },
        }
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

