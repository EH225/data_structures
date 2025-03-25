from all_ds import BinarySearchTree, BinaryIndexTree, Deque, DisjointSets, MinHeap, MaxHeap, LinkedList
from all_ds import DoublyLinkedList, SegmentTree, Trie, LRUCache, LFUCache
import pytest


def test_LinkedList():
    """
    Runs basic tests for the LinkedList data structure, tests methods and functionality.
    """
    test_data = [1, 5, 8, 7]
    obj = LinkedList()

    with pytest.raises(IndexError):  # Test indexing out of range
        obj[7]

    with pytest.raises(IndexError):  # Test inserting out of range
        obj.insert(5, 20)

    with pytest.raises(ValueError):  # Test inserting without providing a value
            obj.insert(5)

    with pytest.raises(IndexError):  # Test updating a node at a non-existant index
            obj[10] = 5

    with pytest.raises(IndexError):  # Test popping from an empty list
        obj.pop()

    obj.insert(0, 5)
    with pytest.raises(IndexError):  # Test popping from out of range
        obj.pop(5)

    assert obj.pop(0) == 5, "Test for pop failed"
    assert len(obj) == 0, "Pop from size 1 list test failed"

    assert str(obj) == "[]", "Test for str representation of linked list failed"
    for x in test_data:
        obj.append(x)

    with pytest.raises(IndexError):  # Test the index method on a value that doesn't exist
        obj.index(20)

    assert len(obj) == len(test_data), "len comparison test failed"
    assert str(test_data) == str(obj), "str representation comparison test failed"
    assert obj.head.val == test_data[0], "Test for obj.head failed"
    assert obj.tail.val == test_data[-1], "Test for obj.tail failed"
    for idx, (a, b) in enumerate(zip(test_data, obj)):
        assert a == b.val
        assert obj.index(a) == idx

    obj.reverse() # Reverse the order of the elements and run tests
    assert obj.head.val == test_data[-1], "Test for obj.head failed"
    assert obj.tail.val == test_data[0], "Test for obj.tail failed"
    for idx, (a, b) in enumerate(zip(test_data[::-1], obj)):
        assert a == b.val
        assert obj.index(a) == idx

    obj.reverse()

    obj.insert(len(obj), 10)
    assert obj[-1].val == 10, "Test for insert failed"

    obj.insert(0, -15)
    assert obj[0].val == -15, "Test for insert failed"

    obj.insert(3, 845315)
    assert obj[3].val == 845315, "Test for insert failed"

    val = obj[4].val
    assert obj[3].val == obj.pop(3), "Test for pop failed"
    assert obj[3].val == val, "Test for pop at index failed"

    obj = LinkedList()
    obj.insert(None, 15)
    assert obj.head.val == 15, "Test for insert in empty list failed"

    obj.insert(len(obj), 6)
    assert obj[-1].val == 6, "Test for insert at index n failed"

    obj.insert(0, 14)
    assert obj[0].val == 14, "Test for insert at 0 failed"

    val = obj[-2].val
    obj.pop(len(obj) - 1)
    assert obj.tail.val == val, "Test for pop at index n-1 failed"

    val = obj[1].val
    assert obj[0].val == obj.pop(0), "Test pop for index 0 failed "
    assert obj.head.val == val, "Test pop for index 0 failed "

    obj.insert(1, 50)
    obj[1] = 5
    assert obj[1].val == 5, "Test for set item failed"


