import arcade
import arcade.gui

from views.game_view import GameView


class StartView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = arcade.gui.UIManager()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.manager.enable()

        v_box = arcade.gui.UIBoxLayout(space_between=20)

        title = arcade.gui.UILabel(
            text="Escape From Sector-9",
            font_size=40,
            text_color=arcade.color.WHITE,
            align="center"
        )
        v_box.add(title)

        start_button = arcade.gui.UIFlatButton(text="Start", width=200)
        v_box.add(start_button)

        @start_button.event("on_click")
        def on_start_click(event):
            game_view = GameView()
            self.window.show_view(game_view)
            self.manager.disable()

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        v_box.add(exit_button)

        @exit_button.event("on_click")
        def on_exit_click(event):
            arcade.close_window()

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=v_box
            )
        )

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
