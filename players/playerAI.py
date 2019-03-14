from board import Board
from players.player import Player

class PlayerAI(Player):
    def __init__(self, id, opponents_id, learning_rate, recalc_weight_enabled=True):
        super().__init__(id)

        self.opponents_id = opponents_id
        self.weights = [] 
        
        # [promedio_distancia_p1,promedio_distancia_p2,cantidad_fichas_en_base_oponente_p1,cantidad_fichas_en_base_oponente_p2]
        self.coefficients = [0, 0, 0, 0]
        
        # se cargan pesos iniciales de archivo
        self.load_weights()

        self.w0 = 0
        self.learning_rate = learning_rate
        self.recalc_weight_enabled = recalc_weight_enabled
        self.value_actual_board = 0
        self._value_next_board = 0

    #--------------------------------------------------------------------------------------------
            
    def do_jump(self, piece_to_jump, index_piece_jumping, initial_position,visited_positions, board):
        jump_move = (0,0)
        #print('indice de la ficha que quiere saltar ' + str(index_piece_jumping) + ' posicion de la ficha a saltar ' + str(piece_to_jump))
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

        #print('intento de salto ' + str(jump_move))
        if(jump_move[0] <= 0 or jump_move[0] >= 10 or
           jump_move[1] <= 0 or jump_move[1] >= 10 or
           (jump_move in board.pieces_p1) or
           (jump_move in board.pieces_p2) or (jump_move == initial_position) or
           (jump_move in visited_positions)):
            # No puedo realizar el salto:
            #   - La ficha se fue de rango
            #   - Hay otra ficha en el lugar que va a saltar
            #print('no salto')
            return (piece_jumping, -1)
        

        
        # Hago el cambio en el stack
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
                (next_move, next_value) = self.do_jump(next_move, index_piece_jumping, initial_position,visited_positions, board)
                if (next_value > max_value):
                    max_value = next_value
                    position_to_move = next_move
        
        # Revierto los cambios en el stack
        if(self.id == 1):
            board.pieces_p1[index_piece_jumping] = previous_move
        else:
            board.pieces_p2[index_piece_jumping] = previous_move
        
        return (position_to_move, max_value)
        
    #--------------------------------------------------------------------------------------------
            
    # No hace cambios en el tablero, sino que retorna la mejor posicion del tablero
    # para realiar el siguiente movimiento.
    def do_move(self,board):
      
        _board = board
    
        if(self.id == 1): 
            pieces = board.pieces_p1
        else:
            pieces = board.pieces_p2
            
        max_value = 0
        position_to_move = (0,0)
        piece_to_move = 0
        can_move = False
        
        for index in range(10):
            for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
                
                next_move = (pieces[index][0] + i, pieces[index][1] + j) # Movimiento a realizar inmediatamente
                next_value = 0                                          # Valor del tablero despues de hacer el movimiento
                
                if (next_move[0] > 0 and next_move[0] <= 9 and next_move[1] > 0 and next_move[1] <= 9):
                    # El movimiento no se va del tablero
                    if next_move in _board.pieces_p1 or next_move in _board.pieces_p2:
                        # Puedo dar un salto. Llamo a do_jump que es recursiva
                        aux_list = []
                        (next_move, next_value) = self.do_jump(next_move, index, pieces[index],aux_list, _board)
                        if next_value != -1:
                            can_move = True
                    else:
                        can_move = True
                        # Hago el movimiento en el stack
                        previous_move = (0,0)
                        if(self.id == 1):
                            previous_move = _board.pieces_p1[index]
                            _board.pieces_p1[index] = next_move
                        else:
                            previous_move = _board.pieces_p2[index]
                            _board.pieces_p2[index] = next_move
                        
                        # Calculo el peso del tablero hecho el movimiento
                        next_value = self.board_value(_board)
                        
                        # Revierto el movimiento en el stack
                        if(self.id == 1):
                            _board.pieces_p1[index] = previous_move
                        else:
                            _board.pieces_p2[index] = previous_move
                            
                    if next_value > max_value:
                        position_to_move = next_move
                        max_value = next_value
                        piece_to_move = index
        
        self.value_actual_board = max_value
        if can_move:
            return piece_to_move,position_to_move
        else:
            # No hay movimiento posible
            pass
    #--------------------------------------------------------------------------------------------
    
    def recalc_weights(self, board_after_opoonent_move):
        if not self.recalc_weight_enabled:
            return
        
        # se realiza el mejor_movimiento o random del oponente y se retorna el valor del tablero 
        value_next_board = self.board_value(board_after_opoonent_move)

        delta_board = self.learning_rate * (value_next_board - self.value_actual_board)
        
        self.w0 = self.w0 + delta_board
        for i in range(0, 4):
            self.weights[i] = self.weights[i] + delta_board * self.coefficients[i]

        self.save_weights()
    
    def distance_average(self, pieces, target):
        count = 0
        for i in range(10):
            count += (target[0] - pieces[i][0]) + (target[1] - pieces[i][1])
        if count < 0:  
            count = count * -1
        count = count / 10  # promedio real
        count = count / 100
        return (1 - count)

    # ARREGLAR CON UNA VARIABLE GLOBAL QUE SE ACTUALICE EN EL DO_MOVE
    def in_opponent_base(self, pieces, target):
        count = 0
        for i in range(10):
            if pieces[i] in target:
                count += 1
        return count
    
    def board_value(self, board) -> float:
        end, winner = board.end_of_game()
        if end:
            if winner == self.id:
                return 100
            else:
                return -100

        # se obtiene el promedio de las fichas de p1 y p2, y la cantidad de fichas en base contraria de p1 y p2
        self.coefficients[0] = self.distance_average(board.pieces_p1, (9,9))
        self.coefficients[1] = self.distance_average(board.pieces_p2, (1,1))
        self.coefficients[2] = self.in_opponent_base(board.pieces_p1, board.target_p1)
        self.coefficients[3] = self.in_opponent_base(board.pieces_p2, board.target_p2)

        # board_value = sum(xi * wi)
        board_value = self.w0
        board_value += self.coefficients[0] * self.weights[0]
        board_value += self.coefficients[1] * self.weights[1]
        board_value += self.coefficients[2] * self.weights[2]
        board_value += self.coefficients[3] * self.weights[3]

        return board_value

    def load_weights(self):
        if self.id == 1:
            with open('weights_1.txt', 'r') as file_to_read:
                file_to_read.readline()  # skip comment
                for i in range(1, 5):
                    self.weights.append(float(file_to_read.readline()))
        else:
            with open('weights_2.txt', 'r') as file_to_read:
                file_to_read.readline()  # skip comment
                for i in range(1, 5):
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
