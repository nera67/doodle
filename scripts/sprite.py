class Sprite:
    """Класс-родитель для всех игровых объектов на сцене."""

    def __init__(self, center, image):
        # Свойства спрайта
        self.image = image.copy()
        self.rect = self.image.get_frect()
        self.rect.center = center

    def render(self, surface, offset_y):
        """Отобразить кратинку спрайта"""
        rect = self.rect.move(0, -offset_y)
        surface.blit(self.image, rect)

    def collide_sprite(self, other):
        """Сталкивается ли текущий спрайт с другим спрайтом"""
        return self.rect.colliderect(other.rect)
