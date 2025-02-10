import pygame
from models.settings import *
from models.player import Player
from models.sec_player import SecondPlayer
from models.borders import WorldBorder
from models.bullet import Bullet
from models.platform import Platform

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SCALED | pygame.DOUBLEBUF | pygame.HWSURFACE
        )
        pygame.display.set_caption("PyShooter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT
        self.background = pygame.image.load('assets/bg-fullhd.png').convert()
        self.world_border = WorldBorder()
        self.platforms = pygame.sprite.Group()
        
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self.bullets)
        self.sec_player = SecondPlayer(SCREEN_WIDTH - SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.15)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.sec_player)

        for _ in range(10):
            platform = Platform(self.platforms)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

        self.font = pygame.font.Font(None, 36)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.VIDEORESIZE:
                self.world_border.screen_width = event.w
                self.world_border.screen_height = event.h
                self.background = pygame.transform.smoothscale(
                    pygame.image.load('assets/bg-fullhd.png').convert(),
                    (event.w, event.h)
                )
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # LMB
                    current_time = pygame.time.get_ticks()
                    if current_time - self.player.last_shot > self.player.shoot_delay:
                        bullet = Bullet(self.player.rect.center, pygame.mouse.get_pos())
                        self.bullets.add(bullet)
                        self.player.last_shot = current_time

    def update(self):
        self.player.move(self.sec_player, self.platforms)
        self.sec_player.update()
        self.bullets.update()
        self.world_border.keep_within_bounds(self.player)
        self.world_border.keep_within_bounds(self.sec_player)

        # Check if player HP is 0 or less and kill them
        if self.player.hp <= 0:
            self.player.kill()
        if self.sec_player.hp <= 0:
            self.sec_player.kill()

        if not self.player.alive() or not self.sec_player.alive():
            self.display_winner()
            self.running = False

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.platforms.draw(self.screen)
        self.draw_player_hp()
        pygame.display.update()

    def draw_player_hp(self):
        # Draw HP for the first player
        if self.player.alive():
            hp_text = self.font.render(f'HP: {self.player.hp}', True, (255, 255, 255))
            self.screen.blit(hp_text, (self.player.rect.x, self.player.rect.y - 20))
        
        # Draw HP for the second player
        if self.sec_player.alive():
            sec_hp_text = self.font.render(f'HP: {self.sec_player.hp}', True, (255, 255, 255))
            self.screen.blit(sec_hp_text, (self.sec_player.rect.x, self.sec_player.rect.y - 20))

    def display_winner(self):
        self.screen.fill((0, 0, 0))
        if self.player.alive():
            winner_text = self.font.render('Player 1 Won!', True, (255, 255, 255))
        elif self.sec_player.alive():
            winner_text = self.font.render('Player 2 Won!', True, (255, 255, 255))
        else:
            winner_text = self.font.render('No Players Left!', True, (255, 255, 255))
        text_rect = winner_text.get_rect(center=(self.screen_width / 2, self.screen_height / 2))
        self.screen.blit(winner_text, text_rect)
        pygame.display.update()
        pygame.time.wait(3000)  # Wait for 3 seconds before closing the game
