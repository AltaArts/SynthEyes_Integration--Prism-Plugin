## SynthEyes Format Naming
SynthFormatNames: dict = {
    "USD  (.usda)": {
            "synthName": "USD ASCII Scene",
            "format": ".usda"
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
