from scripts.constants import display_size
from scripts.sprite import Sprite


class Platform(Sprite):
    type = "Platform"

    def update(self):
        pass


class MovingPlatform(Platform):
    type = "MovingPlatform"

    def __init__(self, center, image, speed):
        super().__init__(center, image)
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.left < 0:
            self.speed = abs(self.speed)
        elif self.rect.right > display_size[0]:
            self.speed = -abs(self.speed)


class DisappearingPlatform(Platform):
    type = "DisappearingPlatform"

    def __init__(self, center, image, disappearance_time):
        super().__init__(center, image)
        self.player_touched = False
        self.disappearance_start_time = disappearance_time
        self.disappearance_time = disappearance_time

    def update(self):
        if self.player_touched:
            self.disappearance_time -= 1
            mult = self.disappearance_time / self.disappearance_start_time
            self.image.set_alpha(int(255 * mult))


class BreakingPlatform(Platform):
    type = "BreakingPlatform"


class SpringPlatform(Platform):
    type = "SpringPlatform"
