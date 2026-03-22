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
        -  Object json lookup and identify the screenshot in the UI (use region using recorder co-ordinates)    --> [Status: Pending]

    - Perform operations                                                --> [Status: Done]
        - Click on  --> Click on the Item with name (Object)
        - Type      --> Text
        - Hotkey Ctrl + X   --> hotkey combination simulation like Ctrl + X
        - Specail Keys e.g. TAB, ESC etc                                --> [Status: Not Done]
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
2. Unable to find the object name eventhough it is available? self.finder.find_object(object_name)


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
Image based clicking with auto retry
smart UI detection
resolution independence


=========================================================================================================
Project Context - v1.2
=========================================================================================================
Below is a **clean, compact context summary** you can paste into a **new chat** so we can continue improvements without losing context or wasting tokens.

I optimized it to **keep all technical state** but **minimize tokens**.

---

# Project Context Summary (Continue Development)

### Project

Python **No-Code Desktop UI Automation Tool**

Goal:
Allow **non-technical users** to **record, edit, and play automation workflows** similar to simple RPA tools.

Tech Stack:

* Python
* PySide6 (UI)
* pynput (record mouse/keyboard)
* pyautogui (playback automation)

---

# Current Application Architecture

```
automation_tool
│
├── recorder
│   └── action_recorder.py
│
├── player
│   └── action_player.py
│
├── ui
│   └── main_window.py
│
└── main.py
```

---

# Recorder Features Implemented

`ActionRecorder`

Captures:

Mouse

```
Mouse Move X,Y
Mouse Left Click
Mouse Right Click
Mouse Double Click
```

Keyboard

```
Type text H
Hotkey Ctrl + C
Hotkey Ctrl + Shift + S
Key Enter
Key Backspace
```

Timing

```
Wait 1.2
```

Other logic implemented:

* Mouse move noise reduction
* Double click detection
* Dynamic hotkey detection
* Fix for Ctrl character mapping (Ctrl+Z issue)
* Modifier key tracking
* Recording stop hotkey

Stop Recording

```
Ctrl + Alt + S
```

---

# Player Features Implemented

`ActionPlayer`

Executes commands:

```
Mouse Move
Mouse Left Click
Mouse Right Click
Mouse Double Click
Type text
Hotkey
Key Enter
Wait
```

Additional features implemented:

Playback speed control

```
self.speed
```

Stop automation hotkey

```
Ctrl + Alt + Q
```

Fail-safe stop

```
Move mouse to (0,0)
```

Resolution-independent click support

Supports both:

```
Mouse Move 500,300
Mouse Move 0.52,0.41
```

---

# UI Features Implemented

`MainWindow` using PySide6

UI contains:

```
Record
Play
Load
Save
```

Workflow steps displayed in:

```
QListWidget
```

Capabilities:

* Record workflow
* Load workflow
* Save workflow
* Run workflow

Important behavior implemented:

Automation UI hides during:

```
Recording
Playback
```

and reappears when finished.

Execution runs in **background threads**.

---

# Current Workflow Script Format

Example automation file:

```
Mouse Move 520,410
Mouse Left Click
Wait 1
Type text Hello
Hotkey Ctrl + C
Hotkey Ctrl + V
Key Enter
```

---

# Known Improvements Planned (Next Phase)

Recorder Improvements

1. Merge typed characters

Instead of

```
Type text H
Type text e
Type text l
```

store

```
Type text Hello
```

2. Merge wait steps

```
Wait 3.96
Wait 0.29
```

→

```
Wait 4.25
```

3. Prevent duplicate mouse clicks

---

UI Improvements

* Add Step
* Delete Step
* Move Step Up/Down
* Edit Step
* Drag-drop steps
* Recording indicator

---

Architecture Improvement Planned

Move from **text-based step storage** to **structured actions**

Example:

Instead of:

```
Mouse Move 500,300
```

Use:

```
Action(type="mouse_move", x=500, y=300)
```

Benefits:

* safer editing
* easier validation
* easier UI building
* extensible automation engine

---

# Next Feature to Implement

Improve **Workflow Editor UI**

Add:

```
Add Step
Delete Step
Move Step Up
Move Step Down
Edit Step
```

Then upgrade automation engine to **structured step objects**.

---

# Instruction for Next Chat

Continue improving the **Python UI Automation Tool**.

Focus on:

```
Workflow editor improvements
Step editing UI
Structured action model
Cleaner recorder output
```

Maintain:

* simple code
* modular architecture
* independently testable classes
* beginner-friendly comments.

---

When you start the new chat, just paste the summary and say:

**“Continue improving the automation tool from this state.”**

Then we can continue building the **next major improvements efficiently.**
