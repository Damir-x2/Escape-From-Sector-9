import arcade
import arcade.gui

from views.game_view import GameView


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.manager.enable()
        self.manager.clear()

        v_box = arcade.gui.UIBoxLayout(space_between=20)

        title = arcade.gui.UILabel(
            text="Escape From Sector-9",
            font_size=40,
            text_color=arcade.color.WHITE
        )
        v_box.add(title)

        start_button = arcade.gui.UIFlatButton(text="Start", width=200)
        v_box.add(start_button)

        @start_button.event("on_click")
        def start_game(event):
            self.manager.disable()
            self.window.show_view(GameView())

        exit_button = arcade.gui.UIFlatButton(text="Exit", width=200)
        v_box.add(exit_button)

        @exit_button.event("on_click")
        def exit_game(event):
            arcade.close_window()

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.manager.add(anchor)


    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
