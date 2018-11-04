"""STAR."""
import glob
import errno
import csv


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

	def addWord(self, word):
		"""Add a word to the trie."""
		currentNode = self.head

		for i in range(len(word)):
			# print(word)
			# print(word[i])
			# print(word[i] in currentNode.children)
			# print(currentNode.children)
			if word[i] in currentNode.children:
				currentNode = currentNode.children[word[i]]
				if i == len(word) - 1:
					currentNode.end = True
			else:
				if i < len(word) - 1:
					currentNode.children[word[i]] = Node(False)
				else:
					currentNode.children[word[i]] = Node(True, word)
				currentNode = currentNode.children[word[i]]

	def hasWord(self, word):
		"""If the trie has the word being searched for return true."""
		if word is '' or word is None:
			return False

		currentNode = self.head
		for letter in word:
			# print(letter)
			# print(letter in currentNode.children)
			# print(currentNode.end)
			if letter in currentNode.children:
				currentNode = currentNode.children[letter]

		if currentNode.end is False:
			return False
		else:
			return True


def setup(trie):
	"""Add each word from csv files to trie data structure."""
	path = './words/*.csv'
	files = glob.glob(path)
	for name in files:
		try:
			with open(name) as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				for row in reader:
					trie.addWord(row[0].lower())
		except IOError as exc:
			if exc.errno != errno.EISDIR:
				raise


if __name__ == '__main__':
	""" Example use """
	trie = Trie()
	setup(trie)
	# words = 'ice iceberg icebergs iceblink iceblinks icebox iceboxes iced'
	# for word in words.split():
	# 	trie.addWord(word)
	print("good in trie:", trie.hasWord('good'))
	print("goodbye in trie:", trie.hasWord('goodbye'))
	print("sumo in trie:", trie.hasWord('sumo'))
	print("iced in trie:", trie.hasWord('iced'))
	print("icebox in trie:", trie.hasWord('icebox'))
	print("iceboxes in trie:", trie.hasWord('iceboxes'))
