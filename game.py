from board import Board
from players.player import Player

class Game(object):

    def __init__(self, board: Board):
        self.board = board
    
    def start_game(self, player1: Player, player2: Player, start_player=1):
        if start_player not in (1, 2):
            raise Exception('Invalid player id')
        
        self.board.init_board(start_player)
        p1, p2 = self.board.players
        players = {p1: player1, p2: player2}
        while (1):
            current_player = self.board.current_player
            player_in_turn = players[current_player]
            move = player_in_turn.do_move(self.board)
            self.board.do_move(move)
            end, winner = self.board.game_end()
            if end:
                return winner