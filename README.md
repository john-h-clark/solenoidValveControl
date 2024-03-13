# solenoidValveControl
Code to control a solenoid valve 
## Overview
This script is used to control one solenoid valve for the purpose of injecting 
CO<sub>2<\sub> into the C200 testing space in a remote fashion

## Usage
0. Prior to running the script: 
- ensure that the directory for the log is set correctly
    - If this isnt performed, have no fear, the script will still run and the log 
    will still be saved, it will just be saved in the same directory as the 
    scripts, this is likely not ideal for you as a user but you will still have 
    access to all of the data
- If running from a new computer:
    - Install Python (works on Python 3.11, but any version of Python 3 will work). 
        - https://www.python.org/downloads/release/python-3110/
    - Install LabJack for Python packages
        - From: https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Finstaller-downloads%2Fu12-software-installer-u12%2F
        - Download: LabVIEW 7.1 Runtime Engine installer
            - No need to run “installers silently.” The installer will do its thing.
        - Download : LabJack-U12-Installer-2016-09-14.
            - From https://labjack.com/pages/support?doc=%2Fsoftware-driver%2Fexample-codewrappers%2Flabjackpython-for-ud-exodriver-u12-windows-mac-linux%2F
            - Download LabJackPython-2.1.0.zip. Unzip and put u12.py in folder with working .py file

1. Run the script, a GUI will be created On the left is the valve status and on 
the right are the valve control buttons, click the "Open CO<sub>2<\sub>" button 
to open the solenoid valve, this will automatically update the log in the middle
2. Wait 20 - 30 seconds to ensure that sufficient CO<sub>2<\sub> is injected into
the experimental space
3. Click the "Close CO<sub>2<\sub>" button on the right hand side of the log, 
the log will automatically update to show the status of the solenoid valve
4. Leave the script running so an accurate log of the valve status is obtained
throughout the duration of the CO<sub>2<\sub> decay.

## Authors
- Written by KJM
- Modifications after 20240426 Made by:
    - [John Clark](https://github.com/jclark6)
    - Lauren Garafalo 