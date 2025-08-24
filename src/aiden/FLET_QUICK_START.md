# Flet Quick Start Guide

## The Issue with Colors

If you see the error `flet has no attribute colors`, the fix is simple:

**❌ Wrong:**
```python
import flet as ft
ft.colors.BLUE  # This will fail
```

**✅ Correct:**
```python
import flet as ft
ft.Colors.BLUE  # Note the capital C
```

## Minimal Working Example

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Hello Flet"
    page.add(ft.Text("Hello, World!"))

ft.app(target=main)
```

## Common Flet Patterns

### 1. Basic Structure
Every Flet app follows this pattern:
```python
import flet as ft

def main(page: ft.Page):
    # Configure page
    page.title = "My App"
    
    # Create controls
    text = ft.Text("Hello!")
    
    # Add to page
    page.add(text)

ft.app(target=main)
```

### 2. Interactive Elements
```python
def button_click(e):
    text.value = "Button clicked!"
    page.update()  # Important: call update after changes

button = ft.ElevatedButton("Click me", on_click=button_click)
text = ft.Text("Original text")

page.add(button, text)
```

### 3. Colors (Note the Capital C)
```python
# Text with color
ft.Text("Colored text", color=ft.Colors.BLUE)

# Button with colored background
ft.ElevatedButton(
    "Button",
    style=ft.ButtonStyle(
        bgcolor=ft.Colors.GREEN_600,
        color=ft.Colors.WHITE
    )
)

# Container with background color
ft.Container(
    content=ft.Text("Container"),
    bgcolor=ft.Colors.BLUE_50,
    padding=20
)
```

### 4. Layout
```python
# Vertical layout
ft.Column([
    ft.Text("Item 1"),
    ft.Text("Item 2"),
    ft.Text("Item 3")
])

# Horizontal layout
ft.Row([
    ft.Text("Left"),
    ft.Text("Center"),
    ft.Text("Right")
])
```

### 5. User Input
```python
name_field = ft.TextField(
    label="Name",
    hint_text="Enter your name"
)

def submit(e):
    print(f"Name: {name_field.value}")
    page.update()

submit_btn = ft.ElevatedButton("Submit", on_click=submit)
```

## Key Points to Remember

1. **Colors**: Use `ft.Colors.BLUE` not `ft.colors.blue`
2. **Update**: Call `page.update()` after changing control properties
3. **Event handlers**: Functions that handle events get an `e` parameter
4. **Layout**: Use `ft.Column` for vertical, `ft.Row` for horizontal layout
5. **Styling**: Most visual properties go in style objects or direct parameters

## Running Your App

```python
# Web browser (default)
ft.app(target=main)

# Desktop app
ft.app(target=main, view=ft.FLET_APP)

# Specific port
ft.app(target=main, port=8080)
```

## Simple Complete Example

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Counter App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    counter = ft.Text("0", size=30)
    
    def increment(e):
        counter.value = str(int(counter.value) + 1)
        page.update()
    
    def decrement(e):
        counter.value = str(int(counter.value) - 1)
        page.update()
    
    page.add(
        ft.Column([
            ft.Text("Simple Counter", size=20),
            counter,
            ft.Row([
                ft.ElevatedButton("-", on_click=decrement),
                ft.ElevatedButton("+", on_click=increment)
            ], alignment=ft.MainAxisAlignment.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
```

## Installation

```bash
pip install flet
```

That's it! Save any of these examples as a `.py` file and run with:
```bash
python your_app.py
```

The app will open in your web browser automatically.