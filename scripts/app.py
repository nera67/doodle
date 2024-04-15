import pygame

from scripts.constants import display_size, CreatePlatformEvent
from scripts.game import Game
from scripts.functions import load_image


class App:
    """Отвечает за работу окна приложения"""

    def __init__(self):
        # Свойства окна
        self.running = True  # Флаг, отвечающий за работу главного игрового цикла
        self.maxFPS = 60  # Максимальный fps

        self.display = pygame.display.set_mode(display_size)  # "Сцена", на которой будут отрисовываться все игровые объекты
        self.clock = pygame.time.Clock()  # "Часы", которые нужны для установки определённого fps
        self.game = Game()

        # Настройка окна
        pygame.display.set_caption("Doodle Jump")  # Задаём заголовок окна
        pygame.display.set_icon(load_image("assets", "icons", "icon.ico"))  # Загружаем картинку и устанавливаем как иконку окна

    def handle_events(self):
        """Обработка всех событий pygame"""

        # Перебираем все события
        for event in pygame.event.get():
            # Если окно закрывают (alt + f4 или нажимают на крестик)
            if event.type == pygame.QUIT:
                self.running = False  # Отключаем игровой цикл

            # Если нажата какая-либо клавиша
            elif event.type == pygame.KEYDOWN:
                self.game.handle_key_down_event(event.key)

            # Если отпущена какая-либо клавиша
            elif event.type == pygame.KEYUP:
                self.game.handle_key_up_event(event.key)

            # Если создаём платформу
            elif event.type == CreatePlatformEvent:
                self.game.handle_create_platform_event(event.platform)

    def update(self):
        """Обновление данных игры"""
        self.game.update()

    def render(self):
        """Отображение всех изменений на сцене"""
        self.display.fill((0, 0, 0))    # Закрашиваем предыдущий кадр сцены
        self.game.render(self.display)  # Отрисовываем все игровые объекты
        pygame.display.update()         # Отображаем все изменения, отрисованные на сцене

    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            self.clock.tick(self.maxFPS)
