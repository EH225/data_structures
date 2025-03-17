# -*- coding: utf-8 -*-
"""
Trie data structure.
"""

from typing import Optional, List


class TrieNode:
    def __init__(self, n: int, n_prefix: int):
        self.n = n  # Record the number of words ending at this character (could be 0)
        self.n_prefix = n_prefix  # Record the number of words with this prefix (always >= 1 if not root)
        self.children = {}


class Trie:
    """
    Data structure that is able to hold a set of words and quickly determine if a word has been added and what
    words can be built from a given prefix. E.g. prefix = "app" can be used to create the words "apple",
    "application", "apply" etc. This data structure allows quick generation of words that originate from a
    given prefix and to check how many words in the collection of added words begin with a given prefix and/or
    return all such words.
    """

    def __init__(self, words: Optional[List[str]] = None):
        self.root = TrieNode(0, 0)  # Instantiate a root node instance for the blank string ""
        words = [] if words is None else words  # Convert to an iterable
        for word in words:  # Add the initial word collection to the Trie if provided
            self.insert(word)

    def insert(self, word: str) -> None:
        """
        Method for adding an input word into the Trie. Duplicate words will increase the word and prefix
        counters. The input word must be a non-empty string.
        """
        assert isinstance(word, str) and len(word) > 0, "word must be a non-empty string"
        node = self.root  # Begin with the root node of the Trie
        node.n_prefix += 1  # Record that a new word has been added, "" is a prefix to all words in the trie

        word_len = len(word)  # Used to check which iteration is the last letter
        for i, letter in enumerate(word):  # Iterate through each letter of the input word
            if letter not in node.children:  # If this letter does not already exist at this level, create one
                node.children[letter] = TrieNode((i == word_len - 1) * 1, 1)
            else:  # If this letter already exists, update its properties
                node.children[letter].n += (i == word_len - 1) * 1  # Add 1 if this is the last letter
                node.children[letter].n_prefix += 1  # Increment the prefix counter
            node = node.children[letter]  # Update for next iter, continue until we've covered all chr in word

    def get_word_count(self, word: int) -> int:
        """
        Returns the number of instances of the input word that have been added to the Trie. The input word
        must be a non-empty string.
        """
        assert isinstance(word, str) and len(word) > 0, "word must be a non-empty string"
        node = self.root
        for L in word:
            node = node.children.get(L, None)
            if node is None:  # If this letter of word cannot be found, the word is not known in the Trie
                return 0
        return node.n

    def is_word(self, word: str) -> bool:
        """
        Method for testing whether an input word is located in the Trie. The input word must be a non-empty
        string.
        """
        return self.get_word_count(word) >= 1  # Check if this word occurs at least once in the Trie

    def get_prefix_word_count(self, prefix: str) -> int:
        """
        Returns the number of words in the Trie that begin with a given input prefix. This includes prefix
        itself if prefix is a word in the True. The prefix must be a non-empty string.
        """
        assert isinstance(prefix, str) and len(prefix) > 0, "prefix must be a non-empty string"
        node = self.root
        for L in prefix:
            node = node.children.get(L, None)
            if node is None:  # If this letter of the prefix cannot be found, the prefix is not known
                return 0
        return node.n_prefix

    def is_prefix(self, prefix: str) -> bool:
        """
        Method for checking if a given prefix is contained in the search tree. Unlike in the is_word method,
        prefix does not need to form a word by itself. The prefix must be a non-empty string.
        """
        return self.get_prefix_word_count(prefix) >= 1  # Check if this prefix is followed by at least 1 word

    def remove_word(self, word: str, remove_all: bool = False) -> None:
        """
        Removes 1 or all instances of a given word from the Trie if it exists. The input word must be a
        non-empty string.
        """
        assert isinstance(word, str) and len(word) > 0, "word must be a non-empty string"
        word_count = self.get_word_count(word)  # Count how many times this word occurs in the Trie
        if word_count == 0:  # If this word isn't even in the Trie, no action needed
            return None

        # Otherwise, remove 1 or all instances of this word from the Trie (according to remove_all)
        node = self.root
        n_remove = word_count if remove_all is True else 1  # Record how many copies to remove
        node.n_prefix -= n_remove  # The root is a prefix to all words, remove n_prefix values here

        # Traverse the tree until we reach the node for the last letter of word or prune early
        for L in word:  # Iterate over each letter and navigate down the tree
            next_node = node.children[L]  # We have already checked that word is in the Trie, L must exist
            if next_node.n_prefix == n_remove:  # The number of words supporting this branch is equal to the
                # number of words we are removing, therefore we will remove all words on this branch
                del node.children[L]  # Delete the branch and exit early
                return None
            else:  # Otherwise there is at least 1 other word supporting this node's existence in the Trie
                next_node.n_prefix -= n_remove  # Decrement the prefix count by the words being removed
            node = next_node  # Update ref for next iteration
        node.n -= n_remove  # Decrement the terminal node word count by the number to remove

    def first_prefix_word(self, word: str) -> str:
        """
        Returns the first word found in the Trie along the node path leading to the input word provided.
        Note, the input word itself does not necessarily need to be a word in the Trie. The input word must
        be a non-empty string.
        
        E.g. let word="apple". If "app" is a word in the Trie while "a" and "ap" are not, then "app" will be
        returned. If none of the proper prefixes of "apple" are in the Trie, but "apple" is, then "apple"
        will be returned. If "apple" and none of its prefixes are in the Trie, then None will be returned.
        """
        assert isinstance(word, str) and len(word) > 0, "word must be a non-empty string"
        node = self.root
        for i, letter in enumerate(word):  # Iterate through each letter in word, trace down the tree
            if letter in node.children:  # Check that this next letter is a child node
                if node.children[letter].n > 0:  # Check if this next letter creates a valid word
                    # if so, then return the valid word we found that is a prefix of the original input word
                    return word[:(i + 1)]  # Return the letters up through i (+1 to include i)
                else:  # Keep searching down the branch nodes searching for a valid prefix
                    node = node.children[letter]  # Update ref for next iter
            else:  # Otherwise if the order of letters is broken, then word is not part of the tree, nor is
                # any prefix of it, return None
                return None

    def get_words_by_prefix(self, prefix: str, unique_only: bool = True) -> List[str]:
        """
        Returns a list of words that are in the Trie that begin with the input prefix provided. If the prefix
        is not found in the Trie, an empty list is returned. If the prefix provided is a word itself, it will
        be included in the output list. Set unique_only = True to return only unique words rather than all
        words in their given multiplicities. Passing the empty string in for prefix will return all words
        in the Trie.
        """
        assert isinstance(prefix, str), "prefix must be a string"
        output = []  # Collect all words in the Trie starting with the given prefix
        node = self.root  # Start with the root node and explore downwards
        for L in prefix:  # Iterate over the letters of prefix, descend to the node where it ends
            node = node.children.get(L, None)  # Move down to the next node
            if node is None:  # If the next letter is not found in the Trie, no words follow it
                return []

        # We're now at the node of the last letter in prefix, we can explore pathways from here to find words
        # Explore pathways from this node onwards using DFS
        stack = [(node, prefix)]  # Begin with the current node and its string prefix
        while stack:  # Iterate until we've reached all possible words
            node, prefix = stack.pop()  # Get the next prefix letter pathway
            if node.n > 0:  # Check if this is itself a word
                if unique_only:  # Add only 1 copy for this word
                    output.append(prefix)  # If so, add it to the output list
                else:  # Add as many copies of this word as are in the Trie
                    output.extend([prefix] * node.n)

            for next_letter, next_node in node.children.items():  # Keep searching for words beyond
                stack.append((next_node, prefix + next_letter))  # Append child pathways to the stack

        return output

    def __len__(self) -> int:
        """
        Returns the number of words that are in the current Trie (including duplicate words).
        """
        return self.root.n_prefix
