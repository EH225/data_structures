# -*- coding: utf-8 -*-
"""
Disjoint sets data structure utilizing the union find algorithm.
"""
from typing import List
from collections import defaultdict


class DisjointSets():
    """
    Data structure for handling n objects labeled 0 to (n-1) that are arranged in a series of disjoint set.
    """

    def __init__(self, n: int):
        # Record the parent node for each object i.e. self.parent[x]
        # records the parent node for node x. Root nodes are ones
        # where the parent node is itself i.e. self.parent[x] == x
        self.parent = [i for i in range(n)]
        self.rank = [1 for i in range(n)]  # Ranks for each start at 1
        self.n_sets = n  # Track the total number of disjoint sets
        self.n = n  # The number of elements tracked in the data structure

    def find_root(self, x: int) -> int:
        """
        Returns the root node of input node x. Uses recursion to evaluate and path compression to speed
        up any future operations.
        """
        if x == self.parent[x]:  # A root node is its own parent node
            return x  # Recursion base-case
        else:  # Otherwise, x is not a root node, recursively call this
            # method on the parent node of x until we find the root node
            common_root = self.find_root(self.parent[x])
            self.parent[x] = common_root  # Update along the way so that
            # the root nodes is the parent node of all its successors
            return common_root

    def join_sets(self, x: int, y: int) -> None:
        """
        Joins the 2 disjoint sets together to which x and y belong. If x and y belong to the same set, 
        no action occurs. If they belong to different sets i.e. have different root nodes, then they
        are joined. The node belonging to the set that has a root with a lower rank is linked to the
        larger set root node.
        """
        root_x, root_y = self.find_root(x), self.find_root(y)
        if root_x != root_y:  # Join together if they are not the same
            if self.rank[root_x] > self.rank[root_y]:
                self.parent[root_y] = root_x  # Set the parent of root_y equal
                #  to the root of x thereby linking all elements in y's set to root_x
            elif self.rank[root_y] > self.rank[root_x]:
                self.parent[root_x] = root_y  # Set the parent of root_x equal
                #  to the root of y thereby linking all elements in x's set to root_y
            else:  # When the ranks are equal
                self.parent[root_y] = root_x  # Set the parent of root_y equal
                #  to the root of x thereby linking all elements in y's set to root_x
                self.rank[root_x] += 1  # The max depth has now increased by 1

            self.n_sets -= 1  # Decrement the number of total sets after
            # joining 2 together to make 1 larger set

    def is_connected(self, x: int, y: int) -> bool:
        """
        Returns a boolean value indicating if node x and y are in the same disjoint set.
        """
        return self.find_root(x) == self.find_root(y)

    def get_sets(self) -> List[List[int]]:
        """
        Returns a list of the disjoint sets recorded in this data structure.
        """
        dj_sets = defaultdict(list)  # Aggregate node values by root node
        for val in range(self.n):  # For each node, append it to the root node list
            dj_sets[self.find_root(val)].append(val)
        # Return a list lists, one for each disjoint set
        return list(dj_sets.values())
