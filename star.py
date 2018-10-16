"""STAR."""
import sys


class Node:
	"""Node object for binary search tree."""

	def __init__(self, key):
		"""Each node has a value, indicator, lower node pointer, higher node pointer and middle node pointer."""
		self.lower = None
		self.higher = None
		self.middle = None
		self.indicator = 0
		self.val = key


def insert():
	"""Insert a word into the data structure."""


def setup():
	"""Create data structure of words and points."""


if len(sys.argv) > 1:
	input1 = sys.argv[1]
	if input1 == '-r':
		if len(sys.argv) > 2:
			# run program for given characters
			pass
		else:
			print('Not enough arguments')
	elif input1 == '-help':
		print('==== help entered ====')
		print('-r [x] run program. If true is returned then input is accepted')
	else:
		print('Input not recognised')
else:
	print('Input not recognised')
