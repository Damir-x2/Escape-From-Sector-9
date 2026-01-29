import arcade


class Enemy(arcade.SpriteSolidColor):
    def __init__(self, x, y, left_bound, right_bound):
        super().__init__(40, 40, arcade.color.RED)

        self.center_x = x
        self.center_y = y

        self.change_x = 2

        self.left_bound = left_bound
        self.right_bound = right_bound

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x

        if self.left < self.left_bound or self.right > self.right_bound:
            self.change_x *= -1
