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

## Adding words to trie

When adding to the trie the start point is the trie head. From here the trie is traversed until either a node is not present in the current node children or the current character being checked is the last letter in the word being added. If the node is not present then a new node is added. If the current character being checked is the last letter in the word being added then the node is edited to say it is then end of a word.

```Python

def addWord(self, word):
	"""Add a word to the trie."""
	currentNode = self.head

	for i in range(len(word)):
		# if letter already exists in children move to the node
		if word[i] in currentNode.children:
			currentNode = currentNode.children[word[i]]
			# if letter is then end of word being added update node to show this
			if i == len(word) - 1:
				currentNode.end = True
				currentNode.data = word
		# if letter is not in children add it
		else:
			if i < len(word) - 1:
				currentNode.children[word[i]] = Node(False)
			else:
				currentNode.children[word[i]] = Node(True, word)
			currentNode = currentNode.children[word[i]]

```

## Finding all words from a list

wordSearch will recursively call itself and on each call will check to see if the current node is the end of a word. To make sure the same path is not searched twice a list of current letters searched is kept. If a letter is already present in this then that letter is skipped.

Given a list of characters wordSearch will return a list of all words that can be created with them.

```Python

def wordSearch(self, letters, currentNode=None):
	"""Given a list of letters find all words that can be made."""
	# list of all words found
	words = []

	if currentNode is None:
		currentNode = self.head

	# if word found then add it to words
	if currentNode.end:
		words.append(currentNode.data)

	if len(letters) is not 0:
		# i keeps track of current letter
		# searched stop duplicate searches if input has repeated letters
		i = 0
		searched = []
		for letter in letters:
			if letter not in searched:
				searched.append(letter)
				if letter in currentNode.children:
					newLetters = letters.copy()
					del newLetters[i]
					words += self.wordSearch(newLetters, currentNode.children[letter])
			i += 1

	# return words found
	return words

```

## Environment

STAR has a complete environment to represent Scrabble (WIP). It has various abilities with the current offerings being:

```

\q			-	Exit STAR
isAccepted		-	Enter a single word to find out if it is accepted or not
findWords		-	Find all words you can make with a given set of characters
findWordsPrefix		-	Find all words you can make with a given set of characters + a prefix
findWordsSuffix		-	Find all words you can make with a given set of characters + a suffix
findWordsContains	-	Find all words you can make with a given set of characters + a suffix
findMoves		-	Find all words you can make with a given player and the board
board			-	Display the current state of the board
addLetter		-	Add a letter to the board
letters			-	Display the current letters available to take
makePlayer		-	Makes a new player (max 4)
takeLetters		-	Fills up a specified players letters
playerLetters		-	Prints the letters a given player has
playTurn		-	Make a move for the current players turn
activePlayer		-	Print the current active player

```

Over time some of these will be removed in order to only allow legal moves. Following from the data structure section of this project isAccepted and findWords allow interaction with the word trie. All other actions will interact with the game environment.


### playTurn

The option playTurn allowa the current active player to enter a word to place, starting position (X and Y) on the board and word direction (right or down). This input will be checked with the game rules and if legal will be played and the player updated with a new score and tiles. The environment will then move onto the next player. Once all tiles have been given to players and a player runs out of tiles the game will end. After each go the board will be updated and shown on the UI.

### UI

STAR has a basic UI. For now (and possibly always) the UI will only show the current board state. To interact with the enviroment you will need to use the command line interface.

![alt text](https://github.com/JackFurby/STAR/blob/master/UI.png)
