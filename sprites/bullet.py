import arcade


class Bullet(arcade.Sprite):
    def __init__(self, x, y, dx, dy):
        super().__init__()

        self.texture = arcade.make_soft_circle_texture(
            8, arcade.color.YELLOW, 255
        )

        self.center_x = x
        self.center_y = y

        speed = 10
        self.change_x = dx * speed
        self.change_y = dy * speed

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
