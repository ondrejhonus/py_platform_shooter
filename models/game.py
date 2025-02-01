import pygame
from models.settings import *
from models.player import Player
from models.sec_player import SecondPlayer
from models.borders import WorldBorder
from models.bullet import Bullet

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
        self.world_border = WorldBorder(self.screen_width, self.screen_height)
        
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player(self.bullets)
        self.sec_player = SecondPlayer(SCREEN_WIDTH - SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.15)

        self.all_sprites.add(self.player)
        self.all_sprites.add(self.sec_player)

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
        self.player.move(self.sec_player)
        self.sec_player.update()
        self.bullets.update()
        self.world_border.keep_within_bounds(self.player)
        self.world_border.keep_within_bounds(self.sec_player)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        pygame.display.update()
