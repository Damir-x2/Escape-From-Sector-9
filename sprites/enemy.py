import arcade
import random
import math


class Enemy(arcade.Sprite):
    def __init__(self, x, y, left, right):
        super().__init__()

        self.target_size = 45

        self.center_x = x
        self.center_y = y

        self.health = 3
        self.dead = False

        self.speed = random.uniform(1.0, 2.5)

        self.change_x = 0
        self.change_y = 0

        self.move_timer = 0.0
        self.move_interval = random.uniform(0.8, 2.5)

        self.facing_x = 1
        self.facing_y = 0

        self._load_textures()
        self._apply_facing_texture()
        self.pick_new_direction()

    def _load_textures(self):
        self.texture_up = arcade.load_texture("assets/enemies/enemie1_back.png")
        self.texture_down = arcade.load_texture("assets/enemies/enemie1_front.png")
        self.texture_left = arcade.load_texture("assets/enemies/enemie1_left.png")
        self.texture_right = arcade.load_texture("assets/enemies/enemie1_right.png")

        self.scale = self.target_size / self.texture_right.width

    def _apply_facing_texture(self):
        if self.facing_y > 0:
            self.texture = self.texture_up
        elif self.facing_y < 0:
            self.texture = self.texture_down
        elif self.facing_x < 0:
            self.texture = self.texture_left
        else:
            self.texture = self.texture_right

    def pick_new_direction(self):
        directions = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (0, 0),
        ]

        dx, dy = random.choice(directions)

        self.change_x = dx * self.speed
        self.change_y = dy * self.speed
        self.facing_x = dx
        self.facing_y = dy
        self._apply_facing_texture()

    def update(self, delta_time: float = 1 / 60):
        if self.dead:
            return

        self.move_timer += delta_time

        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            self.move_interval = random.uniform(0.8, 2.5)
            self.pick_new_direction()

        self.center_x += self.change_x
        self.center_y += self.change_y
        self._apply_facing_texture()

    def die(self):
        self.dead = True
        self.change_x = 0
        self.change_y = 0
        self.remove_from_sprite_lists()
