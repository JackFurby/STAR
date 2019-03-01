"""STAR."""
import time
from game import Board, Tiles, Game
from setup import setup, letterScore, getScore, save_trie, load_trie
from trie import Trie, Node
import copy

import pygame
import sys

from pygame.locals import *

pygame.init()
WIDTH = 45 * 16
HEIGHT = 45 * 16
background_colour = (255, 255, 255)
white = (255, 255, 255)
black = (0,0,0)
red = (255,0,0)
lightRed = (255,102,102)
blue = (0,128,255)
lightBlue = (153,204,255)
tile = (255,229,204)
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('STAR')
screen.fill(background_colour)

# trie = Trie()
# setup(trie)
# save_trie(trie, 'v1')

trie = load_trie('v1')
game = Game()
currentTiles = Tiles()


def numInput(userInput):
	"""Make sure the user enters an integer."""
	if userInput.isdigit():
		return int(userInput)
	else:
		userInput = input("You must enter a integer: ")
		return numInput(userInput)


def update():
	"""Text interface for user"""
	print()
	for playerNum in range(len(game.players)):
		player = game.players[playerNum]
		print("Player " + str(playerNum + 1) + "	-	" + str(player.score))
	print()
	action = input("What do you want to do? Enter 'help' for more: ")

	if action == "\q":
		pygame.quit()
		sys.exit()
	elif action == "isAccepted":
		inputLetters = input("Enter a word to check: ")

		# Makes sure input is in lower case
		inputLetters = inputLetters.lower()

		if trie.hasWord(inputLetters):
			print("Yes")
		else:
			print("No")
	elif action == "findWords":
		inputLetters = input("Enter letters ('?' is a wildcard): ").lower()

		start = time.time()
		wordList = trie.wordSearch(list(inputLetters))
		wordList.sort(key=lambda tup: -tup[1])
		print(*wordList, sep='\n')
		end = time.time()
		print("Completed search in", end - start, 'seconds')
	elif action == "findWordsPrefix":
		prefixLetters = input("Enter prefix (in order): ").lower()
		inputLetters = input("Enter letters ('?' is a wildcard): ").lower()

		start = time.time()
		wordList = trie.prefix(list(inputLetters), prefixLetters)
		wordList.sort(key=lambda tup: -tup[1])
		print(*wordList, sep='\n')
		end = time.time()
		print("Completed search in", end - start, 'seconds')
	elif action == "findWordsSuffix":
		suffixLetters = input("Enter suffix (in order): ").lower()
		inputLetters = input("Enter letters ('?' is a wildcard): ").lower()

		start = time.time()
		wordList = trie.wordSearch(list(inputLetters), suffix=suffixLetters)
		wordList.sort(key=lambda tup: -tup[1])
		print(*wordList, sep='\n')
		end = time.time()
		print("Completed search in", end - start, 'seconds')
	elif action == "findWordsContains":
		suffixLetters = input("Enter string words must contain (in order): ").lower()
		inputLetters = input("Enter letters ('?' is a wildcard): ").lower()

		start = time.time()
		wordList = trie.contains(list(inputLetters), suffixLetters)
		wordList.sort(key=lambda tup: -tup[1])
		print(*wordList, sep='\n')
		end = time.time()
		print("Completed search in", end - start, 'seconds')
	elif action == "findMoves":
		player = game.players[numInput(input("Enter player number: ")) - 1]
		start = time.time()
		wordList = game.possibleMoves(player, trie)
		#wordList.sort(key=lambda tup: -tup[1])
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
			print("Player " + str(game.active + 1) + " it's your turn")
			player = game.players[game.active]

			turn = True

			while turn:
				print()
				player.printLetters()
				print()

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
							player.swapLetters(game, swapTiles)
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
					word = []  # List of tiles to play with score (in order)
					playerBackup = copy.deepcopy(player.letters)  # backup of player tiles incase input is not accepted
					stillEntering = True
					while stillEntering:
						selectedTile = numInput(input("Input a tile to use in order (0 is the first tile, 6 is the last). Enter 7 to stop selection: "))
						if selectedTile == 7:  # Stop adding tiles to play
							print(word)
							stillEntering = False
						elif selectedTile >= 0 and selectedTile <= 6:  # Add tile to play
							if player.letters[selectedTile] is None:
								print("Tile already selected")
							else:
								if player.letters[selectedTile] is '?':  # If tile is a blank then provide character and add score of 0
									while True:
										char = input("input letter: ")
										if char.isalpha():
											break
										print("Please enter characters a-z only")
									word.append([char.lower(), 0])
								else:  # Add tile to word list
									word.append([player.letters[selectedTile], letterScore(player.letters[selectedTile])])
								player.letters[selectedTile] = None
								print("letters left: " + str(player.letters))
								print("letters used: " + str(word))
								if len(word) == 7:  # swap all tiles
									stillEntering = False
						else:
							print("Input out of range")

					if len(word) > 0:
						# Add tiles start position and direction
						x = numInput(input("Enter x of first tile (starting from 0 in top left): "))
						y = numInput(input("Enter y of first tile (starting from 0 in top left): "))

						while True:
							direction = input("enter direction of word (right/down): ")
							if direction == 'right' or direction == 'down':
								break
							print("Input not recognised")

						# Verify word placement is valid and play it if it is
						tilesAdded, score = game.board.addWord(word, x, y, direction, trie, player)
						if tilesAdded:
							# Word accepted. End turn and update score
							turn = False
							player.score = player.score + score
							print("Player " + str(game.active + 1) + " you scored " + str(score))
						else:
							# Word not accepeted. Reset player and try again
							player.letters = playerBackup
							print("Input not accepted")
					else:
						print("No tiles selected. Turn skipped")
						turn = False

				else:
					print("input not recognised")
			# refill player letters
			player.takeLetters(game.tiles)

			# If player has no tiles after refilling there are not tiles left. Game ends
			emptyTiles = True
			for tile in player.letters:
				if tile is not None:
					emptyTiles = False

			if emptyTiles:
				print("")
				print("=== Game Over ===")
				print("")
				for playerNum in range(len(game.players)):
					player = game.players[playerNum]
					print("Player " + str(playerNum + 1) + "	-	" + str(player.score))

				pygame.quit()
				sys.exit()

			# change player
			game.nextPlayer()
	elif action == "activePlayer":
		if len(game.players) == 0:
			print("No current players")
		else:
			print("Player " + str(game.active + 1) + " it's your turn")
	elif action == "help":
		print("")
		print("=== STAR help ===")
		print("")
		print("\q			-	Exit STAR")
		print("isAccepted		-	Enter a single word to find out if it is accepted or not")
		print("findWords		-	Find all words you can make with a given set of characters")
		print("findWordsPrefix		-	Find all words you can make with a given set of characters + a prefix")
		print("findWordsSuffix		-	Find all words you can make with a given set of characters + a suffix")
		print("findWordsContains	-	Find all words you can make with a given set of characters + a suffix")
		print("findMoves		-	Find all words you can make with a given player and the board")
		print("board			-	Display the current state of the board")
		print("addLetter		-	Add a letter to the board")
		print("letters			-	Display the current letters available to take")
		print("makePlayer		-	Makes a new player (max 4)")
		print("takeLetters		-	Fills up a specified players letters")
		print("playerLetters		-	Prints the letters a given player has")
		print("playTurn		-	Make a move for the current players turn")
		print("activePlayer		-	Print the current active player")
		print("")
	else:
		print("Input not recognised")


