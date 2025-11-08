#!/usr/bin/env python3
"""
Hello World Flet Example
The simplest possible Flet application to demonstrate basic concepts.
"""

import flet as ft


def main(page: ft.Page):
    """Main function that defines the app"""

    # Set page properties
    page.title = "Hello Flet!"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Create a text field for user input
    name_field = ft.TextField(
        label="Enter your name",
        width=300
    )

    # Create a text widget to display greeting
    greeting = ft.Text(
        "Hello, World!",
        size=20,
        color=ft.colors.BLUE
    )

    # Define button click handler
    def say_hello(e):
        if name_field.value:
            greeting.value = f"Hello, {name_field.value}!"
        else:
            greeting.value = "Hello, World!"
        page.update()

    # Create a button
    hello_button = ft.ElevatedButton(
        text="Say Hello",
        on_click=say_hello
    )

    # Add components to the page
    page.add(
        ft.Column([
            ft.Text("Simple Flet App", size=30, weight=ft.FontWeight.BOLD),
            name_field,
            hello_button,
            greeting
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20)
    )


# Run the app
if __name__ == "__main__":
    ft.app(target=main)
