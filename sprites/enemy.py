import arcade
import random
import math


class Enemy(arcade.Sprite):
    def __init__(self, x, y, left, right):
        super().__init__()

        self.texture = arcade.make_soft_square_texture(
            28, arcade.color.RED, 255
        )

        self.center_x = x
        self.center_y = y

        self.health = 3
        self.dead = False

        self.speed = random.uniform(1.0, 2.5)

        self.change_x = 0
        self.change_y = 0

        self.move_timer = 0.0
        self.move_interval = random.uniform(0.8, 2.5)

        self.pick_new_direction()

    def pick_new_direction(self):
        directions = [
            (1, 0), (-1, 0),
            (0, 1), (0, -1),
            (0, 0),
        ]

        dx, dy = random.choice(directions)

        self.change_x = dx * self.speed
        self.change_y = dy * self.speed

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

    def die(self):
        self.dead = True
        self.change_x = 0
        self.change_y = 0
        self.remove_from_sprite_lists()
