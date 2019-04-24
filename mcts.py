"""Monte Carlo Tree Search."""
import time
# https://www.baeldung.com/java-monte-carlo-tree-search
# https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/


class Node:
	"""Node object for trie."""

	# State is a point of a game
	# Parent is the parent node to the node
	# Children are other nodes that branch off this node
	def __init__(self, state, parent):
		"""Initilise the node."""
		self.state = state
		self.parent = parent
		self.children = dict()


class Tree:
	"""Tree data structure."""

	def __init__(self):
		"""Initilise the tree."""
		self.root = Node()


class State:
	"""A state the game is in."""

	def __init__(self, board, tiles, playerNo, move):
		"""Initilise the state."""
		self.board = board
		self.tiles = tiles
		self.playerNo = playerNo
		self.visitCount = 0
		self.winScore = 0
		self.move = move


class MonteCarloTreeSearch:
	"""MCTS class."""

	def __init__(self, score, level, opponents):
		"""Initilise search."""
		self.score = score
		self.level = level
		self.opponents = opponents

	def update(self, state):
		# Takes a game state, and appends it to the history.
		pass

	def get_play(self):
		# Causes the AI to calculate the best move from the
		# current game state and return it.
		pass

	def run_simulation(self):
		# Plays out a "random" game from the current position,
		# then updates the statistics tables with the result.
		pass
