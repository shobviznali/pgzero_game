from pgzero.actor import Actor
from abc import ABC, abstractmethod


class Animated(ABC):
    def __init__(self, image: str, start_x, start_y):
        self.image = image
        self.image = image
        self.actor = Actor(image, (start_x, start_y))
        self.start_x = start_x
        self.start_y = start_y
        self.frame_delay = 5

    @abstractmethod
    def animate(self):
        pass

    def _draw(self):
        pass


class AnimatedEnemyWalking(Animated):
    def __init__(self, image: str, start_x, start_y, walking_speed):
        super().__init__(image, start_x, start_y)
        self.walking_speed = walking_speed
        self.direction = "left"
        self.current_frame = 0
        self.walking = ['game_images/enemys/enemywalking1', 'game_images/enemys/enemywalking3']

    def animate(self):
        self.frame_delay -= 1
        if self.frame_delay == 0:
            self.current_frame = (self.current_frame + 1) % len(self.walking)
            self.actor.image = self.walking[self.current_frame]
            self.frame_delay = 5
            if self.direction == "left":
                self.actor.x -= self.walking_speed
                if self.actor.x <= self.start_x - 35:
                    self.direction = "right"
            elif self.direction == "right":
                self.actor.x += self.walking_speed
                if self.actor.x >= self.start_x + 35:
                    self.direction = "left"


class AnimatedEnemyFlying(Animated):
    def __init__(self, image: str, start_x, start_y, flying_speed):
        super().__init__(image, start_x, start_y)
        self.flying_speed = flying_speed
        self.direction = "up"
        self.current_frame = 0
        self.flying = ['game_images/enemys/enemy_flying2', 'game_images/enemys/enemy_flying3']

    def animate(self):
        self.frame_delay -= 1
        if self.frame_delay == 0:
            self.current_frame = (self.current_frame + 1) % len(self.flying)
            self.actor.image = self.flying[self.current_frame]
            self.frame_delay = 5
            if self.direction == "up":
                self.actor.y -= self.flying_speed
                if self.actor.y <= self.start_y - 35:
                    self.direction = "down"
            elif self.direction == "down":
                self.actor.y += self.flying_speed
                if self.actor.y >= self.start_y + 35:
                    self.direction = "up"
