class Node:
    def __init__(self, val):
        self.l_child = None
        self.r_child = None
        self.data = val


def insert(root, node):
    if root:
        if root.data < node.data:
            if root.r_child:
                insert(root.r_child, node)
            else:
                root.r_child = node
        else:
            if root.l_child:
                insert(root.l_child, node)
            else:
                root.l_child = node


def inOrder(root):
    if root:
        inOrder(root.l_child)
        print(root.data)
        inOrder(root.r_child)