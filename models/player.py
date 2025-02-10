import pygame
import settings as settings
import bullet as bullet
import platform as platform

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
        self.last_shot_time = 0  # Rename to avoid confusion with the method
        self.shoot_delay = 500  # Delay between shots in milliseconds
        self.on_ground = False
        self.hp = 100

    def move(self, sec_player, platforms):
        keys = pygame.key.get_pressed()

        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.rect.colliderect(sec_player.rect):
                self.rect.x += self.speed
            else:
                self.directions = "left"

        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.rect.colliderect(sec_player.rect):
                self.rect.x -= self.speed
            else:
                self.directions = "right"

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = -20
            self.directions = "jump"

        # Apply gravity
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        # Check if on ground
        self.on_ground = False
        if self.rect.y >= settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.15:
            self.rect.y = settings.SCREEN_HEIGHT - settings.SCREEN_HEIGHT * 0.15
            self.velocity_y = 0
            self.on_ground = True
            self.directions = "idle"

        # Collisions with second player
        if self.rect.colliderect(sec_player.rect) and self.velocity_y > 0:
            self.rect.y = sec_player.rect.top - self.height
            self.velocity_y = 0
            self.on_ground = True

        # Collisions with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                self.rect.y = platform.rect.top - self.height
                self.velocity_y = 0
                self.on_ground = True

        # Handle bullet collisions with player
        for bullet in self.bullets:
            if self.rect.colliderect(bullet.rect):
                self.hp -= 25
                bullet.kill()

        # Handle collisions between the second player's bullets and the first player
        for bullet in sec_player.bullets:
            if self.rect.colliderect(bullet.rect):
                self.hp -= 25
                bullet.kill()

    def shoot(self, target):
        """Handle shooting logic."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            # Create a bullet targeting the mouse or direction
            bullet_obj = bullet.Bullet(self.rect.center, target)
            self.bullets.add(bullet_obj)
            self.last_shot_time = current_time

    def stop_movement(self):
        """Stops player movement (usually for idle state)."""
        self.velocity_y = 0
        self.directions = "idle"

    def draw(self, screen):
        """Draw the player on the screen."""
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        """Handle taking damage."""
        self.hp -= amount
        if self.hp <= 0:
            self.kill()  # Kill the player when HP reaches 0

    def respawn(self):
        """Respawn the player after death."""
        self.hp = 100
        self.rect.topleft = (settings.SCREEN_WIDTH - 100, settings.SCREEN_HEIGHT - 100)

    def draw_hp(self, screen):
        """Draw the player’s HP on the screen."""
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f'HP: {self.hp}', True, (255, 255, 255))
        screen.blit(hp_text, (self.rect.x, self.rect.y - 20))
