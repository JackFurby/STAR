"""STAR."""
import glob
import errno
import csv


class Node:
	"""Node object for binary search tree."""

	def __init__(self, key):
		"""Each node has a value, indicator, and 26 node pointers (one for every letter in alphabet)."""
		"Each of the pointers will point to another node or None"
		"If indicator == True then all of the nodes leading up to and including the current node makes an accepted word"
		"value is used to hold the current concatination of letters"
		self.a = None
		self.a = None
		self.b = None
		self.c = None
		self.d = None
		self.e = None
		self.f = None
		self.g = None
		self.h = None
		self.i = None
		self.j = None
		self.k = None
		self.l = None
		self.m = None
		self.n = None
		self.o = None
		self.p = None
		self.q = None
		self.r = None
		self.s = None
		self.t = None
		self.u = None
		self.v = None
		self.w = None
		self.x = None
		self.y = None
		self.z = None
		self.indicator = False
		self.value = None


def insert():
	"""Insert a word into the data structure."""


def setup():
	"""Create data structure of words and points."""
	path = './words/*.csv'
	files = glob.glob(path)
	for name in files:
		try:
			with open(name) as csvfile:
				reader = csv.reader(csvfile, delimiter=',')
				for row in reader:
					print(row[0])
		except IOError as exc:
			if exc.errno != errno.EISDIR:
				raise


def main():
	setup()


if __name__ == '__main__':
	main()
