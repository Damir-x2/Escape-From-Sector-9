import arcade
from views.start_view import StartView

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Escape From Sector-9"


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    def setup(self):
        self.show_view(StartView())


def main():
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
