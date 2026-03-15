Simple Automation Tool which will allow user to type and execute the workflow or record and reply the workflow


How to Run
============
1. Run .\.smartvenv2\Scripts\activate
2. Run python .\auto_ui.py
3. Type the commands in UI
    e.g. 
        Click on File
        Click on Open
        type .gitignore
        Click on Open  (Current version confused if multiple Open text in UI and select the first Open)
4. Press Play


Requirements
=======================
1. User will be able to  add commands in Text box.
2. Upon click on "Play" button, system should 
    - Hide the AUtomation UI
    - identify the controls with name and  
        - Control Name from Text in Screen (OCR)                        --> [Status: Working except for Control with multiple word] OR
        -  Object json lookup and identify the screenshot in the UI    --> [Status: Pending]

    - Perform operations                                                --> [Status: Done]
        - Click on  --> Click on the Item with name
        - Type      --> Text
        - Hotkey Ctrl + X   --> hotkey combination simulation like Ctrl + X
    - Mouse operation simulation for commands like                       --> [Status: Done]
        - Mouse Move X,Y        --> move the mouse to specified location
        - Mouse Right Click     --> Mouse right click
        - Mouse Left Clcik      --> Mouse left click
        - Mouse Double Click    --> MOuse double click
    - Playback Speed Control                                            --> [Status: Done]
    - Screen Resolution Scaling
    - Stop Automation Hotkey (Ctrl + Alt + Q)                           --> [Status: Done]
    - Display the Automation UI on stop
 
3. Upon Click on "Insert Screenshot Object" button                      --> [Status: Done]
    - Hide the Automation Tool UI (all UIs)
    - Show a Transparent overlay UI with Recntagle Snipping Area which user can resize and Press Enter Key
    - Close the Overlay and Popup UI with Screenshot of the snipped Area, Co-ordinates and name text box. user can type the name of the object and press save 
    - These details will be stored in file system (image under result/objects and result/objectmapping.json having imagepath, co-oridnates and name)

3. Upon click on "Record" button, system should                         --> [Status: Pending]
    - Hide the Automation Tool UI (all UIs)
    
    - Record the Mouse and Key board operations (eventhough UI hide) Commands with required parameters and store as temp file under results/recordings/                                --> [Status: Partial, file location to be corrected]
    - On Specific HotKey Combination Ctrl+Atl+V --> It should show overlay and allow to select the Rectangle and take the screenshot and store the co-ordinate as validation command --> Reuse Snipping overlay
    - On Ctrl+ Alt+ S --> Stop the Recording and show the UI with option to save the file and Replay Command UI should fill with these command and allow to play.                   --> [Status: Partial]
    - Visual Recorder Indicator

4. Step Management
    Add Step
    Edit step
    Delete Step
    Move Step Up
    Move Step Down
Issue seen
=============
1. Snipping Area and screenshot taken has small difference 


Possible Limitations
======================
1. OCR accuracy depends on screen clarity
2. Works best with clear UI text
3. Not good for icons                                   - Need Solution
4. Multi-monitor may need adjustment                    - Need Solution
5. Same Text in UI confusion scneario                   - Need Solution
6. Multiple word text treated as seperate Scenario      - Need Solution


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

