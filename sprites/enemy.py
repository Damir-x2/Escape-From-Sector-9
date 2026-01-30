import arcade


class Enemy(arcade.Sprite):
    def __init__(self, x, y, left, right):
        super().__init__()

        self.texture = arcade.make_soft_square_texture(
            28, arcade.color.RED, 255
        )

        self.center_x = x
        self.center_y = y

        self.left_bound = left
        self.right_bound = right

        self.change_x = 2
        self.health = 3

        self.dead = False
        self.death_timer = 0.0

    def update(self, delta_time: float = 1 / 60):
        if self.dead:
            self.death_timer += delta_time

            # анимация смерти
            self.alpha = max(0, self.alpha - 15)
            self.width *= 0.9
            self.height *= 0.9

            if self.death_timer > 0.4:
                self.remove_from_sprite_lists()
            return

        self.center_x += self.change_x

        if self.center_x < self.left_bound or self.center_x > self.right_bound:
            self.change_x *= -1

    def die(self):
        self.dead = True
        self.change_x = 0
