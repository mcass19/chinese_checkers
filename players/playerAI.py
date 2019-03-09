from board import Board
from players.player import Player

class PlayerAI(Player):
    def __init__(self, id, learning_rate, recalc_weight_enabled=True):
        super().__init__(id)

        self.weights = [] 
        # cargo pesos iniciales de archivo
        self.load_weights()

        self.w0 = 0
        self.learning_rate = learning_rate
        self.recalc_weight_enabled = recalc_weight_enabled

    def average(self, lista_fichas):

    def in_opponent_base(self, lista_fichas, lista_target):
        count = 0
        for i in range(0, 10):
            

    def board_value(self, board) -> float:
        has_a_winner, winner = board.has_a_winner()
        if has_a_winner:
            if winner == self.id:
                return 100
            else:
                return -100

        # obtengo el promedio de las fichas del p1 y p2, y la cantidad de fichas en base contraria del p1 y el p2
        p1_average = average(board.lista_fichas_p1)
        p2_average = average(board.lista_fichas_p2)
        p1_in_opponent_base = in_opponent_base(board.lista_fichas_p1, board.target_p1)
        p2_in_opponent_base = in_opponent_base(board.lista_fichas_p2, board.target_p2)

        # board_value = sum(xi * wi)
        board_value += p1_average * self.weights[0]
        board_value += p2_average * self.weights[1]
        board_value += p1_in_opponent_base * self.weights[2]
        board_value += p2_in_opponent_base * self.weights[3]

        return board_value

    def load_weights(self):
        with open('weights.txt', 'r') as file:
            file.readline()  # skip comment
            for i in range(1, 5):
                self.weights.append(float(file.readline()))
            # file.readline()  # skip comment
            # for i in range(1, 5):
            #     self.weights_p2.append(float(file.readline()))

    def save_weights(self):
        with open('weights.txt', 'w') as file:
            file.write('# Weights for p1\n')
            file.writelines([str(c) + '\n' for c in self.weights])
            # file.write('# Weights for p2\n')
            # file.writelines([str(c) + '\n' for c in self.weights_p2])