import urllib.request
import unittest
import sys
from typing import TypeVar, Callable, List

T = TypeVar('T')
S = TypeVar('S')

#################################################################################
# EXERCISE 1
#################################################################################
def partition(lst, low, high, compare):
    i = low - 1
    pivot = lst[high]

    for x in range(low, high):
        if compare(lst[x], pivot) == -1:
            i = i + 1
            lst[i],lst[x] = lst[x],lst[i]
    
    lst[i + 1],lst[high] = lst[high],lst[i + 1]
    return (i + 1)

def quickSortIterative(lst, low, high, compare):
    size = high - low + 1
    stack = [0] * size

    top = -1

    top = top + 1
    stack[top] = low
    top = top + 1
    stack[top] = high

    while top >= 0:
        high = stack[top]
        top = top - 1
        low = stack[top]
        top = top - 1

        p = partition(lst, low, high, compare)

        if p - 1 > low:
            top = top + 1
            stack[top] = low
            top = top + 1
            stack[top] = p - 1

        if p + 1 < high:
            top = top + 1
            stack[top] = p + 1
            top = top + 1
            stack[top] = high

def mysort(lst: List[T], compare: Callable[[T, T], int]) -> List[T]:
    """
    This method should sort input list lst of elements of some type T.

    Elements of the list are compared using function compare that takes two
    elements of type T as input and returns -1 if the left is smaller than the
    right element, 1 if the left is larger than the right, and 0 if the two
    elements are equal.
    """
    quickSortIterative(lst, 0, len(lst) - 1, compare)

    return lst

def mybinsearch(lst: List[T], elem: S, compare: Callable[[T, S], int]) -> int:
    """
    This method search for elem in lst using binary search.

    The elements of lst are compared using function compare. Returns the
    position of the first (leftmost) match for elem in lst. If elem does not
    exist in lst, then return -1.
    """

    #basecase
    if len(lst) > 1:
        midpoint = 1 + (len(lst) - 1) // 2

        #if mid
        if compare(lst[midpoint], elem) == 0:
            return midpoint

        #if bigger than mid
        elif compare(lst[midpoint], elem) == -1:
            result = mybinsearch(lst[midpoint:], elem, compare) 
            if result != -1:
                return result + midpoint
            else:
                return -1

        #if bigger than mid
        else:
            result = mybinsearch(lst[:midpoint], elem, compare) 
            if result != -1:
                return result
            else:
                return -1

    #not in list
    else:
        return -1

class Student():
    """Custom class to test generic sorting and searching."""
    def __init__(self, name: str, gpa: float):
        self.name = name
        self.gpa = gpa

    def __eq__(self, other):
        return self.name == other.name

# 30 Points (total)
def test1():
    """Tests for generic sorting and binary search."""
    print(80 * "#" + "\nTests for generic sorting and binary search.")
    test1_1()
    test1_2()
    test1_3()
    test1_4()
    test1_5()

# 6 Points
def test1_1():
    """Sort ints."""
    print("\t-sort ints")
    tc = unittest.TestCase()
    ints = [ 4, 3, 7, 10, 9, 2 ]
    intcmp = lambda x,y:  0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(sortedints, [2, 3, 4, 7, 9, 10])

# 6 Points
def test1_2():
    """Sort strings based on their last character."""
    print("\t-sort strings on their last character")
    tc = unittest.TestCase()
    strs = [ 'abcd', 'aacz',  'zasa' ]
    suffixcmp = lambda x,y: 0 if x[-1] == y[-1] else (-1 if x[-1] < y[-1] else 1)
    sortedstrs = mysort(strs,suffixcmp)
    tc.assertEqual(sortedstrs, [ 'zasa', 'abcd', 'aacz' ])

# 6 Points
def test1_3():
    """Sort students based on their GPA."""
    print("\t-sort students on their GPA.")
    tc = unittest.TestCase()
    students = [ Student('Josh', 3.0), Student('Angela', 2.5), Student('Vinesh', 3.8),  Student('Jia',  3.5) ]
    sortedstudents = mysort(students, lambda x,y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1))
    expected = [ Student('Angela', 2.5), Student('Josh', 3.0), Student('Jia',  3.5), Student('Vinesh', 3.8) ]
    tc.assertEqual(sortedstudents, expected)

# 6 Points
def test1_4():
    """Binary search for ints."""
    print("\t-binsearch ints")
    tc = unittest.TestCase()
    ints = [ 4, 3, 7, 10, 9, 2 ]
    intcmp = lambda x,y:  0 if x == y else (-1 if x < y else 1)
    sortedints = mysort(ints, intcmp)
    tc.assertEqual(mybinsearch(sortedints, 3, intcmp), 1)
    tc.assertEqual(mybinsearch(sortedints, 10, intcmp), 5)
    tc.assertEqual(mybinsearch(sortedints, 11, intcmp), -1)

# 6 Points
def test1_5():
    """Binary search for students by gpa."""
    print("\t-binsearch students")
    tc = unittest.TestCase()
    students = [ Student('Josh', 3.0), Student('Angela', 2.5), Student('Vinesh', 3.8),  Student('Jia',  3.5) ]
    stcmp = lambda x,y: 0 if x.gpa == y.gpa else (-1 if x.gpa < y.gpa else 1)
    stbincmp = lambda x,y: 0 if x.gpa == y else (-1 if x.gpa < y else 1)
    sortedstudents = mysort(students, stcmp)
    tc.assertEqual(mybinsearch(sortedstudents, 3.5, stbincmp), 2)
    tc.assertEqual(mybinsearch(sortedstudents, 3.7, stbincmp), -1)

