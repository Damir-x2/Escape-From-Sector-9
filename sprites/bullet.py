import arcade


class Bullet(arcade.SpriteSolidColor):
    def __init__(self, x, y, dx, dy):
        super().__init__(10, 10, arcade.color.YELLOW)

        self.center_x = x
        self.center_y = y

        self.change_x = dx * 10
        self.change_y = dy * 10

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
