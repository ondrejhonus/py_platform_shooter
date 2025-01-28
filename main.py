import pygame
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        # Keep window non-resizable so it remains floating in bspwm
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
                # Handle window resizing manually (without RESIZABLE flag)
                if event.type == pygame.VIDEORESIZE:
                    # Manually adjust the screen size based on the resize
                    self.screen_width, self.screen_height = event.w, event.h

            # Adjust background size to the current window size
            background = pygame.image.load('assets/bg.png')
            background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
            self.screen.blit(background, (0, 0))
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
