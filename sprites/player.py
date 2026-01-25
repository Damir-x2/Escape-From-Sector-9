import arcade


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.texture = arcade.make_soft_square_texture(
            48,
            arcade.color.AZURE,
            255
        )
        self.speed = 5

    def update(self, delta_time: float = 0):
        self.center_x += self.change_x
        self.center_y += self.change_y

