# -*- coding: utf-8 -*-
"""
Deque data structure.
"""

from typing import Optional


#############
### Deque ###
#############

class ListNode:
    def __init__(self, val, prev=None, next=None):
        # Use a doubly linked list
        self.val = val
        self.prev = prev
        self.next = next


class Deque:
    """
    A data structure that supports insertion and deletion at the front and back in O(n) time.
    """

    def __init__(self, k: int = 100):
        self.k = k  # The max capacity of the queue
        self.n = 0  # The number of elements in the queue
        self.head = None  # The root of the linked list
        self.tail = None  # The end of the linked list

    def appendLeft(self, value: int) -> None:
        """
        Append a new element to the front of the dequeue if possible.
        """
        if self.n < self.k:  # Can only add if space available
            if self.n == 0:  # No nodes exist yet
                self.head = ListNode(val=value)
                self.tail = self.head  # Only 1 node, both are the same
            else:  # Otherwise add to the existing linked list
                self.head.prev = ListNode(val=value, next=self.head)
                self.head = self.head.prev
            self.n += 1

    def append(self, value: int) -> None:
        """
        Append a new element to the end of the dequeue if possible.
        """
        if self.n < self.k:  # Can only add if space available
            if self.n == 0:  # No nodes exist yet
                self.head = ListNode(val=value)
                self.tail = self.head  # Only 1 node, both are the same
            else:  # Otherwise add to the existing linked list
                self.tail.next = ListNode(val=value, prev=self.tail)
                self.tail = self.tail.next
            self.n += 1

    def popLeft(self) -> Optional[int]:
        """
        Remove the first element in the deque if possible and returns its value.
        """
        if self.n == 0:  # Nothing to delete
            return None
        else:
            return_val = self.head.val
            if self.n == 1:  # Only 1 node
                self.head, self.tail = None, None
            else:  # At least 2 nodes
                self.head = self.head.next
                self.head.prev = None
            self.n -= 1
            return return_val

    def pop(self) -> Optional[int]:
        """
        Remove the last element in the deque if possible and returns its value.
        """
        if self.n == 0:  # Nothing to delete
            return None
        else:
            return_val = self.tail.val
            if self.n == 1:  # Only 1 node
                self.head, self.tail = None, None
            else:  # At least 2 nodes
                self.tail = self.tail.prev
                self.tail.next = None
            self.n -= 1
            return return_val

    def getFront(self) -> int:
        """
        Return the element from the front of the deque or -1 if empty.
        """
        return self.head.val if self.n > 0 else -1

    def getRear(self) -> int:
        """
        Return the element from the rear of the deque or -1 if empty.
        """
        return self.tail.val if self.n > 0 else -1

    def isEmpty(self) -> bool:
        """
        Return True if the deque is empty and False otherwise
        """
        return self.n == 0

    def isFull(self) -> bool:
        """
        Return True if the deque is full and False otherwise.
        """
        return self.n == self.k

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        n = 0
        node = self.head
        while node is not None:
            n += 1
            node = node.next
        return n

    def __repr__(self) -> str:
        output = []
        node = self.head
        while node is not None:
            output.append(str(node.val))
            node = node.next
        return "[" + ", ".join(output) + "]"
