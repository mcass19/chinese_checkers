from board import Board
from players.player import Player

class PlayerAI(Player):
    def __init__(self, id, learning_rate, recalc_weight_enabled=True):
        super().__init__(id)

        self.weights = [] 
        # se cargan pesos iniciales de archivo
        self.load_weights()

        self.w0 = 0
        self.learning_rate = learning_rate
        self.recalc_weight_enabled = recalc_weight_enabled
        self.value_actual_board = 0
        self.next_board_value = 0
        
        # se setean los valores iniciales de los coeficientes 
        # [promedio_distancia_p1,promedio_distancia_p2,cantidad_fichas_en_base_oponente_p1,cantidad_fichas_en_base_oponente_p2]
        self.coefficientes.append(blablabla)
        self.coefficientes.append(blablabla)
        self.coefficientes.append(0)
        self.coefficientes.append(0)

    def move(self):
    
    def recalc_weights(self):
        if not self.recalc_weight_enabled:
            return
        
        # se realiza el mejor_movimiento o random del oponente y se retorna el valor del tablero 
        value_next_board = self.next_board_value()

        delta_board = self.learning_rate * (value_next_board - self.value_actual_board)
        self.w0 = self.w0 + delta_board

        for i in range(0, 4):
            self.weights[i] = self.weights[i] + delta_board * self.coefficients[i]
        
        # hacer norma?
    
    def distance_average(self, lista_fichas):

    # ARREGLAR CON UNA VARIABLE GLOBAL QUE SE ACTUALICE EN EL DO_MOVE
    def in_opponent_base(self, lista_fichas, lista_target):
        count = 0
        for i in range(0, 10):
            if lista_fichas[i] in lista_target:
                count += 1

    def average(self, lista_fichas):
        pass
    
    def in_opponent_base(self, lista_fichas, lista_target):
        count = 0
        for i in range(0, 10):
            pass
    #--------------------------------------------------------------------------------------------
            
    def do_jump(self, ficha_to_jump, index_ficha_jumping, board):
        jump_move = (0,0)
        
        if(id == 1): 
            ficha_jumping = board.lista_fichas_p1
        else:
            ficha_jumping = board.lista_fichas_p2
               
        if (ficha_jumping[0] < ficha_to_jump[0]):
            jump_move[0] = ficha_jumping[0] + 2
        elif (ficha_jumping[0] > ficha_to_jump[0]):
            jump_move[0] = ficha_jumping[0] - 2
            
        if (ficha_jumping[1] < ficha_to_jump[1]):
            jump_move[1] = ficha_jumping[1] + 2
        elif (ficha_jumping[1] > ficha_to_jump[1]):
            jump_move[1] = ficha_jumping[1] - 2
        
        if(jump_move[0] < 0 or jump_move[0] > 10 or
           jump_move[1] < 0 or jump_move[0] > 10 or
           jump_move in board.lista_fichas_p1 or
           jump_move in board.lista_fichas_p2):
            # No puedo realizar el salto:
            #   - La ficha se fue de rango
            #   - Hay otra ficha en el lugar que va a saltar
            return (ficha_jumping, -1)
        
        
        # Hago el cambio en el stack
        previous_move = (0,0)
        if(id == 1):
            previous_move = board.lista_fichas_p1[index_ficha_jumping]
            board.lista_fichas_p1[index_ficha_jumping] = jump_move
        else:
            previous_move = board.lista_fichas_p2[index_ficha_jumping]
            board.lista_fichas_p2[index_ficha_jumping] = jump_move
        
        max_weight = board_value(self, _board)
        position_to_move = jump_move
        
        for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
            next_move = (jump_move[0] + i,jump_move[1] + j)
            next_weight = 0
                
            if (next_move != ficha_to_jump and 
               (next_move in board.lista_fichas_p1 or next_move in board.lista_fichas_p2)):
                # Puedo dar un salto. Llamo a do_jump que es recursiva
                (next_move, next_weight) = do_jump(self, next_move, index_ficha_jumping, board)
                if (next_weight > max_weight):
                    max_weight = next_weight
                    position_to_move = next_move
        
        # Revierto los cambios en el stack
        if(id == 1):
            board.lista_fichas_p1[index_ficha_jumping] = previous_move
        else:
            board.lista_fichas_p2[index_ficha_jumping] = previous_move
        
        return (position_to_move, max_weight)
        
    #--------------------------------------------------------------------------------------------
            
    # No hace cambios en el tablero, sino que retorna la mejor posicion del tablero
    # para realiar el siguiente movimiento.
    def do_move(self,board):
                
        _board = board
    
        if(id == 1): 
            fichas = board.lista_fichas_p1
        else:
            fichas = board.lista_fichas_p2
            
        max_weight = 0
        position_to_move = (0,0)
        ficha_to_move = 0
        can_move = False
        
        for index in range(6):
            for (i,j) in [(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0)]:
                
                next_move = (fichas[index][0] + i, fichas[index][1] + j) # Movimiento a realizar inmediatamente
                next_weight = 0                                 # Peso del tablero despues de hacer el movimiento
                
                if (next_move[0] >= 0 and next_move[0] <= 9 and next_move[1] >= 0 and next_move[1] <= 9):
                    # El movimiento no se va del tablero
                    if next_move in _board.lista_fichas_p1 or next_move in _board.lista_fichas_p2:
                        # Puedo dar un salto. Llamo a do_jump que es recursiva
                        (next_move, next_weight) = do_jump(self, next_move, index, _board)
                        if next_weight != -1:
                            can_move = True
                    else:
                        can_move = True
                        # Hago el movimiento en el stack
                        previous_move = (0,0)
                        if(id == 1):
                            previous_move = _board.lista_fichas_p1[index]
                            _board.lista_fichas_p1[index] = next_move
                        else:
                            previous_move = _board.lista_fichas_p2[index]
                            _board.lista_fichas_p2[index] = next_move
                        
                        # Calculo el peso del tablero hecho el movimiento
                        next_weight = board_value(self, _board)
                        
                        # Revierto el movimiento en el stack
                        if(id == 1):
                            _board.lista_fichas_p1[index] = previous_move
                        else:
                            _board.lista_fichas_p2[index] = previous_move
                            
                    if next_weight > max_weight:
                        position_to_move = next_move
                        max_weight = next_weight
                        ficha_to_move = index
        
        if can_move:
            return ficha_to_move , position_to_move
        else:
            # No hay movimiento posible
            pass
    #--------------------------------------------------------------------------------------------
    
    def board_value(self, board) -> float:
        end, winner = self.board.end_of_game()
        if end:
            if winner == self.id:
                return 100
            else:
                return -100

        # se obtiene el promedio de las fichas de p1 y p2, y la cantidad de fichas en base contraria de p1 y p2
        self.coefficients[0] = self.distance_average(board.pieces_p1)
        self.coefficients[1] = self.distance_average(board.pieces_p2)
        self.coefficients[2] = self.in_opponent_base(board.pieces_p1, board.target_p1)
        self.coefficients[3] = self.in_opponent_base(board.pieces_p2, board.target_p2)

        # board_value = sum(xi * wi)
        board_value = self.w0
        board_value += self.coefficients[0] * self.weights[0]
        board_value += self.coefficients[1] * self.weights[1]
        board_value += self.coefficients[2] * self.weights[2]
        board_value += self.coefficients[3] * self.weights[3]

        return board_value

    def next_board_value(self) -> float:

    def load_weights(self):
        with open('weights.txt', 'r') as file:
            file.readline()  # skip comment
            for i in range(1, 5):
                self.weights.append(float(file.readline()))

    def save_weights(self):
        with open('weights.txt', 'w') as file:
            file.write('# Weights for p1\n')
            file.writelines([str(c) + '\n' for c in self.weights])
<<<<<<< HEAD
=======
            # file.write('# Weights for p2\n')
            # file.writelines([str(c) + '\n' for c in self.weights_p2])
>>>>>>> 4616da5... do_move y do_jump
