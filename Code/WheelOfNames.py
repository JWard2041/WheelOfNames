import arcade

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GAME_TITLE = "Wheel of Names"

def main():
    """Main function to run the game."""
    from gameWindow import GameWindow
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
