import pygame
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PyShooter")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            background = pygame.image.load('assets/bg.png')
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()
    