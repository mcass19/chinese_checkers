import random
from board import Board
from game import Game
from players.playerAI import PlayerAI
from players.playerRandom import PlayerRandom

wons_p1 = 0     # Partidas ganados jugador 1
wons_p2 = 0     # Partidas ganados jugador 2
draws = 0       # Empates
cant_init_1 = 0 # Partidas iniciadas jugador 1 
cant_init_2 = 0 # Partidas iniciadas jugador 2

for i in range(100):
    # Crea el tablero
    board = Board(9, 9)

    # Crea los jugadores
    # PlayerAI recibe: Numero de jugador, Tasa de aprendizaje, Aprendizaje activado/desactivado
    # PlayerRandom solo recibe el numero de jugador  
    p1 = PlayerAI(1, 0.001, True)
    # p2 = PlayerRandom(2) 
    p2 = PlayerAI(2, 0.001, True)

    game = Game(board)

    # Se elije al azar un jugador que inicia la partida
    if random.choice([True, False]):
        cant_init_1 += 1
        winner = game.play_game(p1, p2, 1)
        if winner == 1:
            wons_p1 += 1
        elif winner == 2:
            wons_p2 += 1
        else:
            draws += 1
    else:
        cant_init_2 += 1
        winner = game.play_game(p1, p2, 2)
        if winner == 1:
            wons_p1 += 1
        elif winner == 2:
            wons_p2 += 1
        else:
            draws += 1

    print('Partido {} finalizado'.format(i))

print('Player 1 gano {} veces'.format(wons_p1))
print('Player 2 gano {} veces'.format(wons_p2))
print('Empataron {} veces'.format(draws))
print('Empezo {} veces el jugador 1'.format(cant_init_1))
print('Empezo {} veces el jugador 2'.format(cant_init_2))