// Test GUI bridge integration patterns
import gui;

// Test Pattern 1: Module imports (gui_bridge would import tkinter internally)
print("Testing GUI bridge with nested imports...");

// Test Pattern 3a: Constants as attributes
print("Version: " + gui.VERSION);
print("Max width: " + str(gui.MAX_WIDTH));
print("Anchor: " + gui.ANCHOR_CENTER);

// Test Pattern 3b: Constants as methods
print("Default width: " + str(gui.DEFAULT_WIDTH()));
print("Default height: " + str(gui.DEFAULT_HEIGHT()));

// Test Pattern 2: Object creation and method chaining
window = gui.createWindow("My App");
window.setTitle("Updated Title");
title = window.getTitle();
print("Window title: " + title);

// Create button with callback
button = gui.createButton("Click Me");

// Test callback pattern - ML functions work directly as Python callables!
function handleClick() {
    print("Button was clicked!");
}

button.onClick(handleClick);

// Test method calls on returned objects
button.setText("Click Me Now");
text = button.getText();
print("Button text: " + text);

// Simulate clicks
button.click();
button.click();
clicks = button.getClickCount();
print("Total clicks: " + str(clicks));

// Test object passing (add button to window)
window.addWidget(button);
count = window.getWidgetCount();
print("Widget count: " + str(count));

// Show window
window.show();

print("All integration patterns working!");
