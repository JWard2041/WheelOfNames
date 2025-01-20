import arcade
import math
import random
from getNames import get_names_by_date, read_names_from_file
from path import resource_path

class GameView(arcade.View):
    def __init__(self, names, colors, wheel_speed, api_url, target_date, output_file):
        super().__init__()
        self.names = names
        self.colors = [colors[i % len(colors)] for i in range(len(names))]  # Use as many colors as names
        self.color_options = colors
        self.spin_speed = None
        self.wheel_angle = 0  # Current angle of the wheel
        self.winner = None  # Winner's name (shown when the wheel stops)
        self.is_spinning = False  # Is the wheel spinning?
        self.spin_button = None
        self.update_button = None
        self.back_button = None
        self.spin_deceleration = 0.5 + 1/wheel_speed
        self.radius = None
        self.api_url = api_url
        self.target_date = target_date
        self.output_file = output_file
        self.wheel_sound = arcade.Sound(resource_path("assets/sounds/WheelOfNamesSound.wav"))
        self.celebration = arcade.Sound(resource_path("assets/sounds/CelebrationSound.wav"))
        self.sound_player = None
        self.last_angle = 0

    def on_show(self):
        self.background = arcade.load_texture(resource_path("assets/images/UT_orange_background.png"))
        arcade.set_background_color(arcade.color.ORANGE)
        self.update_radius()

    def update_radius(self):
        """Update the radius of the wheel based on screen size"""
        self.radius = min(self.window.width, self.window.height) // 3 + min(self.window.width, self.window.height) // 7

    def update_buttons(self):
        """Update positions and sizes of all buttons elements."""
        self.spin_button = self.create_button_circle(
            text="Spin",
            center_x=self.window.width // 2,
            center_y=self.window.height // 2,
            radius=self.radius * 0.1,
            fill_color=arcade.color.DARK_BLUE,
            text_color=arcade.color.WHITE, 
        )

        self.update_button = self.create_button_rect(
            text="Update",
            center_x=self.window.width // 12,
            center_y=self.window.height // 15,
            width=self.window.width // 8,
            height=self.window.height // 8,
            fill_color=arcade.color.DARK_BLUE,
            text_color=arcade.color.WHITE,
        )

        self.back_button = self.create_button_rect(
            text="Back",
            center_x=self.window.width // 11,
            center_y=self.window.height - self.window.height // 15,
            width=self.window.width // 10,
            height=self.window.height // 14,
            fill_color=arcade.color.DARK_BLUE,
            text_color=arcade.color.WHITE,
        )

    def create_button_circle(self, text, center_x, center_y, radius, fill_color, text_color):
        """Helper function to create a button."""
        return {
            "text": text,
            "center_x": center_x,
            "center_y": center_y,
            "radius": radius,
            "fill_color": fill_color,
            "text_color": text_color,
        }
    
    def create_button_rect(self, text, center_x, center_y, width, height, fill_color, text_color):
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

    def draw_button_circle(self, button, font_size):
        """Draw a button."""
        # Draw the button rectangle
        arcade.draw_circle_filled(
            center_x=button["center_x"],
            center_y=button["center_y"],
            radius=button["radius"],
            color=button["fill_color"]
        )

        # Draw the button text
        arcade.draw_text(
            text=button["text"],
            start_x=button["center_x"],
            start_y=button["center_y"],
            color=button["text_color"],
            font_size=button["radius"] // font_size,  # Font size proportional to button height
            bold=True,
            anchor_x="center",
            anchor_y="center",
        )

    def draw_button_rect(self, button, font_size):
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

    def on_draw(self):
        self.clear()

        # Draw the background image
        if self.background:
            arcade.draw_lrwh_rectangle_textured(
                0, 0, self.window.width, self.window.height, self.background
            )
        
        # Drawing the wheel
        self.update_radius()
        self.draw_wheel()
        self.draw_stopper()

        # Drawing the buttons
        self.update_buttons()
        self.draw_button_circle(self.spin_button, 2)
        self.draw_button_rect(self.update_button, 4)
        self.draw_button_rect(self.back_button, 3)

        # Display the winner if the wheel has stopped
        self.draw_winner()

    def draw_winner(self):
        """Display the winner prominently in the center of the screen"""
        
        if self.winner:
            if not self.sound_player:
                self.sound_player = arcade.play_sound(self.celebration, volume=1)

            # Draw background to make it easy to see
            arcade.draw_rectangle_filled(
                center_x=self.window.width // 2,
                center_y=self.window.height // 2,
                width= self.window.width // 2 + self.window.width // 3,
                height= self.window.height // 2,
                color=arcade.color.WHITE,
            )

            # Draw text to display winner
            arcade.draw_text(
                text="WINNER:",
                start_x=self.window.width // 2,
                start_y=self.window.height // 2 + self.window.height // 8,
                color=arcade.color.ORANGE,
                font_size=self.window.width // 12,
                bold=True,
                anchor_x="center",
                anchor_y="center",
            )
            arcade.draw_text(
                text=f"{self.winner}",
                start_x=self.window.width // 2,
                start_y=self.window.height // 2 - self.window.height // 8,
                color=arcade.color.ORANGE,
                font_size=self.window.width // 18,
                bold=True,
                anchor_x="center",
                anchor_y="center",
            )
        else:
            if self.sound_player:
                arcade.stop_sound(self.sound_player)
                self.sound_player = None

    def draw_wheel(self):
        """Function to draw the wheel with the names in each section"""
        center_x, center_y = self.window.width // 2, self.window.height // 2
        radius = self.radius 
        num_segments = len(self.names)
        angle_per_segment = 360 / num_segments

        for i, name in enumerate(self.names):
            # Calculate start and end angles for the segment
            start_angle = self.wheel_angle + i * angle_per_segment
            end_angle = start_angle + angle_per_segment

            # Draw the segment
            arcade.draw_arc_filled(
                center_x=center_x, 
                center_y=center_y, 
                width=radius * 2, 
                height=radius * 2, 
                color=self.colors[i], 
                start_angle=start_angle, 
                end_angle=end_angle,
                num_segments=1024,
            )

            # Calculate text position
            text_angle = math.radians(start_angle + angle_per_segment / 2)
            text_x = center_x + radius * 0.7 * math.cos(text_angle)
            text_y = center_y + radius * 0.7 * math.sin(text_angle)

            # Draw the name
            arcade.draw_text(
                text=name,
                start_x=text_x,
                start_y=text_y,
                color=arcade.color.BLACK,
                font_size=min(self.window.width, self.window.height) // (55+(num_segments//35)),
                anchor_x="center",
                anchor_y="center",
                rotation=start_angle + angle_per_segment / 2,
            )

    def draw_stopper(self):
        """Draw a stopper pointing toward the center of the wheel."""
        center_x = self.window.width // 2
        center_y = self.window.height // 2
        radius = self.radius

        # Stopper dimensions
        stopper_width = self.window.width // 24
        stopper_height = self.window.height // 18
        stopper_color = arcade.color.DARK_RED

        # Stopper position (to the right of the wheel)
        stopper_x = center_x + radius + stopper_width - (stopper_width // 4)
        stopper_y = center_y

        # Draw the stopper triangle
        arcade.draw_triangle_filled(
            stopper_x,
            stopper_y - stopper_height // 2,
            stopper_x,
            stopper_y + stopper_height // 2,
            stopper_x - stopper_width,
            stopper_y,
            stopper_color,
        )

    def update(self, delta_time):
        """Update the game state."""
        if self.is_spinning:
            # Update the wheel's angle
            self.wheel_angle += self.spin_speed
            self.wheel_angle %= 360

            # Gradually slow down the spinning
            if self.spin_speed > 0:
                self.spin_speed -= self.spin_deceleration * random.uniform(0.8, 1.2) * delta_time  # Adjustable deceleration

            # Play sound when a segment edge passes the stopper
            self.check_segment_passing()
            
            # Stop spinning when the speed is low enough
            if self.spin_speed <= 0:
                self.is_spinning = False
                self.spin_speed = 0

                # Determine the winner based on the wheel's final position
                angle_per_segment = 360 / len(self.names)
                winning_index = int((360 - self.wheel_angle) // angle_per_segment) % len(
                    self.names
                )
                self.winner = self.names[winning_index]

    def check_segment_passing(self):
        """Check if a segment edge passes the stopper and play a sound."""
        num_segments = len(self.names)
        angle_per_segment = 360 / num_segments
        current_angle = self.wheel_angle % 360

        # Check if the wheel passed a segment boundary
        for i in range(num_segments + 1):
            segment_edge_angle = i * angle_per_segment
            if self.last_angle < segment_edge_angle <= current_angle:
                arcade.play_sound(self.wheel_sound, volume=0.3)

        # Update last_angle
        self.last_angle = current_angle

    def start_spinning(self):
        """Start the spinning animation."""
        if not self.is_spinning:
            self.is_spinning = True
            self.spin_speed = random.uniform(5, 7)  # Initial spin speed
            self.winner = None  # Reset winner

    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse button press."""
        #reset the wheel if the pop up is clicked
        if self.reset(x, y) and self.winner != None:
            self.winner = None

        # Check if Spin button is clicked
        elif self.is_button_clicked_circle(x, y):
            self.start_spinning()  

        # Check if Back button is clicked
        elif self.is_button_clicked_rect(self.back_button, x, y):
            from settingsScreen import SettingsView
            title_view = SettingsView()
            self.window.show_view(title_view)

        #Check if update button is pressed and do logic to update
        elif self.is_button_clicked_rect(self.update_button, x, y):
            get_names_by_date(self.api_url, self.target_date, self.output_file)  
            names = read_names_from_file(resource_path("assets/names/filtered_names.txt"))
            self.names = names
            self.colors = [self.color_options[i % len(self.color_options)] for i in range(len(names))]
            self.on_draw()

    def reset(self, x, y):
        """Helper function to see if the winner pop up is pressed"""
        width = (self.window.width // 2 + self.window.width // 3)
        height = self.window.height // 2
        start_x = (self.window.width - width) / 2
        end_x = start_x + width
        start_y = (self.window.height - height) / 2
        end_y = start_y + height
        return (
            start_x <= x <= end_x and start_y <= y <= end_y
        )

    def is_button_clicked_circle(self, x, y):
        """Check if a button was clicked."""
        center_x = self.window.width // 2
        center_y = self.window.height // 2
        distance_to_center = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
        return (
            distance_to_center <= (self.radius*0.1)
        )
    
    def is_button_clicked_rect(self, button, x, y):
        """Check if a button was clicked."""
        return (
            button["center_x"] - button["width"] // 2 <= x <= button["center_x"] + button["width"] // 2
            and button["center_y"] - button["height"] // 2 <= y <= button["center_y"] + button["height"] // 2
        )