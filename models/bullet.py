import pygame
import models.settings as settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player_pos, mouse_pos):
        super().__init__()
        self.original_image = pygame.Surface((10, 5))
        self.original_image.fill((255, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = player_pos

        # Calculate the direction
        self.direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(player_pos)
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        self.speed = 30
        self.gravity = 0.025  # Gravity factor

        # Calculate the angle for rotation
        self.angle = self.direction.angle_to(pygame.math.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed + self.gravity

        # Apply gravity to the y-direction
        self.direction.y += self.gravity

        # Remove the bullet if it goes out of bounds
        if self.rect.right < 0 or self.rect.left > settings.SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()