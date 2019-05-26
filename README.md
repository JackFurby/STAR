# STAR

Scrabble Turn Automation Robot is a solver for scrabble. Once complete it will be able to find the best move you can make given a board and a set of tiles.

## Data structure

STAR makes use of a trie datastructure which is a tree which stores each character of a word. This makes if efficiant to search. A full description of this can be found in my repo [trie](https://github.com/JackFurby/trie).

To populate the trie I used a wordlist that can be found here: https://www.wordgamedictionary.com/sowpods/. This is a SOWPODS Scrabble word list.

## Environment

STAR has a complete environment to represent Scrabble (WIP). It has various abilities with the current offerings being:

```

\q			-	Exit STAR
isAccepted		-	Enter a single word to find out if it is accepted or not
findWords		-	Find all words you can make with a given set of characters
findWordsPrefix		-	Find all words you can make with a given set of characters + a prefix
findWordsSuffix		-	Find all words you can make with a given set of characters + a suffix
findWordsContains	-	Find all words you can make with a given set of characters + a set string
findMoves		-	Find all words you can make with a given player and the board
lookAhead		-	Return the best moves to make to win a game (Not working)
board			-	Display the current state of the board
letters			-	Display the current letters available to take
probableTiles		-	Print a list of tiles not on the board with the probability of picking that tile
probableTilesWithPlayer	-	Print a list of tiles not on the board or on players rack with the probability of picking that tile
makePlayer		-	Makes a new player (max 4)
playerLetters		-	Prints the letters a given player has
playTurn		-	Make a move for the current players turn
activePlayer		-	Print the current active player

```

Over time some of these will be removed in order to only allow legal moves. Following from the data structure section of this project isAccepted, findWords, findWordsPrefix, findWordsSuffix and findWordsContains allow interaction with the word trie. All other actions will interact with the game environment.


### playTurn

The option playTurn allowa the current active player to enter a word to place, starting position (X and Y) on the board and word direction (right or down). This input will be checked with the game rules and if legal will be played and the player updated with a new score and tiles. The environment will then move onto the next player. Once all tiles have been given to players and a player runs out of tiles the game will end. After each go the board will be updated and shown on the UI.

### UI

STAR has a basic UI. For now (and possibly always) the UI will only show the current board state. To interact with the enviroment you will need to use the command line interface.

![alt text](https://github.com/JackFurby/STAR/blob/master/UI.png)

### findMoves

Find moves will return almost all playable moves a player can make taking into consideration their tiles in their rack and the current state of the board. Some basic notes about how to do this are as follows:

* Scan the board looking for starting positions (positions next to tiles that have already been played)
	* For each stating position add one tile from the players rack at a time in the direction of the tile that the position is next to (extending the current tile). Each time a word is found take note of it.

findMoves was based of the algorithem used in [The World’s Fastest Scrabble Program](http://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf).

Currently words are found by extending right or down on starting positions. It also has the ability to move the starting position up or left by 7 spaces. This results in almost all possible moves being found. The only situation where words are not found are when placing parallel words starting before (above or to the left) of a starting position.

## lookAhead

In order to find the best move to make lookAhead will use a Monte Carlo tree search (MCTS) to find the best move to make considering the affect on the end game. The current implementation of this is basic and there are a number of known issues including the probable player rack is incorrect and the performance is at least 10 times slower than it needts be be to become useful.

A MCTS works by running through the following steps:

1. **Selection** - Recursively select nodes from the root node until a leaf node is found (I am using UCB1 score for selection)
2. **Expansion** - If the leaf node does not end the game then create more nodes from the leaf node (one for each possible move)
3. **Simulation** - From one of the leaf nodes select random moves until an end game is reached
4. **Backpropagation** - from the node containing the end game update each parent node with the score and visit until the root node.

A full description of MCTS can be found at [http://mcts.ai/about/](http://mcts.ai/about/).

For each node in my MCTS I an saving the state of the board, player racks + score and tiles in the game. This is one area that performance is not great. The score of the node is the current players score minus the next highest player score (higher score is better). I would expect this to be improved over time (perhaps with some ML).
	
The tree search will continue for a set amount of time (3 mins ATM). After this time the best searched move will be returned (using UCB1 score but ignoring infinite scores). Due to performance issues this node for the move will normally only get one visit.
