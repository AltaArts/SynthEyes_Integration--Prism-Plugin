# **Installation**

<br/>

Copy the directory named "SynthEyes" to a directory of your choice, or a Prism2 plugin directory.

It is suggested to have the SynthEyes plugin with the other DCC plugins in: *{drive}\ProgramData\Prism2\plugins*

Prism's default plugin directories are: *{installation path}\Plugins\Apps* and *{installation Path}\Plugins\Custom*.

You can add the additional plugin search paths in Prism2 settings.  Go to Settings->Plugins and click the gear icon.  This opens a dialogue and you may add additional search paths at the bottom.

Once added, select the "Add existing plugin" (plus icon) and navigate to where you saved the Fusion folder.

![Adding Plugin](DocsImages/Adding_Plugin.png)

<br/>

![Plugin Folder](DocsImages/Plugin_Folder.png)


Afterwards, you can select the Plugin autoload as desired:

![Autoload](DocsImages/Autoload.png)

To add the integration, go to the "DCC Apps" -> "SynthEyes" tab.  Then click the "add" button and navigate to the folder containing SynthEyes's executable (SynthEyes64.exe).

![Add DCC apps](DocsImages/Add_DCC_Apps.png)

<br/>

## **Python**


In order to use the plugin it is required to have Python 3.11+ installed on the computer https://www.python.org/downloads/release/python-3139/.  The Python executable must be availble to SynthEyes

To check if Fusion can find the Python installation you can open the Console and click the “Py3” button at the top. If you can enter print("test") and execute it without error, Python is installed correctly.

___
jump to:

[**Interface**](Interface.md)

[**Rendering**](Rendering.md)

[**Importing Images**](Importing_2d.md)

[**Importing 3D**](Importing_3d.md)
