import pygame

class SecondPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.width = 64
        self.height = 64
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((0, 255, 0))  # Gren

        # Set the position of the rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def update(self):
        # Dummy player does not move, so no update logic is needed
        pass
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
