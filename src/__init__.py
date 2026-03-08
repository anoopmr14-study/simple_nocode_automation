"""Smart Automation Tool - Production Source Package"""

__version__ = "1.0.0"
__author__ = "Smart Automation Team"
__description__ = "Enterprise-grade UI automation tool with no-code interface"

from src.main import SimpleAutomation
from src.testapps import SnippingOverlayWindow
from src.testapps import SnipPopup

__all__ = [
    'SimpleAutomation',
    'SnippingOverlayWindow'
]