#################################################################################
# EXERCISE 2
#################################################################################
class PrefixSearcher():
    length = 0
    document = ""
    prefixes = []

    def __init__(self, document, k):
        """
        Initializes a prefix searcher using a document and a maximum
        search string length k.
        """
        self.document = document
        self.length = k
        self.prefixes = []
        
        for i in range(1, self.length + 1):
            for x in range(len(self.document)):
                if x + i < len(self.document):
                    self.prefixes.append(self.document[x:x + i])
                else:
                    self.prefixes.append(self.document[x:])

        def strcmp(x, y):
            if(len(x) > len(y)):
                return 1
            elif(len(x) < len(y)):
                return -1
            else:
                if(x > y):
                    return 1
                elif(x < y):
                    return -1
                else:
                    return 0

        document = mysort(self.prefixes, strcmp)
        #print(self.document, ":", self.length, ":", self.prefixes)
                

    def search(self, q):
        """
        Return true if the document contains search string q (of
        length up to n). If q is longer than n, then raise an
        Exception.
        """

        if len(q) > self.length:
            raise Exception("Inputted string length is above the maximum length")
        else:       
            def strcmp(x, y):
                if(len(x) > len(y)):
                    return 1
                elif(len(x) < len(y)):
                    return -1
                else:
                    if(x > y):
                        return 1
                    elif(x < y):
                        return -1
                    else:
                        return 0

            return mybinsearch(self.prefixes, q, strcmp) != -1

# 30 Points
def test2():
    print("#" * 80 + "\nSearch for substrings up to length n")
    test2_1()
    test2_2()

# 15Points
def test2_1():
    print("\t-search in hello world")
    tc = unittest.TestCase()
    p = PrefixSearcher("Hello World!", 1)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("e"))
    tc.assertFalse(p.search("h"))
    tc.assertFalse(p.search("Z"))
    tc.assertFalse(p.search("Y"))
    p = PrefixSearcher("Hello World!", 2)
    tc.assertTrue(p.search("l"))
    tc.assertTrue(p.search("ll"))
    tc.assertFalse(p.search("lW"))

# 20 Points
def test2_2():
    print("\t-search in Moby Dick")
    tc = unittest.TestCase()
    md_url = 'https://www.gutenberg.org/files/2701/2701-0.txt'
    md_text = urllib.request.urlopen(md_url).read().decode()
    p = PrefixSearcher(md_text[0:1000],4)
    tc.assertTrue(p.search("Moby"))
    tc.assertTrue(p.search("Dick"))

#################################################################################
# EXERCISE 3
#################################################################################
class SuffixArray():
    document = ""
    sa = []

    def __init__(self, document: str):
        """
        Creates a suffix array for document (a string).
        """
        self.sa  = []
        self.document = document

        for x in range(len(document)):
            self.sa.append(x)
        
        def strcmp(x, y):
            x_suffix = document[x:]
            y_suffix = document[y:]
            if(x_suffix > y_suffix):
                return 1
            elif(x_suffix < y_suffix):
                return -1
            else:
                return 0

        sa = mysort(self.sa, strcmp)

    def positions(self, searchstr: str):
        """
        Returns all the positions of searchstr in the documented indexed by the suffix array.
        """
        results = []

        def strcmp(x, y):
            x_suffix = self.document[x:]

            if(y == x_suffix[:len(y)]):
                return 0
            elif(x_suffix > y):
                return 1
            elif(x_suffix < y):
                return -1

        results.append(mybinsearch(self.sa, searchstr, strcmp))

        return results

    def contains(self, searchstr: str):
        """
        Returns true of searchstr is contained in document.
        """
        def strcmp(x, y):
            x_suffix = self.document[x:]

            if(y == x_suffix[:len(y)]):
                return 0
            elif(x_suffix > y):
                return 1
            elif(x_suffix < y):
                return -1

        return mybinsearch(self.sa, searchstr, strcmp) != -1  


# 40 Points
def test3():
    """Test suffix arrays."""
    print(80 * "#" + "\nTest suffix arrays.")
    test3_1()
    test3_2()


# 20 Points
def test3_1():
    print("\t-suffixarray on Hello World!")
    tc = unittest.TestCase()
    s = SuffixArray("Hello World!")
    tc.assertTrue(s.contains("l"))
    tc.assertTrue(s.contains("e"))
    tc.assertFalse(s.contains("h"))
    tc.assertFalse(s.contains("Z"))
    tc.assertFalse(s.contains("Y"))
    tc.assertTrue(s.contains("ello Wo"))


# 20 Points
def test3_2():
    print("\t-suffixarray on Moby Dick!")
    tc = unittest.TestCase()
    md_url = 'https://www.gutenberg.org/files/2701/2701-0.txt'
    md_text = urllib.request.urlopen(md_url).read().decode()
    s = SuffixArray(md_text[0:1000])
    tc.assertTrue(s.contains("Moby Dick"))
    tc.assertTrue(s.contains("Herman Melville"))
    tc.assertEqual(s.positions("Moby Dick"), [427])


#################################################################################
# TEST CASES
#################################################################################
def main():
    test1()
    test2()
    test3()

if __name__ == '__main__':
    main()
