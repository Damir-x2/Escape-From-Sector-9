import arcade
from arcade.camera import Camera2D

from sprites.player import Player
from sprites.enemy import Enemy
from sprites.bullet import Bullet
from sprites.particle import Particle


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 50

WORLD_COLS = 40
WORLD_ROWS = 30

WORLD_WIDTH = WORLD_COLS * TILE_SIZE
WORLD_HEIGHT = WORLD_ROWS * TILE_SIZE



class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()


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
        self.particle_list.clear()

        # === ИГРОК ===
        self.player = Player()
        self.player.center_x = TILE_SIZE * 1.5
        self.player.center_y = TILE_SIZE * 1.5
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
        maze = [
            "111111111111111111111111111111",
            "100000000000000000000000000001",
            "101111011111011111011111011101",
            "100001000001000001000001000001",
            "111101111101111101111101111101",
            "100000000000000000000000000001",
            "101111111111111011111111111101",
            "100000000000001000000000000001",
            "111111111111101111111111111101",
            "100000000000000000000000000001",
            "101111011111011111011111011101",
            "100001000001000001000001000001",
            "111101111101111101111101111101",
            "100000000000000000000000000001",
            "101111111111111111111111111101",
            "100000000000000000000000000001",
            "101111011111011111011111011101",
            "100001000001000001000001000001",
            "100000000000000000000000000001",
            "111111111111111111111111111111",
        ]

        for row_index, row in enumerate(maze):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    wall = arcade.SpriteSolidColor(
                        TILE_SIZE,
                        TILE_SIZE,
                        arcade.color.DARK_GRAY
                    )

                    wall.center_x = col_index * TILE_SIZE + TILE_SIZE / 2
                    wall.center_y = row_index * TILE_SIZE + TILE_SIZE / 2

                    self.wall_list.append(wall)

    def create_enemies(self):
        enemy_positions = [
            (3, 2),
            (7, 3),
            (10, 5),
            (5, 6),
            (9, 2),
        ]

        for col, row in enemy_positions:
            x = col * TILE_SIZE + TILE_SIZE / 2
            y = row * TILE_SIZE + TILE_SIZE / 2

            enemy = Enemy(
                x=x,
                y=y,
                left=x - 40,
                right=x + 40
            )

            self.enemy_list.append(enemy)


    def on_draw(self):
        self.clear()

        # === МИР (камера) ===
        with self.camera.activate():
            self.wall_list.draw()
            self.enemy_list.draw()
            self.bullet_list.draw()
            self.particle_list.draw()
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
        self.particle_list.update()
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

                    if enemy.health <= 0 and not enemy.dead:
                        enemy.die()

                        for _ in range(20):
                            particle = Particle(enemy.center_x, enemy.center_y)
                            self.particle_list.append(particle)


    def update_camera(self):
        self.camera.position = (
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2
        )


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
