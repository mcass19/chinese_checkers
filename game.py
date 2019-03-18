import os
from board import Board
from players.player import Player
from collections import deque

class Game(object):
    
    def __init__(self, board: Board):
        self.board = board

    def print_board(self,board):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(1,10):
            line = ""
            for j in range(1,10):
                if (i,j) in board.pieces_p1:
                    line = line + "| 1 / " + str(board.pieces_p1.index((i,j)))
                elif (i,j) in board.pieces_p2:
                    line = line + "| 2 / " + str(board.pieces_p2.index((i,j)))
                else:
                    line = line + "|      "
            line = line + "|"
            print(line)
        print(" Indice | Pos P1 | Pos P2")
        for x in range(10):
            print("     " + str(x) + "  | " + str(board.pieces_p1[x]) + " | " + str(board.pieces_p2[x]))
    
    def play_game(self, player1: Player, player2: Player, start_player):
        if start_player not in (1, 2):
            raise Exception('Invalid player id')
        
        self.board.set_current_player(start_player)
        p1 = player1
        p2 = player2
        first_movement = True
        p1_prev_moves = deque([] ,3)
        p2_prev_moves = deque([] ,3)

        while (1):
            current_player = self.board.current_player

            if current_player == 1:
                p1.set_actual_value_board(self.board)

                index, position_to_move = p1.do_move(self.board)

                if index == -1:
                    return 0

                self.board.do_move(index, position_to_move)

                p1_prev_moves.append((index, position_to_move))

                if not first_movement:
                    p2.recalc_weights(self.board)
                first_movement = False

                self.board.set_current_player(2)
            else:
                p2.set_actual_value_board(self.board)

                index, position_to_move = p2.do_move(self.board)

                if index == -1:
                    return 0

                self.board.do_move(index, position_to_move)

                p2_prev_moves.append((index, position_to_move))

                if not first_movement:    
                    p1.recalc_weights(self.board)
                first_movement = False

                self.board.set_current_player(1)

            self.print_board(self.board)

            if((len(p1_prev_moves) == 3 
               and p1_prev_moves[0] == p1_prev_moves[2]) or
               ( len(p2_prev_moves) == 3 
               and p2_prev_moves[0] == p2_prev_moves[2])):
                return 0

            end, winner = self.board.end_of_game()
            if end:
                return winner

            # is_draw_1 = p1.has_pieces_blocked(self.board)
            # is_draw_2 = p2.has_pieces_blocked(self.board)

            # if is_draw_1 or is_draw_2:
            #     return 0             