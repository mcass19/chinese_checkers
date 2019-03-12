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
