from board import  Board

class Player:
    def __init__(self, id):
        self.id = id

    def do_move(self, board:Board):
        raise NotImplementedError