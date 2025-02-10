import pygame
import models.settings as settings

class WorldBorder:
    def __init__(self):
        self.screen_width = settings.SCREEN_WIDTH
        self.screen_height = settings.SCREEN_HEIGHT

    def keep_within_bounds(self, player):
        if player.rect.left < 0:
            player.rect.left = 0
        if player.rect.right > self.screen_width:
            player.rect.right = self.screen_width
        if player.rect.top < 0:
            player.rect.top = 0
        if player.rect.bottom > self.screen_height:
            player.rect.bottom = self.screen_height