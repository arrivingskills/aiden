#!/usr/bin/env python3
"""
Simple Kivy Counter Application
A basic counter app demonstrating Kivy widgets and event handling.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class CounterApp(App):
    """Simple Counter Kivy Application"""

    def build(self):
        """Build the application UI"""
        # Create main layout
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Title label
        title = Label(
            text='Kivy Counter App',
            font_size='24sp',
            size_hint=(1, 0.3)
        )

        # Counter display
        self.counter_label = Label(
            text='0',
            font_size='48sp',
            size_hint=(1, 0.4)
        )

        # Button layout
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))

        # Decrease button
        decrease_btn = Button(
            text='-',
            font_size='24sp',
            on_press=self.decrease_counter
        )

        # Increase button
        increase_btn = Button(
            text='+',
            font_size='24sp',
            on_press=self.increase_counter
        )

        # Reset button
        reset_btn = Button(
            text='Reset',
            font_size='18sp',
            on_press=self.reset_counter
        )

        # Add buttons to button layout
        button_layout.add_widget(decrease_btn)
        button_layout.add_widget(increase_btn)

        # Add all widgets to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(self.counter_label)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(reset_btn)

        # Initialize counter
        self.counter = 0

        return main_layout

    def increase_counter(self, instance):
        """Increase counter by 1"""
        self.counter += 1
        self.counter_label.text = str(self.counter)

    def decrease_counter(self, instance):
        """Decrease counter by 1"""
        self.counter -= 1
        self.counter_label.text = str(self.counter)

    def reset_counter(self, instance):
        """Reset counter to 0"""
        self.counter = 0
        self.counter_label.text = str(self.counter)


if __name__ == '__main__':
    CounterApp().run()
