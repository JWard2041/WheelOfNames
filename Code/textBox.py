import arcade

class TextBox:
    def __init__(self, x, y, width, height, font_size=16):
        """
        Initialize the TextBox.

        :param x: The x-coordinate of the center of the text box.
        :param y: The y-coordinate of the center of the text box.
        :param width: The width of the text box.
        :param height: The height of the text box.
        :param font_size: Font size for the text inside the text box.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size

        self.text = ""  # User input text
        self.active = False  # Whether the text box is active for input
        self.cursor_visible = False  # Whether the cursor is visible (for blinking)
        self.time_elapsed = 0  # Tracks time for cursor blinking
        self.caps_lock = False  # Tracks caps lock state
        self.update_data = False # Used to track if text should be sent

    def get_text(self):
        """Get the current text in the text box"""
        return self.text
    
    def can_update(self):
        """Function to determine if the data in the text box can be used (the user is done typing)"""
        temp = self.update_data
        self.update_data = False
        return temp

    def draw(self):
        """Draw the text box and its content."""
        # Draw the text box
        color = arcade.color.LIGHT_GRAY if self.active else arcade.color.GRAY
        arcade.draw_rectangle_filled(
            center_x=self.x, 
            center_y=self.y, 
            width=self.width, 
            height=self.height, 
            color=color
        )
        arcade.draw_rectangle_outline(
            center_x=self.x, 
            center_y=self.y, 
            width=self.width, 
            height=self.height, 
            color=arcade.color.BLACK, 
            border_width=2
        )

        # Draw the text inside the box
        text_object = arcade.Text(
            self.text,
            self.x - self.width // 2 + 10,  # Align text to the left inside the box
            self.y - self.font_size // 2,
            arcade.color.BLACK,
            self.font_size,
            width=self.width - 20,
            align="left",
        )
        text_object.draw()

        # Draw the blinking cursor if active
        if self.active and self.cursor_visible:
            cursor_x = text_object.x + text_object.content_width + 2  # Cursor at the end of the text
            cursor_y = text_object.y
            arcade.draw_line(cursor_x, cursor_y, cursor_x, cursor_y + self.font_size, arcade.color.BLACK, 2)

    def on_mouse_press(self, x, y):
        """
        Handle mouse clicks to activate or deactivate the text box.

        :param x: The x-coordinate of the mouse click.
        :param y: The y-coordinate of the mouse click.
        """
        if (self.x - self.width // 2 < x < self.x + self.width // 2 and
                self.y - self.height // 2 < y < self.y + self.height // 2):
            self.active = True
            self.update_data = False
        else:
            if self.active:
                self.update_data = True
            self.active = False

    def on_key_press(self, key, modifiers):
        """
        Handle key presses for text input, special keys, and modifiers.

        :param key: The key that was pressed.
        :param modifiers: Modifiers (e.g., Shift or Ctrl) that were active during the key press.
        """
        if key == arcade.key.CAPSLOCK:
            self.caps_lock = not self.caps_lock
            return

        if self.active:
            # Handle backspace
            if key == arcade.key.BACKSPACE:
                self.text = self.text[:-1]

            # Handle enter key
            elif key == arcade.key.ENTER or key == arcade.key.RETURN:
                if self.active:
                    self.update_data = True
                self.active = False

            # Handle regular keys
            elif 32 <= key <= 126:  # Printable ASCII range
                char = chr(key)

                # Handle shift and caps lock for letters
                if char.isalpha():
                    if self.caps_lock ^ (modifiers & arcade.key.MOD_SHIFT):
                        char = char.upper()
                    else:
                        char = char.lower()

                # Handle shift for special characters
                elif modifiers & arcade.key.MOD_SHIFT:
                    shift_map = {
                        "1": "!",
                        "2": "@",
                        "3": "#",
                        "4": "$",
                        "5": "%",
                        "6": "^",
                        "7": "&",
                        "8": "*",
                        "9": "(",
                        "0": ")",
                        "-": "_",
                        "=": "+",
                        "[": "{",
                        "]": "}",
                        "\\": "|",
                        ";": ":",
                        "'": "\"",
                        ",": "<",
                        ".": ">",
                        "/": "?",
                        "`": "~",
                    }
                    char = shift_map.get(char, char)  # Use shifted version if available

                # Add the character to the text
                self.text += char

    def update(self, delta_time):
        """
        Update the cursor blinking.

        :param delta_time: Time since the last update.
        """
        self.time_elapsed += delta_time
        if self.time_elapsed >= 0.5:  # Toggle visibility every 0.5 seconds
            self.cursor_visible = not self.cursor_visible
            self.time_elapsed = 0