def test_DoublyLinkedList():
    """
    Runs basic tests for the DoublyLinkedList data structure, tests methods and functionality.
    """
    test_data = [1, 5, 8, 7]
    obj = DoublyLinkedList()

    with pytest.raises(IndexError):  # Test indexing out of range
        obj[7]

    with pytest.raises(IndexError):  # Test inserting out of range
        obj.insert(5, 20)

    with pytest.raises(ValueError):  # Test inserting without providing a value
            obj.insert(5)

    with pytest.raises(IndexError):  # Test updating a node at a non-existant index
            obj[10] = 5

    with pytest.raises(IndexError):  # Test popping from an empty list
        obj.pop()

    obj.insert(0, 5)
    with pytest.raises(IndexError):  # Test popping from out of range
        obj.pop(5)

    assert obj.pop(0) == 5, "Test for pop failed"
    assert len(obj) == 0, "Pop from size 1 list test failed"

    assert str(obj) == "[]", "Test for str representation of linked list failed"
    for x in test_data:
        obj.append(x)

    with pytest.raises(IndexError):  # Test the index method on a value that doesn't exist
        obj.index(20)

    assert len(obj) == len(test_data), "len comparison test failed"
    assert str(test_data) == str(obj), "str representation comparison test failed"
    assert obj.head.val == test_data[0], "Test for obj.head failed"
    assert obj.tail.val == test_data[-1], "Test for obj.tail failed"
    for idx, (a, b) in enumerate(zip(test_data, obj)):
        assert a == b.val
        assert obj.index(a) == idx

    obj.reverse() # Reverse the order of the elements and run tests
    assert obj.head.val == test_data[-1], "Test for obj.head failed"
    assert obj.tail.val == test_data[0], "Test for obj.tail failed"
    for idx, (a, b) in enumerate(zip(test_data[::-1], obj)):
        assert a == b.val
        assert obj.index(a) == idx

    obj.reverse()

    obj.insert(len(obj), 10)
    assert obj[-1].val == 10, "Test for insert failed"

    obj.insert(0, -15)
    assert obj[0].val == -15, "Test for insert failed"

    obj.insert(3, 845315)
    assert obj[3].val == 845315, "Test for insert failed"

    val = obj[4].val
    assert obj[3].val == obj.pop(3), "Test for pop failed"
    assert obj[3].val == val, "Test for pop at index failed"

    obj = DoublyLinkedList()
    obj.insert(None, 15)
    assert obj.head.val == 15, "Test for insert in empty list failed"

    obj.insert(len(obj), 6)
    assert obj[-1].val == 6, "Test for insert at index n failed"

    obj.insert(0, 14)
    assert obj[0].val == 14, "Test for insert at 0 failed"

    val = obj[-2].val
    obj.pop(len(obj) - 1)
    assert obj.tail.val == val, "Test for pop at index n-1 failed"

    val = obj[1].val
    assert obj[0].val == obj.pop(0), "Test pop for index 0 failed "
    assert obj.head.val == val, "Test pop for index 0 failed "

    obj.insert(1, 50)
    obj.insert(2, 70)
    obj.insert(3, 80)
    obj[1] = 5
    assert obj[1].val == 5, "Test for set item failed"


def test_BinaryIndexTree():
    """
    Runs basic tests for the BinaryIndexTree data structure, tests methods and functionality.
    """
    test_data = [1, 2, 3, 5, 8, -10, 12]
    obj = BinaryIndexTree(test_data)
    assert len(obj) == len(test_data), "Failed len(obj) test"
    assert isinstance(str(obj), str), "Failed string representation test"

    for start in range(len(test_data)):  # Run tests on all possiable ranges
        for end in range(start, len(test_data)):
            assert sum(test_data[start:end + 1]) == obj.range_query(start, end), "Failed range_query test"

    obj.update(2, 5)
    test_data[2] = 5
    assert obj.range_query(1, 3) == sum(test_data[1:4]), "Failed update test"

    obj[2] = -5
    test_data[2] = -5
    assert obj.range_query(0, 4) == sum(test_data[0:5]), "Failed update test"

    obj[2] = 25
    test_data[2] = 25
    assert obj.range_query(2, 3) == sum(test_data[2:4]), "Failed update test"

    obj[2] = 25
    assert obj.range_query(2, 3) == sum(test_data[2:4]), "Failed update test - no change update"


