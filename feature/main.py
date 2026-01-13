import arcade


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Escape From Sector-9"


# --------------------
# СТАРТОВЫЙ ЭКРАН
# --------------------
class StartView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "Escape From Sector-9",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2 + 100,
            arcade.color.WHITE,
            font_size=40,
            anchor_x="center"
        )

        arcade.draw_text(
            "Нажмите любую клавишу, чтобы начать",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.GRAY,
            font_size=20,
            anchor_x="center"
        )

    def on_key_press(self, key, modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


# --------------------
# ИГРОВОЙ ЭКРАН
# --------------------
class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player = None
        self.player_list = arcade.SpriteList()

    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.setup()

    def setup(self):
        # создание уровня
        self.player = arcade.SpriteSolidColor(
            width=40,
            height=60,
            color=arcade.color.AZURE
        )
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = 5
        elif key == arcade.key.S:
            self.player.change_y = -5
        elif key == arcade.key.A:
            self.player.change_x = -5
        elif key == arcade.key.D:
            self.player.change_x = 5

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0
        elif key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0



class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            SCREEN_TITLE
        )

    def setup(self):
        start_view = StartView()
        self.show_view(start_view)


def main():
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
