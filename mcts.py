"""Monte Carlo Tree Search."""
import time
import copy
# https://www.baeldung.com/java-monte-carlo-tree-search
# https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/


class Tree:
	"""Tree data structure."""

	def __init__(self, state, parent):
		"""Initilise the tree."""
		self.root = Node(state, parent)


class Node:
	"""Node object for trie."""

	# State is a point of a game
	# Parent is the parent node to the node
	# Children are other nodes that branch off this node
	def __init__(self, state, parent):
		"""Initilise the node."""
		self.state = state
		self.parent = parent
		self.children = []

	def expand(self):
		"""Expand the current node children with state.moves."""
		if len(self.children) > 0:  # Only run if not done already
			if self.state.moves == 0:
				self.state.getMoves()

			# Get the index of the next player
			if self.state.currentPlayer == (len(self.state.currentPlayer) - 1):
				nextPlayer = 0
			else:
				nextPlayer = self.state.currentPlayer + 1

			for i in self.state.moves:
				updatedPlayers = copy.deepcopy(self.state.players)
				updatedPlayers[self.state.currentPlayer][1] += i[1]
				self.children.append(State(
					self.state.board,
					self.state.tiles,
					updatedPlayers,
					nextPlayer,
					self.trie,
					self.state.targetPlayer
				))


class State:
	"""A state the game is in."""

	def __init__(self, board, tiles, players, currentPlayer, trie, targetPlayer):
		"""Initilise the state."""
		self.board = board  # Copy of the board object
		self.tiles = tiles  # Copy of the tiles object
		self.players = otherPlayers  # array of player scores and probable racks, player = [rack, score]
		self.currentPlayer = currentPlayer  # Current player number (index in players)
		self.targetPlayer = targetPlayer  # Player number whick we want to win
		self.moves = []

	def getMoves(self):
		"""Get an array of all moves that the current player can make."""
		self.moves = self.board.possibleMoves(self.players[self.currentPlayer][1], trie)


class MonteCarloTreeSearch:
	"""MCTS class."""

	def __init__(self, board, tiles, players, currentPlayer, trie, targetPlayer):
		"""Initilise search."""
		self.trie = trie
		self.tree = Tree(State(board, tiles, players, currentPlayer, self.trie, targetPlayer), None)
		self. tree.root.expand()

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
