# Kivy Installation and Usage Guide

## Overview

Kivy is a powerful Python framework for developing cross-platform applications with natural user interfaces. This guide will help you install Kivy and understand the examples provided.

## Installation

### Basic Installation

```bash
pip install kivy
```

### Platform-Specific Instructions

#### Windows
```bash
# Basic installation
pip install kivy[base]

# With media support (recommended)
pip install kivy[base,media]

# If you encounter issues, try:
python -m pip install --upgrade pip wheel setuptools
python -m pip install kivy[base] --no-deps
python -m pip install kivy_deps.glew kivy_deps.gstreamer kivy_deps.sdl2
```

#### macOS
```bash
# Basic installation
pip install kivy

# If you have issues with dependencies:
brew install pkg-config sdl2 sdl2_image sdl2_ttf sdl2_mixer gstreamer
pip install kivy[base]

# For Apple Silicon Macs:
pip install kivy[base] --no-binary kivy
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies first
sudo apt update
sudo apt install python3-pip python3-kivy

# Or install via pip:
sudo apt install python3-dev python3-setuptools
sudo apt install ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
pip install kivy
```

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv kivy_env

# Activate (Windows)
kivy_env\Scripts\activate

# Activate (macOS/Linux)
source kivy_env/bin/activate

# Install Kivy
pip install kivy
```

## File Overview

This directory contains several Kivy examples of increasing complexity:

### 1. `kivy_hello.py` - Hello World
**Purpose**: Minimal Kivy application
**Features**:
- Basic app structure
- Simple label display
- Window creation

**Run with**:
```bash
python kivy_hello.py
```

### 2. `kivy_simple.py` - Interactive Demo
**Purpose**: Basic interactive application with error handling
**Features**:
- Text input and display
- Button interactions
- Counter functionality
- Status updates
- Proper error handling

**Key Concepts**:
- Event handling with callbacks
- Widget layout with BoxLayout
- State management
- User input validation

### 3. `kivy_counter.py` - Counter Application
**Purpose**: Simple counter with multiple buttons
**Features**:
- Increment/decrement counter
- Reset functionality
- Button styling
- Layout management

### 4. `kivy_form.py` - Comprehensive Form
**Purpose**: Complete form application
**Features**:
- Multiple input types (text, slider, dropdown, checkbox)
- Form validation
- Popup dialogs
- Scrollable interface
- Data submission and display

**Widgets Demonstrated**:
- TextInput (single and multiline)
- Slider with live updates
- Spinner (dropdown)
- CheckBox
- ScrollView
- Popup dialogs

### 5. `kivy_game.py` - Interactive Game
**Purpose**: "Catch the Dots" game
**Features**:
- Real-time graphics with Canvas
- Touch/mouse input handling
- Game loop with Clock
- Collision detection
- Score system
- Dynamic difficulty

**Advanced Concepts**:
- Canvas drawing
- Animation and timing
- Custom widget classes
- Game state management

## Key Kivy Concepts

### 1. App Structure
Every Kivy app follows this pattern:
```python
from kivy.app import App
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text='Hello World')

MyApp().run()
```

### 2. Widgets and Layouts
**Common Widgets**:
- `Label`: Display text
- `Button`: Clickable button
- `TextInput`: Text input field
- `Slider`: Value slider
- `CheckBox`: Checkbox input
- `Spinner`: Dropdown selection

**Layout Widgets**:
- `BoxLayout`: Arrange widgets in rows/columns
- `GridLayout`: Grid arrangement
- `FloatLayout`: Absolute positioning
- `AnchorLayout`: Anchor widgets to edges

### 3. Event Handling
```python
def button_clicked(instance):
    print("Button was clicked!")

button = Button(text='Click me')
button.bind(on_press=button_clicked)
```

### 4. Properties and Binding
```python
# Widget properties
button = Button(
    text='My Button',
    size_hint=(0.5, 0.3),
    pos_hint={'center_x': 0.5, 'center_y': 0.5}
)

