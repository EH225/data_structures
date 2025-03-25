# -*- coding: utf-8 -*-
"""
Singly and doubly linked-lists data structures module, see help(LinkedList) and help(DoublyLinkedList) for
details.
"""

from typing import Union, Optional, List, Tuple, Iterable


##########################
### Singly Linked List ###
##########################

class ListNode:
    """
    A singly-linked list node.
    """

    def __init__(self, val: int, next_=None):
        self.val = val
        self.next_ = next_


class LinkedList:
    """
    Singly-linked list data-structure. Supports append and deletion operations at the head and tail in O(1)
    time. Supports append and deletion operations at an arbitrary index in O(n) time.
    """

    def __init__(self):
        self.head = None  # Maintain a reference to the first node
        self.tail = None  # Maintain a reference to the last node
        self.n = 0  # Record the total number of elements in the list

    def _get(self, index: int) -> Tuple[Optional[ListNode], Optional[ListNode]]:
        """
        Internal helper function for the get method. Returns the node located at index within the linked
        list or None if the index is out of range. Returns the node prior to the one at the given index if
        return_prev is set to True. If there is no node prior, None will be returned. The return order is
        (prior_node, node) if return_prev is True and just node alone if set to False.

        :param index: An integer index value denoting the element in the list to access.
        :param return_prev: Whether to also return the node prior to the one located at index as well.
            The default is False.
        :returns: Returns either the node located at index in the linked list if the index is in range or
            None. If return_prev is True, then a tuple of None or ListNode1 objects are returned.
        """
        if index < 0 or index >= self.n:  # Check for invalid indices
            return None, None
        else:  # Locate the element requested by traversing the list
            prev_node, node = None, self.head
            for i in range(index):
                prev_node, node = node, node.next_
            return prev_node, node

    def get(self, index: int, return_value: bool = True) -> Optional[Union[ListNode, int]]:
        """
        Retrieves the node or value of the node at the input index.

        :param index: An integer index value denoting the element in the list to access.
        :param return_value: Whether to return the value of the node or the node itself. The default is True.
        :returns: The value associated with a node or a pointer to the node itself at the index.
        """
        prev_node, node = self._get(index)
        if node is None:
            return None
        else:
            return node.val if return_value is True else node

    def insert(self, index: int = None, val: int = None) -> None:
        """
        In-place method for adding a new node with a value of val at a given index in the linked list.

        If index == 0, then the new node will be added at the head. If index == n or None, then the new node
        will be added at the end of the list. The new node will become the node at the index provided.

        :param val: The value to be added to the linked list.
        :param index: The index where the new value should be inserted, the default is None, which will result
            in the new node being appended to the end.
        :returns: None, adds a new node to the data structure.
        """
        if val is None:
            raise ValueError("val must not be None")

        index = self.n if index is None else index
        if index < 0 or index > self.n:
            raise IndexError(f"Index={index} out of range")

        if index == 0:  # Then insert before the head node, create a new head node with this value
            if self.head is None:  # No elements currently in the list
                new_node = ListNode(val=val)  # Create a new node
                self.head, self.tail = new_node, new_node
            else:  # If we already have a head node, insert prior
                self.head = ListNode(val=val, next_=self.head)

        elif index == self.n:  # Insert at the end, append a new node to the tail
            # If the length of the list is 0, then insertion will be at index 0 and handled above, otherwise
            # the length will be >= 1 so there must already be a tail node present
            self.tail.next_ = ListNode(val=val)  # Add a new tail node
            self.tail = self.tail.next_  # This new node is now the last node

        else:  # Otherwise insert the new node at an index somewhere internally, between the head and tail
            # Attempt to get this node from the list and its predecessor
            prev_node, node = self._get(index)
            new_node = ListNode(val=val, next_=node)
            prev_node.next_ = new_node

        self.n += 1  # Update length of list counter

    def append(self, val: int) -> None:
        """
        In-place method for appending a new value to the end of the linked list. This method is the same as
        using obj.insert(len(obj), val).

        :param val: The value to be added to the end of the linked list.
        :returns: None, adds a new node to the data structure.
        """
        self.insert(self.n, val)

    def pop(self, index: int = None) -> int:
        """
        In-place method for deleting a node located at a particular index in the linked list and returning
        the associated value. If index is left as None (not provided), the default behavior will be to pop
        from the end of the list. If the index provided is not valid, an IndexError is raised.

        :param index: An integer denoting the location of the node to be deleted. Must be [0, n-1].
        :returns: The associated value if possible for this node to be removed.
        """
        if self.n == 0:
            raise IndexError("Cannot pop from an empty list")

        index = self.n - 1 if index is None else index
        prev_node, node = self._get(index)
        if node is None:
            raise IndexError(f"Index={index} is out of range")

        ans = node.val  # Make note of what value this is before removing the node
        if self.n == 1:  # Remove the only node in the linked list
            self.head, self.tail = None, None

        else:  # Then there are at least 2 nodes in the linked list, we will
            # have either a prev or next node or both
            next_node = node.next_
            if prev_node is None:  # Delete the first element in the list
                self.head = node.next_  # Move head ref to next element
            elif next_node is None:  # Delete the last element in the list
                self.tail = prev_node  # Move the tail ref back 1 element
                self.tail.next_ = None  # Remove forward ref at new tail
            else:  # Delete some middle element in the linked list
                prev_node.next_ = next_node

        self.n -= 1  # Update length of list counter
        return ans

    def index(self, val: int) -> int:
        """
        Returns the first index where a given input value occurs in the linked list. If the provided value
        cannot be found, an index error is raised.
        """
        idx = 0  # Track the index of the node as the linked list is traversed
        node = self.head  # Begin with the head node
        while node is not None:  # Iterate until we reach the tail
            if node.val == val:  # Check if the target value is matched, if so return the index of occurence
                return idx
            else:  # Otherwise move to the next node and keep searching
                node = node.next_
                idx += 1
        raise IndexError(f"Could not locate {val} in linked list")

    def reverse(self) -> None:
        """
        In-place method that reverses the order of elements stored in the linked list.
        """
        if self.n > 1:  # Only need to take action if there is more than 1 node in the linked list
            stack = []  # Use a stack to perform a LIFO traversal of the nodes
            node = self.head

            while node is not None:
                stack.append(node)
                node = node.next_

            self.head = stack.pop()  # The old tail becomes the new head
            last_node = self.head  # Keep track of the prior node so that we can add the next_ linkage
            while stack:
                node = stack.pop()
                last_node.next_ = node
                last_node = node  # Update ref for next iteration

            node.next_ = None  # The new tail node is the old head node, set the next_ pointer to None
            self.tail = node  # Update the pointer to the tail node

    def __len__(self) -> int:
        """
        Returns the length of the linked list.
        """
        return self.n

    def __getitem__(self, index: int) -> ListNode:
        """
        Add support for indexing e.g. my_list[5]
        """
        if index < 0:  # Allow for negative indexing
            ref_idx = self.n - index * (-1)
        else:
            ref_idx = index
        node = self.get(index=ref_idx, return_value=False)
        if node is not None:
            return node
        else:
            raise IndexError(f"Index={index} is out of range")

    def __setitem__(self, index: int, val: int) -> None:
        """
        Supports obj[index] = val updates to existing nodes in the linked list.
        """
        node = self.get(index, return_value=False)
        if node is None:
            raise IndexError(f"Index={index} out of range")
        else:  # Update the value associated with this node
            node.val = val

    def __iter__(self) -> Optional[ListNode]:
        """
        Add support to allow for iteration e.g.
            a = LinkedList()
            a.addAtTail(1)
            a.addAtTail(2)
            a.addAtTail(3)
            for node in a:
                print(node.val)
        """
        current_node = self.head
        while current_node is not None:
            yield_node = current_node
            current_node = current_node.next_
            yield yield_node

    def __repr__(self) -> str:
        """
        Returns a string representation of the linked list.
        """
        if self.head is None:
            return "[]"
        else:
            node_vals = []
            node = self.head
            while node is not None:
                node_vals.append(str(node.val))
                node = node.next_
            return "[" + ", ".join(node_vals) + "]"

    def __str__(self) -> str:
        """
        Returns a string representation of the linked list.
        """
        return self.__repr__()