def test_SegmentTree():
    """
    Runs basic tests for the SegmentTree data structure, tests methods and functionality.
    """
    test_data = [1, 2, 3, 5, 8, -10, 12]
    obj = SegmentTree(test_data, "sum")
    assert len(obj) == len(test_data), "Failed len(obj) test"
    assert isinstance(str(obj), str), "Failed string representation test"

    for start in range(len(test_data)):  # Run tests on all possiable ranges
        for end in range(start, len(test_data)):
            assert sum(test_data[start:end + 1]) == obj.range_query(start, end), "Failed range_query test"

    obj.update(2, 5)
    test_data[2] = 5
    assert obj.range_query(1, 3) == sum(test_data[1:4]), "Failed update test"

    obj[2] = -5
    test_data[2] = -5
    assert obj.range_query(0, 4) == sum(test_data[0:5]), "Failed update test"

    obj[2] = 25
    test_data[2] = 25
    assert obj.range_query(2, 3) == sum(test_data[2:4]), "Failed update test"

    obj[2] = 25
    assert obj.range_query(2, 3) == sum(test_data[2:4]), "Failed update test - no change update"

    obj.append(10)
    test_data.append(10)
    assert obj.range_query(2, 4) == sum(test_data[2:5]), "Failed append update test"

    assert obj.pop() == test_data.pop()
    assert obj.pop() == test_data.pop()
    assert obj.range_query(2, 4) == sum(test_data[2:5]), "Failed pop update test"

    with pytest.raises(ValueError):  # Test selecting an unknown eval function
        obj = SegmentTree(test_data, "xyz")


def test_BinarySearchTree():
    """
    Runs basic tests for the BinarySearchTree data structure, tests methods and functionality.
    """
    obj = BinarySearchTree()
    for x in list(range(30, 40)) + list(range(25)):
        obj.insert(x)

    assert len(obj) == 35, "Search for __len__ value check failed"

    assert obj.print_tree() is None  # Should give a print statement because the tree is too deep
    assert obj.search(10).val == 10, "Search for valid value check failed"
    assert obj.search(1.2) is None, "Search for missing value check failed"

    assert obj.inorderSuccessor(obj.root, obj.search(10)).val == 11, "inorderSuccessor check failed"
    assert obj.inorderSuccessor(obj.root, obj.search(39)) == None, "inorderSuccessor check failed"

    obj.rebalance()  # Should run without failure

    assert obj.find_first_le(28) == 24, "find_first_le check failed"
    assert obj.find_first_ge(28) == 30, "find_first_ge check failed"

    assert obj.preOrderTraversal() == [17, 8, 4, 2, 1, 0, 3, 6, 5, 7, 13, 11, 10, 9, 12, 15, 14, 16, 31, 22,
                                       20, 19, 18, 21, 24, 23, 30, 36, 34, 33, 32, 35, 38, 37, 39]
    inOrderTraversal = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                        24, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
    assert obj.inOrderTraversal() == inOrderTraversal, "Test for inOrderTraversal failed"
    assert [x for x in obj] == inOrderTraversal, "Test for inOrderTraversal failed"
    assert str(obj) == str(inOrderTraversal), "Test for inOrderTraversal failed"
    assert [x.val for x in obj.inOrderTraversal(return_vals=False)] == inOrderTraversal

    postOrderTraversal = [0, 1, 3, 2, 5, 7, 6, 4, 9, 10, 12, 11, 14, 16, 15, 13, 8, 18, 19, 21, 20, 23,
                          30, 24, 22, 32, 33, 35, 34, 37, 39, 38, 36, 31, 17]
    assert obj.postOrderTraversal() == postOrderTraversal, "Test for postOrderTraversal failed"
    assert [x.val for x in obj.postOrderTraversal(return_vals=False)] == postOrderTraversal

    levelOrderTraversal = [17, 8, 31, 4, 13, 22, 36, 2, 6, 11, 15, 20, 24, 34, 38, 1, 3, 5, 7, 10, 12, 14,
                           16, 19, 21, 23, 30, 33, 35, 37, 39, 0, 9, 18, 32]
    assert obj.levelOrderTraversal() == levelOrderTraversal, "Test for levelOrderTraversal failed"
    assert [x.val for x in obj.levelOrderTraversal(return_vals=False)] == levelOrderTraversal
    levels = [[17],
              [8, 31],
              [4, 13, 22, 36],
              [2, 6, 11, 15, 20, 24, 34, 38],
              [1, 3, 5, 7, 10, 12, 14, 16, 19, 21, 23, 30, 33, 35, 37, 39],
              [0, 9, 18, 32]]
    assert obj.levelOrderTraversal(return_levels=True) == levels, "Test for levelOrderTraversal failed"

    assert obj.isValidBST() is True, "Test for isValidBST failed"
    assert obj.get_max_depth() == 6, "Test for get_max_depth failed"

    for val in [30, 32, 18, 1, 17]:
        obj.delete(val)
        assert obj.search(val) is None, "Deletion check failed"

    assert obj.delete(500) is None, "Deletion check failed"
    assert obj.inorderSuccessor(obj.root, obj.search(7)).val == 8, "inorderSuccessor check failed"

    assert obj.find_first_le(obj.root.val) == obj.root.val, "find_first_le check failed"
    assert obj.find_first_ge(obj.root.val) == obj.root.val, "find_first_ge check failed"
    obj.print_tree()  # Should run without crashing


