import pygame

class SecondPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Green color for the dummy player
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        # Dummy player does not move, so no update logic is needed
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)