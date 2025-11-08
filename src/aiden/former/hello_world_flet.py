#!/usr/bin/env python3
"""
Hello World Flet - The Simplest Possible Example
This is the most basic Flet application you can create.
"""

import flet as ft


def main(page: ft.Page):
    """Main function that defines our app"""

    page.title = "Hello World"

    # Add a simple text to the page
    page.add(ft.Text("Hello, World!"))


# Run the app
if __name__ == "__main__":
    ft.app(target=main)