def test_Deque():
    """
    Runs basic tests for the Deque data structure, tests methods and functionality.
    """
    obj = Deque(10)
    assert obj.is_empty() is True, "Test for isEmpty failed"
    obj.append(5)
    obj.append_left(1)

    assert obj.get_front() == 1, "Test for getFront failed"
    assert obj.get_rear() == 5, "Test for getRear failed"
    for i in range(10):
        obj.append(i)

    assert obj.is_full() is True, "Test for isFull failed"
    assert obj.pop() == 7, "Test for pop failed"
    assert obj.pop_left() == 1, "Test for popLeft failed"
    assert obj.is_full() is False, "Test for isFull failed"
    assert len(obj) == 8, "Test for __len__ failed"
    assert str(obj) == "[5, 0, 1, 2, 3, 4, 5, 6]", "Test for __str__ failed"

    obj = Deque(10)
    assert obj.pop() is None, "Test for pop failed"
    assert obj.pop_left() is None, "Test for popLeft failed"
    obj.append_left(5)
    assert obj.pop() == 5, "Test for pop failed"
    obj.append(8)
    assert obj.pop_left() == 8, "Test for popLeft failed"


def test_MinHeap():
    """
    Runs basic tests for the MinHeap data structure, tests methods and functionality.
    """
    test_data = [1, 6, -9, 0, 12, 1, 8, 2]
    obj = MinHeap()

    with pytest.raises(IndexError):  # Test indexing out of range
        obj.pop()

    obj.push(5)
    assert obj.pop() == 5, "Test for pop failed"

    for x in test_data:
        obj.push(x)

    assert len(obj) == len(test_data), "Test for __len__ failed"
    assert str(obj) == '[-9, 0, 1, 2, 12, 1, 8, 6]', "Test for __str__ failed"
    assert obj.top() == min(test_data), "Test for top failed"

    test_data.sort(reverse=True)
    while test_data:
        assert test_data.pop() == obj.pop(), "Test for pop failed"


def test_MaxHeap():
    """
    Runs basic tests for the MaxHeap data structure, tests methods and functionality.
    """
    test_data = [1, 6, -9, 0, 12, 1, 8, 2]
    obj = MaxHeap()

    with pytest.raises(IndexError):  # Test indexing out of range
        obj.pop()

    obj.push(5)
    assert obj.pop() == 5, "Test for pop failed"

    for x in test_data:
        obj.push(x)

    assert len(obj) == len(test_data), "Test for __len__ failed"
    assert str(obj) == '[12, 6, 8, 2, 1, -9, 1, 0]', "Test for __str__ failed"
    assert obj.top() == max(test_data), "Test for top failed"

    test_data.sort()
    while test_data:
        assert test_data.pop() == obj.pop(), "Test for pop failed"


