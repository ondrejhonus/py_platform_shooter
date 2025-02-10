import socket
import pickle
import threading

# Store players' data
players = {}
platforms = [(100, 100), (300, 200), (500, 300), (700, 400)]  # List of platform positions

def handle_client(client_socket, player_id):
    print(f"Player {player_id} connected")
    
    # Add player to the game state
    players[player_id] = {
        'socket': client_socket,
        'pos': (100, 100),  # Starting position of the player
        'health': 100
    }

    # Send the initial state of the game (platforms)
    initial_state = {'platforms': platforms}
    client_socket.sendall(pickle.dumps(initial_state))

    while True:
        try:
            # Receive game state from player
            data = client_socket.recv(1024)
            if not data:
                break

            game_state = pickle.loads(data)
            # Update player's state
            players[player_id]['pos'] = game_state['player_pos']
            players[player_id]['health'] = game_state['health']

            # Send updated state to all players
            for pid, player in players.items():
                if pid != player_id:
                    player['socket'].sendall(pickle.dumps(game_state))

        except Exception as e:
            print(f"Error with player {player_id}: {e}")
            break

    client_socket.close()
    del players[player_id]
    print(f"Player {player_id} disconnected")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))
    server_socket.listen(2)  # Listen for two players

    print("Server started, waiting for players...")

    # Accept the connections from players
    player_socket, address = server_socket.accept()
    print(f"Player 1 connected: {address}")
    
    # Send Player 1 ID (usually 1)
    player_socket.send(pickle.dumps(1))

    player_socket2, address2 = server_socket.accept()
    print(f"Player 2 connected: {address2}")
    
    # Send Player 2 ID
    player_socket2.send(pickle.dumps(2))
    
    # Continue to manage the game state here
    # (sending/receiving game state between players)
    
    # Close sockets
    player_socket.close()
    player_socket2.close()

if __name__ == "__main__":
    start_server()
