"""STAR."""
import glob
import errno
import pickle
import time


class Node:
	"""Node object for trie."""

	# children contains linkks to other nodes
	# data contains current letter
	# end indicates if the current node is the end of a word
	def __init__(self, end=False, data=None):
		"""Initilise the node."""
		self.end = end
		self.data = data
		self.children = dict()


class Trie:
	"""Trie data structure."""

	def __init__(self):
		"""Initilise the trie."""
		self.head = Node()

	def addWord(self, word, score):
		"""Add a word to the trie."""
		currentNode = self.head

		for i in range(len(word)):
			# if letter already exists in children move to the node
			if word[i] in currentNode.children:
				currentNode = currentNode.children[word[i]]
				# if letter is then end of word being added update node to show this
				if i == len(word) - 1:
					currentNode.end = True
					currentNode.data = [word, score]
			# if letter is not in children add it
			else:
				if i < len(word) - 1:
					currentNode.children[word[i]] = Node(False)
				else:
					currentNode.children[word[i]] = Node(True, [word, score])
				currentNode = currentNode.children[word[i]]

	def hasWord(self, word):
		"""If the trie has the word being searched for return true."""
		if word is '' or word is None:
			return False

		currentNode = self.head
		for letter in word:
			if letter in currentNode.children:
				currentNode = currentNode.children[letter]

		# if final node marks the end of a word return true
		if currentNode.end is False:
			return False
		else:
			return True

	def wordSearch(self, letters, currentNode=None):
		"""Given a list of letters find all words that can be made."""
		# list of all words found
		words = []

		if currentNode is None:
			currentNode = self.head

		# if word found then add it to words
		if currentNode.end:
			# only add word and word score to words list
						words.append([currentNode.data[0], currentNode.data[1]])


		if len(letters) is not 0:
			# i keeps track of current letter
			# searched stop duplicate searches if input has repeated letters
			i = 0
			searched = []
			for letter in letters:
				if letter not in searched:
					searched.append(letter)
					# if wildcard played then look at all children
					if letter == '?':
						for char in currentNode.children:
							newLetters = letters.copy()
							del newLetters[i]
							words += self.wordSearch(newLetters, currentNode.children[char])
					elif letter in currentNode.children:
						newLetters = letters.copy()
						del newLetters[i]
						words += self.wordSearch(newLetters, currentNode.children[letter])
				i += 1

		# return words found
		return words


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


def getScore(word):
	"""Return a tuple with a score and breakdown a given word would get."""
	breakdown = []
	for letter in word:
		breakdown.append(letterScore(letter))
	total = sum(breakdown)
	return total


def setup(trie):
	"""Add each word from csv files to trie data structure."""
	path = './words/*.txt'
	files = glob.glob(path)
	for name in files:
		try:
			f = open(name, "r").read().splitlines()
			lines = list(f)
			print(len(lines), 'total words')
			for word in lines:
				# make sure word is in lowercase
				word = word.lower()
				trie.addWord(word, getScore(word))
		except IOError as exc:
			if exc.errno != errno.EISDIR:
				raise


def save_trie(trie, name):
	"""Save a trie to a file."""
	with open('./words/' + name + '.pkl', 'wb') as f:
		pickle.dump(trie, f, pickle.HIGHEST_PROTOCOL)


def load_trie(name):
	"""Load a trie from a file."""
	with open('./words/' + name + '.pkl', 'rb') as f:
		return pickle.load(f)


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

		start = time.time()
		wordList = trie.wordSearch(list(inputLetters))
		wordList.sort(key=lambda tup: -tup[1])
		print(*wordList, sep='\n')
		end = time.time()
		print("Completed search in", end - start, 'seconds')
	# print("goodbye in trie:", trie.hasWord('goodbye'))
	# print("furby in trie:", trie.hasWord('furby'))
	# print("words in ['h', 'e', 'l', 'l', 'o']:", trie.wordSearch(['h', 'e', 'l', 'l', 'o']))
	# print("words in ['i', '?']:", trie.wordSearch(['i', '?']))
	# print("words in ['a', 'z', 'j', 'g', 'd', 'i', '?']:", trie.wordSearch(['a', 'z', 'j', 'g', 'd', 'i', '?']))
