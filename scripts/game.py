import pygame

from scripts.constants import display_size
from scripts.functions import load_image, get_path
from scripts.platform_generator import PlatformGenerator
from scripts.player import Player


class Game:
    """Отвечает за хранение информации об игре, обновлении всех игровых объектов и их отрисовку"""

    def __init__(self):
        self.background_image = load_image(
            "assets", "images", "background.png"
        )  # Загружаем задний фон
        self.platform_generator = PlatformGenerator(200)

        # Загружаем звуки
        self.jump_sound = pygame.mixer.Sound(
            get_path("assets", "sounds", "jump.mp3")
        )
        self.fallig_sound = pygame.mixer.Sound(
            get_path("assets", "sounds", "falling.mp3")
        )
        self.breaking_sound = pygame.mixer.Sound(
            get_path("assets", "sounds", "platform-break.mp3")
        )
        self.breaking_sound.set_volume(0.5) # Не обязательно

        # Загружаем музыку
        pygame.mixer.music.load(get_path("assets", "music", "caves.mp3"))
        pygame.mixer.music.play(- 1)
        pygame.mixer.music.set_volume(0.4)

        self.offset_y = 0
        self.player = Player(
            (240, 600), load_image("assets", "images", "player.png"), 5, 20, 0.65
        )

        self.losed = False
        self.font = pygame.Font(get_path("assets", "fonts", "pixel.ttf"), 32)
        self.platforms = list()

    def restart(self):
        """Перезапускает игру"""
        self.player.reset((240, 600))
        self.losed = False
        self.offset_y = 0
        self.platforms = list()
        self.platform_generator.create_start_configuration()
        self.fallig_sound.stop()

    def handle_key_down_event(self, key):
        """Обрабатываем нажатие клавиш"""
        if self.losed:
            self.restart()

        elif key == pygame.K_a:
            self.player.is_walking_left = True
        elif key == pygame.K_d:
            self.player.is_walking_right = True

    def handle_key_up_event(self, key):
        """Обрабатываем отпускание клавиш"""
        if key == pygame.K_a:
            self.player.is_walking_left = False
        elif key == pygame.K_d:
            self.player.is_walking_right = False

    def handle_create_platform_event(self, platform):
        """Добавляем платформу в список"""
        self.platforms.append(platform)

    def update(self):
        """Обновленяем данные игры"""
        prev_losed = self.losed
        self.losed = (
            self.player.rect.top - self.offset_y >= display_size[1]
        )  # Выпал ли игрок

        if not prev_losed and self.losed:
            self.fallig_sound.play()

        if self.losed:
            return

        self.player.update()

        for platform in self.platforms.copy():
            platform.update()
            if self.player.collide_sprite(platform):
                self.player.on_platform = True
                self.jump_sound.play()

                if platform.type == "BreakingPlatform":
                    self.platforms.remove(platform)
                    self.breaking_sound.play()
                elif platform.type == "DisappearingPlatform":
                    platform.player_touched = True
                elif platform.type == "SpringPlatform":
                    self.player.on_spring_platform = True

            if (platform.type == "DisappearingPlatform"
                and platform.disappearance_time <= 0):
                self.platforms.remove(platform)

        if self.player.rect.bottom - self.offset_y < display_size[1] / 3:
            self.offset_y = self.player.rect.bottom - display_size[1] / 3
        if self.platforms:
            self.platform_generator.update(self.offset_y, self.platforms)

    def render(self, surface):
        """Отрисовываем каждый игровой объект"""
        surface.blit(self.background_image, (0, 0))  # Отрисовываем задний фон

        for platform in self.platforms:
            platform.render(surface, self.offset_y)
        self.player.render(surface, self.offset_y)

        score = round(-self.offset_y / 10)

        if self.losed:
            score_text = self.font.render(f"Ваш рекорд: {score}", True, (1, 1, 1))
            hint_text = self.font.render("Нажмите любую клавишу", True, (1, 1, 1))

            score_rect = score_text.get_rect(
                centerx=display_size[0] / 2, centery=display_size[1] / 2 - 25
            )
            hint_rect = hint_text.get_rect(
                centerx=display_size[0] / 2, centery=display_size[1] / 2 + 25
            )

            surface.blit(score_text, score_rect)
            surface.blit(hint_text, hint_rect)

        else:
            text = self.font.render(str(score), True, (1, 1, 1))
            surface.blit(text, text.get_rect(midtop=(display_size[0] / 2, 10)))
