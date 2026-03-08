How to Run
============
.\.smartvenv2\Scripts\activate
python .\auto_ui.py

type the commands
    e.g. 
        Click on File
        Click on Open
        type .gitignore
        Click on Open  (Confused Two Open)


Requirements and Status
=======================
1. User will be able to  add commands in Text box.
2. Upon click on Play button, system should 
    - identify the controls with name and perform operations
        - Click on  --> Click on the Item with name
        - Type      --> Text
        - Hotkey    --> hotkey combination
    - Mouse operation simulation for commands like 
        - Mouse Move X,Y        --> move the mouse to specified location
        - Mouse Right Click     --> Mouse right click
        - Mouse Left Clcik      --> Mouse left click
        - Mouse Double Click    --> 

3. Upon 
2. 

Simplified UI Automation application
1. It should record and replay and store the mouse and keyboard actions in 



Advantages of this application
=================================
✔ No complex parsing
✔ No AI
✔ No object detection
✔ Just OCR text matching
✔ Single screenshot per click
✔ Minimal threading

Possible Improvements
======================
Highlight detected text before clicking
Continuous OCR refresh
Add "Wait until visible"
Add confidence threshold slider
Add command validation
Package using PyInstaller

Possible Limitations
======================
OCR accuracy depends on screen clarity
Works best with clear UI text
Not good for icons
Multi-monitor may need adjustment