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
			else:
				return False

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
