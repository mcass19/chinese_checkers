import  random
from players.player import Player

class PlayerRandom(Player):

    def do_move(self, board):
        return random.choice(board.availables)