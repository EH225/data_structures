# -*- coding: utf-8 -*-
"""
Segment tree data structure module, see help(SegmentTree) for details.
"""

import math
from typing import Union, List, Optional


class SegmentTreeNode:
    """
    Generic segment tree node object. Stores start and end which denote the indices of the first and last
    elements falling withing this node's interval range. Also stores the value of the operation applied to
    that interval e.g. val = sum(arr[start_index, end_index + 1]). Also stores pointers to left and right
    child elements to form a hierarchical tree structure.
    """

    def __init__(self, start: int, end: int, val: Union[int, float], left=None, right=None):
        self.start = start  # Store the index of the first element covered by this interval
        self.end = end  # Store the index of the last element covered by this interval
        self.val = val  # The value of the function evaluated on this interval i.e. f(arr[start, end + 1])
        self.left = left  # Record a pointer to the left child node (if any, else leave as None)
        self.right = right  # Record a pointer to the right child node (if any, else leave as None)

    def __repr__(self) -> str:
        """
        String representation that reports the segment indices and value of this node e.g. [3, 5] 26
        """
        return f"[{self.start}, {self.end}] {self.val}"


class SegmentTree:
    """
    Segment tree data-structure.

    Segment trees allow for range queries to be executed on an array in O(log2(n)) time which is much faster
    than O(n) which is required to traverse the array element by element to evaluate. A range query is some
    function e.g. sum, max, min etc. applied over a given range of elements of an array e.g. sum(arr[4:8]).

    Segment trees also support making updates to elements in the array in O(log2(n)) time. This gives them
    an advantage over prefix sums which require O(n) time to make updates to an arbitrary element in the
    array. Segment trees also support the usage of monotonic, non-linear operators such as max and min which
    prefix sumes do not.

    Segment trees are well suited to handle a stream of range queries and array updates. They are less well
    suited to handle insertions or deletions to the array, which requires a rebuild of the segment tree.
    """

    def __init__(self, arr: List[Union[int, float]], eval_func: str):
        """
        Constructor method for SegmentTree data structure.

        Parameters
        ----------
        arr : List[Union[int, float]]
            An input array of values for which the segment tree is built upon.
        eval_func : str
            The function that will be evaluated over various ranges of arr in the segment tree.
            Must be one of the following: ["min", "max", "sum", "gcd", "lcm"]. Note, gcd and lcm are only
            appropriate if all values in arr are non-negative integers.

        """
        # Record a dictionary of possible evaluation functions that can be applied over the elements of arr
        # Each expects 2 numbers as inputs and returns a number as an output after combining
        self.func_dict = {"min": min, "max": max, "sum": lambda x, y: x + y, "gcd": math.gcd, "lcm": math.lcm}
        self.eval_func, self.arr, self.seg_tree = None, None, None  # Initialize as None
        self.build_tree(arr, eval_func)  # Construct the segmentation tree using the input array and function
        self.n = len(arr)  # Record the length of the internal array

    def build_tree(self, arr: List[Union[int, float]], eval_func: str) -> None:
        """
        Constructs a segment tree using an input array (arr) and specified evaluation function (eval_func),
        which will be computed over various segments of arr. This method is called when the SegmentTree object
        is instantiated and also again after certain other methods that make changes to the internal array
        (e.g. insert, pop).

        This method can also be used to re-build the internal segment tree for a new input array or choice of
        evaluation function if desired by the user without creating a new instance of the SegmentTree class.

        When this method is called, a copy of the input array and the evaluation function are saved as
        properties to this object in self.arr and self.eval_func respectively.

        Parameters
        ----------
        arr : List[Union[int, float]]
            An input array of values for which the segment tree is built upon.
        eval_func : str
            The function that will be evaluated over various ranges of arr in the segment tree.
            Must be one of the following: ["min", "max", "sum", "gcd", "lcm"]. Note, gcd and lcm are only
            appropriate if all values in arr are non-negative integers.

        """
        assert len(arr) > 0 and isinstance(arr, list), "arr must be a non-empty python list"
        self.arr = arr.copy()  # Make a copy of the array to store internally
        assert isinstance(eval_func, str), "eval_func must be a string value"
        if eval_func not in self.func_dict:  # Check that the operation requested is known
            raise ValueError(f"eval_func must be one of the following: {list(self.func_dict.keys())}")
        self.eval_func = eval_func  # Record the eval_func used to construct the tree
        self.n = len(arr)  # Record the length of the internal array
        self.seg_tree = self._build_tree(0, len(arr) - 1)  # Call recursive _build_tree helper function

    def _build_tree(self, start: int, end: int) -> Optional[SegmentTreeNode]:
        """
        Internal helper method that creates and returns a SegmentTreeNode root node.

        Creates a segment tree for the elements of self.arr and a specified evaluation function
        (self.eval_func e.g. sum, max etc.). The segment tree is constructed by splitting arr into a left and
        right half and recursively calling this _build_tree helper method on the segments. At the bottom of
        the tree, the leaf nodes will be where start==end, each containing one of the individual values of
        self.arr. The array and evaluation function are assumed to already be saved to self.arr and
        self.eval_func respectively.

        Parameters
        ----------
        start : int
            The index denoting the start of the segment this sub-tree will represent.
        end : int
            The index denoting the end of the segment this sub-tree will represent.

        Returns
        -------
        Optional[SegmentTreeNode]
            A root node representing the interval of indices [start, end] in the internal array.

        """
        n = end - start + 1  # Compute the length of the segment
        if n == 0:  # Recursion base-case, return None if the segment is empty
            return None
        elif n == 1:  # Recursion base-case, return a leaf node if the segment contains only 1 element
            return SegmentTreeNode(start, end, self.arr[start], None, None)  # Create a leaf node
        else:  # Otherwise, recursively create child nodes by splitting the interval in 2, cache the value
            # of the evaluation function applied to the entire segment of self.arr
            n_L = n - n // 2  # The number of elements in the LHS segment, n // 2 in the RHS, give more to
            # the LHS segment when there is an odd number e.g. n= 5 -> [0, 2] and [4, 5]
            left = self._build_tree(start, start + n_L - 1)  # Recursively build the left branch
            right = self._build_tree(start + n_L, end)  # Recursively build the right branch
            return SegmentTreeNode(start, end, self.func_dict[self.eval_func](left.val, right.val),
                                   left, right)

    def append(self, val: Union[int, float]) -> None:
        """
        Appends a new value to the end of the internal array and updates the segment tree accordingly. This
        method is a special case of insert i.e. when idx = self.n = len(self.arr).

        Parameters
        ----------
        val : Union[int, float]
            The new value to be appended to the end of the internal array.

        """
        self.insert(self.n, val)

    def insert(self, idx: int, val: Union[int, float]) -> None:
        """
        Inserts a new value into the internal array at a sepcified index location and updates the segment
        tree accordingly. The index of the newly added element in the internal array will be idx after
        insertion is complete. Use idx=0 to insert at the front of the array. Use idx = self.n to insert
        at the end of the array (or use the append method).

        Parameters
        ----------
        idx : int
            The index location where the new value is to be added to the internal array.
        val : Union[int, float]
            The new value to be inserted into the internal array.

        """
        assert 0 <= idx <= self.n, f"idx must be [0, {self.n}], got {idx}"
        self.arr.insert(idx, val)  # Mirror the same change to the copy of arr stored internally
        self.build_tree(self.arr, self.eval_func)  # Rebuild the segment tree after the addition has been made

    def pop(self, idx: int = None) -> Union[int, float]:
        """
        Removes an element from the internal array at a specified index location and updates the segment tree
        accordingly. Valid idx values are 0 through (self.n - 1). If idx=None (the default), then the
        last element of the internal array will be popped and returned.

        Parameters
        ----------
        idx : int, optional
            The index in the internal array to remove and return. The default is None which will be the last
            element of the array.

        Returns
        -------
        Union[int, float]
            The value that was popped (and removed) from the internal array.

        """
        idx = self.n - 1 if idx is None else idx  # Default to the last element if unspecified
        assert 0 <= idx <= self.n - 1, f"idx must be [0, {self.n - 1}], got {idx}"
        ans = self.arr.pop(idx)  # Mirror the same change to the copy of arr stored internally
        self.build_tree(self.arr, self.eval_func)  # Rebuild the segment tree after the element was removed
        return ans  # Return the popped value from the internal array

    def update(self, idx: int, val: Union[int, float]) -> None:
        """
        Updates the value of an element in the internal array located at a particular index (idx) and also the
        segment tree accordingly. For a SegmentTreeNode object (seg_tree), an update can also be accomplished
        with: seg_tree[idx] = val

        Parameters
        ----------
        idx : int
            The index of the value in the internal array to update.
        val : Union[int, float]
            The new value to store in the internal array at idx.

        """
        root = self.seg_tree
        # Check that this operation can even be done, check that the index requested is within the array
        assert idx >= 0 or idx <= root.end, f"idx out of range for stored segment tree: [0, {root.end}]"
        if self.arr[idx] == val:  # Check if the existing value is the same as the new value, if so then exit
            return None  # since no change is needed, no change will actually occur once updated
        self.arr[idx] = val  # Mirror the same change to the copy of arr stored internally

        node_stack = []  # Track the nodes that are traversed from root to leaf to update the value at idx

        node = root  # Traverse the tree from root to leaf until we reach the input idx edit location
        while node.start != idx or node.end != idx:
            node_stack.append(node)  # Add a pointer to this node to the stack to be revisited later
            node = node.left if idx <= node.left.end else node.right
        # Node stack only records the nodes from root to leaf, but does not include the leaf
        node.val = val  # Update the leaf node's value directly, recursion-base case
        # Once we reach the leaf node, update all values from leaf to root where this change has an effect
        while node_stack:  # Update the node values going up to reflect this updated leaf node value
            node = node_stack.pop()  # Go through the nodes in reverse order, LIFO
            node.val = self.func_dict[self.eval_func](node.left.val, node.right.val)

    def range_query(self, start: int, end: int, root: Optional[SegmentTreeNode] = None) -> Union[float, int]:
        """
        Performs a range query using the internal segment tree and returns the aggregate answer. Computes the
        evaluation function over the interval [start, end] of the internal array. Computes and returns the
        value of f(arr[start, end + 1]) using the tree's pre-cached values.

        Parameters
        ----------
        start : int
            The starting index of the range query.
        end : int
            The ending index of the range query.
        root : SegmentTreeNode, optional
            The SegmentTreeNode used to evaluate the range query. Leave as None to evaluate from the root.

        Returns
        -------
        Union[float, int]
            The evaluation of the range query i.e. f(arr[start, end + 1]).

        """
        root = self.seg_tree if root is None else root  # Default to the tree-root if not specified
        # Perform data validation on the interval endpoints requested
        msg = f"start must be an integer in the range [{root.start}, {root.end}], got {start}"
        assert root.start <= start <= root.end, msg
        msg = f"end must be an integer in the range [{root.start}, {root.end}], got {end}"
        assert root.start <= end <= root.end, msg
        assert start <= end, f"start must be <= end, got {start} and {end}"

        if start == root.start and end == root.end:  # Check if requested interval matches this node's bounds
            # Recursion base-case, if so, then return the cached value at this node for this interval
            return root.val
        else:  # Otherwise the interval requested [start, end] is some subset of the root interval range,
            # recursively evaluate in parts and construct the answer by aggregating LHS and RHS results
            # If no part of the interval [start, end] is in the LHS child interval, set the value to None
            LHS_upper_idx = min(end, root.left.end)  # Used as the LHS recursive call endpoint idx
            LHS_ans = self.range_query(start, LHS_upper_idx, root.left) if start <= root.left.end else None
            # If no part of the interval [start, end] is in the RHS child interval, set the value to None
            RHS_lower_idx = max(start, root.right.start)  # Used as the RHS recursive call start point
            RHS_ans = self.range_query(RHS_lower_idx, end, root.right) if end >= root.right.start else None
            if LHS_ans is None:  # If no LHS answer, then return the RHS answer
                return RHS_ans
            elif RHS_ans is None:  # If no RHS answer, then return the LHS answer
                return LHS_ans
            else:  # If there is a LHS and RHS answer, combine them together using self.eval_func and return
                return self.func_dict[self.eval_func](LHS_ans, RHS_ans)  # Aggregate and return

    def __setitem__(self, idx: int, val: Union[int, float]) -> None:
        """
        Support for obj[idx] = val changes to the underlying array and segmentation tree data structure.
        """
        self.update(idx, val)

    def __repr__(self) -> str:
        """
        String representation of the object, reports the underlying array and the operation specified.
        """
        return str(self.arr) + " " + str(self.eval_func)

    def __str__(self) -> str:
        """
        String representation of the object, reports the underlying array and the operation specified.
        """
        return self.__repr__()

    def __len__(self):
        """
        Returns the length of the internal array.
        """
        return self.n
