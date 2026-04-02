# **Rendering**

The SynthEyes Prism integration has three rendering states: RenderShot, STMap, and Playblast.  Each state has its purpose, and uses specific SynthEyes functions.

<br/>

##  Common Render Options

- **Camera:**  Selects the Camera/Shot to Render.  For multiple cameras in a scene, use a separate state for each.

- **Scaling:** If the override is disabled, the rendered image size will be the same as the SynthEyes scene.

- **Format:**  The desired image output format. 

<br/>

## **RenderShot**

![RenderShot Overview](DocsImages/RenderShot_Overview.png)

The RenderShot state uses the SynthEyes 'Save Sequence' function to output a video file or image sequence from a Shot's Camera.


### **Options**
- **Include RGB:**  Renders the visible color images (RGB).  Normally enabled for almost all purposes.  May be disabled for Alpha-only render.
- **Include Alpha:**  Includes an Alpha channel in the render.  Only available in supported output formats.
- **Include Mesh:**  Includes the scene's 3D meshes in the render.
- **Include Burn-in:**  Includes burn-in data in the render. (NOTE: not functioning as expected - see **Dev Notes below).




<br/>

## **STMap**

![STMap Overview](DocsImages/STMap_Overview.png)


### **Options**
- **Single / Sequence:**  Selects either single-image Distortion maps, or an image sequence. 
- **Map Types:**  Includes an Alpha channel in the render.  Only available in supported output formats.


Dev Note:  This uses the SynthEyes

<br/>

## **Playblast**

![Playblast Overview](DocsImages/Playblast_Overview.png)

This state uses the SynthEyes 'Preview Movie' from the Perspective View.


### **Options**
- **Include Viewport Items:**
- **Include Grid:**
- **Include Burn-in:**  Includes burn-in data in the render. (NOTE: not functioning as expected - see **Dev Notes below).
- **Include RGB:**  Renders the visible color images (RGB).  Normally enabled for almost all purposes.  May be disabled for Alpha-only render.
- **Include Alpha:**  Includes an Alpha channel in the render.  Only available in supported output formats.
- **Include Depth:**  Includes the scene's 3D meshes in the render.


<br/>

___
jump to:

[**Interface**](Interface.md)

[**Adding Shots**](AddShots.md)

[**Importing 3D**](Importing_3d.md)

[**Scene Export**](Export_Scene.md)
