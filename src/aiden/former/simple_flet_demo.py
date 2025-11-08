#!/usr/bin/env python3
"""
Simple Flet Counter Demo
A basic example showing how to create a simple counter app with Flet.
"""

import flet as ft


def main(page: ft.Page):
    """Main function for the Flet app"""

    # Configure the page
    page.title = "Simple Counter App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 400
    page.window_height = 300

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
        on_click=increment_click,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.GREEN_600,
            color=ft.colors.WHITE
        )
    )

    decrement_btn = ft.ElevatedButton(
        text="➖ Subtract",
        on_click=decrement_click,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.RED_600,
            color=ft.colors.WHITE
        )
    )

    reset_btn = ft.OutlinedButton(
        text="🔄 Reset",
        on_click=reset_click
    )

    # Create layout
    page.add(
        ft.Container(
            content=ft.Column([
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
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(30),
            bgcolor=ft.colors.WHITE,
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.GREY_300,
                offset=ft.Offset(0, 2),
            )
        )
    )


if __name__ == "__main__":
    # Run the app
    ft.app(target=main, view=ft.WEB_BROWSER, port=8081)
