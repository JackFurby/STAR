"""STAR."""
import time
from game import Board, Tiles, Game
from setup import setup, letterScore, getScore, save_trie, load_trie
from trie import Trie, Node


def numInput(userInput):
	"""Make sure the user enters an integer."""
	if userInput.isdigit():
		return int(userInput)
	else:
		userInput = input("You must enter a integer: ")
		return numInput(userInput)


if __name__ == '__main__':
	""" Example use """
	# trie = Trie()
	# setup(trie)
	# save_trie(trie, 'v1')

	trie = load_trie('v1')
	game = Game()
	currentTiles = Tiles()

	run = True

	while run:
		action = input("What do you want to do? Enter 'help' for more: ")

		if action == "\q":
			run = False
			break
		elif action == "isAccepted":
			inputLetters = input("Enter a word to check: ")

			# Makes sure input is in lower case
			inputLetters = inputLetters.lower()

			if trie.hasWord(inputLetters):
				print("Yes")
			else:
				print("No")
		elif action == "findWords":
			inputLetters = input("Enter letters ('?' is a wildcard): ")

			# Makes sure input is in lower case
			inputLetters = inputLetters.lower()

			start = time.time()
			wordList = trie.wordSearch(list(inputLetters))
			wordList.sort(key=lambda tup: -tup[1])
			print(*wordList, sep='\n')
			end = time.time()
			print("Completed search in", end - start, 'seconds')
		elif action == "board":
			game.board.printBoard()
		elif action == "addLetter":
			letter = input("Enter letter: ")
			value = numInput(input("Enter tile value: "))
			x = numInput(input("Enter x (starting from 0 in top left): "))
			y = numInput(input("Enter y (starting from 0 in top left): "))
			if game.board.addLetter(letter, value, x, y):
				print("Board updated")
			# If addLetter returns False then x or y is out of range (specified in board.py)
			else:
				print("X and Y cannot be above 14 or ontop of another tile")
		elif action == "letters":
			game.tiles.printLetters()
		elif action == "makePlayer":
			playerIndex = game.newPlayer()
			if playerIndex is not False:
				print("Player " + str(playerIndex + 1) + " created")
				# add 7 tiles to player
				game.players[playerIndex].takeLetters(game.tiles)
			else:
				print("Max player limit reached")
		elif action == "takeLetters":
			# Get the player index in array
			player = game.players[numInput(input("Enter player number: ")) - 1]
			player.takeLetters(game.tiles)
		elif action == "playerLetters":
			# Get the player index in array
			player = game.players[numInput(input("Enter player number: ")) - 1]
			player.printLetters()
		elif action == "playTurn":
			if len(game.players) == 0:
				print("No current players")
			else:
				player = game.players[game.active]

				turn = True

				while turn:
					playOption = input("Enter 1 to skip turn, 2 to swap some letters or 3 to place tile(s): ")

					# player selects what they want to do
					if playOption == '1':
						# Go skipped
						print("Go skipped")
						turn = False
					elif playOption == '2':
						# Player replaces 0 or more tiles
						player.printLetters()
						swapTiles = []  # list of tiles to swap
						stillEntering = True
						while stillEntering:
							selectedTile = numInput(input("Input a tile to replace (0 is the first tile, 6 is the last). Enter 7 to stop selection: "))
							if selectedTile == 7:  # stop swapping tiles. All tiles in swapTiles are replaces
								player.takeLetters(game.tiles)
								game.tiles.letters.extend(swapTiles)
								stillEntering = False
							elif selectedTile >= 0 and selectedTile <= 6:
								if player.letters[selectedTile] is None:
									print("Tile already selected")
								else:
									swapTiles.append(player.letters[selectedTile])
									player.letters[selectedTile] = None
									print("letters left: " + str(player.letters))
									print("letters removed: " + str(swapTiles))
									if len(swapTiles) == 7:  # swap all tiles
										player.takeLetters(game.tiles)
										game.tiles.letters.extend(swapTiles)
										stillEntering = False
							else:
								print("Input out of range")
						turn = False
					elif playOption == '3':
						# Player places 1 or more tiles
						removeTiles = input("Enter tiles to replace (0 is the first tile, 6 is the last) seperated by commas: ")
						turn = False
					else:
						print("input not recognised")

				# Player makes a move
				# > player choses between placing a word, changing tiles or doing nothing
				# > enter word to play (if selected)
				# 	- enter word direction (right or down)
				# 	- if word is valid then play word and update player score

				print("Player " + str(game.active + 1) + " your score is " + str(player.score))
				# refill player letters
				player.takeLetters(game.tiles)
				# change player
				game.nextPlayer()
				print("Player " + str(game.active + 1) + " it's your turn")
		elif action == "activePlayer":
			if len(game.players) == 0:
				print("No current players")
			else:
				print("Player " + str(game.active + 1) + " it's your turn")
		elif action == "help":
			print("")
			print("=== STAR help ===")
			print("")
			print("\q		-	Exit STAR")
			print("isAccepted	-	Enter a single word to find out if it is accepted or not")
			print("findWords	-	Find all words you can make with a given set of characters")
			print("board		-	Display the current state of the board")
			print("addLetter	-	Add a letter to the board")
			print("letters		-	Display the current letters available to take")
			print("makePlayer	-	Makes a new player (max 4)")
			print("takeLetters	-	Fills up a specified players letters")
			print("playerLetters	-	Prints the letters a given player has")
			print("playTurn	-	Make a move for the current players turn")
			print("activePlayer	-	Print the current active player")
			print("")
		else:
			print("Input not recognised")

	# print(board)
	# print("goodbye in trie:", trie.hasWord('goodbye'))
	# print("furby in trie:", trie.hasWord('furby'))
	# print("words in ['h', 'e', 'l', 'l', 'o']:", trie.wordSearch(['h', 'e', 'l', 'l', 'o']))
	# print("words in ['i', '?']:", trie.wordSearch(['i', '?']))
	# print("words in ['a', 'z', 'j', 'g', 'd', 'i', '?']:", trie.wordSearch(['a', 'z', 'j', 'g', 'd', 'i', '?']))
