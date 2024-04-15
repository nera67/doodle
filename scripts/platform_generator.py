from random import randint
import pygame

from scripts.constants import display_size, CreatePlatformEvent
from scripts.functions import load_image
from scripts.platform import (
    BreakingPlatform,
    DisappearingPlatform,
    MovingPlatform,
    Platform,
    SpringPlatform,
)


class PlatformGenerator:
    def __init__(self, step):
        self.step = step  # Насколько высоко должна появляться следующая платформа

        # Картинки всех платформ
        self.platform_images = [
            load_image("assets", "images", "platform.png"),
            load_image("assets", "images", "breaking-platform.png"),
            load_image("assets", "images", "platform.png"),
            load_image("assets", "images", "moving-platform.png"),
            load_image("assets", "images", "spring-platform.png"),
        ]

        self.create_start_configuration()

    def create_start_configuration(self):
        """Создание начальной конфигурации уровня"""

        # Платформа, над которой игрок появляется в начале игры
        platform = Platform(
            (display_size[0] / 2, display_size[1] - 50), self.platform_images[0]
        )
        event = pygame.Event(CreatePlatformEvent, {"platform": platform})
        pygame.event.post(event)

        for y in range(int(display_size[1] / self.step), -1, -1):
            self.create_platform(y * self.step)

    def create_platform(self, center_y):
        """Создаёт платформу"""

        number = randint(0, 4)
        image = self.platform_images[number]
        min_x = image.get_width() // 2
        max_x = display_size[0] - image.get_width() // 2
        center = (randint(min_x, max_x), center_y)

        if number == 0:
            info = {"platform": Platform(center, image)}
        elif number == 1:
            info = {"platform": BreakingPlatform(center, image)}
        elif number == 4:
            info = {"platform": SpringPlatform(center, image)}
        elif number == 2:
            info = {
                "platform": DisappearingPlatform(
                    center, image, 180 + randint(0, 100)
                )
            }
        else:
            info = {"platform": MovingPlatform(
                center, image, randint(100, 300) / 100)
            }
        event = pygame.Event(CreatePlatformEvent, info)
        pygame.event.post(event)

    def update(self, offset_y, platforms):
        """Обновляем данные"""

        # Если верхняя платформа опустилась слишком низко
        if platforms[-1].rect.centery - offset_y >= self.step:
            self.create_platform(offset_y)
        if platforms[0].rect.top - offset_y >= display_size[1]:
            platforms.remove(platforms[0])
