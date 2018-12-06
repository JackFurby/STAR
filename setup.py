import glob
import errno
import pickle
from game import letterScore


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
