import json


class LevelManager:
    def __init__(self, level_files):
        self.levels = [self.load_level(file) for file in level_files]
        self.current_level_index = 0

    def load_level(self, file):
        with open(file, 'r') as f:
            return json.load(f)

    def switch_level(self):
        self.current_level_index = (self.current_level_index + 1) % len(self.levels)

    def get_current_level(self):
        return self.levels[self.current_level_index]

