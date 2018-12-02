import glob
import errno
import pickle


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
