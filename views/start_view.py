import arcade
import arcade.gui

from views.game_view import GameView


class StartView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.music_label = None
        self.sfx_label = None

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

        self.music_label = arcade.gui.UILabel(
            text="Music volume: 50%",
            font_size=16,
            text_color=arcade.color.WHITE
        )
        v_box.add(self.music_label)

        music_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        music_minus = arcade.gui.UIFlatButton(text="-", width=50)
        music_plus = arcade.gui.UIFlatButton(text="+", width=50)
        music_row.add(music_minus)
        music_row.add(music_plus)
        v_box.add(music_row)

        self.sfx_label = arcade.gui.UILabel(
            text="SFX volume: 60%",
            font_size=16,
            text_color=arcade.color.WHITE
        )
        v_box.add(self.sfx_label)

        sfx_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        sfx_minus = arcade.gui.UIFlatButton(text="-", width=50)
        sfx_plus = arcade.gui.UIFlatButton(text="+", width=50)
        sfx_row.add(sfx_minus)
        sfx_row.add(sfx_plus)
        v_box.add(sfx_row)

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

        @music_minus.event("on_click")
        def decrease_music(event):
            self.window.update_volume("music_volume", -0.1)
            self.update_volume_labels()

        @music_plus.event("on_click")
        def increase_music(event):
            self.window.update_volume("music_volume", 0.1)
            self.update_volume_labels()

        @sfx_minus.event("on_click")
        def decrease_sfx(event):
            self.window.update_volume("sfx_volume", -0.1)
            self.update_volume_labels()

        @sfx_plus.event("on_click")
        def increase_sfx(event):
            self.window.update_volume("sfx_volume", 0.1)
            self.update_volume_labels()

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            v_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )

        self.manager.add(anchor)
        self.update_volume_labels()

    def update_volume_labels(self):
        settings = getattr(self.window, "settings", {})
        music_percent = int(settings.get("music_volume", 0.5) * 100)
        sfx_percent = int(settings.get("sfx_volume", 0.6) * 100)
        self.music_label.text = f"Music volume: {music_percent}%"
        self.sfx_label.text = f"SFX volume: {sfx_percent}%"


    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()