##########################
### Doubly Linked List ###
##########################

class DoublyListNode:
    """
    Doubly-linked list node.
    """

    def __init__(self, val, prev_=None, next_=None):
        self.val = val
        self.prev_ = prev_
        self.next_ = next_


class DoublyLinkedList:
    """
    A doubly-linked list data-structure.Supports append and deletion operations at the head and tail in O(1)
    time. Supports append and deletion operations at an arbitrary index in O(n) time.
    """

    def __init__(self):
        self.head = None  # Maintain a reference to the first node
        self.tail = None  # Maintain a reference to the last node
        self.n = 0  # Record the total number of elements in the list

    def _get(self, index: int) -> Optional[DoublyListNode]:
        """
        Internal helper function for the get method. Returns the node located at index within the linked
        list or None if the index is out of range.

        :param index: An integer index value denoting the element in the list to access.
        :returns: Either the node located at index in the linked list if the index is in range or None.
        """
        if index < 0 or index >= self.n:  # Check for invalid indices
            return None
        else:  # Locate the element requested by traversing the list
            # We can find it faster by iterating from the side that the index is closest to
            # # i.e. either the head or tail and moving inwards
            if index + 1 <= self.n // 2:  # The index is in the first half
                node = self.head  # Start from the head and move right
                for i in range(index):
                    node = node.next_
            else:  # The index is in the second half of the list
                node = self.tail  # Start from the tail and move left
                for i in range(self.n - 1 - index):
                    node = node.prev_
            return node

    def get(self, index: int, return_value: bool = True):
        """
        Retrieves the node or value of the node at the input index.

        :param index: An integer index value denoting the element in the list to access.
        :param return_value: Whether to return the value of the node or the node itself. The default is True.
        :returns: The value associated with a node or a pointer to the node itself at the index.
        """
        node = self._get(index)
        if node is None:
            return None
        else:
            return node.val if return_value is True else node

    def insert(self, index: int = None, val: int = None) -> None:
        """
        In-place method for adding a new node with a value of val at a given index in the linked list.

        If index == 0, then the new node will be added at the head. If index == n or None, then the new node
        will be added at the end of the list. The new node will become the node at the index provided.

        :param val: The value to be added to the linked list.
        :param index: The index where the new value should be inserted, the default is None, which will result
            in the new node being appended to the end.
        :returns: None, adds a new node to the data structure.
        """
        if val is None:
            raise ValueError("val must not be None")

        index = self.n if index is None else index
        if index < 0 or index > self.n:
            raise IndexError(f"Index={index} out of range")

        if index == 0:  # Then insert before the head node, create a new head node with this value
            if self.head is None:  # No elements currently in the list
                new_node = DoublyListNode(val=val)  # Create a new node
                self.head, self.tail = new_node, new_node
            else:  # If we already have a head node, insert prior
                new_node = DoublyListNode(val=val, next_=self.head)
                self.head.prev_ = new_node  # Link back to the new node
                self.head = new_node  # This new node is now the first node

        elif index == self.n:  # Insert at the end, append a new node to the tail
            # If the length of the list is 0, then insertion will be at index 0 and handled above, otherwise
            # the length will be >= 1 so there must already be a tail node present
            new_node = DoublyListNode(val=val, prev_=self.tail)
            self.tail.next_ = new_node  # Link ahead to the new node
            self.tail = new_node  # This new node is now the last node

        else:  # Otherwise insert the new node at an index somewhere internally, between the head and tail
            # Attempt to get this node from the list and its predecessor
            node = self._get(index)  # Get a pointer to the node currently at this index in the list
            prev_node = node.prev_
            new_node = DoublyListNode(val=val, next_=node, prev_=prev_node)
            prev_node.next_, node.prev_ = new_node, new_node

        self.n += 1  # Update length of list counter

    def append(self, val: int) -> None:
        """
        In-place method for appending a new value to the end of the linked list. This method is the same as
        using obj.insert(len(obj), val).

        :param val: The value to be added to the end of the linked list.
        :returns: None, adds a new node to the data structure.
        """
        self.insert(self.n, val)

    def pop(self, index: int = None) -> int:
        """
        In-place method for deleting a node located at a particular index in the linked list and returning
        the associated value. If index is left as None (not provided), the default behavior will be to pop
        from the end of the list. If the index provided is not valid, an IndexError is raised.

        :param index: An integer denoting the location of the node to be deleted. Must be [0, n-1].
        :returns: The associated value if possible for this node to be removed.
        """
        if self.n == 0:
            raise IndexError("Cannot pop from an empty list")

        index = self.n - 1 if index is None else index

        node = self._get(index)  # Attempt to get this node from the list
        if node is None:
            raise IndexError(f"Index={index} is out of range")

        ans = node.val  # Make note of what value this is before removing the node
        if self.n == 1:  # Remove the only node in the linked list
            self.head, self.tail = None, None

        else:  # Then there are at least 2 nodes in the linked list, we will
            # have either a prev or next node or both
            prev_node, next_node = node.prev_, node.next_
            if prev_node is None:  # Delete the first element in the list
                self.head = node.next_  # Move head ref to next element
                self.head.prev_ = None  # Remove backward ref at new head
            elif next_node is None:  # Delete the last element in the list
                self.tail = node.prev_  # Move the tail ref back 1 element
                self.tail.next_ = None  # Remove forward ref at new tail
            else:  # Delete some middle element in the linked list
                prev_node.next_, next_node.prev_ = next_node, prev_node

        self.n -= 1  # Update length of list counter
        return ans

    def index(self, val: int) -> int:
        """
        Returns the first index where a given input value occurs in the linked list. If the provided value
        cannot be found, an index error is raised.
        """
        idx = 0  # Track the index of the node as the linked list is traversed
        node = self.head  # Begin with the head node
        while node is not None:  # Iterate until we reach the tail
            if node.val == val:  # Check if the target value is matched, if so return the index of occurence
                return idx
            else:  # Otherwise move to the next node and keep searching
                node = node.next_
                idx += 1
        raise IndexError(f"Could not locate {val} in linked list")

    def reverse(self) -> None:
        """
        In-place method that reverses the order of elements stored in the linked list.
        """
        if self.n > 1:  # Only need to take action if there is more than 1 node in the linked list
            node = self.head  # The old head becomes the new tail
            self.head, self.tail = self.tail, self.head  # Update pointers
            while node is not None:  # Iterate through and reverse the pointers
                node.next_, node.prev_ = node.prev_, node.next_
                node = node.prev_  # The next node to visit is now the prev node

    def __len__(self) -> int:
        """
        Returns the length of the linked list.
        """
        return self.n

    def __getitem__(self, index: int) -> Optional[DoublyListNode]:
        """
        Add support for indexing e.g. my_list[5]
        """
        if index < 0:  # Allow for negative indexing
            ref_idx = self.n - index * (-1)
        else:
            ref_idx = index
        node = self.get(index=ref_idx, return_value=False)
        if node is not None:
            return node
        else:
            raise IndexError(f"Index {index} is out of range")

    def __setitem__(self, index: int, val: int) -> None:
        """
        Supports obj[index] = val updates to existing nodes in the linked list.
        """
        node = self.get(index, return_value=False)
        if node is None:
            raise IndexError(f"Index={index} out of range")
        else:  # Update the value associated with this node
            node.val = val

    def __iter__(self) -> Optional[DoublyListNode]:
        """
        Add support to allow for iteration e.g.
            a = DoublyLinkedList()
            a.addAtTail(1)
            a.addAtTail(2)
            a.addAtTail(3)
            for node in a:
                print(node.val)
        """
        current_node = self.head
        while current_node is not None:
            yield_node = current_node
            current_node = current_node.next_
            yield yield_node

    def __repr__(self) -> str:
        """
        Returns a string representation of the linked list.
        """
        if self.head is None:
            return "[]"
        else:
            node_vals = []
            node = self.head
            while node is not None:
                node_vals.append(str(node.val))
                node = node.next_
            return "[" + ", ".join(node_vals) + "]"

    def __str__(self) -> str:
        """
        Returns a string representation of the linked list.
        """
        return self.__repr__()
