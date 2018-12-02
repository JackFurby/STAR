"""STAR."""
import time
from board import board
from setup import setup, letterScore, getScore, save_trie, load_trie
from trie import Trie, Node


if __name__ == '__main__':
	""" Example use """
	# trie = Trie()
	# setup(trie)
	# save_trie(trie, 'v1')

	trie = load_trie('v1')

	run = True

	while run:
		inputLetters = input("Enter letters ('?' is a wildcard): ")

		if inputLetters == '\q':
			run = False
			break

		# Makes sure input is in lower case
		inputLetters = inputLetters.lower()

		start = time.time()
		wordList = trie.wordSearch(list(inputLetters))
		wordList.sort(key=lambda tup: -tup[1])
		print(*wordList, sep='\n')
		end = time.time()
		print("Completed search in", end - start, 'seconds')

	# print(board)
	# print("goodbye in trie:", trie.hasWord('goodbye'))
	# print("furby in trie:", trie.hasWord('furby'))
	# print("words in ['h', 'e', 'l', 'l', 'o']:", trie.wordSearch(['h', 'e', 'l', 'l', 'o']))
	# print("words in ['i', '?']:", trie.wordSearch(['i', '?']))
	# print("words in ['a', 'z', 'j', 'g', 'd', 'i', '?']:", trie.wordSearch(['a', 'z', 'j', 'g', 'd', 'i', '?']))
