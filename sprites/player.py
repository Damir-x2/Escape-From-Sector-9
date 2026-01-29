import arcade


class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(40, 40, arcade.color.BLUE)

        self.speed = 5
        self.health = 100

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y
