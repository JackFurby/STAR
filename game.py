"""Game environment."""
import random
from trie import Trie
import copy

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

	def extendLeft(self, x, y, direction, letters, trie, currentNode=None, TileClose=False, nextTile=None):
		"""Return moves that can be made given a starting position, player and direction."""
		# list of all words found
		words = []

		if currentNode is None:
			currentNode = trie.head

		# if word found, at least one player letter has been used, word is next to existing tiles and the next tile is not populated
		if currentNode.end and (len(letters) < 7) and TileClose and nextTile in [None, 'DL', 'DW', 'TL', 'TW']:
			if direction == 'right':
				startX = x - len(currentNode.data[0]) + 1  # end of word x coordinate - lengh of word found + 1 to correct offset
				startY = y
			else:
				startX = x
				startY = y - len(currentNode.data[0]) + 1 # end of word y coordinate - lengh of word found + 1 to correct offset

			words.append([currentNode.data, startX, startY, direction])

		nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.board.nextToTiles(x, y)

		if not TileClose:
			TileClose = nextToTile

		if direction == 'right':
			nextSpace = right
		else:
			nextSpace = down

		# If current space is occupied then add it into the current word search and move on
		if nextSpace:
			if direction == 'right':
				letter = self.board.board[y][x + 1]
				nextLetter = self.board.board[y][x + 2]
				nextX = x + 1
				nextY = y
			else:
				letter = self.board.board[y + 1][x]
				nextLetter = self.board.board[y + 2][x]
				nextX = x
				nextY = y + 1
			if letter[0] in currentNode.children:
				newLetters = letters.copy()
				words += self.extendLeft(nextX, nextY, direction, newLetters, trie, currentNode.children[letter[0]], TileClose, nextLetter)
		# add letter from player tiles into current word search
		elif len(letters) is not 0:
			if direction == 'right':
				boardEnd = rightEnd
				nextX = x + 1
				nextY = y
				if boardEnd:
					nextLetter = None
				else:
					# if next space is off the board set it to none
					if nextX + 1 > 14:
						nextLetter = None
					# if next space is on the board, see if it is populated
					else:
						nextLetter = self.board.board[nextY][nextX + 1]
			else:
				boardEnd = downEnd
				nextX = x
				nextY = y + 1
				# if next space is off the board set it to none
				if boardEnd:
					nextLetter = None
				else:
					# if next space is off the board set it to none
					if nextY + 1 > 14:
						nextLetter = None
					# if next space is on the board, see if it is populated
					else:
						nextLetter = self.board.board[nextY + 1][nextX]
			# make sure tiles are not going off the board
			if boardEnd is not True:
				# i keeps track of current letter
				# searched stop duplicate searches if input has repeated letters

				i = 0
				searched = []
				for letter in letters:
					if letter not in searched:
						searched.append(letter)
						if letter == '?':
							for char in currentNode.children:

								# If new tile creates a word in the other direction check it!
								if direction == 'right':
									nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.board.nextToTiles(x + 1, y)
									if not TileClose:
										TileClose = nextToTile
									if up or down:
										newWordAccepted = self.board.blindCheckWord(x + 1, y, char, 'down', trie, up, down)
									# Dont need to check if another word is valid
									else:
										newWordAccepted = True
								elif direction == 'down' and (left or right):
									nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.board.nextToTiles(x, y + 1)
									if not TileClose:
										TileClose = nextToTile
									if left or right:
										newWordAccepted = self.board.blindCheckWord(x, y + 1, char, 'right', trie, left, right)
									# Dont need to check if another word is valid
									else:
										newWordAccepted = True
								# Dont need to check if another word is valid
								else:
									newWordAccepted = True

								newLetters = letters.copy()
								del newLetters[i]
								if newWordAccepted:
									words += self.extendLeft(nextX, nextY, direction, newLetters, trie, currentNode.children[char], TileClose, nextLetter)
						elif letter in currentNode.children:

							# If new tile creates a word in the other direction check it!
							if direction == 'right':
								nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.board.nextToTiles(x + 1, y)
								if not TileClose:
									TileClose = nextToTile
								if up or down:
									newWordAccepted = self.board.blindCheckWord(x + 1, y, letter, 'down', trie, up, down)
								# Dont need to check if another word is valid
								else:
									newWordAccepted = True
							elif direction == 'down':
								nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.board.nextToTiles(x, y + 1)
								if not TileClose:
									TileClose = nextToTile
								if left or right:
									newWordAccepted = self.board.blindCheckWord(x, y + 1, letter, 'right', trie, left, right)
								# Dont need to check if another word is valid
								else:
									newWordAccepted = True
							# Dont need to check if another word is valid
							else:
								newWordAccepted = True

							newLetters = letters.copy()
							del newLetters[i]
							if newWordAccepted:
								words += self.extendLeft(nextX, nextY, direction, newLetters, trie, currentNode.children[letter], TileClose, nextLetter)

					i += 1

		# return words found
		return words

	def possibleMoves(self, player, trie):
		"""Return all possible moves a given player can make with the current board and player tiles."""
		# If board is empty return words from players tiles in all posible moves
		moves = []

		if self.board.playedTiles == 0:
			words = trie.wordSearch(player.letters)
			# Get all moves (all words and placements)
			for word in words:
				for x in range(len(word[0])):
					moves.append([word, 7 - x, 7, 'right'])  # [word + score, x, y, direction]
				for y in range(len(word[0])):
					moves.append([word, 7, 7 - y, 'down'])
			return moves
		# If there are tiles on the board include them in the possible moves
		else:
			# Search the board for empty positions next to tiles in play
			for y in range(len(self.board.board)):
				for x in range(len(self.board.board[y])):
					# If current position is empty and next to a tile in play add it to list with direction a new word would have to go
					if self.board.board[y][x] in [None, 'DL', 'DW', 'TL', 'TW']:
						nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.board.nextToTiles(x, y)
						if nextToTile:
							if right:
								for i in range(8):
									if x - i >= 0:
										moves += self.extendLeft(x - i, y, 'right', player.letters, trie)

							if down:
								for i in range(8):
									if y - i >= 0:
										moves += self.extendLeft(x, y - i, 'down', player.letters, trie)

			return moves


