from sarkicore import sarkicore as core
import Othello_Core as core2
from random import shuffle
import multiprocessing as mp
import os
from time import sleep

inf = float('inf')

class sarkistrat:
	def __init__(self):
		self.movedict = {}
		self.core = core()

	def best_strategy(self, board, player, best_move, still_running):
		"""Run Multi-Processed Alpha-Beta, get the best move, and put it in best_move.
		   Runs while still_running evaluates to true.  
		"""     
		self.best_move = best_move
		self.still_running = still_running
		self.player = player
		self.mpalphabeta(board, player)

	def mpalphabeta(self, board, player):
		"""Places the best possible move calculated in the time alotted (10 seconds) in self.best_value"""
		for i in range(1, 18, 4):
			self.m_depth = i
			q = mp.Queue()
			if player is core2.WHITE:
				moves = self.core.legal_moves(core2.WHITE, board)
				shuffle(moves)
				jobs = [mp.Process(target=self.min_dfs, args=(q, m, self.core.make_move(m, core2.WHITE, board), 0, -inf, inf)) for m in moves]
				for job in jobs: job.start()
				for job in jobs: job.join()
				results = []
				for i in range(len(jobs)):
					results.append(q.get())
				results.sort(key=lambda x: x[1], reverse=True)
				self.best_move.value = results[0][0]
				print('AI move: ', self.best_move.value)
			elif player is core2.BLACK:
				moves = self.core.legal_moves(core2.BLACK, board)
				shuffle(moves)
				jobs = [mp.Process(target=self.max_dfs, args=(q, m, self.core.make_move(m, core2.BLACK, board), 0, -inf, inf)) for m in moves]
				for job in jobs: job.start()
				for job in jobs: job.join()
				results = []
				for i in range(len(jobs)):
					results.append(q.get())
				results.sort(key=lambda x: x[1])
				self.best_move.value = results[0][0]
				print('AI move: ', self.best_move.value)
		return
		

	def max_dfs(self, parent_q, move, board, c_depth, alpha, beta):
		"""The 'MAX' portion of the MiniMax algorithm."""
		if self.game_over(board):
			if parent_q: parent_q.put((move, self.winning_value(board)))
			else: return (-1, self.winning_value(board))
		if self.terminal(board): 
			if parent_q: parent_q.put((move, self.terminal_value(board, core2.WHITE)))
			else: return (-1, self.terminal_value(board, core2.WHITE))
		if c_depth == self.m_depth: 
			if parent_q: parent_q.put((move, self.eval(board, core2.WHITE)))		
			else: return (-1, self.eval(board, core2.WHITE))
		moves = self.core.legal_moves(core2.WHITE, board)
		ret = moves[0]
		for m in moves:
			if alpha >= beta:
				break
			val = self.min_dfs(None, -1, self.core.make_move(m, core2.WHITE, board), c_depth + 1, alpha, beta)[1]
			if val > alpha:
				alpha = val
				ret = m
		if parent_q: parent_q.put((move, alpha)) 
		else: return (ret, alpha)
					
	def min_dfs(self, parent_q, move, board, c_depth, alpha, beta):
		"""The 'MIN' portion of the MiniMax algorithm."""
		if self.game_over(board):
			if parent_q: parent_q.put((move, self.winning_value(board)))
			else: return (-1, self.winning_value(board))
		if self.terminal(board): 
			if parent_q: parent_q.put((move, self.terminal_value(board, core2.BLACK)))
			else: return (-1, self.terminal_value(board, core2.BLACK))
		if c_depth == self.m_depth: 
			if parent_q: parent_q.put((move, self.eval(board, core2.BLACK)))
			else: return (-1, self.eval(board, core2.BLACK))
		moves = self.core.legal_moves(core2.WHITE, board)
		ret = moves[0]
		for m in moves:
			if alpha >= beta:
				break
			val = self.max_dfs(None, -1, self.core.make_move(m, core2.WHITE, board), c_depth + 1, alpha, beta)[1]
			if val < beta:
				beta = val
				ret = m
		if parent_q: parent_q.put((move, beta))
		else: return (ret, beta)
	
	def game_over(self, board):
		"""Returns true if neither player has any moves, else false"""
		return not self.core.any_legal_move(core2.WHITE, board) and not self.core.any_legal_move(core2.BLACK, board)

	def winning_value(self, board):
		"""Returns the winning value on board"""
		if self.core.score(core2.WHITE, board) > 0:
			return inf
		elif self.core.score(core2.WHITE, board) < 0:
			return -inf
		else:
			return 0
		
	def terminal(self, board):
		"""Returns true if either player has no move, else false"""
		return not self.core.any_legal_move(core2.WHITE, board) or not self.core.any_legal_move(core2.BLACK, board)

	def terminal_value(self, board, player):
		"""Returns a value that will influence the MiniMax algorithm based on a scoring matrix heuristic."""
		if player is core2.WHITE:
			if not self.core.any_legal_move(core2.WHITE, board):
				return -inf
			else:
				return self.core.score(core2.WHITE, board) + 5
		else:
			if not self.core.any_legal_move(core2.BLACK, board):
				return inf
			else:
				return -self.core.score(core2.BLACK, board) - 5

	def eval(self, board, player):
		"""Returns the intermediate evaluation of board using a scoring matrix heuristic."""
		return self.core.score(player, board) if player is core2.WHITE else -self.core.score(player, board)


class sarkirandom:
	"""Random 'AI' for testing."""
	def __init__(self):
		self.core = core()

	def best_strategy(self, board, player, best_move, still_running):
		"""Places a random, legal move into best_move"""
		move = self.random_move(board, player)
		best_move.value = move
		print("RAND move: ", move)
		return move		
		

	def random_move(self, board, player):
		"""Returns a legal, random move"""
		l = self.core.legal_moves(player, board)
		shuffle(l)
		return l[0]

class sarkiref:
	"""Referee class to facilitate games"""
	def __init__(self):
		self.core = core()
	
	def initial_board(self):
		"""Return the empty board"""
		return self.core.initial_board()

	def display(self, board):
		"""Print board formatted to StdOut"""
		print(self.core.print_board(board)) 

	def make_move(self, move, player, board):
		"""Return a mutated copy of board that reflects move"""
		return self.core.make_move(move, player, board)

	def next_player(self, board, player):
		"""Return the next player to move. Could not neccesarily be the other player."""
		return self.core.opponent(player) if self.any_legal_move(self.core.opponent(player), board) else player if self.any_legal_move(player, board) else None

	def is_legal_move(self, move, player, board):
		"""Returns if a move is legal"""
		return self.core.is_legal(move, player, board)

	def any_legal_move(self, player, board):
		"""Returns if a player has any possible move on board"""
		return self.core.any_legal_move(player, board)

	def score(self, player, board):
		"""Returns the score of player in the given board"""
		ret = 0 
		for i in self.core.squares():
			if board[i] is player:
				ret += 1
			elif board[i] is self.core.opponent(player):
				ret -= 1
		return ret

if __name__ == '__main__': #DEBUG
	print(core2.WHITE)
	print(core2.BLACK)
