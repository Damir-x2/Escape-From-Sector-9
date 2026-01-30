import arcade
import random
import math


class Particle(arcade.SpriteCircle):
    def __init__(self, x, y):
        radius = random.randint(2, 4)
        color = arcade.color.ORANGE_RED

        super().__init__(radius, color)

        self.center_x = x
        self.center_y = y

        angle = random.uniform(0, math.tau)
        speed = random.uniform(2, 6)

        self.change_x = math.cos(angle) * speed
        self.change_y = math.sin(angle) * speed

        self.life = 30

    def update(self, delta_time: float = 1/60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.life -= 1
        self.alpha = int(255 * (self.life / 30))

        if self.life <= 0:
            self.remove_from_sprite_lists()
