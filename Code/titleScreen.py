import arcade
from path import resource_path

class TitleScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.play_button = None
        self.quit_button = None

    def setup(self):
        """Set up the game variables."""
        # Load the background image
        self.background = arcade.load_texture(resource_path("assets/images/background.jpg"))
        arcade.set_background_color(arcade.color.SKY_BLUE)  # Fallback background
        self.update_buttons()

    def update_buttons(self):
        """Update positions and sizes of all button elements."""
        self.play_button = self.create_button(
            text="Play",
            center_x=self.window.width // 2,
            center_y=self.window.height // 2, #+ self.window.height // 24,
            width=self.window.width // 4,
            height=self.window.height // 12,
            fill_color=arcade.color.DARK_BLUE,
            text_color=arcade.color.WHITE, 
        )
        
        self.quit_button = self.create_button(
            text="Quit",
            center_x=self.window.width // 2,
            center_y=self.window.height // 2 - self.window.height // 8,
            width=self.window.width // 4,
            height=self.window.height // 12,
            fill_color=arcade.color.DARK_BLUE,
            text_color=arcade.color.WHITE,
        )

    def create_button(self, text, center_x, center_y, width, height, fill_color, text_color):
        """Helper function to create a button."""
        return {
            "text": text,
            "center_x": center_x,
            "center_y": center_y,
            "width": width,
            "height": height,
            "fill_color": fill_color,
            "text_color": text_color,
        }

    def draw_button(self, button):
        """Draw a button."""
        # Draw the button rectangle
        arcade.draw_rectangle_filled(
            center_x=button["center_x"],
            center_y=button["center_y"],
            width=button["width"],
            height=button["height"],
            color=button["fill_color"],
        )
        # Draw the button text
        arcade.draw_text(
            text=button["text"],
            start_x=button["center_x"],
            start_y=button["center_y"],
            color=button["text_color"],
            font_size=button["height"] // 3,  # Font size proportional to button height
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )

    def on_show(self):
        self.background = arcade.load_texture(resource_path("assets/images/background.jpg"))
        arcade.set_background_color(arcade.color.SKY_BLUE)  # Fallback background

    def on_draw(self):
        """Render the screen."""
        self.clear()
        arcade.start_render()

        # Draw the background image
        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, self.window.width, self.window.height, self.background
            )

        # Draw title
        arcade.draw_text(
            text="Wheel of Names",
            start_x=self.window.width // 2,
            start_y=self.window.height - self.window.height // 4,
            color=arcade.color.DARK_BLUE,
            font_size=self.window.height // 15,  # Scale font size with height
            bold=True,
            anchor_x="center",
        )

        # Draw subtitle
        arcade.draw_text(
            text="Who will be picked?",
            start_x=self.window.width // 2,
            start_y=self.window.height - self.window.height // 3,
            color=arcade.color.DARK_BLUE,
            font_size=self.window.height // 30,  # Scale font size with height
            anchor_x="center",
        )
 
        # Draw buttons
        self.update_buttons()
        self.draw_button(self.play_button)
        self.draw_button(self.quit_button)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button press."""
        # Check if Play button is clicked
        if self.is_button_clicked(self.play_button, x, y):
            from settingsScreen import SettingsView
            settings_view = SettingsView()
            self.window.show_view(settings_view)

        # Check if Quit button is clicked
        elif self.is_button_clicked(self.quit_button, x, y):
            arcade.close_window()

    def is_button_clicked(self, button, x, y):
        """Check if a button was clicked."""
        return (
            button["center_x"] - button["width"] // 2 <= x <= button["center_x"] + button["width"] // 2
            and button["center_y"] - button["height"] // 2 <= y <= button["center_y"] + button["height"] // 2
        )