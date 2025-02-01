import pygame
import models.settings as settings
import models.bullet as bullet

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

    def last_shot(self):
        self.last_shot = pygame.time.get_ticks()

    def shoot(self, bullets, mouse_pos):
        bullet_direction = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(self.rect.center)
        bullet_direction = bullet_direction.normalize()
        new_bullet = bullet.Bullet((self.rect.centerx, self.rect.centery), mouse_pos)
        bullets.add(new_bullet)