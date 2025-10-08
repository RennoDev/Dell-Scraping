"""
Módulo de gerenciamento de browser.
Sistema completo para automação web com Playwright.
"""

from .browser_manager import BrowserManager, browser_manager
from .pace_manager import (
    OperationType,
    PaceLevel,
    PaceManager,
    TemporaryPace,
    configure_pace,
    pace_manager,
    wait_click,
    wait_extraction,
    wait_fill,
    wait_navigation,
    wait_network,
    wait_retry,
    wait_scroll,
)
from .utils import (
    ElementNotFoundError,
    PageWaitTimeout,
    extract_attribute,
    extract_text,
    get_page_info,
    safe_click,
    safe_fill,
    safe_goto,
    scroll_to_bottom,
    take_screenshot,
    wait_for_element,
    wait_for_network_idle,
)

__all__ = [
    # Browser Management
    "BrowserManager",
    "browser_manager",
    # Pace Management
    "PaceLevel",
    "OperationType",
    "PaceManager",
    "pace_manager",
    "configure_pace",
    "TemporaryPace",
    # Pace Functions
    "wait_click",
    "wait_extraction",
    "wait_fill",
    "wait_navigation",
    "wait_retry",
    "wait_scroll",
    "wait_network",
    # Browser Utils
    "ElementNotFoundError",
    "PageWaitTimeout",
    "extract_attribute",
    "extract_text",
    "get_page_info",
    "safe_click",
    "safe_fill",
    "safe_goto",
    "scroll_to_bottom",
    "take_screenshot",
    "wait_for_element",
    "wait_for_network_idle",
]
