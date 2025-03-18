# -*- coding: utf-8 -*-
"""
Min and max heap data structures.
"""


class MinHeap:
    """
    An implementation of a min-heap, code based on leetcode's template. Generally we would just use a list 
    and python's heapq package instead. This data structure implements the methods of heap operations
    manually i.e. push and pop. For simplicity, one can push each element of a collection separately to
    heapify them in their entirety and add them to the data structure.
    """

    def __init__(self):
        self.heap = []  # Maintain a min heap as a binary tree stored as an array

    def push(self, x) -> None:
        """
        Inserts a new element x into the min-heap data structure. Assumes the rest of the elements already
        satisfy the heap property.
        """
        self.heap.append(x)  # Add the new element to the heap as a leaf node
        idx_x = len(self.heap)  # Get the index of the newely added node with indexing starting at 1
        idx_parent = idx_x // 2  # Get the index of the parent node with indexing starting at 1

        # Note: Zero indexing makes this a little more complicated. If we index starting with 1 i.e. the root
        # node is at index 1, then the following rules hold:
        #    1). index_x // 2 is the parent node of a node_x located at index_x
        #    2). The left child element of node_x located at index_x is located at index_x * 2
        #    2). The right child element of node_x located at index_x is located at index_x * 2 + 1
        # Since python lists are indexed starting at 0, we will have to make the translation to and from
        # before using these relationships.

        # Heapify by swapping elements until the parent nodes are all smaller than the child nodes
        # This operation assumes that the rest of the nodes are already in an ordering that satisfies the 
        # heap property. If this newly added node is smaller than its parent node, then swap it with the
        # parent node and continue swimming the new x up the tree until that is no longer the case.
        while (self.heap[idx_x - 1] < self.heap[idx_parent - 1] and idx_x > 1):
            # Stop once we either reach a parent that is smaller or x is now the root node i.e. idx_x == 1
            # If x is smaller than its parent then it is also < than its sibling since x < parent < sibling
            self.heap[idx_parent - 1], self.heap[idx_x - 1] = self.heap[idx_x - 1], self.heap[idx_parent - 1]
            idx_x = idx_parent  # Update the index of x after the swap is made with the parent node
            idx_parent = idx_x // 2  # Update the parent node index based on the new index of x

    def pop(self):
        """
        Removes the element at the top of the heap and returns it i.e. the min element.
        """
        if len(self.heap) == 0:
            raise IndexError("Cannot pop from an empty heap")

        # To minimize the number of operations needed, we swap the root node with the last leaf node and
        # maintain the ordering of the other elements as is, which are assumed to already satisfy the heap
        # property. Then we remove the last leaf node to get the min-value to be returned. Then we process
        # the root node value which may not be in the right place and have it swim down until it is in the
        # right location
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]  # Swap the root and last leaf node
        output = self.heap.pop()  # Remove the last leaf node element
        # Now process the element at the root node location, iterate until it has be correctly moved
        idx_x = 1  # Use 1-indexing, track where this misplaced value x is located
        n = len(self.heap)
        while idx_x <= n:  # Stop iterating if it becomes the last leaf node, no further swimming down is
            # possible or needed for this x value to find its right location in the binary tree
            idx_L, idx_R = idx_x * 2, idx_x * 2 + 1  # Get the indices of the left and right children
            # Make swaps as needed to make sure the parent node is smaller than the current node
            idx, L, R = idx_x - 1, idx_L - 1, idx_R - 1  # Convert to 0 indexing for brevity

            # Check if the child elements exist, if so then we can make comparisons with it
            has_left, has_right = idx_L <= n, idx_R <= n

            if has_left is True:  # The left child exists (left child must exist for right child to exist)
                bool_1 = self.heap[idx] > self.heap[L]  # Check if x > left child
                if has_right is True:  # The right child also exists
                    # Check if either child node is smaller than the parent node x
                    bool_2 = self.heap[idx] > self.heap[R]  # Check if x > right child
                    if (bool_1 or bool_2):  # If either is true, then a swap is needed
                        if self.heap[L] < self.heap[R]:  # The left child is smaller than the right child so
                            # swap with the left one so that the new parent < both children
                            self.heap[L], self.heap[idx] = self.heap[idx], self.heap[L]
                            idx_x = idx_L  # Update the new index of x after making this swap
                        else:  # Then the right child is smaller so swap x currently in the parent node with
                            # the right child element so that the new parent < both children
                            self.heap[R], self.heap[idx] = self.heap[idx], self.heap[R]
                            idx_x = idx_R  # Update the new index of x after making this swap
                    else:  # Otherwise the value x is now in the right spot i.e. x < left_child, right_child
                        break
                else:  # No right child element, only compare with the left
                    if bool_1:  # Then x > left child so we need to swap them
                        self.heap[L], self.heap[idx] = self.heap[idx], self.heap[L]
                        idx_x = idx_L  # Update the new index of x after making this swap
                    else:  # The value x is now in the right spot i.e. x < left_child, the only child
                        break
            else:  # Doesn't have any child nodes, already a leaf node, no further comparisons to make
                break

        return output

    def size(self) -> int:
        """
        Returns the number of elements in the heap.
        """
        return len(self.heap)

    def top(self):
        """
        Returns the element at the top of the heap without removing it.
        """
        return self.heap[0]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.heap)

    def __len__(self):
        return self.size()


