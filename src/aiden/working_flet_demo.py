#!/usr/bin/env python3
"""
Working Flet Demo - Simple Interactive Application
A complete working example of Flet that demonstrates core features.
"""

import flet as ft


def main(page: ft.Page):
    """Main function for the Flet application"""

    # Configure the page
    page.title = "Simple Flet Demo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # State variables
    counter_value = 0

    # Create UI components
    title = ft.Text(
        "Welcome to Flet!",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700
    )

    # Name input section
    name_field = ft.TextField(
        label="Your Name",
        hint_text="Enter your name here",
        width=300
    )

    greeting_text = ft.Text(
        "Hello, World!",
        size=18,
        color=ft.Colors.GREEN_600
    )

    # Counter section
    counter_display = ft.Text(
        str(counter_value),
        size=40,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.PURPLE_600
    )

    # Event handlers
    def say_hello(e):
        name = name_field.value.strip() if name_field.value else ""
        if name:
            greeting_text.value = f"Hello, {name}! 👋"
        else:
            greeting_text.value = "Hello, World! 🌍"
        page.update()

    def increment_counter(e):
        nonlocal counter_value
        counter_value += 1
        counter_display.value = str(counter_value)
        page.update()

    def decrement_counter(e):
        nonlocal counter_value
        counter_value -= 1
        counter_display.value = str(counter_value)
        page.update()

    def reset_counter(e):
        nonlocal counter_value
        counter_value = 0
        counter_display.value = str(counter_value)
        page.update()

    def show_info(e):
        # Create a dialog
        def close_dialog(e):
            info_dialog.open = False
            page.update()

        info_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("About This Demo"),
            content=ft.Text(
                "This is a simple Flet demonstration showing:\n\n"
                "• Text input and display\n"
                "• Button interactions\n"
                "• Counter functionality\n"
                "• Dialog boxes\n"
                "• Basic styling\n\n"
                "Flet makes it easy to build beautiful apps with Python!"
            ),
            actions=[
                ft.TextButton("Close", on_click=close_dialog)
            ]
        )

        page.dialog = info_dialog
        info_dialog.open = True
        page.update()

    # Create buttons
    hello_button = ft.ElevatedButton(
        "Say Hello",
        on_click=say_hello,
        icon=ft.Icons.WAVING_HAND
    )

    plus_button = ft.ElevatedButton(
        "+",
        on_click=increment_counter,
        width=60
    )

    minus_button = ft.ElevatedButton(
        "-",
        on_click=decrement_counter,
        width=60
    )

    reset_button = ft.OutlinedButton(
        "Reset",
        on_click=reset_counter,
        icon=ft.Icons.REFRESH
    )

    info_button = ft.IconButton(
        icon=ft.Icons.INFO,
        tooltip="About this demo",
        on_click=show_info
    )

    # Create the main layout
    main_content = ft.Container(
        content=ft.Column(
            [
                # Header
                ft.Row(
                    [title, info_button],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                ft.Divider(height=30),

                # Greeting section
                ft.Container(
                    content=ft.Column([
                        ft.Text("👋 Greeting Section", size=20, weight=ft.FontWeight.BOLD),
                        name_field,
                        hello_button,
                        greeting_text
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    width=400
                ),

                ft.Container(height=20),  # Spacer

                # Counter section
                ft.Container(
                    content=ft.Column([
                        ft.Text("🔢 Counter Section", size=20, weight=ft.FontWeight.BOLD),
                        counter_display,
                        ft.Row([
                            minus_button,
                            plus_button
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                        reset_button
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=10,
                    width=400
                ),

                ft.Container(height=20),  # Spacer

                # Sample data display
                ft.Container(
                    content=ft.Column([
                        ft.Text("📊 Sample Features", size=20, weight=ft.FontWeight.BOLD),
                        ft.ProgressBar(value=0.7, width=300),
                        ft.Text("Progress: 70%", size=14),
                        ft.Row([
                            ft.Chip(
                                label=ft.Text("Python"),
                                leading=ft.Icon(ft.Icons.CODE)
                            ),
                            ft.Chip(
                                label=ft.Text("Flet"),
                                leading=ft.Icon(ft.Icons.WEB)
                            ),
                            ft.Chip(
                                label=ft.Text("Demo"),
                                leading=ft.Icon(ft.Icons.PLAY_ARROW)
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=20,
                    bgcolor=ft.Colors.ORANGE_50,
                    border_radius=10,
                    width=400
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10
        ),
        padding=30
    )

    # Add everything to the page
    page.add(main_content)


# Run the application
if __name__ == "__main__":
    print("🚀 Starting Flet Demo...")
    print("📱 The app will open in your web browser")
    print("🔗 URL: http://localhost:8550")
    print("⏹️  Press Ctrl+C to stop")

    ft.app(target=main, view=ft.WEB_BROWSER)
