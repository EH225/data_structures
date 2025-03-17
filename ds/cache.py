# -*- coding: utf-8 -*-
"""
LRU cache and LFU cache data structures.
"""

from collections import defaultdict, OrderedDict


#################
### LFU Cache ###
#################

class ListNode:
    def __init__(self, val, prev=None, next=None):
        self.val = val
        self.next = next
        self.prev = prev


class LRUCache:
    """
    Least recently used cache (LFU) data structure. Caches elements and 
    drops the one that was least recently used when out of space and adding
    a new element.
    
    Great explination: https://www.romaglushko.com/blog/design-lru-cache/
    """

    def __init__(self, capacity: int):
        self.capacity = capacity  # How many keys in total may be stored
        self.dict = {}  # A hashmap to quickly find data associated with
        # each key
        # Also store the head and tail of a double linked list that will
        # be able to track our usage of different keys. When a key is used
        # or added, it will be added to the tail and removed from the other
        # part of the list if it exists already
        self.head, self.tail = None, None
        # When we want to add a new element and there are too many to add, we
        # will drop the most element most distantly used, i.e. the head element
        # and we will know what that is by keeping a pointer to the head of
        # this linked list in memory

    def get(self, key: int) -> int:
        """
        Returns the value associated with a key if it exists, and -1 otherwise.
        """
        val, node = self.dict.get(key, (-1, None))  # Attempt to retrieve val
        if node is not None:  # Then this key does exist already, update the
            # internal linked list to reflect that it has been recently used
            self._update_usage(key)
        return val

    def _update_usage(self, key: int) -> None:
        node_pointer = self.dict[key][1]  # Get the node pointer of this key
        if node_pointer == self.tail:  # If this node is already the tail node
            return None  # then return None, nothing to update
        else:  # Move this existing node from where it currently is to the tail
            if node_pointer == self.head:  # If the head node, handle special case
                # self.head != self.tail since the above condition was not met
                self.head = self.head.next  # Move to the next node
                self.head.prev = None  # Disconnect to make this the new head
            else:  # If not the first node, nor the last, update pointers
                # Link the prior node to the next node to skip over this node
                node_pointer.prev.next = node_pointer.next
                node_pointer.next.prev = node_pointer.prev
            # Now add this removed node to the end as a new node
            self.tail.next = node_pointer  # Move to the tail of the LL
            node_pointer.prev = self.tail  # Link backwards
            self.tail = self.tail.next  # Update the tail reference
            self.tail.next = None  # Break the old next connection, the tail
            # node should always have a .next pointing to None

    def _add_new_key(self, key: int) -> None:
        if self.tail is None:  # If no linked list currently
            self.head = ListNode(val=key)
            self.tail = self.head
        else:  # If there is already a tail node, add the new node at the end
            self.tail.next = ListNode(val=key, prev=self.tail)  # Add node
            self.tail = self.tail.next  # Update tail pointer

    def put(self, key: int, value: int) -> None:
        # If the key already exists, update the value already there
        if key in self.dict:
            self.dict[key][0] = value  # Edit the value of the key
            self._update_usage(key)  # Reflect that this key was recently used

        else:  # Otherwise if not already in the dict, add it
            self._add_new_key(key)  # Add the new key to the recency linked list
            self.dict[key] = [value, self.tail]  # Store both the value and node pointer
            # keys added are always added at the end and become the new tail node

            if len(self.dict) > self.capacity:  # Check if adding this new element
                # puts us over the limit, ifso, drop the most distantly used element
                drop_key = self.head.val  # The element used least recently
                self.head = self.head.next  # Move the head to the next element, which
                # is guarenteed to exist since we just added a new node which put us
                # over the limit which is >= 1
                self.head.prev = None  # Drop the prior ref link
                del self.dict[drop_key]  # Delete from the dictionary as well


#################
### LFU Cache ###
#################


class LFUCache:
    def __init__(self, capacity: int):
        """
        Least frequently used cache (LFU) data structure. Caches elements and 
        drops the one that was least frequently used when out of space and adding
        a new element.
        """
        self.capacity = capacity  # The max number of elements allowed
        self.dict = {}  # Create a dict to hold the (key:(val, usage_count)) pairs
        self.freq_dict = defaultdict(OrderedDict)  # Create another dict to hold
        # (usage_count:OrderedDict(key:None)) to organize the frequency of uasge 
        # within each usage count bucket
        self.min_freq = None  # Keep track of the min usage frequency

    def _incriment_usage_count(self, key: int) -> None:
        """
        Increments the usage_count of a particular key by 1.
        """
        val, usage_count = self.dict[key]
        del self.freq_dict[usage_count][key]  # Remove from the old dict
        if len(self.freq_dict[usage_count]) == 0:  # If there are no keys left
            del self.freq_dict[usage_count]  # after the removal, drop this entry
            # If the bin this key was in no longer exists, check if that would
            if self.min_freq == usage_count:  # impact the min_freq value
                # If the usage_count bin that was just dropped was the min_freq
                self.min_freq += 1  # Then the new min_freq is 1 higher at the
                # new bin where this key is now stored
            # Otherwise, leave min_freq as is since there are still elements in
            # that usage_count bin that can be accessed
        new_usage_count = usage_count + 1  # Update the usage count by 1
        self.freq_dict[new_usage_count][key] = None  # Add this key to the new
        # usage count dict to reflect the get action
        self.dict[key][1] = new_usage_count  # Update the usage count

    def get(self, key: int) -> int:
        val, usage_count = self.dict.get(key, (-1, None))
        if usage_count is not None:
            # If the key does exist, update the usage_count
            self._incriment_usage_count(key)
        return val

    def put(self, key: int, value: int) -> None:
        if key in self.dict:  # If this key already exists
            self.dict[key][0] = value  # Update the value associated with the key
            self._incriment_usage_count(key)  # Record a new usage instance for this key

        else:  # Otherwise the key does not yet exist, so add it to the data structure
            self.dict[key] = [value, 1]  # The usage_count starts at 1 when added
            self.freq_dict[1][key] = None  # Add to the freq dict in the usage_count 1 bin
            # and create one if one doesn't already exist

            # Now check if adding this key has put us over the capacity limit
            if len(self.dict) > self.capacity:  # If so, then drop the least frequently
                # used element and break ties using the recency usage
                for key in self.freq_dict[self.min_freq]:  # Get the first key which
                    break  # is also the least frequently used key in this bin
                del self.freq_dict[self.min_freq][key]  # Remove key from bin
                # Drop the least frequently used key among all keys that have been
                # used min_freq number of times        
                if len(self.freq_dict[self.min_freq]) == 0:  # If this freq dict is now empty
                    del self.freq_dict[self.min_freq]  # then drop it from the data structure

                del self.dict[key]  # Drop this key from the other dict as well

            self.min_freq = 1  # The smallest min_freq can ever be is 1 which is now the
            # new min since we've added a new element with a usage count of 1
