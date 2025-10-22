"""Test GUI bridge module for integration pattern verification.

This module demonstrates all three integration patterns:
1. Module imports (gui_bridge imports Python modules)
2. Object attribute/method access with @ml_class decoration
3. Constant export (both class attributes and methods)
"""

from mlpy.stdlib.decorators import ml_module, ml_function, ml_class


# =============================================================================
# Wrapper Classes for GUI Widgets
# =============================================================================

@ml_class(description="Simple GUI window wrapper")
class TkWindow:
    """Wrapper for a tkinter window (demonstrates object wrapping pattern)."""

    def __init__(self, title: str = "Window"):
        """Create window with title."""
        self.title = title
        self.widgets = []
        self.is_shown = False

    @ml_function(description="Set window title")
    def setTitle(self, title: str) -> None:
        """Set window title."""
        self.title = title

    @ml_function(description="Get window title")
    def getTitle(self) -> str:
        """Get window title."""
        return self.title

    @ml_function(description="Add widget to window")
    def addWidget(self, widget) -> None:
        """Add widget to window (demonstrates accepting wrapper objects)."""
        self.widgets.append(widget)

    @ml_function(description="Show window")
    def show(self) -> None:
        """Show window (simulated)."""
        self.is_shown = True
        print(f"[GUI] Window '{self.title}' shown with {len(self.widgets)} widgets")

    @ml_function(description="Get widget count")
    def getWidgetCount(self) -> int:
        """Get number of widgets."""
        return len(self.widgets)


@ml_class(description="Simple GUI button wrapper")
class TkButton:
    """Wrapper for a tkinter button (demonstrates callback pattern)."""

    def __init__(self, text: str = "Button"):
        """Create button with text."""
        self.text = text
        self.callback = None
        self.click_count = 0

    @ml_function(description="Set button text")
    def setText(self, text: str) -> None:
        """Set button text."""
        self.text = text

    @ml_function(description="Get button text")
    def getText(self) -> str:
        """Get button text."""
        return self.text

    @ml_function(description="Set click callback")
    def onClick(self, callback) -> None:
        """Set click callback (ML function passed directly)."""
        self.callback = callback

    @ml_function(description="Simulate button click")
    def click(self) -> None:
        """Simulate button click."""
        self.click_count += 1
        print(f"[GUI] Button '{self.text}' clicked ({self.click_count} times)")
        if self.callback is not None:
            # Call ML callback directly - transpiled ML functions are Python callables!
            self.callback()

    @ml_function(description="Get click count")
    def getClickCount(self) -> int:
        """Get number of clicks."""
        return self.click_count


# =============================================================================
# Main GUI Bridge Module
# =============================================================================

@ml_module(
    name="gui",
    description="Minimal GUI bridge for testing integration patterns",
    capabilities=["gui.create", "gui.window"],
    version="1.0.0"
)
class GuiBridge:
    """Minimal GUI bridge demonstrating all three integration patterns."""

    # Pattern 3a: Constants as class attributes (direct access)
    VERSION = "1.0.0"
    MAX_WIDTH = 800
    MAX_HEIGHT = 600

    # Pattern 3a: String constants (tkinter pattern)
    ANCHOR_CENTER = "center"
    ANCHOR_LEFT = "left"
    ANCHOR_RIGHT = "right"

    @ml_function(description="Create new window", capabilities=["gui.create"])
    def createWindow(self, title: str = "Window") -> TkWindow:
        """Create new window (demonstrates returning wrapped object)."""
        print(f"[GUI] Creating window: {title}")
        return TkWindow(title)

    @ml_function(description="Create new button", capabilities=["gui.create"])
    def createButton(self, text: str = "Button") -> TkButton:
        """Create new button (demonstrates returning wrapped object)."""
        print(f"[GUI] Creating button: {text}")
        return TkButton(text)

    # Pattern 3b: Constants as methods (callable pattern)
    @ml_function(description="Get default window width")
    def DEFAULT_WIDTH(self) -> int:
        """Get default window width."""
        return 640

    @ml_function(description="Get default window height")
    def DEFAULT_HEIGHT(self) -> int:
        """Get default window height."""
        return 480

    @ml_function(description="Get version string")
    def version(self) -> str:
        """Get GUI bridge version."""
        return self.VERSION


# Create global instance for ML import
gui = GuiBridge()


# Export public API
__all__ = [
    "GuiBridge",
    "TkWindow",
    "TkButton",
    "gui",
]
