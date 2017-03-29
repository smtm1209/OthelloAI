
import sarkistrat as ai
import Othello_Core as core
import time
from multiprocessing import Process, Value
import os, signal, sys, getopt

ai1 = ai.sarkistrat() 
ai2 = ai.sarkirandom()
ref = ai.sarkiref()

def tournament_player(black_choice, white_choice, black_name="Black", white_name="White", time_limit=5):
    """ runs a tournament of an even number of games, alternating black/white with each strategy
        and returns the results """
    ai1_wins = 0
    rounds = 1
    pg = False
    for i in range(rounds):
        try:
            (black, white) = black_choice, white_choice
            board, score = play(black, white, black_name, white_name, time_limit, pg)
            ai1_wins += 1 if score > 0 else 0
            print('%s wins!' % ('AI1' if score > 0 else 'AI2'))

            (black, white) = white_choice, black_choice
            board, score = play(black, white, black_name, white_name, time_limit, pg)
            ai1_wins += 1 if score < 0 else 0
            print('%s wins!' % ('AI2' if score > 0 else 'AI1'))
            pg = not pg
        except core.OthelloCore.IllegalMoveError as e:
            print(e)
            return
    print("strategy A won", ai1_wins, "out of", 2*rounds)
    return ai1_wins


def play(black_strategy, white_strategy, black_name, white_name, time_limit=60, pg=False):
    """Play a game of Othello and return the final board and score."""
    board = ref.initial_board()
    player = core.WHITE
    print("Time Limit: ", time_limit)
    print("PG: ", pg)
    strategy = lambda who: black_strategy if who == core.BLACK else white_strategy
    while player is not None:
        start_time = time.time()

        best_shared = Value("i", -1)
        best_shared.value = -1
        running = Value("i", 1)
        p = Process(target = strategy(player), args = (board, player, best_shared, running))
        p.start()
        t1 = time.time()
        p.join(time_limit)
        running.value = 0
        time.sleep(0.01)
        p.terminate()
        time.sleep(0.01)
        if p.is_alive(): os.kill(p.pid, signal.SIGKILL)
        move = best_shared.value
        print("move = ", move)
        board = ref.make_move(move, player, board)
        print(ref.score(player, board))
        print(ref.display(board))
        player = ref.next_player(board, player)

    black_score = ref.score(core.BLACK, board)
    if black_score > 0:
        winner = black_name
    elif black_score < 0:
        winner = white_name
    else:
        winner = "TIE"

    return board, ref.score(core.BLACK, board)


if __name__ == "__main__":
    tournament_player(ai1.best_strategy, ai2.best_strategy, "black", "white", 10)

