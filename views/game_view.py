import arcade
from arcade.camera import Camera2D
from sprites.player import Player

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.player = None

        self.camera = Camera2D()

        self.physics_engine = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x = 100
        self.player.center_y = 100
        self.player_list.append(self.player)

        # СТЕНЫ
        self.create_walls()

        # ФИЗИКА
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.wall_list
        )

        self.center_camera_to_player()

    def create_walls(self):
        thickness = 40

        wall = arcade.SpriteSolidColor(WORLD_WIDTH, thickness, arcade.color.GRAY)
        wall.center_x = WORLD_WIDTH // 2
        wall.center_y = thickness // 2
        self.wall_list.append(wall)

        wall = arcade.SpriteSolidColor(WORLD_WIDTH, thickness, arcade.color.GRAY)
        wall.center_x = WORLD_WIDTH // 2
        wall.center_y = WORLD_HEIGHT - thickness // 2
        self.wall_list.append(wall)

        wall = arcade.SpriteSolidColor(thickness, WORLD_HEIGHT, arcade.color.GRAY)
        wall.center_x = thickness // 2
        wall.center_y = WORLD_HEIGHT // 2
        self.wall_list.append(wall)

        wall = arcade.SpriteSolidColor(thickness, WORLD_HEIGHT, arcade.color.GRAY)
        wall.center_x = WORLD_WIDTH - thickness // 2
        wall.center_y = WORLD_HEIGHT // 2
        self.wall_list.append(wall)

        for x in range(400, 1600, 200):
            wall = arcade.SpriteSolidColor(40, 200, arcade.color.RED)
            wall.center_x = x
            wall.center_y = 800
            self.wall_list.append(wall)

    def on_draw(self):
        self.clear()
        self.camera.activate()

        self.wall_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.center_camera_to_player()

    def center_camera_to_player(self):
        camera_x = self.player.center_x - SCREEN_WIDTH / 2
        camera_y = self.player.center_y - SCREEN_HEIGHT / 2

        camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))

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
