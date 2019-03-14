import random
from players.player import Player

class PlayerRandom(Player):
    
    def __init__(self, id):
        super().__init__(id)

    # Implementar
    def do_move(self, board):
        return random.choice(board.availables)