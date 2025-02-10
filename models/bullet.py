import pygame
import settings

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.image.load('assets/bullet.png')  # Replace with your bullet image
        self.rect = self.image.get_rect()
        self.rect.center = start_pos
        
        # Calculate direction vector (normalized)
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = (dx**2 + dy**2)**0.5
        self.direction = (dx / distance, dy / distance)
        
        self.speed = 10  # Bullet speed

    def update(self):
        """Update the bullet's position."""
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        
        # Remove bullet if it goes out of screen bounds
        if not settings.SCREEN_RECT.colliderect(self.rect):
            self.kill()
