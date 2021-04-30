from unittest import TestCase
import random

class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right

        def rotate_left(self):
            ### BEGIN SOLUTION
            n = self.right
            self.val, n.val = n.val, self.val
            self.right, n.right, self.left, n.left = n.right, n.left, n, self.left
            ### END SOLUTION

        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None

    @staticmethod
    def rebalance(t):
        ### BEGIN SOLUTION
        balancefactor = height(t.right) - height(t.left)
        if balancefactor < -1:
            if height(t.left.left) > height(t.left.right):
                newNode = t.left
                t.rotate_right()
                AVLTree.rebalance(newNode)
            else:
                newNode = t.left.right  
                t.left.rotate_left()
                t.rotate_right()
                AVLTree.rebalance(newNode)
            return
        if balancefactor > 1:
            if height(t.right.right) > height(t.right.left):
                newNode = t.right
                t.rotate_left()
                AVLTree.rebalance(newNode)
            else:
                newNode = t.right.left
                t.right.rotate_right()          
                t.rotate_left()
                AVLTree.rebalance(newNode)
            return
        ### END SOLUTION

    def add(self, val):
        assert(val not in self)
        ### BEGIN SOLUTION
        if self.root is None:
            self.root = self.Node(val, None, None)
            return

        path = []
        curNode = self.root
        while True:
            path.append(curNode)
            if val < curNode.val:
                if curNode.left:
                    curNode = curNode.left
                else:
                    curNode.left = self.Node(val, None, None)
                    break
            else:
                if curNode.right:
                    curNode = curNode.right
                else:
                    curNode.right = self.Node(val, None, None)
                    break

        for x in reversed(path):
            if abs(height(x.left) - height(x.right)) > 1:
                self.rebalance(x)
                break
            
        ### END SOLUTION

    def __delitem__(self, val):
        assert(val in self)
        ### BEGIN SOLUTION
        path = []
        parentNode = self.root
        delNode = None

        if val == self.root.val:
            if self.root.left is None and self.root.right is None:
                self.root = None
                return
            elif self.root.left and self.root.right is None:
                self.root = self.root.left
            elif self.root.left is None and self.root.right:
                self.root = self.root.right
            elif self.root.left and self.root.right:
                largestparent = self.root.left
                largestchild = largestparent.right
                path.append(largestparent)
                if largestchild:
                    while largestchild.right:
                        largestparent = largestchild
                        largestchild = largestchild.right
                        path.append(largestparent)
                    self.root.val = largestchild.val
                    largestparent.right = largestchild.left
                else:
                    largestchild = largestparent
                    largestchild.right = self.root.right
                    self.root = largestchild

                for x in reversed(path):
                    if abs(height(x.left) - height(x.right)) > 1:
                        self.rebalance(x)

                self.rebalance(self.root)
            return

        while True:
            path.append(parentNode)
            if val < parentNode.val:
                if parentNode.left.val == val:
                    delNode = parentNode.left
                    break
                else:
                    parentNode = parentNode.left
            else:
                if parentNode.right.val == val:
                    delNode = parentNode.right
                    break
                else:
                    parentNode = parentNode.right

        # no children
        if delNode.left is None and delNode.right is None:
            if delNode.val < parentNode.val:
                parentNode.left = None
            else:
                parentNode.right = None
        # one child
        elif delNode.left is None and delNode.right:
            if delNode.val < parentNode.val:
                parentNode.left = delNode.right
            else:
                parentNode.right = delNode.right
        elif delNode.left and delNode.right is None:
            if delNode.val < parentNode.val:
                parentNode.left = delNode.left
            else:
                parentNode.right = delNode.left
        # two children
        elif delNode.left and delNode.right:
            largestparent = delNode.left
            largestchild = largestparent.right
            path.append(largestparent)
            if largestchild:
                while largestchild.right:    
                    largestparent = largestchild
                    largestchild = largestchild.right
                    path.append(largestparent)
                delNode.val = largestchild.val
                largestparent.right = largestchild.left
            else:
                largestparent.right = delNode.right
                if delNode.val < parentNode.val:
                    parentNode.left = delNode.left
                else:
                    parentNode.right = delNode.left
                
        if val < parentNode.val:
            if parentNode.left:
                path.append(parentNode.left)
        elif parentNode.right:
            path.append(parentNode.right)

        for x in reversed(path):
            if abs(height(x.left) - height(x.right)) > 1:
                self.rebalance(x)
        ### END SOLUTION

    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)

################################################################################
# TEST CASES
################################################################################
def height(t):
    if not t:
        return 0
    else:
        return max(1+height(t.left), 1+height(t.right))

def traverse(t, fn):
    if t:
        fn(t)
        traverse(t.left, fn)
        traverse(t.right, fn)

# LL-fix (simple) test
# 10 points
def test_ll_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 2, 1]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RR-fix (simple) test
# 10 points
def test_rr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 2, 3]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# LR-fix (simple) test
# 10 points
def test_lr_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [3, 1, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# RL-fix (simple) test
# 10 points
def test_rl_fix_simple():
    tc = TestCase()
    t = AVLTree()

    for x in [1, 3, 2]:
        t.add(x)

    tc.assertEqual(height(t.root), 2)
    tc.assertEqual([t.root.left.val, t.root.val, t.root.right.val], [1, 2, 3])

# ensure key order is maintained after insertions and removals
# 30 points
def test_key_order_after_ops():
    tc = TestCase()
    vals = list(range(0, 100000000, 333333))
    random.shuffle(vals)

    t = AVLTree()
    for x in vals:
        t.add(x)

    for _ in range(len(vals) // 3):
        to_rem = vals.pop(random.randrange(len(vals)))
        del t[to_rem]

    vals.sort()

    for i,val in enumerate(t):
        tc.assertEqual(val, vals[i])

# stress testing
# 30 points
def test_stress_testing():
    tc = TestCase()

    def check_balance(t):
        tc.assertLess(abs(height(t.left) - height(t.right)), 2, 'Tree is out of balance')

    t = AVLTree()
    vals = list(range(1000))
    random.shuffle(vals)
    for i in range(len(vals)):
        t.add(vals[i])
        for x in vals[:i+1]:
            tc.assertIn(x, t, 'Element added not in tree')
        traverse(t.root, check_balance)

    random.shuffle(vals)
    for i in range(len(vals)):
        del t[vals[i]]
        for x in vals[i+1:]:
            tc.assertIn(x, t, 'Incorrect element removed from tree')
        for x in vals[:i+1]:
            tc.assertNotIn(x, t, 'Element removed still in tree')
        traverse(t.root, check_balance)



################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "#" + "\n" + f.__name__ + "\n" + 80 * "#" + "\n")

def say_success():
    print("----> SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_ll_fix_simple,
              test_rr_fix_simple,
              test_lr_fix_simple,
              test_rl_fix_simple,
              test_key_order_after_ops,
              test_stress_testing]:
        say_test(t)
        t()
        say_success()
    print(80 * "#" + "\nALL TEST CASES FINISHED SUCCESSFULLY!\n" + 80 * "#")

if __name__ == '__main__':
    main()
