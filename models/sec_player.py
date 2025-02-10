import pygame
import settings

class SecondPlayer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assets/player.png')  # Replace with your second player's image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Initial position
        self.speed = 5  # Movement speed
        self.hp = 100  # Health points
        self.last_shot = 0
        self.shoot_delay = 500  # Delay between shots in milliseconds
        self.bullets = pygame.sprite.Group()

    def update(self):
        """Update the second player's state (e.g., movement and other logic)."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Constrain player within the screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.SCREEN_HEIGHT:
            self.rect.bottom = settings.SCREEN_HEIGHT

        self.bullets.update()

    def shoot(self, target):
        """Handle shooting logic for the second player."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            # Create a bullet that moves towards the target
            bullet = Bullet(self.rect.center, target)
            self.bullets.add(bullet)
            self.last_shot = current_time

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
        """Draw the second player's HP on the screen."""
        font = pygame.font.Font(None, 36)
        hp_text = font.render(f'HP: {self.hp}', True, (255, 255, 255))
        screen.blit(hp_text, (self.rect.x, self.rect.y - 20))
