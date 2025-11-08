#!/usr/bin/env python3
"""
Kivy Form Application
A comprehensive form example demonstrating various Kivy widgets and form handling.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.checkbox import CheckBox
from kivy.uix.slider import Slider
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class FormApp(App):
    """Comprehensive Kivy Form Application"""

    def build(self):
        """Build the application UI"""
        # Create main layout with scroll capability
        scroll = ScrollView()
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))

        # Title
        title = Label(
            text='Kivy Registration Form',
            font_size='28sp',
            size_hint_y=None,
            height='60dp',
            color=(0.2, 0.4, 0.8, 1)
        )

        # Form container
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Name fields
        form_layout.add_widget(Label(text='First Name:', size_hint_y=None, height='40dp'))
        self.first_name = TextInput(
            multiline=False,
            size_hint_y=None,
            height='40dp',
            hint_text='Enter your first name'
        )
        form_layout.add_widget(self.first_name)

        form_layout.add_widget(Label(text='Last Name:', size_hint_y=None, height='40dp'))
        self.last_name = TextInput(
            multiline=False,
            size_hint_y=None,
            height='40dp',
            hint_text='Enter your last name'
        )
        form_layout.add_widget(self.last_name)

        # Email field
        form_layout.add_widget(Label(text='Email:', size_hint_y=None, height='40dp'))
        self.email = TextInput(
            multiline=False,
            size_hint_y=None,
            height='40dp',
            hint_text='Enter your email address'
        )
        form_layout.add_widget(self.email)

        # Age slider
        form_layout.add_widget(Label(text='Age:', size_hint_y=None, height='40dp'))
        age_container = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        self.age_slider = Slider(
            min=18,
            max=100,
            value=25,
            step=1
        )
        self.age_label = Label(text='25', size_hint_x=None, width='50dp')
        self.age_slider.bind(value=self.on_age_change)
        age_container.add_widget(self.age_slider)
        age_container.add_widget(self.age_label)
        form_layout.add_widget(age_container)

        # Country spinner
        form_layout.add_widget(Label(text='Country:', size_hint_y=None, height='40dp'))
        self.country = Spinner(
            text='Select Country',
            values=['USA', 'Canada', 'UK', 'Germany', 'France', 'Australia', 'Japan', 'Other'],
            size_hint_y=None,
            height='40dp'
        )
        form_layout.add_widget(self.country)

        # Newsletter checkbox
        form_layout.add_widget(Label(text='Newsletter:', size_hint_y=None, height='40dp'))
        checkbox_container = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        self.newsletter = CheckBox(size_hint_x=None, width='40dp')
        checkbox_container.add_widget(self.newsletter)
        checkbox_container.add_widget(Label(text='Subscribe to newsletter'))
        form_layout.add_widget(checkbox_container)

        # Comments field
        form_layout.add_widget(Label(text='Comments:', size_hint_y=None, height='40dp'))
        self.comments = TextInput(
            multiline=True,
            size_hint_y=None,
            height='80dp',
            hint_text='Enter any additional comments'
        )
        form_layout.add_widget(self.comments)

        # Button layout
        button_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height='50dp')

        # Submit button
        submit_btn = Button(
            text='Submit',
            background_color=(0.2, 0.8, 0.2, 1),
            on_press=self.submit_form
        )

        # Clear button
        clear_btn = Button(
            text='Clear',
            background_color=(0.8, 0.8, 0.2, 1),
            on_press=self.clear_form
        )

        # Exit button
        exit_btn = Button(
            text='Exit',
            background_color=(0.8, 0.2, 0.2, 1),
            on_press=self.exit_app
        )

        button_layout.add_widget(submit_btn)
        button_layout.add_widget(clear_btn)
        button_layout.add_widget(exit_btn)

        # Add all sections to main layout
        main_layout.add_widget(title)
        main_layout.add_widget(Label(size_hint_y=None, height='20dp'))  # Spacer
        main_layout.add_widget(form_layout)
        main_layout.add_widget(Label(size_hint_y=None, height='30dp'))  # Spacer
        main_layout.add_widget(button_layout)

        scroll.add_widget(main_layout)
        return scroll

    def on_age_change(self, instance, value):
        """Update age label when slider changes"""
        self.age_label.text = str(int(value))

    def submit_form(self, instance):
        """Handle form submission"""
        # Validate form
        errors = []

        if not self.first_name.text.strip():
            errors.append("First name is required")

        if not self.last_name.text.strip():
            errors.append("Last name is required")

        if not self.email.text.strip():
            errors.append("Email is required")
        elif '@' not in self.email.text:
            errors.append("Invalid email format")

        if self.country.text == 'Select Country':
            errors.append("Please select a country")

        if errors:
            self.show_popup("Validation Errors", "\n".join(errors))
            return

        # Create success message
        message = f"""Form submitted successfully!

Name: {self.first_name.text} {self.last_name.text}
Email: {self.email.text}
Age: {int(self.age_slider.value)}
Country: {self.country.text}
Newsletter: {'Yes' if self.newsletter.active else 'No'}
Comments: {self.comments.text or 'None'}"""

        self.show_popup("Success", message)

    def clear_form(self, instance):
        """Clear all form fields"""
        self.first_name.text = ''
        self.last_name.text = ''
        self.email.text = ''
        self.age_slider.value = 25
        self.country.text = 'Select Country'
        self.newsletter.active = False
        self.comments.text = ''

    def exit_app(self, instance):
        """Exit the application"""
        self.stop()

    def show_popup(self, title, message):
        """Show a popup message"""
        content = BoxLayout(orientation='vertical', padding=20, spacing=10)

        message_label = Label(
            text=message,
            text_size=(300, None),
            halign='left',
            valign='top'
        )

        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height='40dp'
        )

        content.add_widget(message_label)
        content.add_widget(close_btn)

        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.6),
            auto_dismiss=True
        )

        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    FormApp().run()
