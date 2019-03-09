
class Board(object):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.lista_fichas_p1 = [(1,1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (3,1), (3,2), (4,1)]
        self.lista_fichas_p2 = [(9,9), (9,8), (9,7), (9,6), (8,9), (8,8), (8,7), (7,9), (7,8), (6,9)]

        self.target_p1 = [(9,9), (9,8), (9,7), (9,6), (8,9), (8,8), (8,7), (7,9), (7,8), (6,9)]
        self.target_p2 = [(1,1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (3,1), (3,2), (4,1)]

        # self.players = [Board.PLAYER_ONE, Board.PLAYER_TWO]
        # # keep available moves in a list
        # self.availables = None
        # self.current_player = None
        # self.state = None
        # self.counters = None