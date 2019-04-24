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

	def __init__(self, board, tiles, playerNo, playerTiles, move):
		"""Initilise the state."""
		self.board = board  # Copy of the board object
		self.tiles = tiles  # Copy of the tiles still in play (not in a player rack)
		self.playerNo = playerNo  # Number of players in the game
		self.playerTiles = playerTiles  # Current player rack
		self.winScore = 0  # Score of best game from that node (known)


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
