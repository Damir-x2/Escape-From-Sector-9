import arcade


class GameView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Game Started",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.WHITE,
            font_size=30,
            anchor_x="center"
        )
