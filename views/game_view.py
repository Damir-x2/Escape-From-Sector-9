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



class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.particle_list = arcade.SpriteList()
        self.floor_list = arcade.SpriteList()

        self.camera_lock_x = False
        self.camera_lock_y = False

        self.last_player_x = 0
        self.last_player_y = 0  
        self.is_dead = False
        self.enemy_physics = []

        self.player: Player | None = None
        self.camera = Camera2D()

        self.physics_engine = None

        self.music = None

        self.shoot_sound = arcade.load_sound("assets/sounds/shoot.wav")
        self.player_die_sound = arcade.load_sound("assets/sounds/player_die.wav")
        self.enemy_die_sound = arcade.load_sound("assets/sounds/enemy_die.wav")
        self.music = arcade.Sound("assets/sounds/music.ogg", streaming=True)
        self.music_player = None



    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.setup()

    def setup(self):
        self.player_list.clear()
        self.enemy_list.clear()
        self.wall_list.clear()
        self.floor_list.clear()
        self.bullet_list.clear()
        self.particle_list.clear()

        self.floor_texture = arcade.load_texture("assets/tiles/floor.png")
        self.wall_texture = arcade.load_texture("assets/tiles/wall2.png")

        # === ИГРОК ===
        self.player = Player()
        self.player.center_x = TILE_SIZE * 1.5
        self.player.center_y = TILE_SIZE * 1.5
        self.player_list.append(self.player)
        self.camera_lock_x = False
        self.camera_lock_y = False

        self.last_player_x = self.player.center_x
        self.last_player_y = self.player.center_y
        self.camera_offset_x = SCREEN_WIDTH / 2
        self.camera_offset_y = SCREEN_HEIGHT / 2




        # === СТЕНЫ И ПОЛ ===
        self.create_walls()
        self.floor_texture = arcade.load_texture("assets/tiles/floor.png")
        self.wall_texture = arcade.load_texture("assets/tiles/wall.png")

        # === ВРАГИ ===
        self.create_enemies()

        # === ФИЗИКА ===
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player,
            self.wall_list
        )
        self.enemy_physics = [
            arcade.PhysicsEngineSimple(enemy, self.wall_list)
            for enemy in self.enemy_list
        ]
        # === ЗВУКИ ===
        self.music_player = self.music.play(
            volume=1,
            loop=True
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

        scale = TILE_SIZE / self.floor_texture.width

        for row_index, row in enumerate(maze):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE + TILE_SIZE / 2
                y = row_index * TILE_SIZE + TILE_SIZE / 2

                # === ПОЛ ===
                floor = arcade.Sprite()
                floor.texture = self.floor_texture
                floor.scale = scale
                floor.center_x = x
                floor.center_y = y
                self.floor_list.append(floor)

                # === СТЕНА ===
                if cell == "1":
                    wall = arcade.Sprite()
                    wall.texture = self.wall_texture
                    wall.scale = scale
                    wall.center_x = x
                    wall.center_y = y
                    self.wall_list.append(wall)
                        
    def create_enemies(self):
        # Столбец, строка
        enemy_positions = [
            # Столбец, строка
            (2, 1), (5, 11), (23, 1), (26, 1),

            (9, 3), (12, 3), (15, 3), (18, 3), (21, 3), (24, 3),

            (2, 5), (5, 5), (8, 5), (11, 5),(26, 5),

            (3, 7), (7, 7), (11, 7), (15, 7), (19, 7), (23, 7),

            (2, 9), (20, 9), (23, 9), (26, 9),

            (3, 11), (6, 11), (9, 11), (12, 11), (24, 11),

            (2, 13), (6, 13), (10, 13), (14, 13), (18, 13), (22, 13), (26, 13),

            (11, 15), (15, 15), (19, 15), (23, 15),

            (5, 17), (10, 17),
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
        if self.is_dead:
            arcade.draw_text(
                "YOU DIED",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 + 20,
                arcade.color.RED,
                40,
                anchor_x="center"
            )

            arcade.draw_text(
                "Returning to menu...",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2 - 30,
                arcade.color.GRAY_BLUE,
                20,
                anchor_x="center"
            )
            return

        with self.camera.activate():
            self.floor_list.draw()
            self.wall_list.draw()
            self.enemy_list.draw()
            self.bullet_list.draw()
            self.particle_list.draw()
            self.player.draw()
        arcade.draw_text(
            f"HP: {self.player.health}",
            10,
            SCREEN_HEIGHT - 30,
            arcade.color.PALATINATE_PURPLE,
            20
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

        for engine in self.enemy_physics:
            engine.update()
        
        if self.is_dead:
            self.death_timer += delta_time

            if self.death_timer >= 5:
                from views.start_view import StartView
                self.window.show_view(StartView())
            return

        if not self.is_dead and self.player.health <= 0:
            self.is_dead = True
            self.death_timer = 0

            arcade.stop_sound(self.music_player)
            arcade.play_sound(self.player_die_sound, volume=3)

            self.player.change_x = 0
            self.player.change_y = 0


        self.update_camera()



    def check_enemy_collision(self):
        for enemy in self.enemy_list:
            if arcade.check_for_collision(self.player, enemy):
                self.player.health -= 1





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
                        arcade.play_sound(self.enemy_die_sound, volume=9)

                        for _ in range(20):
                            particle = Particle(enemy.center_x, enemy.center_y)
                            self.particle_list.append(particle)

            if arcade.check_for_collision_with_list(bullet, self.wall_list):
                bullet.remove_from_sprite_lists()


    def update_camera(self):
        cam_x, cam_y = self.camera.position
        
        cam_center_x = 600
        cam_center_y = 360

        if not self.camera_lock_x:
            if self.player.center_x >= cam_center_x:
                cam_x = cam_center_x
                self.camera_lock_x = True
                self.last_player_x = self.player.center_x
        else:
            dx = self.player.center_x - self.last_player_x
            cam_x += dx
            self.last_player_x = self.player.center_x

        if not self.camera_lock_y:
            if self.player.center_y >= cam_center_y:
                cam_y = cam_center_y
                self.camera_lock_y = True
                self.last_player_y = self.player.center_y
        else:
            dy = self.player.center_y - self.last_player_y
            cam_y += dy
            self.last_player_y = self.player.center_y


        self.camera.position = (cam_x, cam_y)



    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y,
                self.player.facing_x,
                self.player.facing_y
            )
            self.bullet_list.append(bullet)
            bullet = Bullet(
                self.player.center_x,
                self.player.center_y,
                self.player.facing_x,
                self.player.facing_y
            )
            self.bullet_list.append(bullet)

            arcade.play_sound(self.shoot_sound, volume=0.6)


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
