import arcade
from arcade.camera import Camera2D
from sprites.player import Player

WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = arcade.SpriteList()
        self.player = None
        self.camera = Camera2D()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.setup()
        self.center_camera_to_player()

    def setup(self):
        self.player_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = WORLD_WIDTH // 2
        self.player.center_y = WORLD_HEIGHT // 2

        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()

        self.camera.activate()

        arcade.draw_text(
            "GAME VIEW",
            20,
            WORLD_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

        self.player_list.draw()

    def on_update(self, delta_time):
        self.player_list.update(delta_time)

        if self.player.left < 0:
            self.player.left = 0
        if self.player.right > WORLD_WIDTH:
            self.player.right = WORLD_WIDTH

        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.top > WORLD_HEIGHT:
            self.player.top = WORLD_HEIGHT

        self.center_camera_to_player()

    def center_camera_to_player(self):
        camera_x = max(
            0,
            min(
                self.player.center_x - self.window.width / 2,
                WORLD_WIDTH - self.window.width
            )
        )

        camera_y = max(
            0,
            min(
                self.player.center_y - self.window.height / 2,
                WORLD_HEIGHT - self.window.height
            )
        )

        self.camera.position = (camera_x, camera_y)

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
