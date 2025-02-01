import pygame
import models.settings as settings

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('assets/player.png')
        self.width = 64
        self.height = 64
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.directions = "idle"
        self.rect.x = settings.SCREEN_WIDTH - settings.SCREEN_WIDTH * 0.9
        self.rect.y = settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.2
        self.speed = 5
        self.gravity = 0.6
        self.velocity_y = 0

    def move(self, sec_player):
        keys = pygame.key.get_pressed()

        # Move left
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            # Prevent moving left if colliding with sec_player
            if self.rect.colliderect(sec_player.rect):
                self.rect.x += self.speed
            else:
                self.directions = "left"

        # Move right
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            # Prevent moving right if colliding with sec_player
            if self.rect.colliderect(sec_player.rect):
                self.rect.x -= self.speed
            else:
                self.directions = "right"

        # Jump
        if keys[pygame.K_SPACE] and self.rect.y >= settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.16:
            self.velocity_y = -20
            self.directions = "jump"

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        if self.rect.y >= settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.15:
            self.rect.y = settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.15
            self.velocity_y = 0
            self.directions = "idle"

        if self.rect.colliderect(sec_player.rect) and self.velocity_y > 0:
            self.rect.y = sec_player.rect.top - self.height
            self.velocity_y = 0

    def stop_movement(self):
        self.velocity_y = 0
        self.directions = "idle"

    def draw(self, screen):
        screen.blit(self.image, self.rect)
