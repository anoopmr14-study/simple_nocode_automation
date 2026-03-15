"""Smart Automation Tool - Production Source Package"""

__version__ = "1.0.0"
__author__ = "Smart Automation Team"
__description__ = "Enterprise-grade UI automation tool with no-code interface"

from internal.main import SimpleAutomation
from internal.ui import SnippingOverlayWindow
from internal.ui import SnipPopup


__all__ = [
    'SimpleAutomation',
    'SnippingOverlayWindow',
    'SnipPopup'
]
