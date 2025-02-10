import pygame
import settings as settings
import random

class Platform(pygame.sprite.Sprite):
    def __init__(self, existing_platforms, x=None, y=None):
        super().__init__()
        self.image = pygame.image.load('assets/platform.png')
        self.rect = self.image.get_rect()

        # If no x or y is provided, generate random positions for them
        if x is None or y is None:
            margin_x = 100
            margin_y = 200
            min_distance = 50
            max_attempts = 100
            for _ in range(max_attempts):
                self.rect.x = random.randint(margin_x, settings.SCREEN_WIDTH - self.rect.width - margin_x)
                self.rect.y = random.randint(margin_y, settings.SCREEN_HEIGHT - self.rect.height - margin_y)
                if not any(self.rect.colliderect(platform.rect.inflate(min_distance, min_distance)) for platform in existing_platforms):
                    break
            else:
                raise Exception("Could not place platform without overlapping after {} attempts".format(max_attempts))
        else:
            self.rect.x = x
            self.rect.y = y
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pass

    def check_collision(self, player):
        return self.rect.colliderect(player.rect)

