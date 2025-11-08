#!/usr/bin/env python3
"""
Basic Flet Demo - Simple Counter App
A minimal example that works with basic Flet installation.
"""

import flet as ft


def main(page: ft.Page):
    """Main function for the Flet app"""

    # Configure the page
    page.title = "Basic Flet Demo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Create a counter variable
    counter = ft.Text("0", size=40, weight=ft.FontWeight.BOLD)

    # Define click handlers
    def increment_click(e):
        counter.value = str(int(counter.value) + 1)
        page.update()

    def decrement_click(e):
        counter.value = str(int(counter.value) - 1)
        page.update()

    def reset_click(e):
        counter.value = "0"
        page.update()

    # Create buttons
    increment_btn = ft.ElevatedButton(
        text="➕ Add",
        on_click=increment_click
    )

    decrement_btn = ft.ElevatedButton(
        text="➖ Subtract",
        on_click=decrement_click
    )

    reset_btn = ft.OutlinedButton(
        text="🔄 Reset",
        on_click=reset_click
    )

    # Create layout
    page.add(
        ft.Column([
            ft.Text("Simple Counter", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),  # Spacer
            counter,
            ft.Container(height=30),  # Spacer
            ft.Row([
                decrement_btn,
                increment_btn
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=20),  # Spacer
            reset_btn
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )


if __name__ == "__main__":
    # Run the app
    ft.app(target=main)
