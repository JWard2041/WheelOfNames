import arcade
from titleScreen import TitleScreen

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)

    def setup(self):
        """Initial setup to show the title screen."""
        title_screen = TitleScreen()
        title_screen.setup()
        self.show_view(title_screen)

    def on_resize(self, width, height):
        """Handle window resizing."""
        super().on_resize(width, height)