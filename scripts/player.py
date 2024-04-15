import pygame
from scripts.constants import display_size
from scripts.sprite import Sprite


class Player(Sprite):
    """Класс игрока"""

    def __init__(self, center, image, speed, jump_power, gravity):
        super().__init__(center, image)

        # Свойства игрока
        self.original_image = image.copy()
        self.jump_power = jump_power
        self.speed = speed
        self.gravity = gravity

        self.velocity_y = 0
        self.is_walking_right = False
        self.is_walking_left = False
        self.on_platform = False
        self.on_spring_platform = False

    def update(self):
        """Обновляем данные игрока"""

        # Если игрок стоит на платформе
        if self.on_platform:
            self.velocity_y = -self.jump_power
            if self.on_spring_platform:
                self.velocity_y *= 2
                self.on_spring_platform = False

        self.velocity_y = min(self.velocity_y + self.gravity, 15)  # Гравитация
        self.rect.y += self.velocity_y  # Двигаем игрока

        # Логика движения игрока
        if self.is_walking_right != self.is_walking_left:
            if self.is_walking_right:
                self.rect.x += self.speed
                self.image = self.original_image.copy()
            else:
                self.rect.x -= self.speed
                self.image = pygame.transform.flip(self.original_image, True, False)

        self.on_platform = False

        if self.rect.right < 0:
            self.rect.left = display_size[0]
        if self.rect.left > display_size[0]:
            self.rect.right = 0

    def collide_sprite(self, other):
        """Проверяем столкновене с платформой"""
        return super().collide_sprite(other) and self.velocity_y > 0

    def reset(self, center):
        """Возвращает игрока в начальное состояние"""
        super().__init__(center, self.original_image)
        self.velocity_y = 0
        self.is_walking_right = False
        self.is_walking_left = False
        self.on_platform = False