def gridItem(surface, bgColour, colour, text, x, y, w, h, score=None):
	"""Create a item (tile or space) for the board."""
	largeText = pygame.font.Font('freesansbold.ttf',20)
	smallText = pygame.font.Font('freesansbold.ttf',15)

	pygame.draw.rect(screen, colour, (x, y, w, h))
	pygame.draw.rect(screen, bgColour, (x + 2, y + 2, w - 4, h - 4))
	textItem = largeText.render(text, True, black)
	screen.blit(textItem, (x + 3, y + 3))
	if score is not None:
		scoreItem = smallText.render(score, True, black)
		screen.blit(scoreItem, (x + w - 20, y + h - 20))


def render():
	screen.fill(background_colour)  # clear the screen with white
	largeText = pygame.font.Font('freesansbold.ttf',20)

	# For every tile on the board
	for x in range(len(game.board.board[0]) + 1):
		for y in range(len(game.board.board) + 1):
			# Print tile index
			if x is 0 or y is 0:
				if x is 0 and y is not 0:
					textSurface = largeText.render(str(y - 1), True, black)
				elif y is 0 and x is not 0:
					textSurface = largeText.render(str(x - 1), True, black)
				else:
					textSurface = largeText.render('', True, black)

				screen.blit(textSurface, ((((WIDTH / 16) * x) + 45 / 2, ((HEIGHT / 16) * y) + 45 / 2)))
			# Create and display tiles
			else:
				if game.board.board[y - 1][x - 1] is 'DW':
					gridItem(screen, lightRed, black, 'DW', (WIDTH / 16) * x, (HEIGHT / 16) * y, 45, 45)
				elif game.board.board[y - 1][x - 1] is 'DL':
					gridItem(screen, lightBlue, black, 'DL', (WIDTH / 16) * x, (HEIGHT / 16) * y, 45, 45)
				elif game.board.board[y - 1][x - 1] is 'TL':
					gridItem(screen, blue, black, 'TL', (WIDTH / 16) * x, (HEIGHT / 16) * y, 45, 45)
				elif game.board.board[y - 1][x - 1] is 'TW':
					gridItem(screen, red, black, 'TW', (WIDTH / 16) * x, (HEIGHT / 16) * y, 45, 45)
				elif game.board.board[y - 1][x - 1] is None:
					gridItem(screen, white, black, '', (WIDTH / 16) * x, (HEIGHT / 16) * y, 45, 45)
				else:
					gridItem(screen, tile, black, game.board.board[y - 1][x - 1][0].upper(), (WIDTH / 16) * x, (HEIGHT / 16) * y, 45, 45, str(game.board.board[y - 1][x - 1][1]))




	pygame.display.update()

def mainLoop():
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

		update()
		render()

		clock.tick(60)


if __name__ == '__main__':
	mainLoop()