def test_Trie():
    """
    Runs basic tests for the Trie data structure, tests methods and functionality.
    """
    words = "this is a collection of some test words for us to work with".split()
    obj = Trie(words)
    obj.insert("another")

    assert obj.get_word_count("is") == 1, "Test for get_word_count failed"

    obj.insert("is")
    assert obj.get_word_count("is") == 2, "Test for get_word_count failed"

    obj.get_word_count("unknown")
    assert obj.is_word("is") is True, "Test for is_word failed"

    assert obj.is_word("something") is False, "Test for is_word failed"
    assert len(obj) == 15

    assert obj.get_prefix_word_count("w") == 3, "Test for get_prefix_word_count failed"
    assert obj.is_prefix("wo") is True, "Test for is_prefix failed"
    assert obj.is_prefix("work") is True, "Test for is_prefix failed"
    assert obj.is_prefix("worked") is False, "Test for is_prefix failed"

    obj.remove_word("is")
    assert obj.get_word_count("is") == 1, "Test for get_word_count failed"
    obj.remove_word("is")
    assert obj.get_word_count("is") == 0, "Test for get_word_count failed"
    obj.remove_word("is")
    assert obj.get_word_count("is") == 0, "Test for get_word_count failed"
    for i in range(10):
        obj.insert("is")
    obj.remove_word("is", remove_all=True)
    assert obj.get_word_count("is") == 0, "Test for get_word_count failed"

    assert obj.first_prefix_word("zoo") is None, "Test for first_prefix_word failed"
    assert obj.first_prefix_word("something") == "some", "Test for first_prefix_word failed"
    obj.insert("something")
    obj.insert("something")
    obj.insert("somewhere")
    obj.insert("someone")
    assert obj.get_words_by_prefix("some") == ['some', 'someone', 'somewhere', 'something']
    assert obj.get_words_by_prefix("some", unique_only=False) == ['some', 'someone', 'somewhere',
                                                                  'something', 'something']
    assert obj.get_words_by_prefix("zoo") == [], "Test for get_words_by_prefix failed"


def test_DisjointSets():
    """
    Runs basic tests for the DisjointSets data structure, tests methods and functionality.
    """
    obj = DisjointSets(10)

    assert obj.find_root(5) == 5, "Test for find_root failed"

    obj.join_sets(5, 6)
    obj.join_sets(1, 2)
    assert obj.is_connected(1, 2) is True, "Test for is_connected failed"
    assert obj.is_connected(5, 6) is True, "Test for is_connected failed"
    assert obj.is_connected(1, 6) is False, "Test for is_connected failed"

    obj.join_sets(6, 2)
    assert obj.is_connected(1, 6) is True, "Test for is_connected failed"

    assert obj.get_sets() == [[0], [1, 2, 5, 6], [3], [4], [7], [8], [9]], "Test for get_sets failed"

    obj.join_sets(0, 2)
    obj.join_sets(2, 9)
    assert obj.get_sets() == [[0, 1, 2, 5, 6, 9], [3], [4], [7], [8]], "Test for get_sets failed"


def test_LFUCache():
    """
    Runs basic tests for the LFUCache data structure, tests methods and functionality.
    """
    obj = LFUCache(3)
    for i in list(range(20)) + [1, 2, 3]:
        obj.put(i, i * 5)

    assert obj.dict == {1: [5, 1], 2: [10, 1], 3: [15, 1]}, "Test for put failed"

    for j in [1, 1, 2, 2, 3, 1, 1]:
        assert obj.get(j) == j * 5, "Test for get failed"

    obj.put(7, 7 * 5)
    assert obj.dict == {1: [5, 5], 2: [10, 3], 7: [35, 1]}, "Test for put failed"

    obj.put(7, 7 * 4)
    assert obj.get(7) == 7 * 4, "Test for put failed"

    obj[7] = 7 * 3
    assert obj.get(7) == 7 * 3, "Test for obj[key]=val put method failed"

    assert len(obj) == 3, "Test for len(obj) failed"


def test_LRUCache():
    """
    Runs basic tests for the LRUCache data structure, tests methods and functionality.
    """
    obj = LRUCache(3)
    for i in list(range(20)) + [1, 2, 3]:
        obj.put(i, i * 5)

    for j in [1, 1, 2, 2, 3, 1, 1]:
        assert obj.get(j) == j * 5, "Test for get failed"

    obj.put(7, 7 * 5)
    assert set(obj.dict.keys()) == set([1, 3, 7]), "Test for put failed"

    obj.put(1, 1 * 4)
    assert obj.get(1) == 1 * 4, "Test for put failed"

    obj[7] = 7 * 3
    assert obj.get(7) == 7 * 3, "Test for obj[key]=val put method failed"

    assert len(obj) == 3, "Test for len(obj) failed"
