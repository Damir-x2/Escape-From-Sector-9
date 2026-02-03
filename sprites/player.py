import arcade


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.textures_map = {
            "front": arcade.load_texture("assets/player/player_front.png"),
            "back": arcade.load_texture("assets/player/player_back.png"),
            "right": arcade.load_texture("assets/player/player_right.png"),
            "left": arcade.load_texture(
                "assets/player/player_right.png",
                flipped_horizontally=True,
            ),
        }
        self.texture = self.textures_map["front"]
        self.scale = 0.6

        self.speed = 2

        # направление (куда смотрит)
        self.facing_x = 1
        self.facing_y = 0

        self.health = 100

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.update_texture()

    def update_texture(self):
        if self.facing_y > 0:
            self.texture = self.textures_map["back"]
        elif self.facing_y < 0:
            self.texture = self.textures_map["front"]
        elif self.facing_x > 0:
            self.texture = self.textures_map["right"]
        elif self.facing_x < 0:
            self.texture = self.textures_map["left"]
