"""Monte Carlo Tree Search."""
import time
import copy
import math
import random
# https://www.baeldung.com/java-monte-carlo-tree-search
# https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/


class Tree:
	"""Tree data structure."""

	def __init__(self, state):
		"""Initilise the tree."""
		self.root = Node(state, None)


class Node:
	"""Node object for trie."""

	def __init__(self, state, parent):
		"""Initilise the node."""
		self.state = state  # State is a point of a game
		self.parent = parent  # Parent is the parent node to the node
		self.children = []  # Children are other nodes that branch off this node
		self.score = 0  # The sum of all scores backpropagated up
		self.visits = 0  # The depth of nodes from this node (how many times we have visited this node)
		self.bias = 2  # The biad used in caculating the next node to visit

	def expand(self, trie):
		"""Expand the current node children with state.moves."""
		if len(self.children) == 0:  # Only run if not done already
			if len(self.state.moves) == 0:
				self.state.getMoves(trie)

			for i in self.state.moves:
				newNode = self.makeFromMove(i, trie)
				#newNode.updateFromMove(trie)

	def newChild(self, move, trie):
		remainingTiles = []

		# Clone remaining tiles
		for i in self.state.remainingTiles:
			remainingTiles.append(i[:])

		newNode = Node(State(
			self.state.players.copy(),
			self.state.tiles.copy(),
			remainingTiles,
			updatedPlayers,
			nextPlayer,
			self.state.targetPlayer,
			gameEnd,
			move
		), self)

		self.children.append(newNode)

		return newNode

	def makeFromMove(self, move, trie):
		"""Make a new node given a move."""
		# Get the index of the next player
		if self.state.currentPlayer == (len(self.state.players) - 1):
			nextPlayer = 0
		else:
			nextPlayer = self.state.currentPlayer + 1

		#print('first:', self.state.players)

		updatedPlayers = []

		# Clone players
		for i in self.state.players:
			player = []
			for j in i:
				if type(j) == int:
					player.append(j)
				else:
					player.append(j[:])
			updatedPlayers.append(player)

		remainingTiles = []

		# Clone remaining tiles
		for i in self.state.remainingTiles:
			remainingTiles.append(i[:])

		#updatedPlayers = copy.deepcopy(self.state.players)
		updatedBoard = self.state.board.copy()
		updatedTiles = self.state.tiles.copy()
		#remainingTiles = copy.deepcopy(self.state.remainingTiles)

		# Convert tiles into a format that can be placed on the board + place tiles
		playerTiles = []
		for tile in move[5]:
			playerTiles.append([tile[1], tile[2]])
			updatedPlayers[self.state.currentPlayer][0][tile[0]] = None # Remove tile from player
		updatedBoard.addLetters(playerTiles, move[2], move[3], move[4], trie)  # Add word to board (we already have score so dont need to run addWord)

		# Update player tiles + game tiles
		newTiles, updatedRemainingTiles = updatedTiles.getProbableTiles(updatedBoard, len(move[5]), updatedPlayers[0], remainingTiles)
		# Remove all elements that are None from player

		for i in range(len(updatedPlayers[self.state.currentPlayer][0])):
			if updatedPlayers[self.state.currentPlayer][0][i] is None:
				if len(newTiles) > 0:
					updatedPlayers[self.state.currentPlayer][0][i] = newTiles[0]
					del newTiles[0]

		updatedPlayers[self.state.currentPlayer][1] += move[1]  # Add move score to player

		# If this move caused an end game then set gameEnd to true
		if updatedBoard.playedTiles + sum(len(x[0]) for x in updatedPlayers) is 100:
			gameEnd = True
		else:
			gameEnd = False

		#print(id(updatedRemainingTiles))
		#print(updatedRemainingTiles)
		#print(tempTiles)
		#print(id(tempTiles))
		#print(tempTiles)
		#print(updatedPlayers)
		#print(id(updatedPlayers))
		#print(updatedBoard.printBoard())
		#print('move:', move)

		newNode = Node(State(
			updatedBoard,
			updatedTiles,
			updatedRemainingTiles,
			updatedPlayers,
			nextPlayer,
			self.state.targetPlayer,
			gameEnd,
			move
		), self)

		self.children.append(newNode)

		return newNode

	def selectNode(self, final=False):
		"""From the current node select the child node to explore next."""
		selectedChild = self.children[0]  # Select the first child if no other child looks good
		maxUCB1 = 0  # this is only used if all children are not infinite (score and visits are not 0)
		infiniteFound = False
		for i in self.children:
			# If node has not been visited before then set its UCB1 score to infinite
			if i.visits is 0:
				if final is False:  # IF final is true we dont want to look at nodes that have not been searched (we are picking the best move)
					selectedChild = i
					maxUCB1 = 0
					infiniteFound = True
			# If node has been visited then caculate its UCB1 score and if higher than previous max then then update that
			else:
				# http://mcts.ai/about/
				ucb1 = ((i.score / i.visits) + i.bias) * math.sqrt(math.log(i.parent.visits) / i.visits)
				# Only update selectedChild if an infinite node has not been found
				if infiniteFound is not True:
					if ucb1 > maxUCB1:
						maxUCB1 = ucb1
						selectedChild = i

		return selectedChild

	def backpropagation(self, score=0, visit=0):
		"""Update all parent nodes score and visit count."""
		self.score += score
		self.visits += visit

		# Only continue when there are more parents to go to
		if self.parent is not None:
			self.parent.backpropagation(score, visit)

	def simulate(self, trie):
		"""Run through a game picking random moves until the game is over."""
		moves = self.state.getMoves(trie)
		if self.state.gameEnd is False and len(moves) > 0:
			#print("self:", self.state.getMoves(trie))
			#print(self.state.players)
			nextNode = self.makeFromMove(random.choice(moves), trie)
			return nextNode.simulate(trie)  # select child until game is over
		else:
			targetPlayerScore = self.state.players[self.state.targetPlayer][1]
			highestOtherScore = 0
			# Get highest score which is not target player
			for i in range(len(self.state.players) - 1):
				if i is not self.state.targetPlayer:
					if self.state.players[i][1] > highestOtherScore:
						highestOtherScore = self.state.players[i][1]
			return self



