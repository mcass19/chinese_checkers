from __future__ import division
from board import Board
from players.player import Player

class PlayerAI(Player):

    def __init__(self, id, learning_rate, recalc_weight_enabled=True):
        super().__init__(id)

        self.w0 = 0
        self.weights = [] 

        # se cargan pesos iniciales de archivo
        self.load_weights()
        
        # [promedio_distancia_p1,promedio_distancia_p2,cantidad_fichas_en_base_oponente_p1,cantidad_fichas_en_base_oponente_p2,
        #  promedio_distancia_minima_a_lugar_libre_base__oponente_p1,promedio_distancia_minima_a_lugar_libre_base__oponente_p2]
        self.coefficients = [0, 0, 0, 0, 0, 0]

        self.learning_rate = learning_rate
        self.recalc_weight_enabled = recalc_weight_enabled
        self.value_actual_board = 0
        self.last_move = (0,0)
    #--------------------------------------------------------------------------------------------
            
    def do_jump(self, piece_to_jump, index_piece_jumping, visited_positions, board):
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
            return (piece_jumping, -1)
        
        # Hago el cambio en el tablero auxiliar
        previous_move = (0,0)
        if(self.id == 1):
            previous_move = board.pieces_p1[index_piece_jumping]
            board.pieces_p1[index_piece_jumping] = jump_move
        else:
            previous_move = board.pieces_p2[index_piece_jumping]
            board.pieces_p2[index_piece_jumping] = jump_move
        
        max_value = self.board_value(board)
        position_to_move = jump_move
        
        for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
            next_move = (jump_move[0] + i,jump_move[1] + j)
            next_value= 0
                
            if (next_move != piece_to_jump and 
               (next_move in board.pieces_p1 or next_move in board.pieces_p2)):
                # Puedo dar un salto. Llamo a do_jump que es recursiva
                (next_move, next_value) = self.do_jump(next_move, index_piece_jumping, visited_positions, board)
                if (next_value > max_value):
                    max_value = next_value
                    position_to_move = next_move
        
        # Revierto los cambios en el tablero auxiliar
        if(self.id == 1):
            board.pieces_p1[index_piece_jumping] = previous_move
        else:
            board.pieces_p2[index_piece_jumping] = previous_move
        
        return (position_to_move, max_value)
        
    #--------------------------------------------------------------------------------------------

    # No hace cambios en el tablero, sino que retorna la mejor posicion del tablero
    # para realiar el siguiente movimiento.
    def do_move(self, board):
      
        _board = board
    
        if(self.id == 1): 
            pieces = board.pieces_p1
        else:
            pieces = board.pieces_p2
            
        max_value = float('-inf')
        position_to_move = (0,0)
        piece_to_move = 0
        can_move = False
        
        for index in range(10):
            for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
                next_move = (pieces[index][0] + i, pieces[index][1] + j) # Movimiento a realizar inmediatamente
                next_value = 0                                           # Valor del tablero despues de hacer el movimiento
                
                if (next_move[0] > 0 and next_move[0] <= 9 and next_move[1] > 0 and next_move[1] <= 9):
                    # El movimiento no se va del tablero
                    if next_move in _board.pieces_p1 or next_move in _board.pieces_p2:
                        # Puedo dar un salto. Llamo a do_jump que es recursiva
                        aux_list = []
                        (next_move, next_value) = self.do_jump(next_move, index, aux_list, _board)
                        if next_value != -1:
                            can_move = True
                    else:
                        can_move = True
                        # Hago el movimiento en el tablero auxiliar
                        previous_move = (0,0)
                        if(self.id == 1):
                            previous_move = _board.pieces_p1[index]
                            _board.pieces_p1[index] = next_move
                        else:
                            previous_move = _board.pieces_p2[index]
                            _board.pieces_p2[index] = next_move
                        
                        # Calculo el valor del tablero hecho el movimiento
                        next_value = self.board_value(_board)
                        
                        # Revierto el movimiento en el tablero auxiliar
                        if(self.id == 1):
                            _board.pieces_p1[index] = previous_move
                        else:
                            _board.pieces_p2[index] = previous_move
                            
                    if next_value > max_value:
                        position_to_move = next_move
                        max_value = next_value
                        piece_to_move = index
        
        if can_move:
            return piece_to_move,position_to_move
        else:
            # No hay movimiento posible
            pass
    #--------------------------------------------------------------------------------------------
    
    def set_actual_value_board(self, board):
        self.value_actual_board = self.board_value(board)
    
    def recalc_weights(self, board):
        if not self.recalc_weight_enabled:
            return

        _board = board
        v_successor = self.board_value(board)
        
        delta_board = self.learning_rate * (v_successor - self.value_actual_board)
        
        self.w0 = self.w0 + delta_board

        weight_min = float('+inf')
        weight_opponent_max = float('-inf')

        for i in [0, 2, 4]:
            self.weights[i] = self.weights[i] + delta_board * self.coefficients[i]
            self.weights[i + 1] = self.weights[i + 1] + delta_board * self.coefficients[i + 1]

            if self.weights[i] < weight_min:
                weight_min = self.weights[i]

            if self.weights[i + 1] > weight_opponent_max:
                weight_opponent_max = self.weights[i + 1]

        if weight_min < 0 and delta_board != 0:
            self.weights[0] = self.weights[0] + abs(weight_min)
            self.weights[2] = self.weights[2] + abs(weight_min)
            self.weights[4] = self.weights[4] + abs(weight_min)
        
        if weight_opponent_max > 0 and delta_board != 0:
            self.weights[1] = self.weights[1] - weight_opponent_max
            self.weights[3] = self.weights[3] - weight_opponent_max
            self.weights[5] = self.weights[5] - weight_opponent_max

        self.save_weights()
    
    def distance_average(self, pieces, target) -> float:
        count = 0

        for i in range(10):
            aux_1 = abs(target[0] - pieces[i][0]) 
            aux_2 = abs(target[1] - pieces[i][1])
            aux = aux_1 + aux_2
            count += aux

        count = count / 10  # promedio real
        count = count * 0.01
        return (1 - count)
    
    def distance_average_not_in_base(self, pieces, target) -> float:
        cant_pieces = 1
        count = 0
        target_list = []

        for i in range(10):
            if not (target[i] in pieces):
                target_list.append(target[i])

        for i in range(10):
            if not (pieces[i] in target):
                cant_pieces += 1
                aux = 0
                distance_min = float('+inf')
                
                for target_index in target_list:
                    aux_1 = abs(target_index[0] - pieces[i][0]) 
                    aux_2 = abs(target_index[1] - pieces[i][1])
                    aux = aux_1 + aux_2
                    if (aux < distance_min):
                        distance_min = aux
                
                count += distance_min

        count = count / cant_pieces   # promedio real
        count = count * 0.01
        return (1 - count)

    def in_opponent_base(self, pieces, target) -> float:
        count = 0
        for i in range(10):
            if pieces[i] in target:
                count += 1
        return (count / 10)
    
    def board_value(self, board) -> float:
        end, winner = board.end_of_game()
        if end:
            if winner == self.id:
                return 2
            else:
                return -2

        if self.id == 1:
            self.coefficients[0] = self.distance_average(board.pieces_p1, board.target_p1[0])
            self.coefficients[1] = self.distance_average(board.pieces_p2, board.target_p2[0])
            self.coefficients[2] = self.in_opponent_base(board.pieces_p1, board.target_p1)
            self.coefficients[3] = self.in_opponent_base(board.pieces_p2, board.target_p2)
            self.coefficients[4] = self.distance_average_not_in_base(board.pieces_p1, board.target_p1)
            self.coefficients[5] = self.distance_average_not_in_base(board.pieces_p2, board.target_p2)
        else:
            self.coefficients[0] = self.distance_average(board.pieces_p2, board.target_p2[0])
            self.coefficients[1] = self.distance_average(board.pieces_p1, board.target_p1[0])
            self.coefficients[2] = self.in_opponent_base(board.pieces_p2, board.target_p2)
            self.coefficients[3] = self.in_opponent_base(board.pieces_p1, board.target_p1)
            self.coefficients[4] = self.distance_average_not_in_base(board.pieces_p2, board.target_p2)
            self.coefficients[5] = self.distance_average_not_in_base(board.pieces_p1, board.target_p1)

        # board_value = sum(xi * wi)
        board_value = self.w0
        board_value += (self.coefficients[0] / 2) * self.weights[0]
        board_value += (self.coefficients[1] / 2) * self.weights[1]
        board_value += self.coefficients[2] * self.weights[2]
        board_value += self.coefficients[3] * self.weights[3]
        board_value += (self.coefficients[4] / 2) * self.weights[4]
        board_value += (self.coefficients[5] / 2) * self.weights[5]

        return board_value

    def next_value_opponent_board(self, board, player: Player):
        index, position_to_move = player.do_move(board)
        board.do_move_opponent(index, position_to_move)
        result = self.board_value(board)
        return result

    def load_weights(self):
        if self.id == 1:
            with open('weights_1.txt', 'r') as file_to_read:
                file_to_read.readline()  # skip comment
                for i in range(1, 7):
                    self.weights.append(float(file_to_read.readline()))
        else:
            with open('weights_2.txt', 'r') as file_to_read:
                file_to_read.readline()  # skip comment
                for i in range(1, 7):
                    self.weights.append(float(file_to_read.readline()))

    def save_weights(self):
        if self.id == 1:
            with open('weights_1.txt', 'w') as file_to_write:
                file_to_write.write('# Weights for p1\n')
                file_to_write.writelines([str(c) + '\n' for c in self.weights])
        else:
            with open('weights_2.txt', 'w') as file_to_write:
                file_to_write.write('# Weights for p2\n')
                file_to_write.writelines([str(c) + '\n' for c in self.weights])
