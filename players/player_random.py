import  random
from players.player import Player

class PlayerRandom(Player):

    def move(self, board):
        return random.choice(board.availables)