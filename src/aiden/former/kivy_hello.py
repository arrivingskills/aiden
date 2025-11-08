#!/usr/bin/env python3
"""
Simple Kivy Hello World Application
A minimal example to demonstrate Kivy basics.
"""

from kivy.app import App
from kivy.uix.label import Label


class HelloApp(App):
    """Simple Hello World Kivy App"""

    def build(self):
        """Build the application - this method is required"""
        return Label(
            text='Hello, Kivy World!',
            font_size='20sp'
        )


if __name__ == '__main__':
    HelloApp().run()
