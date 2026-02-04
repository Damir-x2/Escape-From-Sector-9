import arcade


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        # Size and position
        self.target_size = 30
        self.center_x = 400
        self.center_y = 300

        self.speed = 2

        # Facing direction
        self.facing_x = 1
        self.facing_y = 0

        self.health = 100
        self._load_textures()
        self._apply_facing_texture()

    def _load_textures(self):
        self.texture_up = arcade.load_texture("assets/player/player_back.png")
        self.texture_down = arcade.load_texture("assets/player/player_front.png")
        self.texture_left = arcade.load_texture("assets/player/player_left.png")
        self.texture_right = arcade.load_texture("assets/player/player_right.png")

        self.scale = self.target_size / self.texture_right.width

    def _apply_facing_texture(self):
        if self.facing_y > 0:
            self.texture = self.texture_up
        elif self.facing_y < 0:
            self.texture = self.texture_down
        elif self.facing_x < 0:
            self.texture = self.texture_left
        else:
            self.texture = self.texture_right

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self._apply_facing_texture()

    def draw(self):
        arcade.draw_sprite(self)
