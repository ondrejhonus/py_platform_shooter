import pygame
from models.settings import *
from models.player import Player
from models.sec_player import SecondPlayer
from models.borders import WorldBorder
from models.game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
