import set

class Board(object):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self, width, height, current_player):
        self.width = width
        self.height = height
        self.current_player = None

        # (i,j,distance_to_opponent_base)
        self.pieces_p1 = [(1,1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (3,1), (3,2), (4,1)]
        self.pieces_p2 = [(9,9), (9,8), (9,7), (9,6), (8,9), (8,8), (8,7), (7,9), (7,8), (6,9)]

        self.target_p1 = [(9,9), (9,8), (9,7), (9,6), (8,9), (8,8), (8,7), (7,9), (7,8), (6,9)]
        self.target_p2 = [(1,1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (3,1), (3,2), (4,1)]
    
    def set_current_player(self, current_player):
        self.current_player = current_player

    def end_of_game(self):
        if set(self.pieces_p1) == set(self.target_p1):
            return True, 1
        elif set(self.pieces_p2) == set(self.target_p2):
            return True, 2
        return False, 0

    def do_move(self, index, position_to_move):
        if self.current_player == 1:
            self.pieces_p1[index] = position_to_move
            self.current_player = 2
        else:
            self.pieces_p2[index] = position_to_move
            self.current_player = 1