# -*- coding: utf-8 -*-
"""
This module exists to centralize all the imports from the various other modules into 1 module for quick
reference i.e. one can import all_ds as a module and have access to all the data structures throughout.
"""
from ds.linked_list import LinkedList, DoublyLinkedList
from ds.heaps import MinHeap, MaxHeap
from ds.deque import Deque
from ds.binary_search_tree import BinarySearchTree
from ds.binary_indexed_tree import BinaryIndexedTree
from ds.segment_tree import SegmentTree
from ds.disjoint_sets import DisjointSets
from ds.trie import Trie
from ds.cache import LRUCache, LFUCache