class State:
	"""A state the game is in."""

	def __init__(self, board, tiles, remainingTiles, players, currentPlayer, targetPlayer, gameEnd, moveMade):
		"""Initilise the state."""
		self.board = board  # Copy of the board object
		self.tiles = tiles  # Copy of the tiles object
		self.remainingTiles = remainingTiles  # List of tiles that are probably remaining to be picked
		self.players = players  # array of player scores and probable racks, player = [rack, score]
		self.currentPlayer = currentPlayer  # Current player number (index in players)
		self.targetPlayer = targetPlayer  # Player number whick we want to win
		self.moves = []
		self.gameEnd = gameEnd  # If this state leads to an end game or not
		self.moveMade = moveMade  # The move that was made to get to that node

	def getMoves(self, trie):
		"""Get an array of all moves that the current player can make."""
		# Only work out moves if not done already
		if len(self.moves) is 0:                                                                                           #<<<<<<<<<<< Add skip go and swap tiles
			self.moves = self.board.possibleMoves(self.players[self.currentPlayer][0], trie)
		return self.moves


class MonteCarloTreeSearch:
	"""MCTS class."""

	def __init__(self, board, tiles, players, currentPlayer, trie, targetPlayer, gameEnd, remainingTiles):
		"""Initilise search."""
		self.trie = trie
		self.tree = Tree(State(board, tiles, remainingTiles, players, currentPlayer, targetPlayer, gameEnd, None))
		self.tree.root.state.getMoves(self.trie)
		self.tree.root.expand(self.trie)

	def run(self, runTime):
		"""Run MCST until time runs out."""
		startTime = time.time()

		while time.time() - startTime < runTime:  # Only continue to serch for a specified number of seconds
			# Select node
			currentNode = self.tree.root.selectNode()
			print("-----------")
			print("Current search")
			print()
			print("Node score:", currentNode.score)
			print("Node visits:", currentNode.visits)
			print("Move:", currentNode.state.moveMade)
			print("Player:", currentNode.state.currentPlayer)
			print("-----------")
			while len(currentNode.children) > 0:
				currentNode = currentNode.selectNode()

			# If node is not infinate then expand
			if currentNode.score is not 0 and currentNode.visits is not 0:
				currentNode.expand(self.trie)
				# Only move to new node if there are nodes to move to
				if len(currentNode.children) > 0:
					currentNode = currentNode.children[0]  # Select first child (all will be infinate ATM)

			# simulate + backprop
			finalNode = currentNode.simulate(self.trie)

			targetPlayerScore = finalNode.state.players[finalNode.state.targetPlayer][1]
			highestOtherScore = 0
			# Get highest score which is not target player
			for i in range(len(finalNode.state.players)):
				if i is not finalNode.state.targetPlayer:
					if finalNode.state.players[i][1] > highestOtherScore:
						highestOtherScore = finalNode.state.players[i][1]
			score = targetPlayerScore - highestOtherScore  # Return the score of target player minus highest other player

			finalNode.backpropagation(score, 1)
		else:
			return self.tree.root.selectNode(True)  # Return the best move found
