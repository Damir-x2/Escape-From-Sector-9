import arcade
from arcade.camera import Camera2D

from sprites.player import Player
from sprites.enemy import Enemy
from sprites.bullet import Bullet


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

WORLD_WIDTH = 2000
WORLD_HEIGHT = 2000


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        self.player: Player | None = None
        self.camera = Camera2D()

        self.physics_engine = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_GRAY)
        self.setup()

    def setup(self):
        self.player_list.clear()
        self.enemy_list.clear()
        self.wall_list.clear()
        self.bullet_list.clear()

        # === ИГРОК ===
        self.player = Player()
        self.player.center_x = 200
        self.player.center_y = 200
        self.player_list.append(self.player)

        # === СТЕНЫ ===
        self.create_walls()

        # === ВРАГИ ===
        self.create_enemies()

        # === ФИЗИКА ===
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.wall_list
        )

        self.update_camera()

    def create_walls(self):
        thickness = 40

        walls = [
            (WORLD_WIDTH, thickness, WORLD_WIDTH // 2, thickness // 2),
            (WORLD_WIDTH, thickness, WORLD_WIDTH // 2, WORLD_HEIGHT - thickness // 2),
            (thickness, WORLD_HEIGHT, thickness // 2, WORLD_HEIGHT // 2),
            (thickness, WORLD_HEIGHT, WORLD_WIDTH - thickness // 2, WORLD_HEIGHT // 2),
        ]

        for w, h, x, y in walls:
            wall = arcade.SpriteSolidColor(w, h, arcade.color.GRAY)
            wall.center_x = x
            wall.center_y = y
            self.wall_list.append(wall)

    def create_enemies(self):
        positions = [
            (600, 400, 500, 900),
            (1200, 700, 1100, 1500),
            (900, 1200, 800, 1200),
        ]

        for x, y, left, right in positions:
            enemy = Enemy(x, y, left, right)
            self.enemy_list.append(enemy)

    def on_draw(self):
        self.clear()

        # === МИР (камера) ===
        with self.camera.activate():
            self.wall_list.draw()
            self.enemy_list.draw()
            self.bullet_list.draw()
            self.player.draw()

        # === UI (БЕЗ камеры) ===
        arcade.draw_text(
            f"HP: {self.player.health}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.RED,
            16
        )


    def on_update(self, delta_time):
        self.player.update()
        self.bullet_list.update(delta_time)
        self.enemy_list.update(delta_time)

        if self.physics_engine:
            self.physics_engine.update()

        self.check_enemy_collision()
        self.check_bullet_hits()
        self.update_camera()



    def check_enemy_collision(self):
        for enemy in self.enemy_list:
            if arcade.check_for_collision(self.player, enemy):
                self.player.health -= 1
                print("HIT! HP =", self.player.health)





    def check_bullet_hits(self):
        for bullet in self.bullet_list:
            hit_list = arcade.check_for_collision_with_list(
                bullet,
                self.enemy_list
            )

            if hit_list:
                bullet.remove_from_sprite_lists()
                for enemy in hit_list:
                    enemy.health -= 1
                    if enemy.health <= 0:
                        enemy.remove_from_sprite_lists()

    def update_camera(self):
        camera_x = self.player.center_x - SCREEN_WIDTH / 2
        camera_y = self.player.center_y - SCREEN_HEIGHT / 2

        camera_x = max(0, min(camera_x, WORLD_WIDTH - SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))

        self.camera.position = (camera_x, camera_y)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y,
                self.player.facing_x,
                self.player.facing_y
            )
            self.bullet_list.append(bullet)

        elif key == arcade.key.W:
            self.player.change_y = self.player.speed
            self.player.facing_x = 0
            self.player.facing_y = 1

        elif key == arcade.key.S:
            self.player.change_y = -self.player.speed
            self.player.facing_x = 0
            self.player.facing_y = -1

        elif key == arcade.key.A:
            self.player.change_x = -self.player.speed
            self.player.facing_x = -1
            self.player.facing_y = 0

        elif key == arcade.key.D:
            self.player.change_x = self.player.speed
            self.player.facing_x = 1
            self.player.facing_y = 0

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0
        elif key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
