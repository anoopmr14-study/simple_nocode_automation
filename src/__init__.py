"""Smart Automation Tool - Production Source Package"""

__version__ = "1.0.0"
__author__ = "Smart Automation Team"
__description__ = "Enterprise-grade UI automation tool with no-code interface"

from src.main import SimpleAutomation
from src.ui import SnippingOverlayWindow
from src.ui import SnipPopup

__all__ = [
    'SimpleAutomation',
    'SnippingOverlayWindow',
    'SnipPopup'
]
