# Simple Flet Demos

This directory contains several simple examples to demonstrate Flet's capabilities. These examples progress from very basic to more comprehensive demonstrations.

## Files Overview

### 1. `hello_flet.py` - Hello World Example
The simplest possible Flet application that demonstrates:
- Basic page setup
- Text input field
- Button interaction
- Dynamic text updates

**Run with:**
```bash
python hello_flet.py
```

### 2. `simple_flet_demo.py` - Counter Application
A basic counter app showing:
- Button styling
- State management
- Layout with containers
- Visual styling (shadows, colors, spacing)

**Run with:**
```bash
python simple_flet_demo.py
```

### 3. `simple_form.py` - Form Handling
A complete form example demonstrating:
- Various input types (text, email, number, dropdown)
- Form validation
- Error handling and display
- Data submission and display

**Run with:**
```bash
python simple_form.py
```

### 4. `flet_features_demo.py` - Comprehensive Demo
A full-featured demo with navigation showing:
- Navigation rail
- Multiple pages/views
- Wide variety of Flet controls
- Layout examples
- Interactive components
- Data display (tables, lists)
- Styling and theming
- Animations

**Run with:**
```bash
python flet_features_demo.py
```

## Key Flet Concepts Demonstrated

### Basic Structure
Every Flet app follows this pattern:
```python
import flet as ft

def main(page: ft.Page):
    # Configure page
    page.title = "My App"
    
    # Create controls
    text = ft.Text("Hello, World!")
    
    # Add to page
    page.add(text)

# Run the app
ft.app(target=main)
```

### Core Controls Shown
- **Text**: Display text with various styles
- **TextField**: User input with validation
- **Button**: Various button types (Elevated, Outlined, Text, Icon)
- **Container**: Layout and styling wrapper
- **Row/Column**: Layout controls
- **Dropdown**: Selection lists
- **Checkbox/Switch/Radio**: Boolean and choice inputs
- **DataTable**: Tabular data display
- **ListView**: Scrollable lists
- **Card**: Material design cards

### Layout Concepts
- **Row**: Horizontal layout
- **Column**: Vertical layout
- **Container**: Wrapper with styling capabilities
- **Responsive**: Adapts to different screen sizes

### Styling Features
- Colors and themes
- Borders and shadows
- Padding and margins
- Border radius
- Background colors
- Text styling

### Interactivity
- Event handling with `on_click`, `on_change`
- State management with `page.update()`
- Dialog boxes and alerts
- Dynamic content updates

## Running the Demos

### Prerequisites
```bash
pip install flet
```

### Quick Start
1. Choose any demo file
2. Run it with Python:
   ```bash
   python filename.py
   ```
3. Your web browser will open automatically
4. Interact with the application

### Ports Used
- `hello_flet.py`: Default port (8550)
- `simple_flet_demo.py`: Port 8081
- `simple_form.py`: Port 8082
- `flet_features_demo.py`: Port 8083

### Desktop Mode
To run as a desktop application instead of web browser:
```python
ft.app(target=main, view=ft.FLET_APP)
```

## Learning Path

1. **Start with `hello_flet.py`** - Understand basic structure
2. **Try `simple_flet_demo.py`** - See styling and layout
3. **Explore `simple_form.py`** - Learn form handling
4. **Dive into `flet_features_demo.py`** - Comprehensive overview

## Next Steps

After understanding these demos:
- Explore the main `form_app/` directory for a complete application
- Check out [Flet documentation](https://flet.dev/)
- Try building your own application
- Experiment with different controls and layouts

## Tips for Development

1. **Use `page.update()`** after changing control properties
2. **Structure your code** with functions for different views
3. **Handle errors gracefully** with try-catch blocks
4. **Use responsive design** principles for different screen sizes
5. **Test on both web and desktop** modes

## Common Patterns

### Event Handling
```python
def button_click(e):
    # Handle the event
    text.value = "Button clicked!"
    page.update()

button = ft.ElevatedButton("Click me", on_click=button_click)
```

### Dynamic Updates
```python
# Change control properties
text.value = "New text"
container.bgcolor = ft.colors.BLUE

# Update the page
page.update()
```

### Layout with Styling
```python
container = ft.Container(
    content=ft.Text("Styled content"),
    padding=ft.padding.all(20),
    bgcolor=ft.colors.BLUE_100,
    border_radius=10,
    shadow=ft.BoxShadow(blur_radius=10)
)
```

Happy coding with Flet! 🚀