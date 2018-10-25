# STAR

Scrabble Turn Automation Robot is a solver to scrabble. It will be able to give accepted words when given a set of characters.

## Data structure

### Trie

A trie is a data structure used to store a dynamic set or associative array where the keys are usually strings. Each node will have a key who's value will be based on its position. This will be such that nodes before node X will be the prefix and nodes after will become the suffix. The root node is the empty string In this project a trie data structure will be used to store accepted words in a format that is efficient to search.

#### node

A ternary search tree is made up of nodes linked together. Each node is made up of a **string**, **indicator** and **pointers**. It is possible for there to be 26 pointers however this is not space efficient and therefore another approach may be used in my implementation.

A word is represented by leaf nodes and by some inner nodes that are marked as accepted words.

[logo]: https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/Trie_example.svg/400px-Trie_example.svg.png

(Image of trie data structure was taken from https://en.wikipedia.org/wiki/Trie)

## Words

Word list files can be found here: http://diginoodles.com/The_English_Open_Word_List_%28EOWL%29 with its licence as follows:

Copyright © J Ross Beresford 1993-1999. All Rights Reserved. The following restriction is placed on the use of this publication: if the UK Advanced Cryptics Dictionary is used in a software package or redistributed in any form, the copyright notice must be prominently displayed and the text of this document must be included verbatim.
