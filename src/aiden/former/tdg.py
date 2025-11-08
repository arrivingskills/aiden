# https://docs.panda3d.org/1.10/python/index
#
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectButton, OnscreenText
from panda3d.core import TextNode

class MyGame(ShowBase):
    def __init__(self):
        super().__init__()

        # Set up the game world
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add a basic UI
        self.create_ui()

    def create_ui(self):
        # Add on-screen text (like a title or game status)
        OnscreenText(
            text="Welcome to Panda3D!",
            style=1,
            fg=(1, 1, 1, 1),
            pos=(-0.9, 0.8),  # X, Y coordinates (screen space)
            scale=0.07,
            align=TextNode.ALeft,
            shadow=(0, 0, 0, 1),  # Black shadow for better readability
        )

        # Add a clickable button
        self.start_button = DirectButton(
            text=("Start Game", "Starting...", "Start?", "Disabled"),  # 4 states
            scale=0.1,
            pos=(0, 0, -0.5),  # X, Z position on the screen
            command=self.start_game,  # Function callback
            extraArgs=["Game Started!"],  # Extra arguments for the callback
        )

    def start_game(self, message):
        print(message)
        # Functionality for the start button can go here
        self.start_button["state"] = "disabled"  # Disable button after click

# Run the game
game = MyGame()
game.run()