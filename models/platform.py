import pygame
import models.settings as settings
import random

class Platform(pygame.sprite.Sprite):
    def __init__(self, existing_platforms):
        super().__init__()
        self.image = pygame.image.load('assets/platform.png')
        self.rect = self.image.get_rect()
        
        # Define margins from the screen edges
        margin_x = 100
        margin_y = 200
        
        # Minimum distance between platforms
        min_distance = 50
        
        # overlap check
        max_attempts = 100
        for _ in range(max_attempts):
            self.rect.x = random.randint(margin_x, settings.SCREEN_WIDTH - self.rect.width - margin_x)
            self.rect.y = random.randint(margin_y, settings.SCREEN_HEIGHT - self.rect.height - margin_y)
            if not any(self.rect.colliderect(platform.rect.inflate(min_distance, min_distance)) for platform in existing_platforms):
                break
        else:
            raise Exception("Could not place platform without overlapping after {} attempts".format(max_attempts))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)
