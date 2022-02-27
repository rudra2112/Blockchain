import hashlib
import json
import math

class Node(object):

    """Creates a new Node object for Merkle Tree"""

    def __init__(self, hash: str, key: str):
        self.key = key
        self.hash = hash
        self.left = None
        self.right = None

    @staticmethod
    def hashFunction(string: str, key: str) -> object:

        """Hash function

        Accepts a string and an identifiable key in form of a string
        
        Returns a Node object with SHA256 hash of the string"""

        to_hash = string.encode()
        hash = hashlib.sha256(to_hash).hexdigest()
        return Node(hash=hash, key=key)

    @staticmethod
    def buildTree(nodes: list) -> object:

        """Builds Merkle Tree

        It takes a list of Leaf objects and return a single Node object containing the Merkle Root"""

        if len(nodes) == 1:
            return nodes[0]

        ancestors = []
        i=0
        while i < len(nodes):
            node = Node.hashFunction(string=(nodes[i].hash+nodes[i+1].hash), key=(nodes[i].key+nodes[i+1].key))
            node.left = nodes[i]
            node.right = nodes[i+1]
            i += 2

            ancestors.append(node)

        return Node.buildTree(ancestors)

class Leaf(object):

    """Creates a new Leaf object for Merkle Tree"""

    def __init__(self, transaction: dict, hash: str, key: str):
        self.key = key
        self.hash = hash
        self.transaction = transaction 

    @staticmethod
    def makeLeaves(transactions: list) -> list:

        """Hashes the list of transactions passed and create Leaf nodes for Merkle Tree.

        It returns a list of Leaf nodes created from the passed list of transactions"""

        leaves = []

        i = 1
        for x in transactions:
            hashed_trans = hashlib.sha256(json.dumps(x).encode()).hexdigest()
            node = Leaf(transaction=x, hash=hashed_trans, key=str(i))
            leaves.append(node)
            i += 1

        return leaves


    @staticmethod
    def is_power_of_2(number_of_leaves: int) -> bool:
        return math.log2(number_of_leaves).is_integer()

    @staticmethod
    def compute_tree_depth(number_of_leaves: int) -> int:
        return math.ceil(math.log2(number_of_leaves))


    @staticmethod
    def fill_set(leaves: list) -> list:

        """Append the list of leaf nodes until they become equal to 2^n
        
        Takes the list of leaf nodes and returns the list with length equal to 2^n"""

        current_number_of_leaves = len(leaves)

        if Leaf.is_power_of_2(current_number_of_leaves):
            return leaves

        total_number_of_leaves = 2**Leaf.compute_tree_depth(current_number_of_leaves)

        if current_number_of_leaves % 2 == 0:
            for i in range(current_number_of_leaves, total_number_of_leaves, 2):
                leaves = leaves + [leaves[-2], leaves[-1]]
        else:
            for i in range(current_number_of_leaves, total_number_of_leaves):
                leaves.append(leaves[-1])

        return leaves

        
def merkleTree(transactions: list) -> Node:

    """Builds The Merkle Tree and returns the Merkle Root
    
    It takes a list of transactions and returns a single Node object"""

    if(len(transactions)==0):
        return Node("No Transactions", -1)

    leaves = Leaf.makeLeaves(transactions)
    full_set_of_leaves = Leaf.fill_set(leaves)
    root = Node.buildTree(full_set_of_leaves)

    return root

# transaction = [{
#     "sender": "anjne",
#     "receiver": "aknkconeoi",
#     "amount": 8
# },
# {
#     "sender": "anjne",
#     "receiver": "aknkconeoi",
#     "amount": 8
# }]

# root = merkleTree(transaction)
# print(root.hash)
