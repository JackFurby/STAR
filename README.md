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
