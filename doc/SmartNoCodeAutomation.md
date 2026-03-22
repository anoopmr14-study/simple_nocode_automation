Smart No-Code Automation Tool

A Python-based No-Code Desktop UI Automation Tool that enables non-technical users to record, capture UI elements, build, and execute workflows using mouse, keyboard and visual object detection.


Key Points

* Simple User Interface and easy to build and execute workflows with No-Code
* Hybrid Step creation  - Tool UI buttons, Record keyboard and mouse operations, capture UI elements
* Smart Step Execution - Replay Mouse and keyboard actions, visual detection and action execution on UI elements
* Workflows, Objects and Report should be saved as JSON



Core Features

* Hybrid Step creation and store as workflow JSON

  * Manual Workflow Steps: create by performing different button operations in Tool UI (add, edit, duplicate, delete, reorder etc.)
  * Record Workflow Steps: Create by capturing mouse \& keyboard actions and stop using hotkey
  * Visual Object-Based Steps:  Create by capture UI elements via inbuilt snipping tool and store them for reuse in other workflows
  * Load Workflow steps: Load workflow steps from JSON and can modify or add new steps using any of the above step creation approaches
* Execute Workflow steps (click, wait, validate etc.) and generate report as JSON

  * Replay mouse and keyboard actions and stop using hotkey
  * Visual detection and execution of UI elements ( region-based image matching, retry, timeout, fallback)



Future Scope

* OCR-based validation (OCR sample logic tested, integration in to tool pending)
* Import/export workflows
* UI Enhancements
* Cross-platform support (Not tested in Linux)