class MaxHeap:
    """
    An implementation of a max-heap, code based on leetcode's template. Generally we would just use a list 
    and python's heapq package instead. This data structure implements the methods of heap operations
    manually i.e. push and pop. For simplicity, one can push each element of a collection separately to
    heapify them in their entirety and add them to the data structure.
    """

    def __init__(self):
        self.heap = []  # Maintain a max heap as a binary tree stored as an array

    def push(self, x) -> None:
        """
        Inserts a new element x into the max-heap data structure. Assumes the rest of the elements already
        satisfy the heap property.
        """
        self.heap.append(x)  # Add the new element to the heap as a leaf node
        idx_x = len(self.heap)  # Get the index of the newly added node with indexing starting at 1
        idx_parent = idx_x // 2  # Get the index of the parent node with indexing starting at 1

        # Note: Zero indexing makes this a little more complicated. If we index starting with 1 i.e. the root
        # node is at index 1, then the following rules hold:
        #    1). index_x // 2 is the parent node of a node_x located at index_x
        #    2). The left child element of node_x located at index_x is located at index_x * 2
        #    2). The right child element of node_x located at index_x is located at index_x * 2 + 1
        # Since python lists are indexed starting at 0, we will have to make the translation to and from
        # before using these relationships.

        # Heapify by swapping elements until the parent nodes are all larger than the child nodes
        # This operation assumes that the rest of the nodes are already in an ordering that satisfies the 
        # heap property. If this newly added node is larger than its parent node, then swap it with the
        # parent node and continue swimming the new x up the tree until that is no longer the case.
        while (self.heap[idx_x - 1] > self.heap[idx_parent - 1] and idx_x > 1):
            # Stop once we either reach a parent that is larger or x is now the root node i.e. idx_x == 1
            # If x is larger than its parent then it is also > than its sibling since x > parent > sibling
            self.heap[idx_parent - 1], self.heap[idx_x - 1] = self.heap[idx_x - 1], self.heap[idx_parent - 1]
            idx_x = idx_parent  # Update the index of x after the swap is made with the parent node
            idx_parent = idx_x // 2  # Update the parent node index based on the new index of x

    def pop(self):
        """
        Removes the element at the top of the heap and returns it i.e. the max element.
        """
        if len(self.heap) == 0:
            raise IndexError("Cannot pop from an empty heap")

        # To minimize the number of operations needed, we swap the root node with the last leaf node and
        # maintain the ordering of the other elements as is, which are assumed to already satisfy the heap
        # property. Then we remove the last leaf node to get the max-value to be returned. Then we process
        # the root node value which may not be in the right place and have it swim down unti it is in the
        # right location
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]  # Swap the root and last leaf node
        output = self.heap.pop()  # Remove the last leaf node element
        # Now process the element at the root node location, iterate until it has be correctly moved
        idx_x = 1  # Use 1-indexing, track where this misplaced value x is located
        n = len(self.heap)
        while idx_x <= n:  # Stop iterating if it becomes the last leaf node, no further swimming down is
            # possible or needed for this x value to find its right location in the binary tree
            idx_L, idx_R = idx_x * 2, idx_x * 2 + 1  # Get the indices of the left and right children
            # Make swaps as needed to make sure the parent node is smaller than the current node
            idx, L, R = idx_x - 1, idx_L - 1, idx_R - 1  # Convert to 0 indexing for brevity

            # Check if the child elements exist, if so then we can make comparisons with it
            has_left, has_right = idx_L <= n, idx_R <= n

            if has_left is True:  # The left child exists (left child must exist for right child to exist)
                bool_1 = self.heap[idx] < self.heap[L]  # Check if x < left child, if so then swap needed
                if has_right is True:  # The right child also exists
                    # Check if either child node is smaller than the parent node x
                    bool_2 = self.heap[idx] < self.heap[R]  # Check if x < right child, if so then swap
                    if (bool_1 or bool_2):  # If either is true, then a swap is needed
                        if self.heap[L] > self.heap[R]:  # The left child is larger than the right child so
                            # swap with the left one so that the new parent > both children
                            self.heap[L], self.heap[idx] = self.heap[idx], self.heap[L]
                            idx_x = idx_L  # Update the new index of x after making this swap
                        else:  # Then the right child is larger so swap x currently in the parent node with
                            # the right child element so that the new parent > both children
                            self.heap[R], self.heap[idx] = self.heap[idx], self.heap[R]
                            idx_x = idx_R  # Update the new index of x after making this swap
                    else:  # Otherwise the value x is now in the right spot i.e. x > left_child, right_child
                        break
                else:  # No right child element, only compare with the left
                    if bool_1:  # Then x < left child so we need to swap them
                        self.heap[L], self.heap[idx] = self.heap[idx], self.heap[L]
                        idx_x = idx_L  # Update the new index of x after making this swap
                    else:  # The value x is now in the right spot i.e. x > left_child, the only child
                        break
            else:  # Doesn't have any child nodes, already a leaf node, no further comparisons to make
                break

        return output

    def size(self) -> int:
        """
        Returns the number of elements in the heap.
        """
        return len(self.heap)

    def top(self):
        """
        Returns the element at the top of the heap without removing it.
        """
        return self.heap[0]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.heap)

    def __len__(self):
        return self.size()
