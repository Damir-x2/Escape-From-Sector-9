import arcade


class Player(arcade.SpriteSolidColor):
    def __init__(self):
        super().__init__(40, 40, arcade.color.BLUE)

        self.speed = 5
        self.health = 100

        self.facing_x = 1
        self.facing_y = 0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x != 0 or self.change_y != 0:
            self.facing_x = self.change_x
            self.facing_y = self.change_y
