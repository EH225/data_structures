# -*- coding: utf-8 -*-
"""
Binary search tree.
"""

from typing import Union, Optional, List, Tuple, Iterable
from collections import deque


##########################
### Binary Search Tree ###
##########################

class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left, self.right = left, right


class BinarySearchTree:
    """
    Binary search tree data-structure.
    """

    def __init__(self):
        self.root = None  # Stores the root node for this
        self.n = 0  # Record how many nodes are in the tree

    def search(self, val: Union[int, float]) -> Optional[TreeNode]:
        """
        Locates the node in the BST with the value of val and returns its pointer if it exists,
        otherwise None is returned.

        :param val: The value of the node to search for.
        :returns: Returns either a pointer to the node associated with val in the BST or None.
        """
        return self._search(self.root, val)

    def _search(self, root: Optional[TreeNode], val: Union[int, float]) -> Optional[TreeNode]:
        """
        Recursive helper function for locating a node with the value of val in the BST. Returns a 
        pointer to the node with this value if it exists, otherwise None is returned.

        :param root: The root node of a BST through which to search for the node containing val.
        :param val: The value of the node to search for.
        :returns: Returns either a pointer to the node associated with val in the BST or None.
        """
        if root is None:  # Base case, if this root value is None, return None
            return None  # Must check this one first since None has no .val property
            # so we would get an error if we tried checking the other first
        elif root.val == val:  # If we find the node with this matching value, return it
            return root
        else:
            # Otherwise we have not yet found the val, but it could still exist down the
            # tree some place else, continue to search for it recursively, use the properties
            # of a BST to search the branch that is applicable given root.val's size vs val
            if root.val > val:  # What we are looking for is smaller, go left
                return self._search(root.left, val)  # Search down the left side
            else:  # root.val < val # What we are looking for is larger, go right
                return self._search(root.right, val)

    def insert(self, val: Union[float, int]) -> None:
        """
        In-place method for adding a new value to the BST.

        :param val: The value to be added.
        :returns: None.
        """
        self.root = self._insert(self.root, val)
        self.n += 1

    def _insert(self, root: Optional[TreeNode], val: int) -> TreeNode:
        """
        Recursive helper function to insert a new value into the BST. Returns a TreeNode object
        i.e. the root of the new BST after insertion.

        :param root: The root node of an existing sub-tree.
        :param val: The value to be added.
        :returns: Returns the root of the new BST after insertion as been done.
        """
        if root is None:  # Base-case when we reach a None ending
            return TreeNode(val=val)
        else:  # Otherwise search and recursively set a new node
            if root.val > val:  # The value to be added is smaller than the root
                root.left = self._insert(root.left, val)  # Add it somewhere on the left
            else:  # The value to be added is greater than or equal to the root
                root.right = self._insert(root.right, val)  # Add it somewhere on the right
        return root

    def delete(self, val: Union[float, int]) -> None:
        """
        In-place method for deleting a value from the BST if it exists.

        :param: val: The value to be deleted from the BST.
        :returns: None.
        """
        if self.search(val) is not None:
            self.n -= 1
        self.root = self._delete(self.root, val)

    def _delete(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """
        Recursive helper function for deleting a node from the BST.

        Approach: This operation can be completed in 2 steps.
        1). First we search the tree and try to locate the key.
        2). If it is found, then we delete the node, otherwise we do nothing.

        Deleting a node can be done by handling the following 3 cases:
        1). If the node has no children, we can delete it without any other steps
        2). If a node has 1 child, we can remove it by replace it with the child
            node leftover
        3). If a node as 2 children, then we can replace its value with the next
            in-order successor and delete the next-inorder successor node.

        :param root: The root of an existing sub-tree.
        :param key: The value in the tree to be deleted.
        :returns: None.
        """
        if root is None:  # Handle special edge case
            return root

        # 1). Search in the BST for this key value and see if it exists, keep track
        #     of what node (if any) precedes it
        key_node, prior_node = self._treeSearch(root, None, key)
        if key_node is not None:  # Then key is in the tree, take steps to delete it
            n_successors = (key_node.left is not None) * 1 + (key_node.right is not None) * 1

            if n_successors == 0:  # If no children, then delete without other steps
                if prior_node is None:  # Special case, root = key_node
                    return None  # Then return None since this that was the only node
                if prior_node.left is not None and prior_node.left.val == key:
                    prior_node.left = None
                else:
                    prior_node.right = None

            elif n_successors == 1:  # If there is 1 child, then replace the key_node with
                # that one child node
                child_node = key_node.left if key_node.left is not None else key_node.right
                if prior_node is None:  # Special case, root = key_node
                    return child_node  # The child node becomes the new root node

                if prior_node.left is not None and prior_node.left.val == key:
                    prior_node.left = child_node
                else:
                    prior_node.right = child_node

            else:  # If there are 2 child nodes, then replace the key_node with the next
                # in-order successor and delete from the tree
                IO_successor = self.inorderSuccessor(root, key_node)  # The in-order successor
                key_node.val = IO_successor.val  # Replace value with in-order successor val
                # Since this key_node has 2 children, we know that the in-order successor must
                # be from the right child since there is a right child. The only way for the
                # IO successor to be the parent node is iff key_node has 1 or fewer children
                # That case is already handled above.
                # Once we make the value swap, then delete the IO successor from the right branch
                key_node.right = self._delete(key_node.right, IO_successor.val)

        # Return the tree root at the end regardless of which above operation were triggered
        return root

    def _treeSearch(self, root: Optional[TreeNode], prior_node: Optional[TreeNode],
                    key: int) -> Tuple[Optional[TreeNode], Optional[TreeNode]]:
        """
        Helper function that returns a pointer to the node that has a value equal to key and
        a pointer to the that node's parent. Returns None for either or both if they do not
        exist. E.g. if key cannot be found, we return None for both. If key is found at the root
        then we return None for prior_node.

        :param root: The root node of an existing sub-tree or None.
        :param prior_node: The node prior to root, i.e. the parent of root or None if it has no parent.
        :param key: The key to locate in the BST.
        :returns: Returns the node and its prior node as a tuple (in that order) if they exist or None
            values instead within the tuple.
        """
        if root is None or root.val == key:  # Base-case, when we either reach the node we
            # are looking for or a None ending indicating that it does not exist
            prior_node = prior_node if root is not None else None
            return root, prior_node
        else:  # Use recursion to evaluate
            if root.val > key:  # Then look down the left-side for the key value
                return self._treeSearch(root.left, root, key)
            else:  # root.val < key so look down the right-side for the key value
                return self._treeSearch(root.right, root, key)

    def inorderSuccessor(self, root: TreeNode, p: TreeNode) -> Optional[TreeNode]:
        """
        To return the in-order successor of p, we will need to handle things in a few
        different cases:
            1). If node p has a right child, then we want to get the left-most child
                of that right successor. A right child means that there is a value larger
                in the tree, and we want the one that is minimally larger so we will look
                for the left-most node in that sub-tree.
            2). If node p does NOT have a right child, then we need to return the last node
                where we took a left turn when traversing the BST to get to p. We can do this
                by recording last_left_turn as we traverse the tree until we find p and return
                it once we reach node p.

        :param root: The root node of a BST.
        :param p: The target node to find the in-order successor of within the BST.
        :returns: Either the node that is the in-order successor of p or None if there is none.
        """
        if p.right is not None:  # If there is a right child node, then return the left-most
            # node of that subtree (i.e. the minimal node larger than p). The subtree that
            # is a right child of p contains the next largest values relative to p
            node = p.right  # Switch to the right child node
            while node.left is not None:  # Iterate until we find the left most node in this subtree
                node = node.left
            return node

        # Otherwise, traverse the BST and return the node that we made a left at last once
        # we reach node p
        last_left_turn = None  # If we never make a right turn, return None, set as the default
        node = root  # Create alias
        target = p.val  # The value we are looking for i.e. p's value
        while node.val != target:  # Iterate until we locate node p
            if node.val < target:  # So increase node.val by going right
                node = node.right
            else:  # node.val > target so decrease node.val by going left
                last_left_turn = node  # Record the node whenever we make a left turn
                node = node.left
        # Once we reach node p which is guaranteed to be in the original tree, return the node
        # where we made our last left turn in the process of getting there
        return last_left_turn

    def rebalance(self) -> None:
        """
        Operates in-place and re-builds the binary search tree stored at self.root into a height-balanced
        binary search tree.
        """
        self.root = self._balanced_BST(self.inOrderTraversal())

    def _balanced_BST(self, inOrderNodeList: list) -> Optional[TreeNode]:
        """
        Helper function that returns a height-balanced BST built off an in-order node traversal.
        """
        if len(inOrderNodeList) == 0:  # Recursion base-case
            return None
        elif len(inOrderNodeList) == 1:
            return TreeNode(val=inOrderNodeList[0])
        else:
            n = len(inOrderNodeList) // 2  # Create a new root using the central element
            root = TreeNode(val=inOrderNodeList[n])
            root.left = self._balanced_BST(inOrderNodeList[:n])  # Recursively construct LHS
            root.right = self._balanced_BST(inOrderNodeList[(n + 1):])  # Recursively construct RHS
            return root

    def find_first_le(self, val: Union[int, float]) -> Optional[Union[int, float]]:
        """
        Finds the first value in the BST that is less than or equal to a given input value.
        Returns None if there is no value that is less than or equal to the value provided.

        :param val: The value that is a ceiling for the largest element to returns from the tree.
        :returns: Returns the largest value in the BST that is less than or equal to val.
        """
        return self._find_le(self.root, val)

    def _find_le(self, root: Optional[TreeNode], val: int) -> Optional[Union[int, float]]:
        """
        Recursive helper function for finding the largest value in the BST that is less than or
        equal to the input val.

        :param val: The value that is a ceiling for the largest element to returns from the tree.
        :returns: Returns the largest value in the BST that is less than or equal to val.
        """
        if root is None:
            return None
        elif root.val == val:  # Exact match found
            return val
        elif val < root.val:  # The val we seek is smaller than this head node so
            # disregard all larger nodes to the right, this head node is also not an
            # option since it is > than the target value
            return self._find_le(root.left, val)
        else:  # if val > root.val # Then this root node is below val, return whichever
            # is larger, this node value or the smallest from the right subtree that is
            # still below val
            right_le = self._find_le(root.right, val)
            if right_le is None:  # If there is no value to the right smaller than val
                return root.val  # Then the root val is the best we can do
            else:  # Otherwise compare the vals and return the larger of the 2 to maximize
                # the lower bound i.e. the largest value in the tree <= val
                return max(root.val, right_le)

    def find_first_ge(self, val: Optional[Union[int, float]]) -> Optional[Union[int, float]]:
        """
        Finds the first value in the BST that is greater than or equal to a given input value.
        Returns None if there is no value that is greater than or equal to the value provided.

        :param val: The value that is a floor for the smallest element to returns from the tree.
        :returns: Returns the smallest value in the BST that is greater than or equal to val.
        """
        return self._find_ge(self.root, val)

    def _find_ge(self, root: Optional[TreeNode], val: int) -> Optional[Union[int, float]]:
        """
        Recursive helper function for finding the smallest value in the BST that is greater than or
        equal to the input val.

        :param val: The value that is a floor for the smallest element to returns from the tree.
        :returns: Returns the smallest value in the BST that is greater than or equal to val.
        """
        if root is None:
            return None
        elif root.val == val:  # Exact match found
            return val
        elif val > root.val:  # The val we seek is larger than this head node so
            # disregard all smaller nodes to the left, this head node is also not an
            # option since it is < than the target value
            return self._find_ge(root.right, val)
        else:  # if val < root.val # Then this root node is above val, return whichever
            # is smaller, this node value or the largest from the left subtree that is
            # still above val
            left_ge = self._find_ge(root.left, val)
            if left_ge is None:  # If there is no value to the left greater than val
                return root.val  # Then the root val is the best we can do
            else:  # Otherwise compare the vals and return the smaller of the 2 to minimize
                # the upper bound i.e. the smallest value in the tree >= val
                return min(root.val, left_ge)

    def preOrderTraversal(self, root: Optional[TreeNode] = 0, return_vals: bool = True) -> list:
        """
        Returns the pre-order traversal of the BST nodes: [root, left, right]

        :param root: The root node of a BST. If set to 0, this method operates on the entire BST.
        :param return_vals: Whether to return values or node pointers from the BST.
        :returns: A list of nodes or values from the pre-order traversal of the BST rooted at root.
        """
        if root == 0:  # Auto-detect if root should be set to the internal BST tree root
            root = self.root

        if root is None:
            return []
        else:  # Visit the root, the left, then the right
            nodes = [root.val] if return_vals is True else [root]
            nodes.extend(self.preOrderTraversal(root.left, return_vals))
            nodes.extend(self.preOrderTraversal(root.right, return_vals))
            return nodes

    def inOrderTraversal(self, root: Optional[TreeNode] = 0, return_vals: bool = True) -> list:
        """
        Returns the in-order traversal of the BST nodes: [left, root, right]

        :param root: The root node of a BST. If set to 0, this method operates on the entire BST.
        :param return_vals: Whether to return values or node pointers from the BST.
        :returns: A list of nodes or values from the in-order traversal of the BST rooted at root.
        """
        if root == 0:  # Auto-detect if root should be set to the internal BST tree root
            root = self.root

        if root is None:
            return []
        else:
            nodes = []
            nodes.extend(self.inOrderTraversal(root.left, return_vals))
            if return_vals is True:
                nodes.append(root.val)
            else:
                nodes.append(root)
            nodes.extend(self.inOrderTraversal(root.right, return_vals))
            return nodes

    def postOrderTraversal(self, root: Optional[TreeNode] = 0, return_vals: bool = True) -> list:
        """
        Returns the post-order traversal of the BST nodes: [left, right, root]

        :param root: The root node of a BST. If set to 0, this method operates on the entire BST.
        :param return_vals: Whether to return values or node pointers from the BST.
        :returns: A list of nodes or values from the post-order traversal of the BST rooted at root.
        """
        if root == 0:  # Auto-detect if root should be set to the internal BST tree root
            root = self.root

        if root is None:
            return []
        else:  # Visit the left, then the right, then the root
            nodes = self.postOrderTraversal(root.left, return_vals)
            nodes.extend(self.postOrderTraversal(root.right, return_vals))
            if return_vals is True:
                nodes.append(root.val)
            else:
                nodes.append(root)
            return nodes

    def levelOrderTraversal(self, root: Optional[TreeNode] = 0, return_vals: bool = True,
                            return_levels: bool = False) -> list:
        """
        Returns the level-order traversal of the BST nodes as a list or list of lists.

        :param root: The root node of a BST. If set to 0, this method operates on the entire BST.
        :param return_vals: Whether to return values or node pointers from the BST.
        :param return_levels: Whether to return a list of lists, one for each layer.
        :returns: A list of nodes or values from the level-order traversal of the BST rooted at root.
            Could be either a list or a list of lists.
        """
        if root == 0:  # Auto-detect if root should be set to the internal BST tree root
            root = self.root

        if root is None:
            return []

        levels = []  # A list of lists, one for each layer
        node_queue = deque([root])  # Use BFS to perform a level order traversal
        while node_queue:  # Iterate until out of nodes in the queue
            level = []  # Populate node values for all nodes in this layer
            for i in range(len(node_queue)):  # Pop all nodes in this layer
                node = node_queue.popleft()  # Get the next node
                if return_vals is True:
                    level.append(node.val)  # Record its value in this layer's list
                else:
                    level.append(node)  # Record a pointer to this node in the layer list
                if node.left is not None:  # Add left child to queue if available
                    node_queue.append(node.left)
                if node.right is not None:  # Add left right to queue if available
                    node_queue.append(node.right)
            levels.append(level)  # Store this set of level's values in the agg list

        if return_levels:  # Return as a list of lists, one list for each level
            return levels
        else:  # Otherwise flatten the nodes into a linear list of nodes
            nodes = []
            for level in levels:
                nodes.extend(level)
            return nodes

    def isValidBST(self) -> bool:
        """
        Recursively evaluates if the BST rooted at root is a valid BST or not by checking that all values
        in the left subtree are <= root.val and that all values in the right subtree are >= root.val.
        Operates by recursively calling a DFS helper function on the left and right child nodes where
        root.val is provided to the left-subtree as the max and root.val is provided to the right-subtree as
        the min value.
        
        :returns: A bool indicating if the BST rooted at root is a valid BST.
        """
        return self._DFS(self.root.left, None, self.root.val) and self._DFS(self.root.right,
                                                                            self.root.val, None)

    def _DFS(self, node: Optional[TreeNode], low: Optional[int], high: Optional[int]) -> bool:
        """
        Helper function for isValidBST that checks if the tree with root as the root node is a valid BST
        based on the input low and high values provided.
        
        :param node: The root of this subtree to be evaluated if it is a valid BST.
        :param low: The min value we should find in this subtree i.e. all values must be >= low.
        :param high: The max value we should find in this subtree i.e. all values must be <= high.
        :returns: Returns a bool indicating if this subtree is a valid BST.
        """
        if node is None:  # If given a blank node, always return True, this is a base case
            return True
        if high != None and node.val >= high:  # If there is an upper limit established for this tree
            # check to make sure that this root node's value is not as large or greater, that would violate
            # the properties of a BST
            return False
        if low != None and node.val <= low:  # If there is a lower bound limit established for this tree
            # check to make sure that this root node's value is not as small or smaller, that would violate
            # the properties of a BST
            return False

        if (node.right is None and node.left is None):  # Another base-case, a node with no children is always
            # a valid BST, this comes second since we need to use the above ifs to check that this is a valid
            # child node of the prior parent node
            return True

        # If both of those conditions are met, then this node is valid for the parent node above it
        else:  # Then check if both children of this node are also valid BSTs as well recursively
            return self._DFS(node.left, low, node.val) and self._DFS(node.right, node.val, high)

    def __iter__(self) -> Optional[TreeNode]:
        """
        Returns the in-order traversal of nodes if iterated on.
        """
        in_order_nodes = self.inOrderTraversal(self.root, True)
        for node in in_order_nodes:
            yield node

    def __len__(self) -> int:
        return self.n

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return str(self.inOrderTraversal(self.root))

    def get_max_depth(self, root: Optional[TreeNode] = 0) -> int:
        """
        Recursive helper function that returns the max depth of the tree rooted at root. Runs on the self.root
        internal BST if root is left as the default value of 0. A tree with only a root is defined to have a
        depth of 1. A tree with no nodes is defined to have a depth of 0.
        
        :param root: The root node of a BST. If set to 0, this method operates on the entire BST.
        :returns: An integer value denoting the max depth of the tree along all of its branches.
        """
        if root == 0:  # Auto-detect that the root node should be used as the input
            root = self.root
        if root is None:  # Recursion base-case
            return 0
        else:  # Otherwise return the max of the child node max depths + 1 for this additional root node layer
            return max(self.get_max_depth(root.left), self.get_max_depth(root.right)) + 1

    def print_tree(self):
        """
        Prints the binary search tree stored at root to the console in a readable format that shows the
        structural relation of various elements to one another. Creates a binary tree with the root on the
        left and leaf elements that extend out to the right. Trees with a max depth up of up to 10 can be
        printed, otherwise it takes too long to print and compute.
        """

        def contains_digit(input_list: list) -> bool:
            """
            Helper function that checks if any entry in input_list is a numerical value. Returns True if any
            element of input_list is either an int or float type value.
            
            :param input_list: An input list of elements, could be of mixed type.
            :returns: A bool indicating if there is at least 1 element that is an int or float date type.
            """
            for x in input_list:
                if isinstance(x, int) or isinstance(x, float):
                    return True
            return False

        max_depth = self.get_max_depth(self.root)  # Get the max depth of the tree i.e. longest root-leaf dist
        width = 2 ** (max_depth - 1)  # Compute the max number of tree nodes that could be at the bottom depth
        width = width * 2 - 1  # Add in additional width for the spacing inbetween nodes, 1 between each val
        if max_depth >= 10:  # For trees that are too large, do not print, it will take too long
            print(f"Tree depth is too large ({max_depth} > 10) to print, try running .rebalance() first to "
                  "reduce the depth.")
            return None
        # Create a list of lists where each inner list is a row in the output print string. We will be 
        # including additional characters to draw the branches between values so we'll need more than just 
        # width number of place holders. Each column of vals is separated from others internally by a column 
        # to hold the branches so we need max_depth cols for the vals + (max_depth - 1) cols for the branching 
        # between. Similarly, for the rows, between 2 child nodes, we will want to have at least 1 space so
        # we'll need width*2 - 1 places
        print_str = [["   " for j in range(max_depth * 2 - 1)] for i in range(width)]
        node_stack = [(self.root, (width // 2, 0), width)]  # (node, (x, y), width), root begins at mid-x, y=0
        # The width of the tree where this node is at the center is important for computing the dist of the 
        # child nodes up and down from the current one. It is 1 + width // 2 = row diff to child nodes
        # Traverse the tree using DFS and fill in values and branch characters as we go
        while node_stack:  # Iterate until we've visited all nodes
            node, (x, y), w = node_stack.pop()  # Get the next node from the stack
            print_str[x][y] = node.val  # Add this node value to the tree where it belongs at (x, y)
            has_left = True if node.left is not None else False  # Check if there is a left child
            has_right = True if node.right is not None else False  # Check if there is a right child

            # Logic to add branch characters to the right of the value just added to the tree
            if has_left is True and has_right is True:  # If this nodes has 2 children, create a split
                print_str[x][y + 1] = " ┤ "
            elif has_left is True:  # If only a left child, indicate as such
                print_str[x][y + 1] = " ┐ "
            elif has_right is True:  # If only a right child, indicate as such
                print_str[x][y + 1] = " ┘ "
            # No branch characters added if this node has no children

            offset = w // 2 // 2 + 1  # Find the row offset size from this current node's x to the child nodes
            # we take the width of the tree that the current node sits in the middle of, split it in half to 
            # get the width of each left and right size, then take half of that to the midpoint within each 
            # half and add 1 since we need to move from the mid row of this width to one of the halfs and that
            # takes 1 step

            if has_left is True:  # Add additional branch characters to connect this node to the left child
                next_x = x + offset  # The x-val of the left child will be at a lower row, add the offset
                for x_ in range(x + 1, next_x):  # Down rows from this node's x to the left child x
                    print_str[x_][y + 1] = " | "  # Add in branch chars to connect this node to the left child
                print_str[next_x][y + 1] = " └ "  # Add a branch going into the left child 1 col prior
                # Add the left child to the stack with the next coordinate of where its value will be placed
                # and the width of the child's subtree is equal to current width split in 2
                node_stack.append((node.left, (next_x, y + 2), w // 2))

            if has_right is True:  # Add additional branch characters to connect this node to the right child
                next_x = x - offset  # The x-val of the right child will be at a higher row, subtract offset
                for x_ in range(next_x + 1,
                                x):  # Going up the rows from this node's x to the right child node
                    print_str[x_][
                        y + 1] = " | "  # Add in branch chars to connect this node to the right child
                print_str[next_x][y + 1] = " ┌ "  # Add a branch going into the right child 1 col prior
                # Add the right child to the stack with the next coordinate of where its value will be placed
                # and the width of the child's subtree is equal to current width split in 2
                node_stack.append((node.right, (next_x, y + 2), w // 2))

        # At the end, remove any row that does NOT have any numbers in it, these are not needed
        print_str = [row for row in print_str if contains_digit(row)]

        # Some values can be of different length, that causes some issues in the print out, make sure that all
        # values in a given column have the same length, add space padding if needed
        for c in range(len(print_str[0])):  # Loop over all cols
            col_vals = [print_str[r][c] for r in range(len(print_str))]
            if contains_digit(col_vals):  # Only edit if the column has values in it, cols are either value
                # cols or branch character cols but not both
                max_len = max([len(str(x)) for x in col_vals if not isinstance(x, str)])  # Max len among nums
                for r in range(len(print_str)):  # Now edit all the entries in this col to be the same length
                    if isinstance(print_str[r][c], str):  # If a str, then this is "   "
                        print_str[r][c] = " " * max_len  # Make the spacing the same length as the max len num
                    else:  # Otherwise this is a num, add " " space padding to the right as needed to make it
                        str_val = str(print_str[r][c])  # have the same max_len str length as everything else
                        print_str[r][c] = str_val + " " * (max_len - len(str_val))

        for row in print_str:  # Print each row
            print("".join(map(str, row)))
