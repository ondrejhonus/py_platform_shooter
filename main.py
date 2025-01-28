import pygame
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PyShooter")
        self.clock = pygame.time.Clock()
        self.running = True
        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.VIDEORESIZE:
                    self.screen_width, self.screen_height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
            self.draw()
            pygame.display.update()

        pygame.quit()
        
    def draw(self):
        background = pygame.image.load('assets/bg.png')
        background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
        self.screen.blit(background, (0, 0))
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
