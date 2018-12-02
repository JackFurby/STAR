"""STAR."""
import time
from board import Board
from setup import setup, letterScore, getScore, save_trie, load_trie
from trie import Trie, Node


def numInput(userInput):
	"""make sure the user enters an integer."""
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
	currentBoard = Board()

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
			currentBoard.printBoard()
		elif action == "addLetter":
			letter = input("Enter letter: ")
			value = numInput(input("Enter tile value: "))
			x = numInput(input("Enter x (starting from 0 in top left): "))
			y = numInput(input("Enter y (starting from 0 in top left): "))
			if currentBoard.addLetter(letter, value, x, y):
				print("Board updated")
			# If addLetter returns False then x or y is out of range (specified in board.py)
			else:
				print("X and Y cannot be above 14")
		elif action == "help":
			print("")
			print("=== STAR help ===")
			print("")
			print("\q		-	Exit STAR")
			print("isAccepted	-	Enter a single word to find out if it is accepted or not")
			print("findWords	-	Find all words you can make with a given set of characters")
			print("board		-	Display the current state of the board")
			print("addLetter	-	Add a letter to the board")
			print("")
		else:
			print("Input not recognised")

	# print(board)
	# print("goodbye in trie:", trie.hasWord('goodbye'))
	# print("furby in trie:", trie.hasWord('furby'))
	# print("words in ['h', 'e', 'l', 'l', 'o']:", trie.wordSearch(['h', 'e', 'l', 'l', 'o']))
	# print("words in ['i', '?']:", trie.wordSearch(['i', '?']))
	# print("words in ['a', 'z', 'j', 'g', 'd', 'i', '?']:", trie.wordSearch(['a', 'z', 'j', 'g', 'd', 'i', '?']))
