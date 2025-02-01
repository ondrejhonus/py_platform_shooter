import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_pos, mouse_pos):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = player_pos

        # Calculate the direction
        self.direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(player_pos)
        self.direction = self.direction.normalize()

        self.speed = 10

    def update(self):
        # Move the bullet
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # Remove the bullet if it goes off-screen
        if self.rect.right < 0 or self.rect.left > pygame.display.get_surface().get_width() or \
           self.rect.bottom < 0 or self.rect.top > pygame.display.get_surface().get_height():
            self.kill()