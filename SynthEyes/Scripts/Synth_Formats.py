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
        "format": ".fbx",
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
            "which": {
                "name": "Export Which Cameras",
                "widgetType": "combo",
                "comboItems": [("Only Active", "0"), ("Set Framerate as Active", "1"), ("All", "2")],
                "factoryDefault": "1",
                "toolTip": "Selects which cameras to export, including the moving objects attached to those cameras.\nAll unparented meshes are always exported."
            },
            "format": {
                "name": "Output Format",
                "widgetType": "combo",
                "comboItems": [("Default (binary)", "Default (binary)"), ("FBX binary (*.fbx)", "FBX binary (*.fbx)"), ("FBX ascii (*.fbx)", "FBX ascii (*.fbx)"), ("FBX 6.0 binary (*.fbx)", "FBX 6.0 binary (*.fbx)"), ("FBX 6.0 Ascii (*.fbx)", "FBX 6.0 Ascii (*.fbx)")],
                "factoryDefault": "Default (binary)",
                "toolTip": "The binary version is usual: smaller and faster.\nFBX 6.0 is to export to older applications."
            },
            "fbxyear": {
                "name": "FBX Version",
                "widgetType": "combo",
                "comboItems": [("Current", ""), ("2020", "FBX202000"), ("2019", "FBX201900"), ("2018", "FBX201800"), ("2016", "FBX201600"), ("2014", "FBX201400"), ("2013", "FBX201300"), ("2012", "FBX201200"), ("2011", "FBX201100")],
                "factoryDefault": "",
                "toolTip": "You can use this control to output FBX files using older versions of the FBX specification,\nif you are using applications that accept only older files."
            },
            "units": {
                "name": "Interpret SynthEyes Units as",
                "widgetType": "combo",
                "comboItems": [("Use scene settings", "scene"), ("None", ""), ("Millimeters", "mm"), ("Centimeters", "cm"), ("Meters", "m"), ("Kilometers", "km"), ("Inches", "in"), ("Feet", "ft"), ("Yards", "yd"), ("Miles", "mi")],
                "factoryDefault": "scene",
                "toolTip": "This is a suggestion to downstream applications as to how they should interpret the values.\nThey might ignore this."
            },
            "scaling": {
                "name": "Additional Scaling",
                "widgetType": "doubleSpin",
                "range": [0.01, 100.00],
                "precision": 2,
                "step": 0.01,
                "factoryDefault": 1,
                "toolTip": "All SynthEyes coordinate values are multiplied by this value,\ntypically to change the apparent units for applications that ignore the units setting."
            },
            "fbxRotOrder": {
                "name": "Rotation Order",
                "widgetType": "combo",
                "comboItems": [("XYZ", "0"), ("ZXY", "1")],
                "factoryDefault": "1",
                "toolTip": "*** At present, the FBX SDK does not write the other choices to the file as expected! ***\nRotation order setting for exported cameras, lights, etc.\nXYZ is the FBX default but some packages might require something different (ZXY for Nuke?)"
            },
            "fixAD": {
                "name": "Fix Anamorphic Distance",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When on and an anamorphic distance is present,\neach mesh has a vertex cache, and tracker positions are compensated,\nso that the shot lines up (as seen only from *this* current active camera)\nin non-savvy downstream applications."
            },
            "exportTrackers": {
                "name": "Export Trackers",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Controls whether or not trackers are exported at all."
            },
            "marker": {
                "name": "Marker Type",
                "widgetType": "combo",
                "comboItems": [("Box", "Box"), ("Bone", "Bone"), ("Capsule", "Capsule"), ("Chisel", "Chisel"), ("Circle", "Circle"), ("Cube", "Cube"), ("Hard Cross", "Hard Cross"), ("Light Cross", "Light Cross"), ("None", "None"), ("Null", "Null"), ("Sphere", "Sphere"), ("Square", "Square"), ("Stick", "Stick")],
                "factoryDefault": "Chisel",
                "toolTip": "Chisels are real meshes that will work in downstream applications for sure.\nOthers are 'suggestions' that may or may not be supported by downstream applications."
            },
            "trksiz": {
                "name": "Relative Tracker Size",
                "widgetType": "doubleSpin",
                "range": [0.001, 10],
                "precision": 3,
                "step": 0.001,
                "factoryDefault": 0.002,
                "toolTip": "The tracker marker size will be this fraction of the camera's world size.\nA good world size minimizes the need to adjust this."
            },
            "relfar": {
                "name": "Relative Far Override",
                "widgetType": "spin",
                "range": [0, 100],
                "step": 1,
                "factoryDefault": 0,
                "toolTip": "If nonzero, multiplied by the world size to determine how far\nthe projection screen is placed from the camera."
            },
            "fov": {
                "name": "Specify View",
                "widgetType": "combo",
                "comboItems": [("Horizontal FOV", "Horizontal FOV"), ("Vertical FOV", "Vertical FOV"), ("Focal Length", "Focal Length")],
                "factoryDefault": "Horizontal FOV",
                "toolTip": "What kind of value is placed in the file.\nHorizontal is recommended.\nFocal Length is discouraged, because only rarely do you know\nan exact sensor (back plate) width."
            },
            "camhack": {
                "name":"Tweak Camera Aim",
                "widgetType": "combo",
                "comboItems": [("None", "0"), ("Left", "1"), ("Right", "2"), ("Backwards", "3")],
                "factoryDefault": "0",
                "toolTip": "Work around applications that mis-read the FBX camera data,\nby re-aiming the camera direction in the output file.\nUse only as needed.\nExample: Left for Houdini."
            },
            "doScreen": {
                "name": "Create Screen",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "If set, creates a projection screen attached to the camera\nto hold the shot imagery.\nThe screen will be deformed to match any computed distortion\nfrom the Lens panel."
            },
            "fixScreen": {
                "name": "Max/Maya Screen Bugfix",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Corrects for a bug in 3dsmax and maya affecting screen placement.\nFixed files will not work in Autodesk's golden FBX Review.\nAdjust as needed for other programs."
            },
            "usePreprocessor": {
                "name": "Based On",
                "widgetType": "combo",
                "comboItems": [("Solver distortion", "0"), ("Image Preprocessor (normal)", "1")],
                "factoryDefault": "1",
                "toolTip": "Where to look for lens distortion information.\nNormally, this should be the Image preprocessor,\nafter running the Lens Workflow script.\nThe solver's distortion can also be selected\nwhen overscan rendering is being used by downstream compositing and 3-D applications."
            },
            "uvScreenMode": {
                "name": "UV Screen Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("If UV present", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "With a UVmap, a projection screen using texture coordinates will work better\nthan a vertex-positioning screen, although animated distortion can't be handled.\nThis controls when the alternate version is used."
            },
            "lmode": {
                "name": "Screen's Lens Mode",
                "widgetType": "combo",
                "comboItems": [("None", "0"), ("Remove (normal)", "1"), ("Apply!", "2")],
                "factoryDefault": "1",
                "toolTip": "If you are tricky, you may be able to use the Apply! setting\nto redistort CG footage in your 3D package.\nBut probably not... so keep it at Remove."
            },
            "vgrid": {
                "name": "Vertical Grids",
                "widgetType": "spin",
                "range": [1, 256],
                "step": 1,
                "factoryDefault": 12,
                "toolTip": "Number of vertical grids in the projection screen.\nWith anything more than minimal distortion,\nincrease for more accurate distortion."
            },
            "useOriginals": {
                "name": "Use Original Numbering",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When checked, the exported mesh will use the original imported vertex,\nnormal, and texture indices, if that data is available.\nOverrides *no repeating vertices*.\nMakes files larger and more complex."
            },
            "makeVertUniq": {
                "name": "No Repeating Vertices",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Enabling this may eliminate seams when read into susceptible apps—Maya?\nMakes files larger and more complex."
            },
            "doQuad": {
                "name": "Use Quads if Possible",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set, meshes will be exported using a mixture of quads and triangles.\nTurn off if your downstream package has a problem with that."
            },
            "doAlphaTrans": {
                "name": "Alpha as Transparency",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When set, send mesh texture alpha channels also as a Transparency Factor,\nwhich may or may not be supported by applications reading the FBX."
            },
            "pcmode": {
                "name": "Deformed Mesh Format",
                "widgetType": "combo",
                "comboItems": [("None", "0"), ("3dsMax (PC2)", "1"), ("Maya (MCX)", "3"), ("Bones", "3")],
                "factoryDefault": "2",
                "toolTip": "Use bones or vertex cache format for animated GeoH deformations.\nSelect to match your desired application;\nother applications may require one or the other."
            },
            "flat": {
                "name": "Texture Lighting",
                "widgetType": "combo",
                "comboItems": [("Light All Textures", "0"), ("Set by Mesh", "1"), ("Don't Light Textures", "4"), ("Light Screens and Meshes", "2"), ("Light Screens, Some Meshes", "3"), ("Light Screens, Not Meshes", "6")],
                "factoryDefault": "1",
                "toolTip": "Light ALL meshes or not if needed,\ngenerally set instead per-mesh from the texture panel.\nChoices that light the screen are for testing."
            },
            "embed": {
                "name": "Embed Media",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When set, shot imagery and still textures are inside the filmbox file,\nmaking it more self-contained and easier to move around,\nthough also much larger."
            },
            "setPlanes": {
                "name": "Set Far/Near Clips",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set, the far and near clipping planes from SynthEyes are stored in the file\nfor consistency.\nWhen off, the reading software will do whatever it usually does."
            }
        }
    },
    "Alembic  (.abc)": {
        "synthName": "Alembic 1.5+",
        "format": ".abc",
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
            "which": {
                "name": "Export Which Shots",
                "widgetType": "combo",
                "comboItems": [("Only Active shot", "0"), ("Same Framerate as Active", "1"), ("Same Framerate and Range as Active", "2"), ("All Shots", "3")],
                "factoryDefault": "1",
                "toolTip": "Controls which shots are exported, when there are more than one in the same scene.\nThe active shot is the shot of the current Active Tracker Host."
            },
            "wantZup": {
                "name": "Output Axis Setting",
                "widgetType": "combo",
                "comboItems": [("Y Up (normal)", "0"), ("Z Up", "1")],
                "factoryDefault": "0",
                "toolTip": "Generates Alembic data with this coordinate placement,\nindependent of what it is in SynthEyes.\nY Up seems to be typical."
            },
            "wantUVFlip": {
                "name": "Image Orientation",
                "widgetType": "combo",
                "comboItems": [("Normal (Blender)", "0"), ("Rotate 180' (Nuke)", "1")],
                "factoryDefault": 0,
                "toolTip": "Rotate the image if needed to support particular hosts."
            },
            "normals": {
                "name": "Include Normals",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Include normals for meshes, if they are present."
            },
            "scaling": {
                "name": "Additional Scene Scaling",
                "widgetType": "doubleSpin",
                "range": [0.01, 100.00],
                "precision": 2,
                "step": 0.01,
                "factoryDefault": 1,
                "toolTip": "Multiplies all scene coordinates by this value,\nfor example for units conversion."
            },
            "fixAD": {
                "name": "Fix Anamorphic Distance",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When on and an anamorphic distance is present, each mesh has a vertex cache,\nand tracker positions are compensated, so that the shot lines up\n(as seen only from *this* current active camera)\nin non-savvy downstream applications."
            },
            "doQuad": {
                "name": "Use Quads if Possible",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set, meshes will be exported using a mixture of quads and triangles.\nTurn off if your downstream package has a problem with that."
            },
            "markers": {
                "name": "Create Tracker Chisels",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "These are upside-down pyramids for each tracker."
            },
            "trksiz": {
                "name": "Chisel Size Override",
                "widgetType": "doubleSpin",
                "range": [0, 10],
                "precision": 4,
                "step": 0.001,
                "factoryDefault": 0,
                "toolTip": "Makes chisels this particular size, if non-zero."
            },
            "doScreen": {
                "name": "Create Screen",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "You can apply the scene as a texture to this.\nAlembic does not permit this to be done automatically."
            },
            "usePreprocessor": {
                "name": "Based On",
                "widgetType": "combo",
                "comboItems": [("Solver distortion", "0"), ("Image Preprocessor (normal)", "1")],
                "factoryDefault": "1",
                "toolTip": "Where to look for lens distortion information.\nNormally, this should be the Image preprocessor,\nafter running the Lens Workflow script.\nThe solver's distortion can also be selected,\nthough this is not recommended."
            },
            "uvScreenMode": {
                "name": "UV Screen Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("If UV present", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "With a UVmap, a projection screen using texture coordinates\nwill work better than a vertex-positioning screen,\nalthough animated distortion can't be handled.\nThis controls when the alternate version is used."
            },
            "lmode": {
                "name": "Screen's Distortion Mode",
                "widgetType": "combo",
                "comboItems": [("None", "0"), ("Remove (normal)", "1"), ("Apply!", "2")],
                "factoryDefault": "1",
                "toolTip": "When set to Remove, pre-distorts the projection screen\nso that the imagery will have the distortion value\non the Lens panel removed from it."
            },
            "scnovr": {
                "name": "Screen Distance Override",
                "widgetType": "spin",
                "range": [0, 1000],
                "step": 1,
                "factoryDefault": 0,
                "toolTip": "Set a specific camera-to-screen distance,\nif this is non-zero."
            },
            "vgrid": {
                "name": "Vertical Screen Grids",
                "widgetType": "spin",
                "range": [1, 256],
                "step": 1,
                "factoryDefault": 12,
                "toolTip": "Vertical grids in the generated projection screen.\nHorizontal determined from image aspect."
            },
            "setPlanes": {
                "name": "Set Far/Near Clipping Planes",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When checked, puts near and far clipping distances\ninto the Alembic file, from their values in SynthEyes."
            }
        }
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
        "format": ".ma",
        "exportSettings": {
            "workarea": {
                "name": "Timeline Setup",
                "widgetType": "combo",
                "comboItems": [("Active part", "0"), ("Entire shot", "1"), ("Match frames", "2")],
                "factoryDefault": "2",
                "toolTip": "Controls which portion of the incoming shot is placed at the Starting frame#.\nMatch Frames makes the placement match the image sequence's frame numbers;\nequivalent to Entire shot for movies."
            },
            "userStart": {
                "name": "Starting Frame",
                "widgetType": "spin",
                "range": [0, 1000000],
                "step": 1,
                "factoryDefault": 1,
                "toolTip": "The first frame of the selected part of the shot will be put at this frame number.\nNot used when Match frames is selected."
            },
            "synunits": {
                "name": "Interpret SynthEyes Units As",
                "widgetType": "combo",
                "comboItems": [("Use scene settings", "scene"), ("None", ""), ("Millimeters", "mm"), ("Centimeters", "cm"), ("Meters", "m"), ("Kilometers", "km"), ("Inches", "in"), ("Feet", "ft"), ("Yards", "yd"), ("Miles", "mi")],
                "factoryDefault": "scene",
                "toolTip": "Interpret SynthEyes units as this; combined with the Maya units we obtain a relative scaling factor.\nKeeping this at cm matches maya's default setting.\nIf None, no scaling factor is applied."
            },
            "mayaunits": {
                "name": "Maya Working Units",
                "widgetType": "combo",
                "comboItems": [("None", ""), ("Millimeters", "mm"), ("Centimeters", "cm"), ("Meters", "m"), ("Kilometers", "km"), ("Inches", "in"), ("Feet", "ft"), ("Yards", "yd"), ("Miles", "mi")],
                "factoryDefault": "cm",
                "toolTip": "This will be the scene's Working Unit setting.\nMaya likes centimeters.\nBe careful, see Autodesk's 'Working in Maya in different scales.'"
            },
            "arnold": {
                "name": "Use Arnold Materials",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Use Arnold materials.\nLights are bright to avoid completely black first renders.\nManually select Arnold in Render Settings."
            },
            "arnoldRoll": {
                "name": "Arnold Rolling Shutter",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "For Arnold only, only if rolling shutter is present,\nset the shutter angles (from the Perspective View's Render Settings)\nand rolling shutter value."
            },
            "rotOrder": {
                "name": "Rotation Order",
                "widgetType": "combo",
                "comboItems": [("XYZ", "XYZ"), ("ZXY", "ZXY")],
                "factoryDefault": "ZXY",
                "toolTip": "Use this rotation order for objects created in Maya."
            },
            "doScreen": {
                "name": "Projection Screen",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("When Distorted", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "When to generate a projection screen to hold the shot imagery,\ndistorted as necessary to match the scene.\nIf a projection screen isn't generated, then an image plane is generated\nto hold the (undistorted!) shot imagery."
            },
            "usePreprocessor": {
                "name": "Based On",
                "widgetType": "combo",
                "comboItems": [("Solver distortion", "0"), ("Image Preprocessor (normal)", "1")],
                "factoryDefault": "1",
                "toolTip": "Where to look for lens distortion information.\nNormally, this should be the Image preprocessor,\nafter running the Lens Workflow script.\nThe solver's distortion can also be selected,\nthough this is not recommended."
            },
            "uvScreenMode": {
                "name": "UV Screen Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("If UV present", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "With a UVmap, a projection screen using texture coordinates will work better\nthan a vertex-positioning screen, although animated distortion can't be handled.\nThis controls when the alternate version is used."
            },
            "nomgrid": {
                "name": "Horizontal Grids",
                "widgetType": "spin",
                "range": [1, 256],
                "step": 1,
                "factoryDefault": 64,
                "toolTip": "Number of horizontal grids for a projection screen.\nThe vertical count is determined from the aspect ratio."
            },
            "relScreenDis": {
                "name": "Screen Relative Distance",
                "widgetType": "spin",
                "range": [0, 20],
                "step": 1,
                "factoryDefault": 3,
                "toolTip": "Distance from camera to projection screen for shot,\nas a multiple of the solver panel's world size."
            },
            "overscanride": {
                "name": "Overscan Override (%)",
                "widgetType": "spin",
                "range": [0, 1000],
                "step": 1,
                "factoryDefault": 0,
                "toolTip": "If non-zero and overscan rendering is needed for zero-pass workflow,\nalways use this overscan percentage rather than calculating a minimal value.\nExample: 20(%) multiplies resolution by 1.2.\nBe sure that multiplying that factor times horizontal and vertical resolution\nis an exact integer in both cases."
            },
            "roundingError": {
                "name": "Max Rounding Error",
                "widgetType": "doubleSpin",
                "range": [0, 1],
                "precision": 4,
                "step": 0.0001,
                "factoryDefault": 0.001,
                "toolTip": "The maximum permitted error, in pixels, as it selects padded image sizes\nto best maintain the original image aspect ratio.\nAny rounding/aspect error reduces the match's accuracy.\nIf the padded size is much too large, slowly increase this.\nValues over 0.5 suppress aspect-maintaining padding."
            },
            "renderTrackers": {
                "name": "Output Trackers as",
                "widgetType": "combo",
                "comboItems": [("Nothing", "0"), ("Locators", "1"), ("Chisel Geo", "2"), ("Both", "3")],
                "factoryDefault": "2",
                "toolTip": "Determines what sort of thing is created for exportable trackers."
            },
            "trackerSize": {
                "name": "Relative Tracker Size",
                "widgetType": "doubleSpin",
                "range": [0.0001, 10],
                "precision": 4,
                "step": 0.0001,
                "factoryDefault": 0.001,
                "toolTip": "Size of the tracker null, as a multiple of the world size."
            },
            "embedMeshes": {
                "name": "Embed Meshes",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("Non-Primitives", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "Which meshes are embedded in the .ma file,\nvs a maya primitive being used.\nIf no suitable primitive is available for a non-embedded mesh,\na box will be output."
            },
            "from_prefix": {
                "name": "Remove Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "To help when files are moved from machine to machine,\nthe Remove path prefix is removed from file names,\nthe Add path prefix is added.\nEx: M: to /Volumes/Imagery"
            },
            "to_prefix": {
                "name": "Add Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "To help when files are moved from machine to machine,\nthe Remove path prefix is removed from file names,\nthe Add path prefix is added.\nEx: Remove M:, add /Volumes/Imagery"
            },
            "far_clip": {
                "name": "Far Clipping Plane Multiplier",
                "widgetType": "spin",
                "range": [1, 100],
                "step": 1,
                "factoryDefault": 10,
                "toolTip": "Far clipping plane distance,\nas a multiple of the world size."
            },
            "enhance": {
                "name": "Enhanced Precision (bigger/more precise)",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When checked, more digits of precision are included\nfor the numbers being exported.\nThe file will be more accurate, but larger."
            }
        }
    },
    "BMD Fusion  (.comp)": {
        "synthName": "Fusion Composition",
        "format": ".comp",
        "exportSettings": {
            "workarea": {
                "name": "Timeline Setup",
                "widgetType": "combo",
                "comboItems": [("Active part", "0"), ("Entire shot", "1"), ("Match frames", "2")],
                "factoryDefault": "0",
                "toolTip": "Controls which portion of the incoming shot is placed at the Starting frame#.\nMatch Frames makes the placement match the image sequence's frame numbers;\nequivalent to Entire shot for movies."
            },
            "userStart": {
                "name": "Starting Frame",
                "widgetType": "spin",
                "range": [0, 1000000],
                "step": 1,
                "factoryDefault": 1,
                "toolTip": "The first frame of the selected part of the shot will be put at this frame number.\nNot used when Match frames is selected."
            },
            "bitdepth": {
                "name": "Project Bit Depth",
                "widgetType": "combo",
                "comboItems": [("8 bit int per Channel (32bit)", "0"), ("16 bit int per Channel (64bit)", "1"), ("16 bit float per Channel (64bit)", "2"), ("32 bit float per Channel (128bit)", "3")],
                "factoryDefault": "2",
                "toolTip": "Sets the Color Depth for the project, as seen in the Frame Format section\nof Fusion's preferences after opening this comp."
            },
            "inter8": {
                "name": "8-bit Interactive",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When set, interactive color depth is set to eight bits per channel (32 bit).\nWhen off, the main Project Color Depth is used."
            },
            "HiQ": {
                "name": "HiQ",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When checked, the HiQ button will be on by default,\nfor better-looking interactive previews."
            },
            "renderTk": {
                "name": "Renderable Trackers",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Make tracker point clouds or locators renderable."
            },
            "useCloud": {
                "name": "Use Point Cloud",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set, a PointCloud3D is generated for all trackers.\nWhen off, Locator3D's are generated for each tracker."
            },
            "maxTrackers": {
                "name": "Max Trackers",
                "widgetType": "spin",
                "range": [0, 100000],
                "step": 1,
                "factoryDefault": 20,
                "toolTip": "Limit the number of exported tracker layers to this.\nRandomly-selected unconstrained trackers are turned off\nto get under this limit if possible.\nSet the value to zero to disable."
            },
            "relTkSize": {
                "name": "Relative Tracker Size",
                "widgetType": "doubleSpin",
                "range": [0.0001, 10],
                "precision": 4,
                "step": 0.0001,
                "factoryDefault": 0.005,
                "toolTip": "Point Cloud point size as a fraction of the SynthEyes world size (Solver Panel)."
            },
            "wantPlanar": {
                "name": "Planar Trackers as Planes",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When on, planar trackers produce a 3D plane in Fusion,\ninstead of a regular tracker."
            },
            "useLensDistort": {
                "name": "Use LensDistort Node",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Use Fusion's LensDistort node instead of STMaps to handle lens distortion.\nSome lens types and parameters cannot be handled by LensDistort."
            },
            "allowSolverDistortion": {
                "name": "Allow Solver Distortion",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When checked, you can export cameras with distortion without running the Lens Distortion script.\nRequires using the LensDistort node, taking advantage of a domain area larger than the frame."
            },
            "overscanride": {
                "name": "Overscan Override (%)",
                "widgetType": "spin",
                "range": [0, 1000],
                "step": 1,
                "factoryDefault": 0,
                "toolTip": "Used by the maya overscan processing pipe.\nIf non-zero, use this overscan percentage rather than calculating a minimal value.\nExample: 20(%) multiplies resolution by 1.2.\nMust match overscan in Maya renders!"
            },
            "roundingError": {
                "name": "Rounding Error",
                "widgetType": "doubleSpin",
                "range": [0, 1],
                "precision": 4,
                "step": 0.0001,
                "factoryDefault": 0.001,
                "toolTip": "The maximum permitted error, in pixels, as it selects padded image sizes\nto best maintain the original image aspect ratio.\nAny rounding/aspect error reduces the match's accuracy.\nIf the padded size is much too large, slowly increase this.\nValues over 0.5 suppress aspect-maintaining padding."
            },
            "useTex": {
                "name": "Use Texture Node",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Use a texture node for faster distortion removal;\nturn OFF if you need an alpha channel—it will use a Custom Tool."
            },
            "mapext": {
                "name": "Map File Type",
                "widgetType": "combo",
                "comboItems": [("DPX Files", "dpx"), ("OpenEXR Files", "exr"), ("PNG Files", "png"), ("SGI Files", "sgi"), ("TIFF Files", "tif")],
                "factoryDefault": "exr",
                "toolTip": "Select the desired file type for image maps.\nSee Writing Image Distortion Maps in the manual."
            },
            "relScnDist": {
                "name": "Screen Distance",
                "widgetType": "spin",
                "range": [0, 20],
                "step": 1,
                "factoryDefault": 3,
                "toolTip": "Distance to the geometry holding the shot imagery,\nas a multiple of the scene's world size (Solver Panel)."
            },
            "useFuse": {
                "name": "Use Fusion Primitives",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When set, the builtin Fusion mesh generator will be used for simple cubes, spheres, etc.\nThat's quick but UV texture values are wrong.\nWhen off, and for all other meshes, an OBJ export and FBXNode is generated."
            },
            "useWireframe": {
                "name": "Wireframe Meshes",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Configure meshes to wireframe by default when on."
            },
            "fullFBX": {
                "name": "Full FBX Paths",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When set, a full absolute pathname will be used for any generated OBJ/FBX files,\nwhich is good for Deadline but not for portability.\nWhen off, a comp-relative filename is output."
            },
            "allSpot": {
                "name": "All Lights as Spotlights",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When set, all lights are forced to be spotlights,\nwhich are the only lights that can cast shadows in Fusion.\nIf needed, reposition lights that were originally directional,\nrather than reaiming them."
            },
            "doAmbient": {
                "name": "Ambient Light",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Set up an ambient light in fusion from the SynthEyes scene setting."
            },
            "use_flen": {
                "name": "Animate Focal Length",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When set, the focal length will be animated,\ninstead of the normal field of view.\nAs usual, it is rare to have exact plate information needed for the correct focal length."
            },
            "glRender": {
                "name": "Use OpenGL Renderer",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When on, the OpenGL renderer will be used.\nWhen off, the software renderer will be used.\nSee the Fusion manual for the differences."
            },
            "doViewer": {
                "name": "Include Viewer (360VR)",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Include 'viewer' for 360VR shots."
            },
            "from_prefix": {
                "name": "Remove Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "If a filename starts with this prefix, then it is replaced with the Add Path prefix,\nto make it easier to export from one system for another."
            },
            "to_prefix": {
                "name": "Add Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "If a filename starts with the Remove prefix, then it is replaced with this prefix,\nto make it easier to export from one system for another."
            },
            "clip": {
                "name": "Copy to Clipboard",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When checked, the exported nodes are put onto the clipboard,\nwhere you can paste it into Fusion, even in an existing comp,\nwhich can save time."
            },
            "incl_prefs": {
                "name": "Include Preferences",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set, includes some simple preferences information\nand a comment with the scene name and export timestamp."
            }
        }
    },
    "Nuke  (.nk)": {
        "synthName": "Nuke (Current)",
        "format": ".nk",
        "exportSettings": {
            "workarea": {
                "name": "Timeline Setup",
                "widgetType": "combo",
                "comboItems": [("Active part", "0"), ("Entire shot", "1"), ("Match frames", "2")],
                "factoryDefault": "2",
                "toolTip": "Controls which portion of the incoming shot is placed at the Starting frame#.\nMatch Frames makes the placement match the image sequence's frame numbers;\nequivalent to Entire shot for movies."
            },
            "userStart": {
                "name": "Starting Frame",
                "widgetType": "spin",
                "range": [0, 1000000],
                "step": 1,
                "factoryDefault": 1,
                "toolTip": "The first frame of the selected part of the shot will be put at this frame number.\nNot used when Match frames is selected."
            },
            "useNew": {
                "name": "Use New USD Nodes",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Use Nuke 14+'s 'new' USD-based 3D nodes (currently in beta)."
            },
            "rescale": {
                "name": "Rescale Scene",
                "widgetType": "spin",
                "range": [0, 100],
                "step": 1,
                "factoryDefault": 1,
                "toolTip": "An extra scaling factor applied to the 3-D coordinates just for this export,\ntypically to change meaningful units in SynthEyes to larger,\nmore compositing-friendly values in Nuke."
            },
            "renderTrackers": {
                "name": "Tracker Export Type",
                "widgetType": "combo",
                "comboItems": [("Nothing", "-1"), ("Axis Cloud", "0"), ("Renderable", "1"), ("Both", "2")],
                "factoryDefault": "2",
                "toolTip": "Determines what sort of thing is created for exportable trackers."
            },
            "maxTrackers": {
                "name": "Max Trackers",
                "widgetType": "spin",
                "range": [0, 100000],
                "step": 1,
                "factoryDefault": 20,
                "toolTip": "Limit the number of exported tracker layers to this.\nRandomly-selected unconstrained trackers are turned off\nto get under this limit if possible.\nSet the value to zero to disable."
            },
            "trkerSize": {
                "name": "Tracker Size",
                "widgetType": "doubleSpin",
                "range": [0.0001, 10],
                "precision": 4,
                "step": 0.0001,
                "factoryDefault": 0.5,
                "toolTip": "The tracker geometry is sized as this many thousandths\nof the world size (from the solver panel)."
            },
            "useLensDistort": {
                "name": "Use LensDistortion Node",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Use Nuke's LensDistortion node instead of STMaps to handle lens distortion.\nSome lens types and parameters cannot be handled by LensDistortion,\nif so, an STMap will be used."
            },
            "allowSolverDistortion": {
                "name": "Allow Solver Distortion",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When checked, you can export cameras with distortion without running the Lens Distortion script.\nRequires using the LensDistortion node, taking advantage of an overscan bounding box larger than the frame."
            },
            "overscanride": {
                "name": "Overscan Override (%)",
                "widgetType": "spin",
                "range": [0, 1000],
                "step": 1,
                "factoryDefault": 0,
                "toolTip": "Used by the maya overscan processing pipe.\nIf non-zero, use this overscan percentage rather than calculating a minimal value.\nExample: 20(%) multiplies resolution by 1.2.\nMust match overscan in Maya renders!"
            },
            "roundingError": {
                "name": "Rounding Error",
                "widgetType": "doubleSpin",
                "range": [0, 1],
                "precision": 4,
                "step": 0.0001,
                "factoryDefault": 0.001,
                "toolTip": "The maximum permitted error, in pixels, as it selects padded image sizes\nto best maintain the original image aspect ratio.\nAny rounding/aspect error reduces the match's accuracy.\nIf the padded size is much too large, slowly increase this.\nValues over 0.5 suppress aspect-maintaining padding."
            },
            "mapext": {
                "name": "Map File Type",
                "widgetType": "combo",
                "comboItems": [("DPX", "dpx"), ("EXR", "exr"), ("PNG", "png"), ("SGI", "sgi"), ("TIFF", "tif")],
                "factoryDefault": "exr",
                "toolTip": "File extension used for the distortion images.\nSee the Save/Export section of the Preferences for image format controls for each type."
            },
            "doScreen": {
                "name": "Projection Screen",
                "widgetType": "combo",
                "comboItems": [("None", "0"), ("Distorted Mesh", "1"), ("Card for Images", "2")],
                "factoryDefault": "1",
                "toolTip": "Generate a distorted mesh to hold the original images,\nor a flat card to hold undistorted images, or neither."
            },
            "uvScreenMode": {
                "name": "UV Screen Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("If UV present", "1"), ("Always", "2")],
                "factoryDefault": "1",
                "toolTip": "With a UVmap, a projection screen using texture coordinates will work better\nthan a vertex-positioning screen, although animated distortion can't be handled.\nThis controls when the alternate version is used. (New 3-D)"
            },
            "nomgrid": {
                "name": "Horizontal Grids",
                "widgetType": "spin",
                "range": [1, 256],
                "step": 1,
                "factoryDefault": 64,
                "toolTip": "Number of horizontal grids for a projection screen.\nThe vertical count is determined from the aspect ratio. (New 3-D)"
            },
            "relScreenDis": {
                "name": "Screen Distance",
                "widgetType": "spin",
                "range": [0, 20],
                "step": 1,
                "factoryDefault": 4,
                "toolTip": "The screen object is placed this multiple of the world size\n(from the solver panel) from the camera in Nuke."
            },
            "writeOBJs": {
                "name": "Write OBJ Mode",
                "widgetType": "combo",
                "comboItems": [("Never", "0"), ("Non-Primitives", "1"), ("All Non-Imported", "3"), ("All", "2")],
                "factoryDefault": "3",
                "toolTip": "Which meshes are written as OBJ files (USD in 'new' mode).\nExcept in either All mode, primitives are created via Nuke nodes.\nThe 'All' modes maintain the grid density set in SynthEyes."
            },
            "display_mode": {
                "name": "Display Mode",
                "widgetType": "combo",
                "comboItems": [("Default", "default"), ("Off", "off"), ("Wireframe", "wireframe"), ("Solid", "solid"), ("Solid-Wireframe", "solid+wireframe"), ("Textured", "textured"), ("Textured-Wireframe", "textured+wireframe")],
                "factoryDefault": "default",
                "toolTip": "Set the Nuke display mode for all exported meshes\nin Nuke's Classic 3D mode."
            },
            "render_mode": {
                "name": "Render Mode",
                "widgetType": "combo",
                "comboItems": [("Default", "default"), ("Off", "off"), ("Wireframe", "wireframe"), ("Solid", "solid"), ("Solid-Wireframe", "solid+wireframe"), ("Textured", "textured"), ("Textured-Wireframe", "textured+wireframe")],
                "factoryDefault": "default",
                "toolTip": "Set the Nuke render mode for all exported meshes\nin Nuke's Classic 3D mode."
            },
            "sclx": {
                "name": "Bake Scaling into Mesh",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "When set and an OBJ is written, scaling in SynthEyes is folded into the mesh vertices.\nWhen off, the Nuke node has the scaling.\nScaling is always burned into USDA files written for new Nuke 3D nodes."
            },
            "doAmbient": {
                "name": "Ambient Light",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Set the ambient lighting in the Scanline renderer\nfrom the SynthEyes scene setting."
            },
            "from_prefix": {
                "name": "Remove Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "To help when files are moved from machine to machine,\nthe Remove path prefix is removed from file names,\nthe Add path prefix is added.\nEx: M: to /Volumes/Imagery"
            },
            "to_prefix": {
                "name": "Add Path Prefix",
                "widgetType": "text",
                "factoryDefault": "",
                "toolTip": "To help when files are moved from machine to machine,\nthe Remove path prefix is removed from file names,\nthe Add path prefix is added.\nEx: Remove M:, add /Volumes/Imagery"
            },
            "toClip": {
                "name": "Copy to Clipboard",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "When checked, the exported nodes are put onto the clipboard,\nwhere you can paste it into Nuke, even in an existing comp,\nwhich can save time."
            },
            "sticky": {
                "name": "Create Sticky Note",
                "widgetType": "checkbox",
                "factoryDefault": 1,
                "toolTip": "Create a Nuke sticky note with some shot information."
            },
            "msg": {
                "name": "Print Import Message",
                "widgetType": "checkbox",
                "factoryDefault": 0,
                "toolTip": "Print a message in Nuke once the import completes,\nwith some file information."
            }
        }
    },
}



