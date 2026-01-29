import arcade
import math


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # размеры
        self.width = 30
        self.height = 30

        # позиция
        self.center_x = 400
        self.center_y = 300

        self.speed = 2

        # направление (куда смотрит)
        self.facing_x = 1
        self.facing_y = 0

        self.health = 100

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

    def draw(self):
        angle = math.atan2(self.facing_y, self.facing_x)

        tip = (
            self.center_x + math.cos(angle) * 20,
            self.center_y + math.sin(angle) * 20
        )
        left = (
            self.center_x + math.cos(angle + 2.5) * 15,
            self.center_y + math.sin(angle + 2.5) * 15
        )
        right = (
            self.center_x + math.cos(angle - 2.5) * 15,
            self.center_y + math.sin(angle - 2.5) * 15
        )

        arcade.draw_polygon_filled(
            [tip, left, right],
            arcade.color.BLUE
        )
