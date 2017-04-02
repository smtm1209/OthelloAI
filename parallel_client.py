#!/usr/bin/python3

import sarkistrat as ai
import Othello_Core as core
import time
from multiprocessing import Process, Value
import os, signal, sys, getopt

ref = ai.sarkiref()

def tournament_player(black_choice, white_choice, black_name="Black", white_name="White", time_limit=5, games=2):
	""" runs a tournament of an even number of games, alternating black/white with each strategy
		and returns the results """
	ai1_wins = 0
	pg = False
	for i in range(games):
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
	print("strategy A won", ai1_wins, "out of", 2*games)
	return ai1_wins


def play(black_strategy, white_strategy, black_name, white_name, time_limit=60, pg=False):
	"""Play a game of Othello and return the final board and score."""
	board = ref.initial_board()
	player = core.WHITE
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
		print("{} move = ".format(player), move)
		board = ref.make_move(move, player, board)
		print("{} score = ".format(player), ref.score(player, board))
		ref.display(board)
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
	helpString ="""Usage: python parallel_client.py [ARGS...]
-a -AI1 [integer]\t: depth of AI1's alpha-beta search (default/max: 15, negative: random AI)
-b -AI2 [integer]\t: depth of AI2's alpha-beta search (default/max: 15, negative: random AI)
-t -timelimit [integer]\t: time limit per move (default: 10, min: 2)
-g -games [integer]\t: number of games to play (default: 2, min: 1)
-h -help\t\t: display this help dialog"""
	ai1, ai2, timelimit, games = ai.sarkistrat(), ai.sarkistrat(), 10, 2
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'ha:b:t:g:', ['help', 'AI1=', 'AI2=', 'timelimit=', 'games='])
	except getopt.GetoptError:
		print("Error: Invalid Argument\n\n" +  helpString)
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print(helpString)
			sys.exit()
		elif opt in ('-a', '-AI1'):
			a = 15
			try:
				a = min(a, int(arg))
			except:
				print('Arguments have to be integers')
				sys.exit(2)
			ai1 = ai.sarkistrat(a) if a >= 0 else ai.sarkirandom()
			print('AI1: {}'.format('RANDOM' if a < 0 else 'depth {:d} minimax'.format(a)))
		elif opt in ('-b', '-AI2'):
			b = 15
			try:
				b = min(b, int(arg))
			except:
				print('Argument have to be integers')
				sys.exit(2)
			ai2 = ai.sarkistrat(b) if b >= 0 else ai.sarkirandom()
			print('AI2: {}'.format('RANDOM' if b < 0 else 'depth {:d} minimax'.format(b)))
		elif opt in ('-t', '-timelimit'):
			t = 2
			try:
				t = max(t, int(arg))
			except:
				print('Argument have to be integers')
				sys.exit(2)
			timelimit = t
		elif opt in ('-g', '-games'):
			g = 1
			try: 
				g = max(g, int(arg))
			except:
				print('Argument have to be integers')
				sys.exit(2)
			games = g
		else:
			print('Unknown option {}'.format(opt))
			sys.exit(2)
	print('Games: {:d}, Time limit: {:d}'.format(games, timelimit))			   
	time.sleep(3)
	print('Starting...')
	time.sleep(0.5)
	tournament_player(ai1.best_strategy, ai2.best_strategy, "black", "white", timelimit, games)

