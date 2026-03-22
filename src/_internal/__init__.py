"""Smart Automation Tool - Production Source Package"""

__version__ = "1.0.0"
__author__ = "Smart Automation Team"
__description__ = "Enterprise-grade UI automation tool with no-code interface"

from _internal.main import SimpleAutomation
from _internal.ui import SnippingOverlayWindow
from _internal.ui import SnipPopup


__all__ = [
    'SimpleAutomation',
    'SnippingOverlayWindow',
    'SnipPopup'
]