# Property binding
def on_text_change(instance, value):
    print(f"Text changed to: {value}")

text_input = TextInput()
text_input.bind(text=on_text_change)
```

### 5. Canvas and Graphics
```python
from kivy.graphics import Color, Rectangle

with widget.canvas:
    Color(1, 0, 0, 1)  # Red color (R, G, B, Alpha)
    Rectangle(pos=(100, 100), size=(200, 100))
```

## Running the Examples

### Prerequisites Check
Before running examples, verify Kivy is installed:
```python
python -c "import kivy; print('Kivy version:', kivy.__version__)"
```

### Running Examples
```bash
# Basic examples
python kivy_hello.py
python kivy_simple.py
python kivy_counter.py

# Advanced examples
python kivy_form.py
python kivy_game.py
```

### Expected Behavior
- **kivy_hello.py**: Shows a simple "Hello, Kivy World!" window
- **kivy_simple.py**: Interactive app with greeting, counter, and buttons
- **kivy_counter.py**: Counter with +/- buttons and reset
- **kivy_form.py**: Registration form with validation and popups
- **kivy_game.py**: Game where you catch falling dots with mouse/touch

## Troubleshooting

### Common Issues

#### "No module named 'kivy'"
**Solution**: Install Kivy using the platform-specific instructions above

#### Black/Empty Window
**Solutions**:
```bash
# Update graphics drivers
# Try different renderer
export KIVY_GL_BACKEND=gl
python your_app.py

# Or force software rendering
export KIVY_GL_BACKEND=mock
python your_app.py
```

#### "ImportError: No module named '_ctypes'"
**Solution** (Linux):
```bash
sudo apt-get install libffi-dev
```

#### Window Too Small/Large
**Solution**: Configure window size in code:
```python
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'resizable', True)
```

#### Touch Events Not Working
**Solution**: Ensure widget has proper size and collision detection:
```python
def on_touch_down(self, touch):
    if self.collide_point(*touch.pos):
        # Handle touch
        return True
    return super().on_touch_down(touch)
```

### Performance Tips

1. **Use appropriate layouts**: BoxLayout is faster than FloatLayout
2. **Minimize canvas updates**: Only redraw when necessary
3. **Unbind events**: Remove event bindings when widgets are destroyed
4. **Use Clock efficiently**: Avoid scheduling too many events

## Development Tips

### 1. Debugging
```python
# Enable debug output
import os
os.environ['KIVY_LOG_LEVEL'] = 'debug'

# Print widget tree
from kivy.base import EventLoop
EventLoop.ensure_window()
print(app.root.walk())
```

### 2. Testing on Mobile
- Use Buildozer for Android packaging
- Use kivy-ios for iOS packaging
- Test touch events thoroughly

### 3. Code Organization
```python
# Separate logic from UI
class GameLogic:
    def __init__(self):
        self.score = 0
    
    def update_score(self, points):
        self.score += points

class GameWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logic = GameLogic()
```

## Next Steps

1. **Start Simple**: Begin with `kivy_hello.py` or `kivy_simple.py`
2. **Experiment**: Modify the examples to understand concepts
3. **Read Documentation**: Visit https://kivy.org/doc/stable/
4. **Build Something**: Create your own application
5. **Join Community**: Kivy Discord, GitHub discussions

## Resources

- **Official Documentation**: https://kivy.org/doc/stable/
- **Garden (Add-ons)**: https://github.com/kivy-garden
- **Examples**: https://github.com/kivy/kivy/tree/master/examples
- **Tutorials**: https://kivy.org/doc/stable/tutorials.html

## Packaging for Distribution

### Desktop (PyInstaller)
```bash
pip install pyinstaller
pyinstaller --onefile your_app.py
```

### Android (Buildozer)
```bash
pip install buildozer
buildozer init
buildozer android debug
```

### iOS (kivy-ios)
```bash
pip install kivy-ios
toolchain build python3 kivy
toolchain create <title> <app_directory>
```

Happy coding with Kivy! 🚀