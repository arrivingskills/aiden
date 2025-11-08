#!/usr/bin/env python3
"""
Corrected Flet Demo - Simple Interactive App
A working example that demonstrates Flet with proper color usage.
"""

import flet as ft


def main(page: ft.Page):
    """Main function for the Flet app"""

    # Configure the page
    page.title = "Corrected Flet Demo"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # Create a counter variable
    counter = ft.Text("0", size=40, weight=ft.FontWeight.BOLD)

    # Create a text input for name
    name_input = ft.TextField(
        label="Enter your name",
        hint_text="What's your name?",
        width=300
    )

    # Create a greeting text
    greeting = ft.Text(
        "Hello, World!",
        size=20,
        color=ft.Colors.BLUE
    )

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

    def say_hello(e):
        if name_input.value and name_input.value.strip():
            greeting.value = f"Hello, {name_input.value}!"
        else:
            greeting.value = "Hello, World!"
        page.update()

    def show_alert(e):
        def close_dialog(e):
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Information"),
            content=ft.Text("This is a working Flet demo!"),
            actions=[
                ft.TextButton("OK", on_click=close_dialog)
            ]
        )

        page.dialog = dialog
        dialog.open = True
        page.update()

    # Create buttons with colors
    increment_btn = ft.ElevatedButton(
        text="➕ Add",
        on_click=increment_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE
        )
    )

    decrement_btn = ft.ElevatedButton(
        text="➖ Subtract",
        on_click=decrement_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE
        )
    )

    reset_btn = ft.OutlinedButton(
        text="🔄 Reset",
        on_click=reset_click
    )

    hello_btn = ft.ElevatedButton(
        text="Say Hello",
        on_click=say_hello,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE
        )
    )

    alert_btn = ft.ElevatedButton(
        text="Show Alert",
        on_click=show_alert,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.PURPLE_600,
            color=ft.Colors.WHITE
        )
    )

    # Create layout with styled containers
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "Corrected Flet Demo",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_900
                ),

                ft.Divider(height=20),

                # Greeting section
                ft.Text("Greeting Section", size=18, weight=ft.FontWeight.BOLD),
                name_input,
                hello_btn,
                greeting,

                ft.Divider(height=20),

                # Counter section
                ft.Text("Counter Section", size=18, weight=ft.FontWeight.BOLD),
                counter,
                ft.Row([
                    decrement_btn,
                    increment_btn
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                reset_btn,

                ft.Divider(height=20),

                # Alert section
                ft.Text("Dialog Section", size=18, weight=ft.FontWeight.BOLD),
                alert_btn,

                # Colored containers demo
                ft.Text("Styled Containers", size=18, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Container(
                        content=ft.Text("Primary", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.BLUE_600,
                        padding=ft.padding.all(15),
                        border_radius=ft.border_radius.all(8),
                        width=100,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text("Success", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.GREEN_600,
                        padding=ft.padding.all(15),
                        border_radius=ft.border_radius.all(8),
                        width=100,
                        alignment=ft.alignment.center
                    ),
                    ft.Container(
                        content=ft.Text("Warning", color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.ORANGE_600,
                        padding=ft.padding.all(15),
                        border_radius=ft.border_radius.all(8),
                        width=100,
                        alignment=ft.alignment.center
                    )
                ], spacing=10, alignment=ft.MainAxisAlignment.CENTER)

            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
            ),
            padding=ft.padding.all(30),
            bgcolor=ft.Colors.GREY_50,
            border_radius=ft.border_radius.all(12),
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.Colors.GREY_300,
                offset=ft.Offset(0, 2),
            ),
            width=500
        )
    )


if __name__ == "__main__":
    # Run the app
    ft.app(target=main, view=ft.WEB_BROWSER, port=8080)
