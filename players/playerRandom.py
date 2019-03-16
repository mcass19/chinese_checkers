import random
from players.player import Player

class PlayerRandom(Player):
    
    def __init__(self, id):
        super().__init__(id)

        self.pieces_already_move = []

    def do_jump(self, piece_to_jump, index_piece_jumping, visited_positions, board):
        return_list = []
        jump_move = (0,0)

        if(self.id == 1): 
            piece_jumping = board.pieces_p1[index_piece_jumping]
        else:
            piece_jumping = board.pieces_p2[index_piece_jumping]
               
        visited_positions.append(piece_jumping)

        # se setea el valor de i
        if (piece_jumping[0] < piece_to_jump[0]):
            jump_move = (piece_jumping[0] + 2, piece_jumping[1])
        elif (piece_jumping[0] > piece_to_jump[0]):
            jump_move = (piece_jumping[0] - 2, piece_jumping[1])
        else:
            jump_move = (piece_jumping[0], piece_jumping[1])
            
        # se setea el valor de j
        if (piece_jumping[1] < piece_to_jump[1]):
            jump_move = (jump_move[0], piece_jumping[1] + 2)
        elif (piece_jumping[1] > piece_to_jump[1]):
            jump_move = (jump_move[0], piece_jumping[1] - 2)
        else:
            jump_move = (jump_move[0], piece_jumping[1])

        if(jump_move[0] <= 0 or jump_move[0] >= 10 or
           jump_move[1] <= 0 or jump_move[1] >= 10 or
           (jump_move in board.pieces_p1) or
           (jump_move in board.pieces_p2) or
           (jump_move in visited_positions)):
            # No puedo realizar el salto:
            #   - La ficha se fue de rango
            #   - Hay otra ficha en el lugar que va a saltar
            return []
        
        return_list.append((index_piece_jumping,jump_move))

        # Hago el cambio en el tablero auxiliar
        previous_move = (0,0)
        if(self.id == 1):
            previous_move = board.pieces_p1[index_piece_jumping]
            board.pieces_p1[index_piece_jumping] = jump_move
        else:
            previous_move = board.pieces_p2[index_piece_jumping]
            board.pieces_p2[index_piece_jumping] = jump_move

        for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
            next_move = (jump_move[0] + i,jump_move[1] + j)
                
            if (next_move != piece_to_jump and 
               (next_move in board.pieces_p1 or next_move in board.pieces_p2)):
                # Puedo dar un salto. Llamo a do_jump que es recursiva
                aux_list = self.do_jump(next_move, index_piece_jumping, visited_positions, board)
                return_list = return_list + aux_list
        
        # Revierto los cambios en el tablero auxiliar
        if(self.id == 1):
            board.pieces_p1[index_piece_jumping] = previous_move
        else:
            board.pieces_p2[index_piece_jumping] = previous_move

        return return_list

    def do_move(self, board):
        
        _board = board
    
        if(self.id == 1): 
            pieces = board.pieces_p1
        else:
            pieces = board.pieces_p2
        
        lista_available_moves = []

        for index in range(10):
            for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
                
                next_move = (pieces[index][0] + i, pieces[index][1] + j) # Movimiento a realizar inmediatamente
                
                if (next_move[0] > 0 and next_move[0] <= 9 and next_move[1] > 0 and next_move[1] <= 9):
                    if next_move in _board.pieces_p1 or next_move in _board.pieces_p2:
                        aux_list = []
                        lista_available_moves_jump = self.do_jump(next_move, index, aux_list, _board)
                        lista_available_moves = lista_available_moves + lista_available_moves_jump
                    else:
                        lista_available_moves.append((index,next_move))
        
        # El siguiente fragmento de codigo se implementa para evitar que el jugador random no mueva las fichas de su base,
        # es decir, elige un movimiento random pero siempre cambia la ficha que mueve
        result = random.choice(lista_available_moves)
        
        # if len(self.pieces_already_move) == 10:
        #     self.pieces_already_move = []
        #     self.pieces_already_move.append(result[0])
        # else:
        #     finish_find_move = False
        #     while not finish_find_move:
        #         if (result[0] in self.pieces_already_move):
        #             result = random.choice(lista_available_moves)
        #         else:
        #             self.pieces_already_move.append(result[0])
        #             finish_find_move = True

        return result

    def recalc_weights(self, board):
        pass

    def set_actual_value_board(self, board):
        pass