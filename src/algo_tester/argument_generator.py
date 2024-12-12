import random
import string
from collections import deque

class TreeNode:
    """A basic Binary Tree node class for demonstration."""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class ListNode:
    """A basic Singly Linked List node class for demonstration."""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class ArgumentGenerator:
    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

    def generate_int_list(self, n=10, min_val=0, max_val=100, unique=False):
        """
        Generates a random list of integers.
        
        Parameters:
        - n: Length of the list
        - min_val: Minimum value for elements
        - max_val: Maximum value for elements
        - unique: If True, generated integers are unique. If n > (max_val-min_val+1), this may fail.
        
        Returns:
        - A tuple containing one list (suitable as a single argument).
        """
        if unique:
            pool = range(min_val, max_val+1)
            arr = random.sample(pool, k=min(n, len(pool)))
        else:
            arr = [random.randint(min_val, max_val) for _ in range(n)]
        return (arr,)

    def generate_string(self, n=10, chars='lower'):
        """
        Generates a random string.
        
        Parameters:
        - n: Length of the string
        - chars: 'lower', 'upper', 'mixed'
        
        Returns:
        - A tuple containing one string.
        """
        if chars == 'lower':
            alphabet = string.ascii_lowercase
        elif chars == 'upper':
            alphabet = string.ascii_uppercase
        else:
            alphabet = string.ascii_letters
        s = ''.join(random.choice(alphabet) for _ in range(n))
        return (s,)

    def generate_matrix(self, rows=3, cols=3, min_val=0, max_val=100):
        """
        Generates a rows x cols matrix of integers.
        
        Returns:
        - A tuple containing one matrix (list of lists).
        """
        matrix = [[random.randint(min_val, max_val) for _ in range(cols)] for _ in range(rows)]
        return (matrix,)

    def generate_binary_tree(self, n=7, min_val=0, max_val=100):
        """
        Generates a binary tree with n nodes using random values.
        The tree is constructed by level order insertion.
        
        Returns:
        - A tuple with the root TreeNode.
        """
        if n == 0:
            return (None,)
        values = [random.randint(min_val, max_val) for _ in range(n)]
        root = TreeNode(values[0])
        queue = deque([root])
        i = 1
        while i < n:
            current = queue.popleft()
            if i < n:
                current.left = TreeNode(values[i])
                i += 1
                queue.append(current.left)
            if i < n:
                current.right = TreeNode(values[i])
                i += 1
                queue.append(current.right)
        return (root,)

    def generate_linked_list(self, n=5, min_val=0, max_val=100):
        """
        Generates a singly linked list with n nodes.
        
        Returns:
        - A tuple with the head ListNode.
        """
        if n == 0:
            return (None,)
        head = ListNode(random.randint(min_val, max_val))
        current = head
        for _ in range(n-1):
            current.next = ListNode(random.randint(min_val, max_val))
            current = current.next
        return (head,)

    def generate_graph(self, n=5, edge_probability=0.2, directed=False):
        """
        Generates a graph represented as an adjacency list.
        
        Parameters:
        - n: number of nodes (labeled 0 to n-1)
        - edge_probability: probability that any two nodes have an edge
        - directed: If False, edges are undirected

        Returns:
        - A tuple with a dictionary representing adjacency list: {node: [neighbors]}
        """
        graph = {i: [] for i in range(n)}
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if random.random() < edge_probability:
                    graph[i].append(j)
                    if not directed:
                        graph[j].append(i)
        # If undirected and we added edges both ways each time, we might have duplicates.
        # Let's remove duplicates in that case:
        if not directed:
            for k in graph:
                graph[k] = list(set(graph[k]))
        return (graph,)
