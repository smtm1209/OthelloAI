import Othello_Core as core2
from Othello_Core import OthelloCore as core
import random

SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 40, -20, 20, 5, 5, 20, -20, 40, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -20, -40, -5, -5, -5, -5, -40, -20, 0,
    0, 40, -20, 20, 5, 5, 20, -20, 40, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]


class sarkicore(core):

	def __init__(self):
		pass
	
	def find_bracket(self, square, player, board, direction):
		"""
		Find a square that forms a bracket with `square` for `player` in the given
		`direction`.  Returns None if no such square exists.
		Returns the index of the bracketing square if found
		"""
		ans = None
		i = square + direction
		#print(i, board[i])
		while(board[i] == self.opponent(player)):
			ans = i
			i += direction
			#print(i, board[i])
		return None if ans is None else i if board[i] is player else None

	def is_valid(self, move):
		"""Is move a square on the board?"""
		return move in self.squares()

	def opponent(self, player):
		"""Get player's opponent piece."""
		return core2.BLACK if player is core2.WHITE else core2.WHITE

	def is_legal(self, move, player, board):
		"""Is this a legal move for the player?"""
		for dire in core2.DIRECTIONS:
			if self.find_bracket(move, player, board, dire):
				return True
		return False

	def make_move(self, move, player, board):
		"""Update the board to reflect the move by the specified player."""
		nb = board[:]
		for dire in core2.DIRECTIONS:
			brac = self.find_bracket(move, player, nb, dire)	
			if brac:
				self.make_flips(move, player, nb, dire)
		nb[move] = player
		return nb
				


	def make_flips(self, move, player, board, direction):
		"""Flip pieces in the given direction as a result of the move by player."""
		final = self.find_bracket(move, player, board, direction)
		if not final: return
		for i in range(move + direction, final, direction):
			board[i] = player

	def legal_moves(self, player, board):
		"""Get a list of all legal moves for player, as a list of integers"""
		ret = []
		for i in self.squares():
			if board[i] is core2.EMPTY and self.is_legal(i, player, board):
				ret.append(i)
		return ret

	def any_legal_move(self, player, board):
		"""Can player make any moves? Returns a boolean"""
		return len(self.legal_moves(player, board)) > 0

	def next_player(self,board, prev_player):
		"""Which player should move next?  Returns None if no legal moves exist."""
		if any_legal_move(self.opponent(prev_player), board):	
			return self.opponent(prev_player)
		elif any_legal_move(prev_player, board):
			return prev_player
		else:
			return None

	def score(self,player, board):
		"""Compute player's score (number of player's pieces minus opponent's)."""
		score = 0
		for i in range(10):
			for j in range(10):
				if board[i*10 + j] == player:
					score += SQUARE_WEIGHTS[i*10 + j]
				elif board[i*10 + j] == self.opponent(player):
					score -= SQUARE_WEIGHTS[i*10 + j]
		return score	 

if __name__ == '__main__': #DEBUG 
	print(core2.WHITE)
	print(core2.BLACK)
