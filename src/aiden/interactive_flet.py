#!/usr/bin/env python3
"""
Interactive Flet Example
A simple but interactive example that demonstrates various Flet features
without using the colors attribute.
"""

import flet as ft


def main(page: ft.Page):
    """Main function for the interactive Flet app"""

    # Configure the page
    page.title = "Interactive Flet Demo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Create interactive elements
    name_input = ft.TextField(
        label="Enter your name",
        hint_text="What's your name?",
        width=300
    )

    age_input = ft.TextField(
        label="Enter your age",
        hint_text="How old are you?",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    color_dropdown = ft.Dropdown(
        label="Favorite color",
        width=300,
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Blue"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Yellow"),
            ft.dropdown.Option("Purple")
        ]
    )

    newsletter_checkbox = ft.Checkbox(
        label="Subscribe to newsletter",
        value=False
    )

    result_text = ft.Text(
        "",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    error_text = ft.Text(
        "",
        size=14
    )

    # Event handlers
    def submit_form(e):
        # Clear previous messages
        error_text.value = ""
        result_text.value = ""

        # Validate inputs
        name = name_input.value or ""
        age = age_input.value or ""
        color = color_dropdown.value or ""

        errors = []
        if not name.strip():
            errors.append("Name is required")

        if not age.strip():
            errors.append("Age is required")
        else:
            try:
                age_num = int(age)
                if age_num < 1 or age_num > 120:
                    errors.append("Age must be between 1 and 120")
            except ValueError:
                errors.append("Age must be a number")

        if errors:
            error_text.value = "Errors: " + "; ".join(errors)
        else:
            result_text.value = f"""
Hello {name}!
Age: {age}
Favorite Color: {color if color else 'Not selected'}
Newsletter: {'Yes' if newsletter_checkbox.value else 'No'}
            """.strip()

        page.update()

    def clear_form(e):
        name_input.value = ""
        age_input.value = ""
        color_dropdown.value = None
        newsletter_checkbox.value = False
        result_text.value = ""
        error_text.value = ""
        page.update()

    def show_alert(e):
        def close_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Information"),
            content=ft.Text("This is a simple alert dialog!"),
            actions=[
                ft.TextButton("OK", on_click=close_dialog)
            ]
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    # Counter section
    counter_value = ft.Text("0", size=30, weight=ft.FontWeight.BOLD)

    def increment_counter(e):
        counter_value.value = str(int(counter_value.value) + 1)
        page.update()

    def decrement_counter(e):
        counter_value.value = str(int(counter_value.value) - 1)
        page.update()

    def reset_counter(e):
        counter_value.value = "0"
        page.update()

    # Progress bar
    progress_bar = ft.ProgressBar(width=400, value=0)
    progress_text = ft.Text("Progress: 0%")

    def update_progress(e):
        current = progress_bar.value
        new_value = min(current + 0.2, 1.0)
        progress_bar.value = new_value
        progress_text.value = f"Progress: {int(new_value * 100)}%"
        page.update()

    def reset_progress(e):
        progress_bar.value = 0
        progress_text.value = "Progress: 0%"
        page.update()

    # Create the layout
    page.add(
        ft.Column([
            # Header
            ft.Text(
                "Interactive Flet Demo",
                size=32,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.CENTER
            ),

            ft.Divider(height=20),

            # Form section
            ft.Text("User Information Form", size=20, weight=ft.FontWeight.BOLD),
            name_input,
            age_input,
            color_dropdown,
            newsletter_checkbox,

            ft.Row([
                ft.ElevatedButton("Submit", on_click=submit_form),
                ft.OutlinedButton("Clear", on_click=clear_form)
            ], spacing=10),

            error_text,
            result_text,

            ft.Divider(height=20),

            # Counter section
            ft.Text("Counter", size=20, weight=ft.FontWeight.BOLD),
            counter_value,
            ft.Row([
                ft.ElevatedButton("- Decrease", on_click=decrement_counter),
                ft.ElevatedButton("+ Increase", on_click=increment_counter),
                ft.OutlinedButton("Reset", on_click=reset_counter)
            ], spacing=10, alignment=ft.MainAxisAlignment.CENTER),

            ft.Divider(height=20),

            # Progress section
            ft.Text("Progress Bar", size=20, weight=ft.FontWeight.BOLD),
            progress_bar,
            progress_text,
            ft.Row([
                ft.ElevatedButton("Update Progress", on_click=update_progress),
                ft.OutlinedButton("Reset Progress", on_click=reset_progress)
            ], spacing=10),

            ft.Divider(height=20),

            # Dialog section
            ft.Text("Dialog Demo", size=20, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Show Alert", on_click=show_alert),

            ft.Container(height=50)  # Bottom spacing

        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15,
        width=500
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
