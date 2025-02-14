import pygame
import socket
import pickle
from settings import *
from player import Player
from sec_player import SecondPlayer
from borders import WorldBorder
from bullet import Bullet
from platform import Platform

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

        self.font = pygame.font.Font(None, 36)

        # Set up the client socket and connect to the server
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(('localhost', 5555))
            print("Connected to server")
        except Exception as e:
            print(f"Error connecting to server: {e}")
            self.running = False

        # Receive the player ID from the server
        data = self.client_socket.recv(1024)
        if data:
            self.player_id = pickle.loads(data)
            print(f"Player ID: {self.player_id}")

            # Create the correct player based on the received player ID
            if self.player_id == 1:
                self.player = Player(self.bullets)
                self.sec_player = SecondPlayer(SCREEN_WIDTH - SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.15)
            elif self.player_id == 2:
                self.player = SecondPlayer(SCREEN_WIDTH - SCREEN_WIDTH * 0.15, SCREEN_HEIGHT - SCREEN_HEIGHT * 0.15)
                self.sec_player = Player(self.bullets)

            self.all_sprites.add(self.player)
            self.all_sprites.add(self.sec_player)

            # Create platforms if you want to use pre-existing positions
            self.create_platforms()

    def create_platforms(self):
        """Create platforms in the game world."""
        for _ in range(10):
            platform = Platform(self.platforms)
            self.platforms.add(platform)
            self.all_sprites.add(platform)

    def handle_events(self):
        """Handles user input and window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    current_time = pygame.time.get_ticks()
                    if current_time - self.player.last_shot > self.player.shoot_delay:
                        bullet = Bullet(self.player.rect.center, pygame.mouse.get_pos())
                        self.bullets.add(bullet)
                        self.player.last_shot = current_time

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            self.send_game_state()
            self.receive_game_state()
        pygame.quit()

    def update(self):
        """Update game logic"""
        # self.player.move(self.sec_player, self.platforms)
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
        """Draw the game screen"""
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.platforms.draw(self.screen)
        self.draw_player_hp()
        pygame.display.update()

    def draw_player_hp(self):
        """Draw HP for both players"""
        if self.player.alive():
            hp_text = self.font.render(f'HP: {self.player.hp}', True, (255, 255, 255))
            self.screen.blit(hp_text, (self.player.rect.x, self.player.rect.y - 20))
        
        if self.sec_player.alive():
            sec_hp_text = self.font.render(f'HP: {self.sec_player.hp}', True, (255, 255, 255))
            self.screen.blit(sec_hp_text, (self.sec_player.rect.x, self.sec_player.rect.y - 20))

    def display_winner(self):
        """Display the winner after the game ends"""
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

    def send_game_state(self):
        """Send the game state to the server"""
        game_state = {
            'player_pos': self.player.rect.topleft,
            'sec_player_pos': self.sec_player.rect.topleft,
            'bullets': [bullet.rect.topleft for bullet in self.bullets],
            'health': self.player.hp
        }
        data = pickle.dumps(game_state)
        try:
            self.client_socket.sendall(data)
        except Exception as e:
            print(f"Error sending game state: {e}")
            self.running = False

    def receive_game_state(self):
        """Receive the updated game state from the server"""
        try:
            data = self.client_socket.recv(1024)
            if data:
                game_state = pickle.loads(data)
                self.player.rect.topleft = game_state['player_pos']
                self.sec_player.rect.topleft = game_state['sec_player_pos']
                for bullet, pos in zip(self.bullets, game_state['bullets']):
                    bullet.rect.topleft = pos
        except Exception as e:
            print(f"Error receiving game state: {e}")
            self.running = False
            self.client_socket.close()


if __name__ == '__main__':
    game = Game()
    game.run()
