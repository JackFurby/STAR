class Board:
	"""Scrabble board."""

	def __init__(self):
		"""Initilise the board."""
		self.board = [
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW'],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					[None, None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, None],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, None, None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					['TW', None, None, 'DL', None, None, None, 'DW', None, None, None, 'DL', None, None, 'TW'],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DL', None, None],
					[None, 'TL', None, None, None, 'TL', None, None, None, 'TL', None, None, None, None, None],
					[None, None, None, None, 'DW', None, None, None, None, None, 'DW', None, None, None, None],
					[None, None, None, 'DW', None, None, None, 'DL', None, None, None, 'DW', None, None, None],
					[None, None, 'DL', None, None, None, 'DL', None, 'DL', None, None, None, 'DW', None, None],
					[None, 'DW', None, None, None, 'TL', None, None, None, 'TL', None, None, None, 'DW', None],
					['TW', None, None, 'DL', None, None, None, 'TW', None, None, None, 'DL', None, None, 'TW']
					]

	def addLetter(self, letter, value, x, y):
		"""Add a letter to the board specifying x and y position."""
		x = int(x)
		y = int(y)

		if x > 14 or y > 14:
			return False
		else:
			# tile stored as list so value of tile can be stored (blanks are worth 0)
			tile = [letter.lower(), value]
			self.board[int(y)][int(x)] = tile
			return True

	def printBoard(self):
		"""Print the current state of the board."""
		for row in self.board:
			print(row)
