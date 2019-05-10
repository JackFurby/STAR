"""Game environment."""
import random
from trie import Trie
from setup import setup, save_trie, load_trie
import copy


class Game:
	"""Scrabble game env."""

	def __init__(self):
		"""Initilise the game."""
		self.board = Board()
		self.players = []
		self.tiles = Tiles()
		self.active = 0
		self.over = False  # True if the game is over
		# trie = Trie()
		# setup(trie)
		# save_trie(trie, 'v1')
		self.trie = load_trie('v1')  # Word list

	def copy(self):
		return copy.deepcopy(self)

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
		# If no players exist return False
		if len(self.players) == 0:
			return False
		# If players exist then return the player requested
		else:
			# If player requested does not exist then return False
			if len(self.players) < (index + 1):
				return False
			else:
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

		"""self.board = [['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW'],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					[None, None, 'DW', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					['TW', None, None, 'DL', None, None, None, ['g', 2], None, None, None, 'DL', None, None, 'TW'],
					[None, None, ['d', 2], ['u', 1], ['e', 1], ['t', 1], ['t', 1], ['o', 1], 'DL', None, None, None, 'DL', None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					['DL', None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, 'DL'],
					[None, None, 'DW', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW']]
		self.playedTiles = 7"""

		self.board = [
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
		self.playedTiles = 0
		self.emptyTiles = [None, 'DL', 'DW', 'TL', 'TW']  # Type of spaces on the board that are empty

	def copy(self):
		return copy.deepcopy(self)

	def extendLeft(self, x, y, direction, letters, trie, playedTiles=None, currentNode=None, TileClose=False, nextTile=None, extraScore=0):
		"""Return moves that can be made given a starting position, player and direction."""
		# list of all words found
		words = []

		# If starting to search for moves then get head of trie
		if currentNode is None:
			currentNode = trie.head

		# If starting to search for moves then set played tiles to an empty array
		if playedTiles is None:
			playedTiles = []

		# if word found, at least one player letter has been used, word is next to existing tiles and the next tile is not populated
		if currentNode.end and (len(letters) < 7) and TileClose and nextTile in self.emptyTiles:
			if direction == 'right':
				startX = x - len(currentNode.data[0]) + 1  # end of word x coordinate - lengh of word found + 1 to correct offset
				startY = y
			else:
				startX = x
				startY = y - len(currentNode.data[0]) + 1 # end of word y coordinate - lengh of word found + 1 to correct offset

			# If all letters placed then add 50 to score
			if len(playedTiles) is 7:
				allLetters = 50
			else:
				allLetters = 0

			# Score for the main new word
			score = 0
			multiplierTotal = 1
			mainWord, mainWordList = self.getBoardSpaces(startX, startY, x, y, direction)
			i = 0  # The index of the player tile currently being evaluated
			for space in mainWordList:
				if space is None:
					score = score + letterScore(playedTiles[i][1])
					i += 1
				elif space is 'DL':
					score = score + (letterScore(playedTiles[i][1]) * 2)
					i += 1
				elif space is 'TL':
					score = score + (letterScore(playedTiles[i][1]) * 3)
					i += 1
				elif space is 'DW':
					multiplierTotal += 2
					i += 1
				elif space is 'TW':
					multiplierTotal += 3
					i += 1
				else:
					score = score + space[1]
			score = score * multiplierTotal

			# [word made, score for move, start x position, start y position, direction of word, [index of player tile, char, char score]]
			words.append([currentNode.data[0], extraScore + score + allLetters, startX, startY, direction, playedTiles])

		nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(x, y)

		if not TileClose:
			if x == 7 and y == 7:  # If playing on center of board (i.e. first word played)
				TileClose = True
			else:
				TileClose = nextToTile

		if direction == 'right':
			nextSpace = right
		else:
			nextSpace = down

		# If current space is occupied then add it onto the current word search and move on
		if nextSpace:
			if direction == 'right':
				letter = self.board[y][x + 1]
				if x + 2 < len(self.board[y]):
					nextLetter = self.board[y][x + 2]
				else:
					nextLetter = None
				nextX = x + 1
				nextY = y
			else:
				letter = self.board[y + 1][x]
				if y + 2 < len(self.board):
					nextLetter = self.board[y + 2][x]
				else:
					nextLetter = None
				nextX = x
				nextY = y + 1
			if letter[0] in currentNode.children:
				# Copy value of letters and playedTiles (otherwise will run into problems with only copying memory address)
				newLetters = letters.copy()
				newPlayedTiles = playedTiles.copy()
				words += self.extendLeft(nextX, nextY, direction, newLetters, trie, newPlayedTiles, currentNode.children[letter[0]], TileClose, nextLetter, extraScore)
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
						nextLetter = self.board[nextY][nextX + 1]
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
						nextLetter = self.board[nextY + 1][nextX]
			# make sure tiles are not going off the board
			if boardEnd is not True:
				# i keeps track of current letter
				# searched stop duplicate searches if input has repeated letters

				i = 0
				searched = []
				for letter in letters:
					if letter not in searched:
						searched.append(letter)
						blindWordScore = 0  # placeholder for score gain from blindCheckWord
						if letter[0] == '?':
							for char in currentNode.children:

								# If new tile creates a word in the other direction check it!
								if direction == 'right':
									nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(x + 1, y)
									if not TileClose:
										TileClose = nextToTile
									if up or down:
										newWordAccepted, blindWordScore = self.blindCheckWord(x + 1, y, [char, letterScore(char)], 'down', trie, up, down)
									# Dont need to check if another word is valid
									else:
										newWordAccepted = True
								elif direction == 'down' and (left or right):
									nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(x, y + 1)
									if not TileClose:
										TileClose = nextToTile
									if left or right:
										newWordAccepted, blindWordScore = self.blindCheckWord(x, y + 1, [char, letterScore(char)], 'right', trie, left, right)
									# Dont need to check if another word is valid
									else:
										newWordAccepted = True
								# Dont need to check if another word is valid
								else:
									newWordAccepted = True

								# Copy value of letters and playedTiles (otherwise will run into problems with only copying memory address)
								newLetters = letters.copy()
								del newLetters[i]
								if newWordAccepted:
									newPlayedTiles = playedTiles.copy()
									newPlayedTiles.append([letter[1], char, 0, '?'])
									words += self.extendLeft(nextX, nextY, direction, newLetters, trie, newPlayedTiles, currentNode.children[char], TileClose, nextLetter, extraScore + blindWordScore)
						elif letter[0] in currentNode.children:

							# If new tile creates a word in the other direction check it!
							if direction == 'right':
								nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(x + 1, y)
								if not TileClose:
									TileClose = nextToTile
								if up or down:
									newWordAccepted, blindWordScore = self.blindCheckWord(x + 1, y, [letter[0], letterScore(letter[0])], 'down', trie, up, down)
								# Dont need to check if another word is valid
								else:
									newWordAccepted = True
							elif direction == 'down':
								nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(x, y + 1)
								if not TileClose:
									TileClose = nextToTile
								if left or right:
									newWordAccepted, blindWordScore = self.blindCheckWord(x, y + 1, [letter[0], letterScore(letter[0])], 'right', trie, left, right)
								# Dont need to check if another word is valid
								else:
									newWordAccepted = True
							# Dont need to check if another word is valid
							else:
								newWordAccepted = True

							# Copy value of letters and playedTiles (otherwise will run into problems with only copying memory address)
							newLetters = letters.copy()
							del newLetters[i]
							if newWordAccepted:
								newPlayedTiles = playedTiles.copy()
								newPlayedTiles.append([letter[1], letter[0], letterScore(letter[0])])
								words += self.extendLeft(nextX, nextY, direction, newLetters, trie, newPlayedTiles, currentNode.children[letter[0]], TileClose, nextLetter, extraScore + blindWordScore)

					i += 1

		# return words found
		return words

	def possibleMoves(self, playerRack, trie):
		"""Return all possible moves a given players rack can make with the current board and player tiles."""
		# If board is empty return words from players tiles in all posible moves
		moves = []

		# Get player letters with index of each tile
		playerLetters = []
		for i in range(len(playerRack)):
			playerLetters.append([playerRack[i], i])

		# If no words played then only check words going over the center of the board (7, 7)
		if self.playedTiles == 0:
			nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(7, 7)
			for i in range(8):
				moves += self.extendLeft(6 - i, 7, 'right', playerLetters, trie)
				moves += self.extendLeft(7, 6 - i, 'down', playerLetters, trie)
		# If there are tiles on the board include them in the possible moves
		else:
			# Search the board for empty positions next to tiles in play
			for y in range(len(self.board)):
				for x in range(len(self.board[y])):
					# If current position is empty and next to a tile in play add it to list with direction a new word would have to go
					if self.board[y][x] in self.emptyTiles:
						nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(x, y)
						if nextToTile:
							if right:
								for i in range(8):
									if x - i >= -1:  # -1 is used as starting position on the board is not used to place a tile
										moves += self.extendLeft(x - i, y, 'right', playerLetters, trie)

							# If left is occupied and up is not
							if left and not up:
								if y - 1 >= -1:  # -1 is used as starting position on the board is not used to place a tile
									moves += self.extendLeft(x, y - 1, 'down', playerLetters, trie)

							if down:
								for i in range(8):
									if y - i >= -1:  # -1 is used as starting position on the board is not used to place a tile
										moves += self.extendLeft(x, y - i, 'down', playerLetters, trie)

							# If up is occupied and left is not
							if up and not left:
								if x - 1 >= -1:  # -1 is used as starting position on the board is not used to place a tile
									moves += self.extendLeft(x - 1, y, 'right', playerLetters, trie)

		return moves

	def nextToTiles(self, x, y):
		"""Given a grid location this will return if there are surrounding tiles and which ones they are."""
		# nextToTile will be true if the position being searched is next to another tile
		# left, right, up and down will be true if there is a tile in that direction of the position
		# leftEnd, rightEnd, upEnd and downEnd will be true if the position being searched is next to the end of the board (in that direction)
		nextToTile = False

		# If the tile to the left of the input is on the board
		if x - 1 >= 0:
			leftEnd = False
			if self.board[y][x - 1] not in self.emptyTiles:
				nextToTile = True
				left = True
			else:
				left = False
		elif x - 1 < 0:
			leftEnd = True
			left = False

		if x + 1 <= len(self.board[y]) - 1:
			rightEnd = False
			if self.board[y][x + 1] not in self.emptyTiles:
				nextToTile = True
				right = True
			else:
				right = False
		elif x + 1 > len(self.board[y]) - 1:
			rightEnd = True
			right = False

		if y - 1 >= 0:
			upEnd = False
			if self.board[y - 1][x] not in self.emptyTiles:
				nextToTile = True
				up = True
			else:
				up = False
		elif y - 1 < 0:
			upEnd = True
			up = False

		if y + 1 <= len(self.board) - 1:
			downEnd = False
			if self.board[y + 1][x] not in self.emptyTiles:
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
		elif self.board[y][x] not in self.emptyTiles:
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
				if (x < 0 or y < 0) or self.board[y][x] in self.emptyTiles:
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
				if (x > 14 or y > 14) or self.board[y][x] in self.emptyTiles:
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
				if (x < 0 or y < 0) or self.board[y][x] in self.emptyTiles:
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
				if (x > 14 or y > 14) or self.board[y][x] in self.emptyTiles:
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
		"""Return a string of tiles given a start and end location on the board."""
		wordListY = self.board[startY:endY + 1]
		wordListX = [item[startX:endX + 1] for item in wordListY]
		if direction == 'right':
			wordList = wordListX[0]
		else:
			wordList = [item[0] for item in wordListX]

		wordListFormatted = [x for x in wordList if x is not None]  # Remove None from list
		word = ''.join([item[0] for item in wordListFormatted])

		return word, wordList

	def blindCheckWord(self, x, y, letter, direction, trie, before, after):
		"""
		Will return true or false if the word to create is valid.
		Will return the score gained from the new word

		* x and y is the location of the tile to be placed
		* the letter is a tile that is being placed and if the tile is blank or not (in the format [letter, True/False])
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
			part1Score = sum(map(lambda x: int(x[1]), wordList1))  # Sum of tile scores before new tile
		else:
			part1 = ''
			part1Score = 0

		# Get word placed on board after the tile to be placed
		if after:
			if direction == 'right':
				newX = x + 1
				newY = y
			else:
				newX = x
				newY = y + 1
			startX2, startY2, endX2, endY2 = self.findWordPosition(newX, newY, True, direction)
			part2, wordList2 = self.getBoardSpaces(startX2, startY2, endX2, endY2, direction)
			part2Score = sum(map(lambda x: int(x[1]), wordList2))  # Sum of tile scores after new tile
		else:
			part2 = ''
			part2Score = 0

		# Get the word and letter multiplyer
		if self.board[y][x] is 'DL':
			multiplierTotal = 1
			letterMultiplier = 2
		elif self.board[y][x] is 'TL':
			multiplierTotal = 1
			letterMultiplier = 3
		elif self.board[y][x] is 'DW':
			multiplierTotal = 2
			letterMultiplier = 1
		elif self.board[y][x] is 'TW':
			multiplierTotal = 3
			letterMultiplier = 1
		else:
			multiplierTotal = 1
			letterMultiplier = 1

		word = part1 + letter[0] + part2  # construct word
		wordScore = (part1Score + part2Score + (letter[1] * letterMultiplier)) * multiplierTotal  # Total word score

		# checks if the word found is accepted
		if trie.hasWord(word.lower()):
			return True, wordScore
		else:
			# If word is a single tile down count it (single tile words are not counted as words)
			if len(word) == 1:
				return True, wordScore
			else:
				return False, wordScore

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

			nextToTile, left, right, up, down, leftEnd, rightEnd, upEnd, downEnd = self.nextToTiles(x, y)

			# Check tiles next to each tiles places to see if they add to existing words
			# If true the new word will be checked and return False if not valid
			if direction == 'right':
				# If tile above and below is not empty
				if up and down:
					newWord, wordScore = self.checkWord(x, y, 'down', None, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile above is not empty
				elif up:
					newWord, wordScore = self.checkWord(x, y, 'down', False, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile below is not empty
				elif down:
					newWord, wordScore = self.checkWord(x, y, 'down', True, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
			else:
				# If tile left and right is not empty
				if left and right:
					newWord, wordScore = self.checkWord(x, y, 'right', None, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile left is not empty
				elif left:
					newWord, wordScore = self.checkWord(x, y, 'right', False, trie, False)
					if newWord is False:
						return False, True, score
					else:
						nextToTiles = True
						score = score + wordScore
				# If tile right is not empty
				elif right:
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
				if right:
					nextToTiles = True
			else:
				if down:
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
			if self.board[int(y)][int(x - 1)] not in self.emptyTiles:
				nextToTiles = True
		else:
			if self.board[int(y - 1)][int(x)] not in self.emptyTiles:
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
			print(*row, sep='\t')

	def lookAhead(self, board, tiles, player, trie, depth=0):
		"""Take a copy of the game and recursivly play all possible moves."""
		boardCopy = board.copy()
		tilesCopy = tiles.copy()
		playerCopy = player.copy()
		return boardCopy.recursiveSearch(boardCopy, tilesCopy, playerCopy, trie)

	def recursiveSearch(self, board, tiles, player, trie, currentMoves=None, depth=0):
		"""Given a player (whos turn it is), return the moves to finish with the highest score."""

		# list of all moves found
		moves = []

		print(board.printBoard())
		print(tiles.letters)
		if len(tiles.letters) < 1:
			moves.append(currentMoves)
		elif depth < 2:
			# No maves made yet
			if currentMoves is None:
				currentMoves = []

			# Refill player tiles with most probable tiles
			player.takeProbableLetters(tiles)

			# Get all playable moves
			canPlay = self.possibleMoves(player, trie)

			# Try each playable move
			searched = []
			for move in canPlay:
				if move not in searched:
					searched.append(move)

					# Convert tiles into a format that can be placed on the board
					playerTiles = []
					for tile in move[5]:
						playerTiles.append([tile[1], tile[2]])
						player.letters[tile[0]] = None  # Remove tile from player

					boardCopy = board.copy()
					tilesCopy = tiles.copy()
					playerCopy = player.copy()
					print(playerCopy.letters)
					tilesAdded, score = boardCopy.addWord(playerTiles, move[2], move[3], move[4], trie, player)
					currentMoves.append(move)
					moves += boardCopy.recursiveSearch(boardCopy, tilesCopy, playerCopy, trie, currentMoves, depth + 1)

		# return moves found
		return moves

class Tiles:
	"""Scrabble tiles available and for each player."""

	def __init__(self):
		"""Initilise the board."""

		# Available tiles that have not been played or held by a player
		self.letters = [
						[0, 'a', 9],
						[1, 'b', 2],
						[2, 'c', 2],
						[3, 'd', 4],
						[4, 'e', 12],
						[5, 'f', 2],
						[6, 'g', 3],
						[7, 'h', 2],
						[8, 'i', 9],
						[9, 'j', 1],
						[10, 'k', 1],
						[11, 'l', 4],
						[12, 'm', 2],
						[13, 'n', 6],
						[14, 'o', 8],
						[15, 'p', 2],
						[16, 'q', 1],
						[17, 'r', 6],
						[18, 's', 4],
						[19, 't', 6],
						[20, 'u', 4],
						[21, 'v', 2],
						[22, 'w', 2],
						[23, 'x', 1],
						[24, 'y', 2],
						[25, 'z', 1],
						[26, '?', 2]]
		self.startingTileCount = sum(map(lambda x: int(x[2]), self.letters))  # Number of tiles in the game

		self.startingTiles = copy.deepcopy(self.letters)  # Starting tiles in the game

	def copy(self):
		return copy.deepcopy(self)

	def takeLetter(self):
		"""Remove a letter from self.letters and return it."""
		if sum(map(lambda x: int(x[2]), self.letters)):  # Sum of all tiles not in play
			remainingTiles = [num for num in self.letters if num[2] > 0] # List of all tiles available to take with quantity
			remainingTilesComplete = []  # list of all tiles (individual) - Makes it more like real life in terms of probability
			for i in remainingTiles:
				for j in range(i[2]):
					remainingTilesComplete.append([i[0], i[1]])  # [index of letter in self.letters, char]
			index = random.randint(0, len(remainingTilesComplete) - 1)
			letter = remainingTilesComplete[index]
			self.letters[letter[0]][2] -= 1
			return letter[1] # Only return char
		else:
			return None

	def returnTiles(self, tiles):
		"""Add tiles back into self.letters array."""
		for tile in tiles:
			for gameTile in self.letters:
				if tile is gameTile[1]:
					gameTile[2] += 1

	def takeProbableLetter(self, player):
		"""Remove a most probable tile from self.letters and return it."""
		if sum(map(lambda x: int(x[2]), self.letters)):  # Sum of all tiles not in play
			allProbableTile = sorted(self.probableTiles(), key=lambda x: -x[2])
			index = allProbableTile[0][0]
			letter = self.letters[index][0]
			self.letters[index][2] -= 1
			# If last tile for a character has been taken remove it from letters
			if self.letters[index][2] < 1:
				del self.letters[index]
			return letter
		else:
			return None

	def printLetters(self):
		"""Print the current letters not taken in the game."""
		print(self.letters)

	def getTileProbability(self, tiles):
		"""Return an array of tiles and probabilities."""
		remaining = sum(map(lambda x: int(x[2]), tiles))  # Number of tiles that are not on the board
		tileProbabilities = []
		for tile in range(len(tiles)):
			tileProbabilities.append([tile, tiles[tile][1], (tiles[tile][2]/remaining)])  # [index of tile in self.letters, letter, probability]
		return tileProbabilities

	def getRemainingTiles(self, board, playerLetters=None):
		"""Return a list of tiles that could be remaining in the game (we only know board and current player)."""
		# Tiles and quantity not on the board
		remainingTiles = copy.deepcopy(self.startingTiles)
		for y in range(len(board.board)):
			for x in range(len(board.board[y])):
				if board.board[y][x] not in board.emptyTiles:
					if board.board[y][x][1] is 0:  # Blank tile
						tile = '?'
					else:
						tile = board.board[y][x][0]
					# Update remainingTiles
					for element in remainingTiles:
						if element[0] is tile:
							element[1] -= 1

		# If player is included also remove their tiles
		if playerLetters:
			for tile in playerLetters:
				for element in remainingTiles:
					if element[1] is tile:
						element[2] -= 1

		return remainingTiles

	def probableTiles(self, board):
		"""Return all tiles with probability of being taken."""

		remainingTiles = self.getRemainingTiles(board)
		return self.getTileProbability(remainingTiles)

	def probableTilesWithPlayer(self, board, player):
		"""Return all tiles with probability of being taken (taking into account a specified player)."""

		remainingTiles = self.getRemainingTiles(board, player)
		return self.getTileProbability(remainingTiles)

	def getProbableTiles(self, board, numberOfTiles, currentPlayerTiles):
		"""Return an array of the X most probable tiles to be picked."""
		probableTiles = []

		# work out what tiles might be available with probability
		remainingTiles = self.getRemainingTiles(board, currentPlayerTiles)

		for i in range(numberOfTiles):
			probableTile = sorted(self.getTileProbability(remainingTiles), key=lambda x: -x[2])[0]
			probableTiles.append(probableTile[1])
			remainingTiles[probableTile[0]][2] -= 1

		return probableTiles, remainingTiles

	def nextProbablePlayer(self, board, player):
		"""Return an array of the 7 most probable tiles to be picked (what the next player probably has)."""
		probableTiles, remainingTiles = self.getProbableTiles(board, 7, player.letters)
		return probableTiles


class Player:
	"""A player instance for the game."""

	def __init__(self):
		"""Initilise the player."""
		self.letters = [None] * 7
		self.score = 0

	def copy(self):
		return copy.deepcopy(self)

	def takeLetters(self, gameLetters):
		"""Add letters to player until player has 7 letters."""
		for i in range(len(self.letters)):
			if self.letters[i] is None:
				self.letters[i] = gameLetters.takeLetter()

	def takeProbableLetters(self, gameLetters):
		"""Add most probable letter to player until player has 7 letters."""
		for i in range(len(self.letters)):
			if self.letters[i] is None:
				self.letters[i] = gameLetters.takeProbableLetter()

	def swapLetters(self, game, swapTiles):
		"""Swap refill player letters and add swapLetters back into board letters."""
		self.takeLetters(game.tiles)
		game.tiles.returnTiles(swapTiles)

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
