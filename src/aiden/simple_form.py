#!/usr/bin/env python3
"""
Simple Form Example with Flet
Demonstrates form handling, validation, and data display.
"""

import flet as ft


def main(page: ft.Page):
    """Main function for the simple form app"""

    # Configure page
    page.title = "Simple Form with Flet"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Form fields
    name_field = ft.TextField(
        label="Full Name",
        hint_text="Enter your full name",
        width=300
    )

    email_field = ft.TextField(
        label="Email",
        hint_text="Enter your email address",
        width=300
    )

    age_field = ft.TextField(
        label="Age",
        hint_text="Enter your age",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER
    )

    # Dropdown for favorite color
    color_dropdown = ft.Dropdown(
        label="Favorite Color",
        width=300,
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Blue"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Yellow"),
            ft.dropdown.Option("Purple"),
        ]
    )

    # Checkbox for newsletter
    newsletter_checkbox = ft.Checkbox(
        label="Subscribe to newsletter",
        value=False
    )

    # Result display area
    result_text = ft.Text(
        "",
        size=16,
        color=ft.colors.GREEN_600
    )

    error_text = ft.Text(
        "",
        size=14,
        color=ft.colors.RED_600
    )

    def validate_form():
        """Simple form validation"""
        errors = []

        if not name_field.value or not name_field.value.strip():
            errors.append("Name is required")

        if not email_field.value or not email_field.value.strip():
            errors.append("Email is required")
        elif "@" not in email_field.value:
            errors.append("Invalid email format")

        if not age_field.value or not age_field.value.strip():
            errors.append("Age is required")
        else:
            try:
                age = int(age_field.value)
                if age < 1 or age > 120:
                    errors.append("Age must be between 1 and 120")
            except ValueError:
                errors.append("Age must be a number")

        return errors

    def submit_form(e):
        """Handle form submission"""
        # Clear previous messages
        error_text.value = ""
        result_text.value = ""

        # Validate form
        errors = validate_form()

        if errors:
            error_text.value = "Errors: " + "; ".join(errors)
        else:
            # Display submitted data
            result_text.value = f"""
Form Submitted Successfully!

Name: {name_field.value}
Email: {email_field.value}
Age: {age_field.value}
Favorite Color: {color_dropdown.value or 'Not selected'}
Newsletter: {'Yes' if newsletter_checkbox.value else 'No'}
            """

        page.update()

    def clear_form(e):
        """Clear all form fields"""
        name_field.value = ""
        email_field.value = ""
        age_field.value = ""
        color_dropdown.value = None
        newsletter_checkbox.value = False
        result_text.value = ""
        error_text.value = ""
        page.update()

    # Submit button
    submit_button = ft.ElevatedButton(
        text="Submit",
        on_click=submit_form,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.BLUE_600,
            color=ft.colors.WHITE
        )
    )

    # Clear button
    clear_button = ft.OutlinedButton(
        text="Clear",
        on_click=clear_form
    )

    # Layout
    page.add(
        ft.Column([
            # Header
            ft.Text(
                "Simple Registration Form",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_900
            ),

            ft.Divider(height=20),

            # Form fields
            name_field,
            email_field,
            age_field,
            color_dropdown,
            newsletter_checkbox,

            ft.Container(height=20),  # Spacer

            # Buttons
            ft.Row([
                submit_button,
                clear_button
            ], spacing=10),

            ft.Container(height=20),  # Spacer

            # Messages
            error_text,
            result_text,

        ], spacing=15, width=400)
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8082)
