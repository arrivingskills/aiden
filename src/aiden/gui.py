from direct.gui.DirectGui import OnscreenText, DirectFrame, DirectButton
from panda3d.core import TextNode


class HUD:
    def __init__(self):
        self.title = OnscreenText(
            text="Shards of the Grove",
            pos=(-1.28, 0.9),
            scale=0.06,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft,
            mayChange=False,
            shadow=(0, 0, 0, 1),
        )
        self.objective = OnscreenText(
            text="",
            pos=(-1.28, 0.8),
            scale=0.05,
            fg=(1, 0.95, 0.7, 1),
            align=TextNode.ALeft,
            mayChange=True,
            shadow=(0, 0, 0, 1),
        )
        self.info = OnscreenText(
            text="",
            pos=(0, -0.9),
            scale=0.05,
            fg=(0.9, 0.9, 1, 1),
            mayChange=True,
            shadow=(0, 0, 0, 1),
        )

    def set_objective(self, text: str):
        self.objective.setText(text)

    def show_info(self, text: str):
        self.info.setText(text)


class Dialog:
    def __init__(self):
        self.root = DirectFrame(frameColor=(0, 0, 0, 0.6), frameSize=(-1.2, 1.2, -0.3, 0.3), pos=(0, 0, -0.6))
        self.root.hide()
        self.text = OnscreenText(text="", parent=self.root, pos=(-1.1, 0.15), scale=0.06, align=TextNode.ALeft,
                                 fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1), mayChange=True)
        self.btn = DirectButton(parent=self.root, text="Continue", scale=0.06, pos=(1.0, 0, -0.2),
                                command=self._on_continue)
        self._callback = None

    def say(self, text: str, on_continue=None):
        self._callback = on_continue
        self.text.setText(text)
        self.root.show()

    def _on_continue(self):
        self.root.hide()
        cb = self._callback
        self._callback = None
        if cb:
            cb()
