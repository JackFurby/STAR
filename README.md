# STAR

Scrabble Turn Automation Robot is a solver to scrabble. It will be able to give accepted words when given a set of characters.

## Data structure

### Ternary Search Tree

A ternary search tree is a data structure where nodes are arranged in a similar manor to a binary search tree but with up to 3 children. This structure can be used as a map for strings and allow incremental string search. This is being used here as it is more space efficient than the trie data structure with the sacrifice of some performance for space complexity. In this project a ternary search tree will be used to store accepted words in a format that is efficient to search.

#### node

A ternary search tree is made up of nodes linked together. Each node is made up of a **character**, an **indicator** to show if a character is at the end of a word and **3 pointers**. One pointer points to a character with a lower value, one to a character with a higher value and one to the next character in the word.

|--------------|
|char|indicator|
|--------------|
|x   |x   |x   |
|--------------|

A word is represented with a prefix node and all other nodes in the middle subtree. It is also possible for a word to have its initial node(s) from nodes thither up the tree which branch out. For instance if there are the nodes [A, N] linked in that order by the next character reference they represent the word 'an'. If there is an additional node 'C' before 'A' in the tree which references 'A' via the lower value reference then we can also show the word 'can'.

## Words

Word list files can be found here: http://diginoodles.com/The_English_Open_Word_List_%28EOWL%29 with its licence as follows:

Copyright © J Ross Beresford 1993-1999. All Rights Reserved. The following restriction is placed on the use of this publication: if the UK Advanced Cryptics Dictionary is used in a software package or redistributed in any form, the copyright notice must be prominently displayed and the text of this document must be included verbatim.
