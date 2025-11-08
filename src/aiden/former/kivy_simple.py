#!/usr/bin/env python3
"""
Simple Kivy Application with Error Handling
A working example that demonstrates Kivy basics with proper error handling.
"""

import sys

try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.config import Config

    # Configure Kivy before other imports
    Config.set('graphics', 'width', '400')
    Config.set('graphics', 'height', '300')
    Config.set('graphics', 'resizable', False)

except ImportError as e:
    print("❌ Kivy is not installed!")
    print("📦 To install Kivy, run:")
    print("   pip install kivy")
    print("")
    print("🔧 If you're on macOS and have issues, try:")
    print("   pip install kivy[base]")
    print("")
    print("🐧 On Linux, you might need:")
    print("   sudo apt-get install python3-kivy")
    print("")
    print("🪟 On Windows, try:")
    print("   pip install kivy[base,media]")
    sys.exit(1)


class SimpleKivyApp(App):
    """Simple Kivy Application demonstrating basic widgets and interactions"""

    def build(self):
        """Build the application UI"""
        # Set window title
        self.title = "Simple Kivy Demo"

        # Create main layout
        main_layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        # Title
        title = Label(
            text='Welcome to Kivy!',
            font_size='24sp',
            size_hint=(1, 0.2),
            color=(0.2, 0.6, 1, 1)  # Blue color
        )

        # Name input section
        name_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        name_label = Label(text='Name:', size_hint=(0.3, 1))
        self.name_input = TextInput(
            hint_text='Enter your name',
            multiline=False,
            size_hint=(0.7, 1)
        )
        name_layout.add_widget(name_label)
        name_layout.add_widget(self.name_input)

        # Greeting display
        self.greeting_label = Label(
            text='Hello, World!',
            font_size='18sp',
            size_hint=(1, 0.2),
            color=(0, 0.7, 0, 1)  # Green color
        )

        # Counter section
        counter_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        self.counter_label = Label(
            text='Count: 0',
            font_size='16sp',
            size_hint=(0.4, 1)
        )

        minus_btn = Button(
            text='-',
            size_hint=(0.2, 1),
            on_press=self.decrease_counter
        )

        plus_btn = Button(
            text='+',
            size_hint=(0.2, 1),
            on_press=self.increase_counter
        )

        reset_btn = Button(
            text='Reset',
            size_hint=(0.2, 1),
            on_press=self.reset_counter
        )

        counter_layout.add_widget(self.counter_label)
        counter_layout.add_widget(minus_btn)
        counter_layout.add_widget(plus_btn)
        counter_layout.add_widget(reset_btn)

        # Action buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))

        greet_btn = Button(
            text='Say Hello',
            background_color=(0.2, 0.8, 0.2, 1),  # Green
            on_press=self.say_hello
        )

        clear_btn = Button(
            text='Clear',
            background_color=(0.8, 0.8, 0.2, 1),  # Yellow
            on_press=self.clear_form
        )

        exit_btn = Button(
            text='Exit',
            background_color=(0.8, 0.2, 0.2, 1),  # Red
            on_press=self.exit_app
        )

        button_layout.add_widget(greet_btn)
        button_layout.add_widget(clear_btn)
        button_layout.add_widget(exit_btn)

        # Status label
        self.status_label = Label(
            text='Ready',
            font_size='14sp',
            size_hint=(1, 0.15),
            color=(0.5, 0.5, 0.5, 1)  # Gray
        )

        # Add all widgets to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(name_layout)
        main_layout.add_widget(self.greeting_label)
        main_layout.add_widget(counter_layout)
        main_layout.add_widget(button_layout)
        main_layout.add_widget(self.status_label)

        # Initialize counter
        self.counter = 0

        return main_layout

    def say_hello(self, instance):
        """Handle say hello button click"""
        name = self.name_input.text.strip()
        if name:
            self.greeting_label.text = f'Hello, {name}! 👋'
            self.status_label.text = f'Greeted {name}'
        else:
            self.greeting_label.text = 'Hello, World! 🌍'
            self.status_label.text = 'Please enter a name'

    def increase_counter(self, instance):
        """Increase counter by 1"""
        self.counter += 1
        self.counter_label.text = f'Count: {self.counter}'
        self.status_label.text = f'Counter increased to {self.counter}'

    def decrease_counter(self, instance):
        """Decrease counter by 1"""
        self.counter -= 1
        self.counter_label.text = f'Count: {self.counter}'
        self.status_label.text = f'Counter decreased to {self.counter}'

    def reset_counter(self, instance):
        """Reset counter to 0"""
        self.counter = 0
        self.counter_label.text = 'Count: 0'
        self.status_label.text = 'Counter reset'

    def clear_form(self, instance):
        """Clear all form fields"""
        self.name_input.text = ''
        self.greeting_label.text = 'Hello, World!'
        self.counter = 0
        self.counter_label.text = 'Count: 0'
        self.status_label.text = 'Form cleared'

    def exit_app(self, instance):
        """Exit the application"""
        self.status_label.text = 'Goodbye!'
        self.stop()


def main():
    """Main function to run the application"""
    try:
        print("🚀 Starting Simple Kivy App...")
        print("📱 A window should open shortly")
        print("⏹️  Close the window or click 'Exit' to quit")

        app = SimpleKivyApp()
        app.run()

    except Exception as e:
        print(f"❌ Error running the application: {e}")
        print("💡 Make sure Kivy is properly installed")
        return 1

    print("👋 Application closed successfully")
    return 0


if __name__ == '__main__':
    sys.exit(main())
