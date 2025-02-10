import pygame
import models.settings as settings
import models.bullet as bullet
import models.platform as platform

class Player(pygame.sprite.Sprite):
    def __init__(self, bullet_group):
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
        self.bullets = bullet_group
        self.mouse_pressed = False
        self.last_shot = 0
        self.shoot_delay = 500
        self.on_ground = False

        self.hp = 100

    def move(self, sec_player, platforms):
        keys = pygame.key.get_pressed()

        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            # Prevent moving left if colliding with sec_player
            if self.rect.colliderect(sec_player.rect):
                self.rect.x += self.speed
            else:
                self.directions = "left"

        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            # Prevent moving right if colliding with sec_player
            if self.rect.colliderect(sec_player.rect):
                self.rect.x -= self.speed
            else:
                self.directions = "right"

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = -20
            self.directions = "jump"

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        self.on_ground = False
        if self.rect.y >= settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.15:
            self.rect.y = settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.15
            self.velocity_y = 0
            self.on_ground = True
            self.directions = "idle"

        if self.rect.colliderect(sec_player.rect) and self.velocity_y > 0:
            self.rect.y = sec_player.rect.top - self.height
            self.velocity_y = 0
            self.on_ground = True

        # Check for collision with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.y = platform.rect.top - self.height
                self.velocity_y = 0
                self.on_ground = True

        # Collisions with bullets
        for bullet in self.bullets:
            if self.rect.colliderect(bullet.rect):
                self.hp -= 25
                bullet.kill()

        # Collisions with sec_player and bullets
        for bullet in self.bullets:
            if sec_player.rect.colliderect(bullet.rect):
                sec_player.hp -= 25
                bullet.kill()

    def stop_movement(self):
        self.velocity_y = 0
        self.directions = "idle"

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def last_shot(self):
        self.last_shot = pygame.time.get_ticks()