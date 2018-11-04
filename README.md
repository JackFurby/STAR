# STAR

Scrabble Turn Automation Robot is a solver for scrabble. It will be able to give accepted words when given a set of characters.

## Data structure

### Trie

A trie is a data structure used to store a dynamic set or associative array where the keys are usually strings. Each node will have a key who's value will be based on its position. This will be such that nodes before node X will be the prefix and nodes after will become the suffix. The root node is the empty string In this project a trie data structure will be used to store accepted words in a format that is efficient to search.

#### node

A trie is made up of nodes linked together. Each node is made up of a **value**, **indicator** and **pointers**. In my implementation the value is called data, indicator is called end and pointers are children.
* The indicator is used to mark the current node as the end of a word.
* The value stores the current word. This is not required but will save time if you want to return the word found.
* the pointers can be seperated out but in my implementation I have used a dictionary as it means I can store as many unique keys as I like and will not be taking up any extra storage for unused pointers.

```Python
class Node:
	def __init__(self, end=False, data=None):
		"""Initilise the node."""
		self.end = end
		self.data = data
		self.children = dict()
```

A word is represented by leaf nodes and by some inner nodes that are marked as accepted words.

![alt text](https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Trie_example.svg/400px-Trie_example.svg.png)

(Image of trie data structure was taken from https://en.wikipedia.org/wiki/Trie)

## Words

Word list file can be found here: https://www.wordgamedictionary.com/sowpods/. This is a SOWPODS Scrabble word list.
