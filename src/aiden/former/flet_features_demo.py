#!/usr/bin/env python3
"""
Comprehensive Flet Features Demo
This file demonstrates various Flet components and features in a single application.
"""

import flet as ft
import time
import threading


def main(page: ft.Page):
    """Main function showcasing various Flet features"""

    # Configure page
    page.title = "Flet Features Demo"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    page.window_width = 900
    page.window_height = 700

    # Navigation rail for different sections
    def on_nav_change(e):
        selected = e.control.selected_index

        # Clear content
        content_area.controls.clear()

        if selected == 0:
            show_basic_controls()
        elif selected == 1:
            show_layout_demo()
        elif selected == 2:
            show_interactive_demo()
        elif selected == 3:
            show_data_display()
        elif selected == 4:
            show_styling_demo()

        page.update()

    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.icons.WIDGETS_OUTLINED,
                selected_icon=ft.icons.WIDGETS,
                label="Controls"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.VIEW_QUILT_OUTLINED,
                selected_icon=ft.icons.VIEW_QUILT,
                label="Layout"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.TOUCH_APP_OUTLINED,
                selected_icon=ft.icons.TOUCH_APP,
                label="Interactive"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.TABLE_CHART_OUTLINED,
                selected_icon=ft.icons.TABLE_CHART,
                label="Data"
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PALETTE_OUTLINED,
                selected_icon=ft.icons.PALETTE,
                label="Styling"
            ),
        ],
        on_change=on_nav_change,
    )

    # Content area
    content_area = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    def show_basic_controls():
        """Demonstrate basic Flet controls"""
        content_area.controls = [
            ft.Text("Basic Controls Demo", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            # Text widgets
            ft.Text("Text Styles:", weight=ft.FontWeight.BOLD),
            ft.Text("Normal text"),
            ft.Text("Bold text", weight=ft.FontWeight.BOLD),
            ft.Text("Italic text", italic=True),
            ft.Text("Colored text", color=ft.colors.BLUE),
            ft.Text("Large text", size=20),

            ft.Divider(),

            # Input controls
            ft.Text("Input Controls:", weight=ft.FontWeight.BOLD),
            ft.TextField(label="Text Field", hint_text="Enter text here"),
            ft.TextField(label="Password", password=True, can_reveal_password=True),
            ft.TextField(label="Multiline", multiline=True, min_lines=3),

            ft.Dropdown(
                label="Dropdown",
                options=[
                    ft.dropdown.Option("Option 1"),
                    ft.dropdown.Option("Option 2"),
                    ft.dropdown.Option("Option 3"),
                ]
            ),

            ft.Checkbox(label="Checkbox"),
            ft.Switch(label="Switch"),
            ft.Radio(value="radio1", label="Radio Button 1"),
            ft.Radio(value="radio2", label="Radio Button 2"),

            ft.Slider(min=0, max=100, value=50, label="Slider: {value}"),

            ft.Divider(),

            # Buttons
            ft.Text("Buttons:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton("Elevated"),
                ft.OutlinedButton("Outlined"),
                ft.TextButton("Text"),
                ft.IconButton(icon=ft.icons.FAVORITE, tooltip="Icon Button"),
            ]),
        ]

    def show_layout_demo():
        """Demonstrate layout controls"""
        content_area.controls = [
            ft.Text("Layout Demo", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            ft.Text("Row Layout:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(ft.Text("Item 1"), bgcolor=ft.colors.RED_100, padding=10),
                ft.Container(ft.Text("Item 2"), bgcolor=ft.colors.GREEN_100, padding=10),
                ft.Container(ft.Text("Item 3"), bgcolor=ft.colors.BLUE_100, padding=10),
            ]),

            ft.Text("Column Layout:", weight=ft.FontWeight.BOLD),
            ft.Container(
                ft.Column([
                    ft.Container(ft.Text("Item A"), bgcolor=ft.colors.YELLOW_100, padding=10),
                    ft.Container(ft.Text("Item B"), bgcolor=ft.colors.PURPLE_100, padding=10),
                    ft.Container(ft.Text("Item C"), bgcolor=ft.colors.ORANGE_100, padding=10),
                ]),
                border=ft.border.all(1, ft.colors.GREY_400)
            ),

            ft.Text("Container with styling:", weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text("Styled Container", color=ft.colors.WHITE),
                margin=10,
                padding=ft.padding.all(15),
                bgcolor=ft.colors.BLUE_600,
                border=ft.border.all(2, ft.colors.BLUE_800),
                border_radius=ft.border_radius.all(10),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=ft.colors.BLUE_GREY_300,
                    offset=ft.Offset(0, 0),
                    blur_style=ft.ShadowBlurStyle.OUTER,
                ),
            ),

            ft.Text("Card Layout:", weight=ft.FontWeight.BOLD),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.ALBUM),
                            title=ft.Text("Card Title"),
                            subtitle=ft.Text("This is a card with content"),
                        ),
                        ft.Row([
                            ft.TextButton("Action 1"),
                            ft.TextButton("Action 2"),
                        ], alignment=ft.MainAxisAlignment.END),
                    ]),
                    width=400,
                    padding=10,
                )
            ),
        ]

    def show_interactive_demo():
        """Demonstrate interactive features"""
        counter = ft.Text("0", size=30)
        progress = ft.ProgressBar(width=400, value=0)
        progress_text = ft.Text("Progress: 0%")

        def increment_counter(e):
            counter.value = str(int(counter.value) + 1)
            page.update()

        def reset_counter(e):
            counter.value = "0"
            page.update()

        def update_progress(e):
            progress.value = min(progress.value + 0.1, 1.0)
            progress_text.value = f"Progress: {int(progress.value * 100)}%"
            page.update()

        def reset_progress(e):
            progress.value = 0
            progress_text.value = "Progress: 0%"
            page.update()

        # Alert dialog demo
        def show_alert(e):
            def close_dialog(e):
                alert_dialog.open = False
                page.update()

            alert_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Alert"),
                content=ft.Text("This is an alert dialog!"),
                actions=[
                    ft.TextButton("OK", on_click=close_dialog),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )

            page.dialog = alert_dialog
            alert_dialog.open = True
            page.update()

        content_area.controls = [
            ft.Text("Interactive Demo", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            ft.Text("Counter:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.ElevatedButton("+ Add", on_click=increment_counter),
                counter,
                ft.OutlinedButton("Reset", on_click=reset_counter),
            ], alignment=ft.MainAxisAlignment.CENTER),

            ft.Divider(),

            ft.Text("Progress Bar:", weight=ft.FontWeight.BOLD),
            progress,
            progress_text,
            ft.Row([
                ft.ElevatedButton("Update Progress", on_click=update_progress),
                ft.OutlinedButton("Reset Progress", on_click=reset_progress),
            ]),

            ft.Divider(),

            ft.Text("Dialog Demo:", weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Show Alert", on_click=show_alert),

            ft.Divider(),

            ft.Text("Loading Indicator:", weight=ft.FontWeight.BOLD),
            ft.ProgressRing(),
        ]

    def show_data_display():
        """Demonstrate data display components"""

        # Data table
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Age")),
                ft.DataColumn(ft.Text("City")),
            ],
            rows=[
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("John")),
                    ft.DataCell(ft.Text("30")),
                    ft.DataCell(ft.Text("New York")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Jane")),
                    ft.DataCell(ft.Text("25")),
                    ft.DataCell(ft.Text("London")),
                ]),
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("Bob")),
                    ft.DataCell(ft.Text("35")),
                    ft.DataCell(ft.Text("Tokyo")),
                ]),
            ],
        )

        # List view
        list_view = ft.ListView(
            expand=1,
            spacing=10,
            padding=ft.padding.all(20),
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.icons.PERSON),
                    title=ft.Text(f"Person {i}"),
                    subtitle=ft.Text(f"Description for person {i}"),
                    trailing=ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(text="Edit"),
                            ft.PopupMenuItem(text="Delete"),
                        ]
                    ),
                )
                for i in range(1, 6)
            ],
        )

        content_area.controls = [
            ft.Text("Data Display Demo", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            ft.Text("Data Table:", weight=ft.FontWeight.BOLD),
            data_table,

            ft.Divider(),

            ft.Text("List View:", weight=ft.FontWeight.BOLD),
            ft.Container(list_view, height=200, border=ft.border.all(1, ft.colors.GREY_400)),

            ft.Divider(),

            ft.Text("Icons:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Icon(ft.icons.FAVORITE, color=ft.colors.RED),
                ft.Icon(ft.icons.STAR, color=ft.colors.YELLOW),
                ft.Icon(ft.icons.THUMB_UP, color=ft.colors.BLUE),
                ft.Icon(ft.icons.HOME, color=ft.colors.GREEN),
            ]),
        ]

    def show_styling_demo():
        """Demonstrate styling and theming"""

        def toggle_theme(e):
            page.theme_mode = (
                ft.ThemeMode.DARK
                if page.theme_mode == ft.ThemeMode.LIGHT
                else ft.ThemeMode.LIGHT
            )
            page.update()

        content_area.controls = [
            ft.Text("Styling Demo", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),

            ft.Text("Theme Toggle:", weight=ft.FontWeight.BOLD),
            ft.ElevatedButton("Toggle Dark/Light Theme", on_click=toggle_theme),

            ft.Divider(),

            ft.Text("Color Examples:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    ft.Text("Primary", color=ft.colors.WHITE),
                    bgcolor=ft.colors.PRIMARY,
                    padding=10,
                    border_radius=5,
                ),
                ft.Container(
                    ft.Text("Secondary", color=ft.colors.WHITE),
                    bgcolor=ft.colors.SECONDARY,
                    padding=10,
                    border_radius=5,
                ),
                ft.Container(
                    ft.Text("Success", color=ft.colors.WHITE),
                    bgcolor=ft.colors.GREEN,
                    padding=10,
                    border_radius=5,
                ),
                ft.Container(
                    ft.Text("Error", color=ft.colors.WHITE),
                    bgcolor=ft.colors.RED,
                    padding=10,
                    border_radius=5,
                ),
            ]),

            ft.Divider(),

            ft.Text("Border and Shadow Examples:", weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Container(
                    ft.Text("Rounded"),
                    padding=20,
                    border_radius=20,
                    bgcolor=ft.colors.BLUE_100,
                ),
                ft.Container(
                    ft.Text("Bordered"),
                    padding=20,
                    border=ft.border.all(2, ft.colors.BLUE),
                ),
                ft.Container(
                    ft.Text("Shadow"),
                    padding=20,
                    bgcolor=ft.colors.WHITE,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.colors.GREY_400,
                        offset=ft.Offset(0, 0),
                    ),
                ),
            ], spacing=20),

            ft.Divider(),

            ft.Text("Animation Example:", weight=ft.FontWeight.BOLD),
            ft.AnimatedSwitcher(
                ft.Text("Click button to animate!"),
                transition=ft.AnimatedSwitcherTransition.SCALE,
                duration=300,
                reverse_duration=100,
                switch_in_curve=ft.AnimationCurve.BOUNCE_OUT,
                switch_out_curve=ft.AnimationCurve.BOUNCE_IN,
            ),
        ]

    # Initialize with basic controls
    show_basic_controls()

    # Main layout
    page.add(
        ft.Row([
            nav_rail,
            ft.VerticalDivider(width=1),
            ft.Container(content_area, expand=True, padding=20),
        ], expand=True)
    )


if __name__ == "__main__":
    ft.app(target=main, view=ft.WEB_BROWSER, port=8083)
