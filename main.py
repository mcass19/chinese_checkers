import random
from board import Board
from game import Game
from players.playerAI import PlayerAI
from players.playerRandom import PlayerRandom

wons_p1 = 0 
wons_p2 = 0
draws = 0

print('*******CHINESE CHECKERS*******')

for i in range(10):
    # creación de tablero
    board = Board(9, 9)

    # creación de jugadores
    p1 = PlayerAI(1, 0.001, True)
    p2 = PlayerRandom(2) 
    # p2 = PlayerAI(2, 0.1, False)

    game = Game(board)

    if random.choice([True, False]):
        winner = game.play_game(p1, p2, 1)
        if winner == 1:
            wons_p1 += 1
        elif winner == 2:
            wons_p2 += 1
        else:
            draws += 1
    else:
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