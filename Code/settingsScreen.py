import arcade
from getNames import get_names_by_date, read_names_from_file
from textBox import TextBox
from path import resource_path

class SettingsView(arcade.View):
    def __init__(self):
        super().__init__()
        self.names = []
        self.colors = [arcade.color.RED, arcade.color.BLUE, arcade.color.GREEN, arcade.color.YELLOW]
        self.wheel_speed = 1
        self.input_mode = "file" 
        self.play_button = None
        self.back_button = None
        self.update_button = None
        self.slider = None   
        self.slider_line = None 
        self.dragging = False
        self.text_box = TextBox(
            x=self.window.width // 12 + min(self.window.width // 6, 400) + self.window.width // 65,
            y=self.window.height - 6*(self.window.height // 9),
            width= min(self.window.width // 6, 400),
            height= self.window.width // 28,
            font_size= min(self.window.width // 65, 24)
        )
        self.target_date = None
        self.api_url = "https://script.google.com/macros/s/AKfycbxX4pt9eTWr7yEDzf-vLy0Uyecyaj4U-NiC2dNK6F1OO3LjCrL1Rro5r2PBcJrS4PtMsg/exec"
        self.output_file = resource_path("assets/names/filtered_names.txt")

    def on_show(self):
        self.background = arcade.load_texture(resource_path("assets/images/background.jpg"))
        arcade.set_background_color(arcade.color.SKY_BLUE)  # Fallback background

    def update_buttons(self):
        """Update positions and sizes of all button elements."""
        self.play_button = self.create_button(
            text="Play",
            center_x=self.window.width // 2,
            center_y=self.window.height // 10, 
            width=self.window.width // 4,
            height=self.window.height // 8,
            fill_color=arcade.color.DARK_BLUE,
            text_color=arcade.color.WHITE, 
        )

        self.back_button = self.create_button(
            text="Back",
            center_x=self.window.width // 11,
            center_y=self.window.height - self.window.height // 15,
            width=self.window.width // 10,
            height=self.window.height // 14,
            fill_color=arcade.color.DARK_BLUE,
            text_color=arcade.color.WHITE,
        )

        self.update_button = self.create_button(
            text="Update Names",
            center_x=self.window.width // 2,
            center_y=self.window.height // 2 - self.window.height // 40,
            width=self.window.width // 4 + self.window.width // 9,
            height=self.window.height // 10,
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
    
    def draw_button(self, button, font_size):
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
            font_size=button["height"] // font_size,  # Font size proportional to button height
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )

    def create_slider_line(self, x_start, x_end, y):
        """Helper function to create the slider."""
        return {
            "x_start": x_start,
            "x_end": x_end,
            "y": y,
        }
    
    def update_slider_line(self):
        """Helper function to update slider elements"""
        self.slider_line = self.create_slider_line(
            x_start= self.window.width // 10,
            x_end= self.window.width - self.window.width // 10,
            y= self.window.height - 3*(self.window.height // 10),
        )

    def create_slider(self, x_start, x_end, y, knob_x, knob_y, knob_radius, range):
        """Helper function to create the slider"""
        return {
            "x_start": x_start,
            "x_end": x_end,
            "y": y,
            "knob_x": knob_x,
            "knob_y": knob_y,
            "knob_radius": knob_radius,
            "range": range,
        }


    def update_slider(self):
        """Update positions and sizes of slider elements."""
        self.update_slider_line()
        self.slider = self.create_slider(
            x_start= self.slider_line["x_start"],
            x_end= self.slider_line["x_end"], 
            y= self.slider_line["y"],
            knob_x= self.slider_line["x_start"] + ((self.wheel_speed - 1) * ((self.slider_line["x_end"] - self.slider_line["x_start"]) / 9)),
            knob_y= self.slider_line["y"],
            knob_radius= self.window.height // 50,
            range= self.slider_line["x_end"] - self.slider_line["x_start"],
        )


    def draw_slider(self, slider):
        """Function to draw the slider"""

        # Draw the slider track
        arcade.draw_line(
            start_x=slider["x_start"], 
            start_y=slider["y"], 
            end_x=slider["x_end"], 
            end_y=slider["y"], 
            color=arcade.color.GRAY, 
            line_width=4,
        )

        # Draw the slider knob
        arcade.draw_circle_filled(
            center_x=slider["knob_x"], 
            center_y=slider["knob_y"], 
            radius=slider["knob_radius"], 
            color=arcade.color.BLUE,
        )

        # Draw the numbers below the slider
        for i in range(1, 11):
            position_x = slider["x_start"] + ((i - 1) * (slider["range"] / 9))
            arcade.draw_text(
                text=str(i), 
                start_x=position_x - self.window.width // 225, 
                start_y=slider["y"] - self.window.height // 20, 
                color=arcade.color.BLACK, 
                font_size=self.window.height // 46,
            )

        # Display the current value above the knob
        arcade.draw_text(
            text=str(self.wheel_speed), 
            start_x=slider["knob_x"] - self.window.width // 225, 
            start_y=slider["y"] + self.window.height // 35, 
            color=arcade.color.BLACK, 
            font_size=self.window.height // 46,
            bold=True,
        )

    def update_text_box(self):
        self.text_box = TextBox(
            x=self.window.width // 12 + min(self.window.width // 6, 400) + self.window.width // 65,
            y=self.window.height - 6*(self.window.height // 9),
            width= min(self.window.width // 6, 400),
            height= self.window.width // 28,
            font_size= min(self.window.width // 65, 24)
        )

    def on_draw(self):
        self.clear()

        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, self.window.width, self.window.height, self.background
            )

        # Draw the title
        arcade.draw_text(
            text="Settings", 
            start_x=self.window.width // 2, 
            start_y=self.window.height - self.window.height // 8, 
            color=arcade.color.BLACK, 
            font_size=self.window.height // 16,
            bold=True, 
            anchor_x="center",
        )
        
        # Draw first setting (Wheel speed)
        arcade.draw_text(
            text="Wheel Speed: ", 
            start_x=self.window.width // 12, 
            start_y=self.window.height - 2*(self.window.height // 9), 
            color=arcade.color.BLACK, 
            font_size=self.window.height // 30,
            bold=True,
        )
        self.update_slider()
        self.draw_slider(self.slider)

        # Draw the second setting (input of names)
        arcade.draw_text(
            text="Input Names Mode: {}".format(self.input_mode), 
            start_x=self.window.width // 12, 
            start_y=self.window.height - 4*(self.window.height // 9), 
            color=arcade.color.BLACK, 
            font_size=self.window.height // 30,
            bold=True,
        )

        # Draw Date input
        arcade.draw_text(
            text="Date: ", 
            start_x=self.window.width // 12, 
            start_y=self.window.height - 6*(self.window.height // 9), 
            color=arcade.color.BLACK, 
            font_size=self.window.height // 30,
            bold=True,
            anchor_y="center"
        )
        self.text_box.draw()

        #Draw buttons
        self.update_buttons()
        self.draw_button(self.play_button, 2)
        self.draw_button(self.back_button, 3)
        if (self.input_mode == "file"):
            self.draw_button(self.update_button, 3)

    def on_resize(self, width, height):
         self.update_text_box() 

    def on_key_press(self, key, modifiers):
        self.text_box.on_key_press(key, modifiers) # Update text box as user is typing

    def on_update(self, delta_time):
        self.text_box.update(delta_time) # Update the text box

        # Update the target date when the user is done typing
        if self.text_box.can_update():
            self.target_date = self.text_box.get_text()

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button press."""
        # Check if Text box is clicked
        self.text_box.on_mouse_press(x, y)

        # Check if the click is within the knob
        if (self.slider["knob_x"] - self.slider["knob_radius"] <= x <= self.slider["knob_x"] + self.slider["knob_radius"] and
                self.slider["knob_y"] - self.slider["knob_radius"] <= y <= self.slider["knob_y"] + self.slider["knob_radius"]):
            self.dragging = True

        # Check if Play button is clicked
        if self.is_button_clicked(self.play_button, x, y):
            if self.input_mode == "file":
                self.names = read_names_from_file(resource_path("assets/names/filtered_names.txt"))
            from wheelScreen import GameView  
            game_view = GameView(self.names, self.colors, self.wheel_speed, self.api_url, self.target_date, self.output_file)
            self.window.show_view(game_view)

        # Check if Back button is clicked
        elif self.is_button_clicked(self.back_button, x, y):
            from titleScreen import TitleScreen
            title_view = TitleScreen()
            self.window.show_view(title_view)

        # Check if Update Names button is clicked
        elif self.is_button_clicked(self.update_button, x, y):
            get_names_by_date(self.api_url, self.target_date, self.output_file)

    def is_button_clicked(self, button, x, y):
        """Check if a button was clicked."""
        return (
            button["center_x"] - button["width"] // 2 <= x <= button["center_x"] + button["width"] // 2
            and button["center_y"] - button["height"] // 2 <= y <= button["center_y"] + button["height"] // 2
        )

    def on_mouse_release(self, x, y, button, modifiers):
        self.dragging = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self.dragging:
            # Update the knob's x position, constrained to the slider range
            raw_x = max(self.slider["x_start"], min(self.slider["x_end"], x))

            # Snap the knob to the nearest whole number increment
            normalized_position = (raw_x - self.slider["x_start"]) / self.slider["range"]
            self.wheel_speed = round(1 + normalized_position * 9)  # Map to range 1-10 
            