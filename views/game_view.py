import arcade
from sprites.player import Player


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_list = arcade.SpriteList()
        self.player = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = self.window.width // 2
        self.player.center_y = self.window.height // 2

        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "GAME VIEW",
            20,
            self.window.height - 40,
            arcade.color.WHITE,
            20
        )

        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.player.speed
        elif key == arcade.key.S:
            self.player.change_y = -self.player.speed
        elif key == arcade.key.A:
            self.player.change_x = -self.player.speed
        elif key == arcade.key.D:
            self.player.change_x = self.player.speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0
        elif key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
