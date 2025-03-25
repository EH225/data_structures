# -*- coding: utf-8 -*-
"""
Deque data structure module, see help(Deque) for details.
"""

from typing import Optional


#############
### Deque ###
#############

class ListNode:
    def __init__(self, val, prev_=None, next_=None):
        """
        Doubly linked list node data structure.
        """
        self.val = val
        self.prev_ = prev_
        self.next_ = next_


class Deque:
    """
    A data structure that supports insertion and deletion at the front and back in O(n) time. Uses a doubly
    linked list internal data structure.
    """

    def __init__(self, k: int = 100):
        self.k = k  # The max capacity of the deque
        self.n = 0  # The number of elements in the deque
        self.head = None  # The root of the linked list
        self.tail = None  # The end of the linked list

    def append_left(self, value: int) -> None:
        """
        Appends a new element to the front of the deque if possible.

        :param value: The value to be added to the front of the deque.
        :returns: None, adds this new value to the data structure.
        """
        if self.n < self.k:  # Can only add if space available
            if self.n == 0:  # No nodes exist yet
                self.head = ListNode(val=value)
                self.tail = self.head  # Only 1 node, both are the same
            else:  # Otherwise add to the existing linked list
                self.head.prev_ = ListNode(val=value, next_=self.head)
                self.head = self.head.prev_
            self.n += 1

    def append(self, value: int) -> None:
        """
        Appends a new element to the end of the deque if possible.

        :param value: The value to be added to the end of the deque.
        :returns: None, adds this new value to the data structure.
        """
        if self.n < self.k:  # Can only add if space available
            if self.n == 0:  # No nodes exist yet
                self.head = ListNode(val=value)
                self.tail = self.head  # Only 1 node, both are the same
            else:  # Otherwise add to the existing linked list
                self.tail.next_ = ListNode(val=value, prev_=self.tail)
                self.tail = self.tail.next_
            self.n += 1

    def pop_left(self) -> Optional[int]:
        """
        Removes the first element in the deque if possible and returns its value.
        """
        if self.n == 0:  # Nothing to delete
            return None
        else:
            return_val = self.head.val
            if self.n == 1:  # Only 1 node
                self.head, self.tail = None, None
            else:  # At least 2 nodes
                self.head = self.head.next_
                self.head.prev_ = None
            self.n -= 1
            return return_val

    def pop(self) -> Optional[int]:
        """
        Removes the last element in the deque if possible and returns its value.
        """
        if self.n == 0:  # Nothing to delete
            return None
        else:
            return_val = self.tail.val
            if self.n == 1:  # Only 1 node
                self.head, self.tail = None, None
            else:  # At least 2 nodes
                self.tail = self.tail.prev_
                self.tail.next_ = None
            self.n -= 1
            return return_val

    def get_front(self) -> int:
        """
        Return the element from the front of the deque or -1 if empty.
        """
        return self.head.val if self.n > 0 else -1

    def get_rear(self) -> int:
        """
        Return the element from the rear of the deque or -1 if empty.
        """
        return self.tail.val if self.n > 0 else -1

    def is_empty(self) -> bool:
        """
        Return True if the deque is empty and False otherwise
        """
        return self.n == 0

    def is_full(self) -> bool:
        """
        Return True if the deque is full and False otherwise.
        """
        return self.n == self.k

    def __str__(self) -> str:
        """
        Returns a string representation of the deque.
        """
        return self.__repr__()

    def __len__(self) -> int:
        """
        Returns the number of element currently in the deque.
        """
        return self.n

    def __repr__(self) -> str:
        """
        Returns a string representation of the deque.
        """
        output = []
        node = self.head
        while node is not None:
            output.append(str(node.val))
            node = node.next_
        return "[" + ", ".join(output) + "]"
