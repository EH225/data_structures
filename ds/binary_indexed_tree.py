# -*- coding: utf-8 -*-
"""
Binary indexed tree data structure module, see help(BinaryIndexedTree) for details.
"""

from typing import Union, List


class BinaryIndexedTree:
    """
    Binary Indexed Tree data-structure.

    Also known as a Fenwick Tree, Binary Indexed Trees allow for evaluation of the sum function over a given
    range in an array in O(log2(n)) time. They also support updates to the values of the array in O(log2(n))
    time which is substantial improvement over O(n) update time required for updates in a prefix-sum.

    The binary representation of the array element's index is used for various purposes in constructing the
    tree, making query evaluations, and updating values, hence the name Binary Indexed Tree.

    See: https://www.youtube.com/watch?v=uSFzHCZ4E-8&t=12s for details.
    """

    def __init__(self, arr: List[Union[int, float]]):
        """
        Constructor method for the BinaryIndexTree data structure.

        Parameters
        ----------
        arr : List[Union[int, float]]
            An input array of values for which the binary indexed tree is built.

        """
        # Construct the binary indexed tree
        self.arr = arr.copy()  # Store a copy of the original array internally
        self.binary_idx_tree = arr.copy()  # Start off with a copy of the original input array
        for idx in range(1, len(self.binary_idx_tree) + 1):  # Use 1-indexing throughout
            parent_idx = idx + (idx & -idx)  # Get the parent range index
            if parent_idx < len(self.binary_idx_tree):  # Check if the parent range index exists
                self.binary_idx_tree[parent_idx - 1] += self.binary_idx_tree[idx - 1]

    def update(self, idx: int, val: Union[int, float]) -> None:
        """
        Updates the value of an element in the original array located at a particular index (idx) and also the
        binary indexed tree accordingly. An update can also be accomplished with: binary_idx_tree[idx] = val.
        Performs updates in O(log2(n)) time.

        Parameters
        ----------
        idx : int
            The index of the value in the internal array to update.
        val : Union[int, float]
            The new value to store in the internal array at idx.

        """
        net_chg = val - self.arr[idx]  # Record the net change to any sum that brackets this value at idx
        if net_chg == 0:  # No action required if the net change is 0, i.e. no update needed
            return None
        self.arr[idx] = val  # Update the value in the original array stored internally
        idx += 1  # Convert to 1-indexing for binary representation operations
        while idx <= len(self.binary_idx_tree):  # Check that the parent index is still in the array
            self.binary_idx_tree[idx - 1] += net_chg  # Apply the net change to this tree node
            idx = idx + (idx & -idx)  # Get the next parent range index

    def _range_query(self, end: int) -> Union[float, int]:
        """
        Internal helper function for performing range queries. Computes the sum of all elements up through
        index end. This method is used by range_query to compute the sum of elements start:end by taking the
        sum through index=end and subtracting off the sum through index=(start-1). Runs in O(log2(n)) time.

        Parameters
        ----------
        end : int
            The ending index of the range query.

        Returns
        -------
        Union[float, int]
            The evaluation of the range sum query from the first element through the end index element.

        """
        end += 1  # Convert to 1-indexing
        sum_total = 0  # Aggregate the sum total across all entries from the start, up through index end
        while end > 0:
            sum_total += self.binary_idx_tree[end - 1]
            end -= (end & -end)  # Flip the last set bit
        return sum_total

    def range_query(self, start: int, end: int) -> Union[float, int]:
        """
        Performs a sum range query using the binary indexed tree and returns the aggregate answer. Computes
        the sum of the array elements falling within the inclusive index interval [start, end] of the original
        array. Runs in O(log2(n)) time.

        Parameters
        ----------
        start : int
            The starting index of the range query.
        end : int
            The ending index of the range query.

        Returns
        -------
        Union[float, int]
            The evaluation of the range query i.e. f(arr[start, end + 1]).

        """
        assert start <= end, "end must be greater than or equal to start"
        assert end < len(self.binary_idx_tree), "end index out of range"
        if start == end:  # Handle special edge case when start == end, return the entry of the original arr
            return self.arr[end]

        ans = self._range_query(end)  # Compute the sum up through the end index
        if start > 0:  # If the start is above index 0, then subtract the sum of elements through (start - 1)
            ans -= self._range_query(start - 1)  # so that the result is the sum of arr[start:(end + 1)]
        return ans

    def __setitem__(self, idx: int, val: Union[int, float]) -> None:
        """
        Support for obj[idx] = val changes to the underlying array and segmentation tree data structure.
        """
        self.update(idx, val)

    def __repr__(self) -> str:
        """
        String representation of the object, reports the underlying array and the operation specified.
        """
        return str(self.binary_idx_tree)

    def __str__(self) -> str:
        """
        String representation of the object, reports the underlying array and the operation specified.
        """
        return self.__repr__()

    def __len__(self):
        """
        Returns the length of binary indexed tree.
        """
        return len(self.binary_idx_tree)
