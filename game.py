"""Game environment."""
import random


class Game:
	"""Scrabble game env."""

	def __init__(self):
		"""Initilise the game."""
		self.board = Board()
		self.players = []
		self.tiles = Tiles()
		self.active = 0

	def newPlayer(self):
		"""Create a new player (max 4 per game) with no tiles."""
		if len(self.players) < 4:
			self.players.append(Player())
			return len(self.players) - 1  # Return the player index
		# Player count is 4. No more allowed
		else:
			return False

	def getPlayer(self, index):
		"""Return a player given an index."""
		return self.players[index]

	def activePlayer(self):
		"""Return the current active player in a given game."""
		if len(self.players) == 0:
			return False
		else:
			return self.players[self.active]

	def nextPlayer(self):
		"""Update active to active +1 wraping to first player after last one."""
		if len(self.players) == 0:
			return False
		# At end of player list. Go back to first one
		elif self.active == len(self.players) - 1:
			self.active = 0
		# Change active player to next player
		else:
			self.active = self.active + 1


class Board:
	"""Scrabble board."""

	def __init__(self):
		"""Initilise the board."""
		self.board = [
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW'],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					['TW', None, None, 'DL', None, None, None, 'DW', None, None, None, 'DL', None, None, 'TW'],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW']
					]
		self.playedTiles = 0

	def addLetter(self, letter, value, x, y):
		"""Add a letter to the board specifying x and y position."""
		x = int(x)
		y = int(y)

		# Tile cannot be out of range
		if (x > 14 or x < 0) or (y > 14 or y < 0):
			return False
		# tile cannot be onto of another tile
		elif self.board[int(y)][int(x)] not in [None, 'DL', 'DW', 'TL', 'TW']:
			return -1
		else:
			# tile stored as list so value of tile can be stored (blanks are worth 0)
			tile = [letter.lower(), value]
			self.board[int(y)][int(x)] = tile
			self.playedTiles = self.playedTiles + 1
			return True

	def checkWord(self, x, y, direction, beginning):
		"""Given the x, y, and if the word stats, ends or contains that tile will return true or false if the word is valid."""

	def addLetters(self, letters, x, y, direction):
		"""Add letters one at a time from word input, checks it and calls itself."""
		# Place tile
		letterPlacement = self.addLetter(letters[0][0], letters[0][1], x, y)

		# Set default values
		nextToTiles = False  # True if tile played is next to tile(s) already in play
		score = 0  # Score of current go

		if letterPlacement is False:
			return False, nextToTiles, score
		elif letterPlacement is -1:
			if direction == 'right':
				return self.addLetters(letters, x + 1, y, 'right')
			else:
				return self.addLetters(letters, x, y + 1, 'down')
		else:
			del letters[0]

			# Check tiles next to each tiles places to see if they add to existing words
			# If true the new word will be checked and return False if not valid
			if direction == 'right':
				# If tile above and below is not empty
				if self.board[int(y - 1)][int(x)] not in [None, 'DL', 'DW', 'TL', 'TW'] and self.board[int(y + 1)][int(x)] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, direction, None)
					if newWord is False:
						return False, nextToTiles, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile above is not empty
				elif self.board[int(y - 1)][int(x)] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, direction, False)
					if newWord is False:
						return False, nextToTiles, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile below is not empty
				elif self.board[int(y + 1)][int(x)] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, direction, True)
					if newWord is False:
						return False, nextToTiles, score
					else:
						nextToTiles = True
						score = score + wordScore
			else:
				# If tile left and right is not empty
				if self.board[int(y)][int(x - 1)] not in [None, 'DL', 'DW', 'TL', 'TW'] and self.board[int(y)][int(x + 1)] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, direction, None)
					if newWord is False:
						return False, nextToTiles, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile left is not empty
				elif self.board[int(y)][int(x - 1)] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, direction, False)
					if newWord is False:
						return False, nextToTiles, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile right is not empty
				elif self.board[int(y)][int(x + 1)] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, direction, True)
					if newWord is False:
						return False, nextToTiles, score
					else:
						nextToTiles = True

		# If at the end of tiles being added to the board check word is accepted
		if len(letters) == 0:
			newWord, wordScore = self.checkWord(x, y, direction, False)
			if newWord is False:
				return False, nextToTiles, score
		# tile placed, move to next tile
		else:
			if direction == 'right':
				return self.addLetters(letters, x + 1, y, 'right')
			else:
				return self.addLetters(letters, x, y + 1, 'down')

	def addWord(self, word, x, y, direction):
		"""Add a word to the board specifying the x and y position of the first tile."""
		# Check if the word placement is valid
		# If placement is valid return score
		# If placement is not valid return False
		boardBackup = self.board.copy()

		if self.addLetters(word, x, y, direction) is False:
			self.board = boardBackup
			return False
		else:
			return True

	def printBoard(self):
		"""Print the current state of the board."""
		for row in self.board:
			print(row)


class Tiles:
	"""Scrabble tiles available and for each player."""

	def __init__(self):
		"""Initilise the board."""
		# All tiles with quantity
		startingLetters = [
						['a', 9],
						['b', 2],
						['c', 2],
						['d', 4],
						['e', 12],
						['f', 2],
						['g', 3],
						['h', 2],
						['i', 9],
						['j', 1],
						['k', 1],
						['l', 4],
						['m', 2],
						['n', 6],
						['o', 8],
						['p', 2],
						['q', 1],
						['r', 6],
						['s', 4],
						['t', 6],
						['u', 4],
						['v', 2],
						['w', 2],
						['x', 1],
						['y', 2],
						['z', 1],
						['?', 2]]

		# Available letters that have not been played or held by a played
		self.letters = []

		# Fills array of letters with all tiles for a game in a random order
		while len(startingLetters) > 0:
			index = random.randint(0, len(startingLetters) - 1)
			# If the last letter is being added then remove it from the array
			if startingLetters[index][1] == 1:
				letter = startingLetters[index][0]
				del startingLetters[index]
			else:
				letter = startingLetters[index][0]
				startingLetters[index][1] = startingLetters[index][1] - 1

			self.letters.append(letter)

	def takeLetter(self):
		"""Remove a letter from self.letters and return it."""
		if len(self.letters) > 0:
			index = random.randint(0, len(self.letters) - 1)
			letter = self.letters[index]
			del self.letters[index]
			return letter
		else:
			return None

	def printLetters(self):
		"""Print the current letters not taken in the game."""
		print(self.letters)


class Player:
	"""A player instance for the game."""

	def __init__(self):
		"""Initilise the player."""
		self.letters = [None] * 7
		self.score = 0

	def takeLetters(self, gameLetters):
		"""Add letters to player until player has 7 letters."""
		for i in range(len(self.letters)):
			if self.letters[i] is None:
				self.letters[i] = gameLetters.takeLetter()

	def printLetters(self):
		"""Print the current letters the player has to use."""
		print(self.letters)

	def printScore(self):
		"""Print the players score."""
		print(self.score)


def letterScore(letter):
	"""Return a score a given letter is worth."""
	return {
		'a': 1,
		'b': 3,
		'c': 3,
		'd': 2,
		'e': 1,
		'f': 4,
		'g': 2,
		'h': 4,
		'i': 1,
		'j': 8,
		'k': 5,
		'l': 1,
		'm': 3,
		'n': 1,
		'o': 1,
		'p': 3,
		'q': 10,
		'r': 1,
		's': 1,
		't': 1,
		'u': 1,
		'v': 4,
		'w': 4,
		'x': 8,
		'y': 4,
		'z': 10,
		'?': 0,
	}[letter]
