import arcade
import json
from pathlib import Path
from views.start_view import StartView

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Escape From Sector-9"
SETTINGS_PATH = Path("settings.json")
DEFAULT_SETTINGS = {
    "music_volume": 0.5,
    "sfx_volume": 0.6,
}


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.settings = self.load_settings()

    def setup(self):
        self.show_view(StartView())

    def load_settings(self):
        if not SETTINGS_PATH.exists():
            self.save_settings(DEFAULT_SETTINGS.copy())
            return DEFAULT_SETTINGS.copy()

        try:
            with SETTINGS_PATH.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            self.save_settings(DEFAULT_SETTINGS.copy())
            return DEFAULT_SETTINGS.copy()

        settings = DEFAULT_SETTINGS.copy()
        settings.update({
            "music_volume": float(data.get("music_volume", settings["music_volume"])),
            "sfx_volume": float(data.get("sfx_volume", settings["sfx_volume"])),
        })

        settings["music_volume"] = max(0.0, min(1.0, settings["music_volume"]))
        settings["sfx_volume"] = max(0.0, min(1.0, settings["sfx_volume"]))
        self.save_settings(settings)
        return settings

    def save_settings(self, settings=None):
        if settings is not None:
            self.settings = settings
        with SETTINGS_PATH.open("w", encoding="utf-8") as file:
            json.dump(self.settings, file, indent=2, ensure_ascii=False)

    def update_volume(self, key, delta):
        if key not in ("music_volume", "sfx_volume"):
            return
        new_value = max(0.0, min(1.0, self.settings[key] + delta))
        self.settings[key] = round(new_value, 2)
        self.save_settings()


def main():
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
