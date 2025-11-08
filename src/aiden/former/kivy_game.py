#!/usr/bin/env python3
"""
Simple Kivy Game - Catch the Dots
An interactive game demonstrating Kivy's canvas, animation, and touch handling.
"""

import random
import math
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector


class GameDot(object):
    """Represents a game dot that falls from the top"""

    def __init__(self, x, y, size=30, speed=2):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = (random.random(), random.random(), random.random(), 1)
        self.caught = False

    def update(self, dt):
        """Update dot position"""
        self.y -= self.speed * 60 * dt  # Move down

    def is_off_screen(self, screen_height):
        """Check if dot has fallen off screen"""
        return self.y + self.size < 0

    def collides_with(self, x, y, radius=20):
        """Check if dot collides with given point"""
        distance = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return distance < (self.size/2 + radius)


class GameArea(Widget):
    """Main game area widget"""

    def __init__(self, **kwargs):
        super(GameArea, self).__init__(**kwargs)

        # Game state
        self.dots = []
        self.score = 0
        self.game_running = False
        self.spawn_rate = 1.0  # seconds between spawns
        self.last_spawn = 0

        # Player cursor
        self.cursor_x = 200
        self.cursor_y = 100
        self.cursor_size = 40

        # Graphics
        self.setup_graphics()

        # Bind touch events
        self.bind(on_touch_down=self.on_touch_down)
        self.bind(on_touch_move=self.on_touch_move)

    def setup_graphics(self):
        """Setup initial graphics"""
        with self.canvas:
            # Background
            Color(0.1, 0.1, 0.2, 1)  # Dark blue background
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

            # Player cursor
            Color(1, 1, 0, 1)  # Yellow cursor
            self.cursor = Ellipse(
                pos=(self.cursor_x - self.cursor_size/2, self.cursor_y - self.cursor_size/2),
                size=(self.cursor_size, self.cursor_size)
            )

        # Bind size updates
        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        """Update graphics when widget size changes"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def start_game(self):
        """Start the game"""
        self.game_running = True
        self.score = 0
        self.dots.clear()
        self.spawn_rate = 1.0
        self.last_spawn = 0

        # Schedule game updates
        Clock.schedule_interval(self.update_game, 1/60.0)  # 60 FPS

    def stop_game(self):
        """Stop the game"""
        self.game_running = False
        Clock.unschedule(self.update_game)
        self.dots.clear()
        self.redraw()

    def update_game(self, dt):
        """Main game update loop"""
        if not self.game_running:
            return False

        # Spawn new dots
        self.last_spawn += dt
        if self.last_spawn >= self.spawn_rate:
            self.spawn_dot()
            self.last_spawn = 0

            # Increase difficulty over time
            if self.spawn_rate > 0.3:
                self.spawn_rate *= 0.99

        # Update existing dots
        for dot in self.dots[:]:  # Copy list to avoid modification during iteration
            dot.update(dt)

            # Remove dots that fell off screen
            if dot.is_off_screen(self.height):
                self.dots.remove(dot)

            # Check for collisions with cursor
            elif dot.collides_with(self.cursor_x, self.cursor_y):
                if not dot.caught:
                    dot.caught = True
                    self.score += 10
                    self.dots.remove(dot)

        # Redraw everything
        self.redraw()

        # Update parent's score display if available
        if hasattr(self.parent, 'update_score'):
            self.parent.update_score(self.score)

    def spawn_dot(self):
        """Spawn a new dot at random position"""
        if self.width > 0:
            x = random.randint(30, int(self.width - 30))
            y = self.height + 30
            size = random.randint(20, 40)
            speed = random.uniform(1.5, 3.5)

            dot = GameDot(x, y, size, speed)
            self.dots.append(dot)

    def redraw(self):
        """Redraw all game elements"""
        # Clear canvas and redraw background
        self.canvas.clear()

        with self.canvas:
            # Background
            Color(0.1, 0.1, 0.2, 1)
            Rectangle(pos=self.pos, size=self.size)

            # Draw dots
            for dot in self.dots:
                Color(*dot.color)
                Ellipse(
                    pos=(dot.x - dot.size/2, dot.y - dot.size/2),
                    size=(dot.size, dot.size)
                )

            # Draw cursor
            Color(1, 1, 0, 0.8)  # Yellow with transparency
            Ellipse(
                pos=(self.cursor_x - self.cursor_size/2, self.cursor_y - self.cursor_size/2),
                size=(self.cursor_size, self.cursor_size)
            )

            # Draw cursor outline
            Color(1, 1, 1, 1)  # White outline
            # Note: For simplicity, we'll skip the outline in this basic version

    def on_touch_down(self, touch):
        """Handle touch/click events"""
        if self.collide_point(*touch.pos):
            self.cursor_x, self.cursor_y = touch.pos
            return True
        return False

    def on_touch_move(self, touch):
        """Handle touch/mouse movement"""
        if self.collide_point(*touch.pos):
            self.cursor_x, self.cursor_y = touch.pos
            return True
        return False


class CatchTheDotsGame(BoxLayout):
    """Main game widget containing game area and UI"""

    def __init__(self, **kwargs):
        super(CatchTheDotsGame, self).__init__(**kwargs)
        self.orientation = 'vertical'

        # Score display
        self.score_label = Label(
            text='Score: 0',
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )

        # Game area
        self.game_area = GameArea()

        # Control buttons
        button_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=60,
            spacing=10,
            padding=10
        )

        self.start_btn = Button(
            text='Start Game',
            background_color=(0.2, 0.8, 0.2, 1),
            on_press=self.start_game
        )

        self.stop_btn = Button(
            text='Stop Game',
            background_color=(0.8, 0.2, 0.2, 1),
            on_press=self.stop_game,
            disabled=True
        )

        instructions_btn = Button(
            text='Instructions',
            background_color=(0.2, 0.2, 0.8, 1),
            on_press=self.show_instructions
        )

        button_layout.add_widget(self.start_btn)
        button_layout.add_widget(self.stop_btn)
        button_layout.add_widget(instructions_btn)

        # Add widgets to main layout
        self.add_widget(self.score_label)
        self.add_widget(self.game_area)
        self.add_widget(button_layout)

    def start_game(self, instance):
        """Start the game"""
        self.game_area.start_game()
        self.start_btn.disabled = True
        self.stop_btn.disabled = False
        self.score_label.text = 'Score: 0'

    def stop_game(self, instance):
        """Stop the game"""
        self.game_area.stop_game()
        self.start_btn.disabled = False
        self.stop_btn.disabled = True

    def update_score(self, score):
        """Update score display"""
        self.score_label.text = f'Score: {score}'

    def show_instructions(self, instance):
        """Show game instructions"""
        from kivy.uix.popup import Popup

        instructions = """
CATCH THE DOTS GAME

HOW TO PLAY:
• Click 'Start Game' to begin
• Move your mouse/finger to control the yellow circle
• Catch the falling colored dots by touching them
• Each dot is worth 10 points
• Game gets faster as you progress
• Click 'Stop Game' to end

TIPS:
• Stay near the middle to catch more dots
• Watch for the spawn pattern
• The game speed increases over time

Good luck and have fun!
        """

        content = BoxLayout(orientation='vertical', padding=20, spacing=10)

        instructions_label = Label(
            text=instructions,
            text_size=(400, None),
            halign='left',
            valign='top'
        )

        close_btn = Button(
            text='Close',
            size_hint_y=None,
            height=40
        )

        content.add_widget(instructions_label)
        content.add_widget(close_btn)

        popup = Popup(
            title='Game Instructions',
            content=content,
            size_hint=(0.8, 0.8)
        )

        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class CatchTheDotsApp(App):
    """Main application class"""

    def build(self):
        """Build the application"""
        self.title = "Catch the Dots - Kivy Game"
        return CatchTheDotsGame()


if __name__ == '__main__':
    CatchTheDotsApp().run()