class Board:
	"""Scrabble board."""

	def __init__(self):
		"""Initilise the board."""

		self.board = [
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW'],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					[None, None, 'DW', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					['TW', None, None, 'DL', None, None, None, ['t', 1], ['a', 1], ['n', 1], None, 'DL', None, None, 'TW'],
					[None, None, 'DL', None, None, None, 'DL', ['h', 4], 'DL', None, None, None, 'DL', None, None],
					[None, 'TL', None, None, None, 'TL', None, ['a', 1], None, 'TL', None, None, None, 'TL', None],
					[None, None, None, None, 'DW', None, None, ['n', 1], None, None, 'DW', None, None, None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, 'DW', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW'],
		]
		self.playedTiles = 6




		"""self.board = [
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW'],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					[None, None, 'DW', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					['TW', None, None, 'DL', None, None, None, 'DW', None, None, None, 'DL', None, None, 'TW'],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, 'DW', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW']
					]
		self.playedTiles = 0"""

	def nextToTiles(self, x, y):
		"""Given a grid location this will return if there are surrounding tiles and which ones they are."""
		# nextToTile will be true if the position being searched is next to another tile
		# left, right, up and down will be true if there is a tile in that direction of the position
		# leftEnd, rightEnd, upEnd and downEnd will be true if the position being searched is next to the end of the board (in that direction)
		nextToTile = False

		# If the tile to the left of the input is on the board
		if x - 1 >= 0:
			leftEnd = False
			if self.board[y][x - 1] not in [None, 'DL', 'DW', 'TL', 'TW']:
				nextToTile = True
				left = True
			else:
				left = False
		elif x - 1 < 0:
			leftEnd = True
			left = False

		if x + 1 <= len(self.board[y]) - 1:
			rightEnd = False
			if self.board[y][x + 1] not in [None, 'DL', 'DW', 'TL', 'TW']:
				nextToTile = True
				right = True
			else:
				right = False
		elif x + 1 > len(self.board[y]) - 1:
			rightEnd = True
			right = False

		if y - 1 >= 0:
			upEnd = False
			if self.board[y - 1][x] not in [None, 'DL', 'DW', 'TL', 'TW']:
				nextToTile = True
				up = True
			else:
				up = False
		elif y - 1 < 0:
			upEnd = True
			up = False

		if y + 1 <= len(self.board) - 1:
			downEnd = False
			if self.board[y + 1][x] not in [None, 'DL', 'DW', 'TL', 'TW']:
				nextToTile = True
				down = True
			else:
				down = False
		elif y + 1 > len(self.board) - 1:
			downEnd = True
			down = False

		return nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd

	def addLetter(self, letter, value, x, y):
		"""Add a letter to the board specifying x and y position."""
		x = int(x)
		y = int(y)

		# Tile cannot be out of range
		if (x > 14 or x < 0) or (y > 14 or y < 0):
			return False
		# tile cannot be onto of another tile
		elif self.board[y][x] not in [None, 'DL', 'DW', 'TL', 'TW']:
			return -1
		else:
			# tile stored as list so value of tile can be stored along with tile / word multipliers
			if self.board[y][x] is 'DL':
				# [letter, value, multiplier, word / tile multiplyer, x coordinate, y coordinate]
				# x and y coordinate are stored for ease of access when updating tile applying appling multiplier
				tile = [letter.lower(), value, 2, False, x, y]
			elif self.board[y][x] is 'TL':
				tile = [letter.lower(), value, 3, False, x, y]
			elif self.board[y][x] is 'DW':
				tile = [letter.lower(), value, 2, True, x, y]
			elif self.board[y][x] is 'TW':
				tile = [letter.lower(), value, 3, True, x, y]
			else:
				tile = [letter.lower(), value]
			self.board[y][x] = tile
			self.playedTiles = self.playedTiles + 1
			return True

	def findWordPosition(self, x, y, beginning, direction):
		"""Find the start and end X and Y of a word from a given location on the word."""
		if beginning is False:
			endX = x
			endY = y

			find = True
			while find:
				if (x < 0 or y < 0) or self.board[y][x] in [None, 'DL', 'DW', 'TL', 'TW']:
					if direction == 'right':
						startY = y
						startX = x + 1
					else:
						startY = y + 1
						startX = x
					find = False
				else:
					if direction == 'right':
						x = x - 1
					else:
						y = y - 1
		elif beginning is True:
			startX = x
			startY = y

			find = True
			while find:
				if (x > 14 or y > 14) or self.board[y][x] in [None, 'DL', 'DW', 'TL', 'TW']:
					if direction == 'right':
						endY = y
						endX = x - 1
					else:
						endY = y - 1
						endX = x
					find = False
				else:
					if direction == 'right':
						x = x + 1
					else:
						y = y + 1
		else:
			middleX = x
			middleY = y

			findStart = True
			while findStart:
				if (x < 0 or y < 0) or self.board[y][x] in [None, 'DL', 'DW', 'TL', 'TW']:
					if direction == 'right':
						startY = y
						startX = x + 1
					else:
						startY = y + 1
						startX = x
					x = middleX
					y = middleY
					findStart = False
				else:
					if direction == 'right':
						x = x - 1
					else:
						y = y - 1

			findEnd = True
			while findEnd:
				if (x > 14 or y > 14) or self.board[y][x] in [None, 'DL', 'DW', 'TL', 'TW']:
					if direction == 'right':
						endY = y
						endX = x - 1
					else:
						endY = y - 1
						endX = x
					findEnd = False
				else:
					if direction == 'right':
						x = x + 1
					else:
						y = y + 1

		return startX, startY, endX, endY

	def getBoardSpaces(self, startX, startY, endX, endY, direction):
		"""Returns a string given a start and end location on the board"""
		wordListY = self.board[startY:endY + 1]
		wordListX = [item[startX:endX + 1] for item in wordListY]
		if direction == 'right':
			wordList = wordListX[0]
		else:
			wordList = [item[0] for item in wordListX]
		word = ''.join([item[0] for item in wordList])

		return word, wordList

	def blindCheckWord(self, x, y, letter, direction, trie, before, after):
		"""
		Will return true or false if the word to create is valid.

		* x and y is the location of the tile to be placed
		* the letter is a tile that is being placed (only the string char)
		* direction can either be right or down and is the direction of the word
		* before and after can be true or false and will show where the word on the board is (used with direction)

		"""

		# Get word placed on board before the tile to be placed
		if before:
			if direction == 'right':
				newX = x - 1
				newY = y
			else:
				newX = x
				newY = y - 1
			startX1, startY1, endX1, endY1 = self.findWordPosition(newX, newY, False, direction)
			part1, wordList1 = self.getBoardSpaces(startX1, startY1, endX1, endY1, direction)
		else:
			part1 = ''

		# Get word placed on board after the tile to be placed
		if after:
			if direction == 'right':
				newX = x
				newY = y + 1
			else:
				newX = x + 1
				newY = y
			startX2, startY2, endX2, endY2 = self.findWordPosition(newX, newY, True, direction)
			part2, wordList2 = self.getBoardSpaces(startX2, startY2, endX2, endY2, direction)
		else:
			part2 = ''

		word = part1 + letter + part2  # construct word

		# checks if the word found is accepted
		if trie.hasWord(word.lower()):
			return True
		else:
			# If word is a single tile down count it (single tile words are not counted as words)
			if len(word) == 1:
				return True
			else:
				return False


	def checkWord(self, x, y, direction, beginning, trie, placedWord):
		"""Given the x, y, and if the word starts, ends or contains that tile will return true or false if the word is valid."""

		startX, startY, endX, endY = self.findWordPosition(x, y, beginning, direction)

		# Gets the new word on the board as a string
		word, wordList = self.getBoardSpaces(startX, startY, endX, endY, direction)

		# Calculates word score
		multiplierTotal = 1
		wordScore = 0
		for letter in wordList:
			# If there is a multiplyer applied to the tile
			if len(letter) > 2:
				# If multiplier applies to word
				if letter[3] is True:
					multiplierTotal = multiplierTotal * letter[2]
					wordScore = wordScore + letter[1]
				# If multiplier applies to tile
				else:
					wordScore = wordScore + (letter[1] * letter[2])

				# If getting score for new word placed (not additional words created) remove multiplyer from tile on board
				if placedWord is True:
					self.board[letter[5]][letter[4]] = [letter[0], letter[1]]
			# If there is no multiplier
			else:
				wordScore = wordScore + letter[1]

		wordScore = wordScore * multiplierTotal  # Apply word multiplier

		# checks if the word found is accepted
		if trie.hasWord(word.lower()):
			return True, wordScore
		else:
			# If word is a single tile down count it (single tile words are not counted as words)
			if len(word) == 1:
				return True, 0
			else:
				return False, 0

	def addLetters(self, letters, x, y, direction, trie):
		"""Add letters one at a time from word input, checks it and calls itself."""
		# Place tile
		letterPlacement = self.addLetter(letters[0][0], letters[0][1], x, y)

		# Set default values
		nextToTiles = False  # True if tile played is next to tile(s) already in play
		score = 0  # Score of current go

		# If x or y is out of range return False
		if letterPlacement is False:
			return False, nextToTiles, score
		# If tile is placed ontop of another move to next spot and try again
		elif letterPlacement is -1:
			if direction == 'right':
				acceptedReturn, nextToTileReturn, scoreReturn = self.addLetters(letters, x + 1, y, 'right', trie)
			else:
				acceptedReturn, nextToTileReturn, scoreReturn = self.addLetters(letters, x, y + 1, 'down', trie)

			nextToTiles = True
			return acceptedReturn, nextToTiles, score + scoreReturn
		else:
			del letters[0]  # tile placed. Remove from list

			# If tile placed is in the center of the board
			if x is 7 and y is 7:
				nextToTiles = True

			# Check tiles next to each tiles places to see if they add to existing words
			# If true the new word will be checked and return False if not valid
			if direction == 'right':
				# If tile above and below is not empty
				if ((y - 1 >= 0) and self.board[y - 1][x] not in [None, 'DL', 'DW', 'TL', 'TW']) and ((y + 1 <= 14) and self.board[y + 1][x] not in [None, 'DL', 'DW', 'TL', 'TW']):
					newWord, wordScore = self.checkWord(x, y, 'down', None, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile above is not empty
				elif (y - 1 >= 0) and self.board[y - 1][x] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, 'down', False, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile below is not empty
				elif (y + 1 <= 14) and self.board[y + 1][x] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, 'down', True, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
			else:
				# If tile left and right is not empty
				if ((x - 1 >= 0) and self.board[y][x - 1] not in [None, 'DL', 'DW', 'TL', 'TW']) and ((x + 1 <= 14) and self.board[y][x + 1] not in [None, 'DL', 'DW', 'TL', 'TW']):
					newWord, wordScore = self.checkWord(x, y, 'right', None, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile left is not empty
				elif (x - 1 >= 0) and self.board[y][x - 1] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, 'right', False, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile right is not empty
				elif (x + 1 <= 14) and self.board[y][x + 1] not in [None, 'DL', 'DW', 'TL', 'TW']:
					newWord, wordScore = self.checkWord(x, y, 'right', True, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore

		# If at the end of tiles being added to the board check word is accepted
		if len(letters) == 0:
			newWord, wordScore = self.checkWord(x, y, direction, None, trie, True)

			# If last tile placed is followed by another tile mark nextToTiles as true
			if direction == 'right':
				if (x + 1 <= 14) and self.board[y][x + 1] not in [None, 'DL', 'DW', 'TL', 'TW']:
					nextToTiles = True
			else:
				if (y + 1 <= 14) and self.board[y + 1][x] not in [None, 'DL', 'DW', 'TL', 'TW']:
					nextToTiles = True

			if newWord is False:
				return False, nextToTiles, score + wordScore
			else:
				return True, nextToTiles, score + wordScore
		# tile placed, move to next tile
		else:
			if direction == 'right':
				acceptedReturn, nextToTileReturn, scoreReturn = self.addLetters(letters, x + 1, y, 'right', trie)
			else:
				acceptedReturn, nextToTileReturn, scoreReturn = self.addLetters(letters, x, y + 1, 'down', trie)

			if nextToTileReturn is True:
				nextToTiles = True
			return acceptedReturn, nextToTiles, score + scoreReturn

	def addWord(self, word, x, y, direction, trie, player):
		"""Add a word to the board specifying the x and y position of the first tile."""
		# Check if the word placement is valid
		# If placement is valid return score
		# If placement is not valid return False and return environment to previous state
		boardBackup = copy.deepcopy(self.board)
		playedTilesBackup = copy.deepcopy(self.playedTiles)
		nextToTiles = False

		if self.playedTiles == 0 and len(word) == 1:
			return False, 0

		if len(word) is 7:
			allLetters = True
		else:
			allLetters = False

		# If first tile placed is preceded by another tile mark nextToTiles as true
		if direction == 'right':
			if self.board[int(y)][int(x - 1)] not in [None, 'DL', 'DW', 'TL', 'TW']:
				nextToTiles = True
		else:
			if self.board[int(y - 1)][int(x)] not in [None, 'DL', 'DW', 'TL', 'TW']:
				nextToTiles = True

		allowed, nextToTilesReturn, score = self.addLetters(word, x, y, direction, trie)

		if nextToTilesReturn:
			nextToTiles = True

		if allowed is True and nextToTiles is True:
			if allLetters:  # All letters placed bonus
				score = score + 50
			return True, score
		else:
			self.board = boardBackup
			self.playedTiles = playedTilesBackup
			return False, score

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

	def swapLetters(self, game, swapTiles):
		"""Swap refill player letters and add swapLetters back into board letters."""
		self.takeLetters(game.tiles)
		game.tiles.letters.extend(swapTiles)

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
