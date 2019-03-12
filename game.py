from board import Board
from players.player import Player

class Game(object):

    def __init__(self, board: Board):
        self.board = board
    
    def play_game(self, player1: Player, player2: Player, start_player=1):
        if start_player not in (1, 2):
            raise Exception('Invalid player id')
        
        self.board.set_current_player(start_player)
        p1 = player1
        p2 = player2
        while (1):
            current_player = self.board.current_player
            if current_player == 1:
                index, position_to_move = p1.move(self.board)
            else:
                index, position_to_move = p2.move(self.board)
            self.board.do_move(index, position_to_move)
            end, winner = self.board.end_of_game()
            if end:
                return winner