"""Smart Automation Tool - Production Source Package"""

__version__ = "1.0.0"
__author__ = "Smart Automation Team"
__description__ = "Enterprise-grade UI automation tool with no-code interface"

from src.ui import MainWindow
from src.recorder import ActionRecorder
from src.player import ActionPlayer
from src.snipping import SnippingOverlayWindow, SnipPopup
from src.object_repo import ObjectRepositoryManager
from src.core import WorkflowManager
from src.core import Action


__all__ = [
    'MainWindow',
    'ActionRecorder',
    'ActionPlayer',
    'SnippingOverlayWindow',
    'SnipPopup', 
    'ObjectRepositoryManager',
    'WorkflowManager',
    'Action'
]
