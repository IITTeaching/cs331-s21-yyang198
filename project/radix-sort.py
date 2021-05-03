import urllib.request

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    text = urllib.request.urlopen(book_url).read().decode()[1:]
    lst = padding(text.split())
    return radix_sort(lst)

# add extra spaces to the ends of words based on the longest word
def padding(lst):
    max_len = -1
    for x in range(len(lst)):
        if len(lst[x]) > max_len:
            max_len = len(lst[x])

        lst[x] = ''.join(c for c in lst[x] if ord(c) < 128)

    for x in range(len(lst)):
        while len(lst[x]) < max_len:
            lst[x] += " "

    return lst

# class for storing the original value as well as digits for radix sort
class Value:
    def __init__(self, val, digits):
        self.val = val
        self.digits = digits

        if isinstance(self.val, str):
            self.val = self.val.strip()

    def __str__(self):
        return str(self.val) + ": " + ' '.join(str(e).lower() for e in self.digits)

    def __repr__(self):
        return self.__str__()

def radix_sort(lst=[None]):

    # seperate the values into digits for sorting (because it uses ascii keys for sorting, negative numbers will not work without applying an offset to the entire list)
    max_digits = len(str(max(lst)))
    parsed_list = []
    for x in lst:
        seperated_digits = [ord(e) for e in str(x).lower()]

        # add padding in front for numbers (if we were sorting strings every value should already have the same length through 'padding()')
        while len(seperated_digits) < max_digits:
            seperated_digits.insert(0, ord('0'))

        parsed_list.append(Value(x, seperated_digits))
    lst = parsed_list

    # go digit by digit starting at the least significant value
    for x in range(max_digits, 0, -1):
        # insert into hashtable (128 buckets because https://python-reference.readthedocs.io/en/latest/docs/str/ASCII.html)
        hashtable = [None] * 128
        for value in lst:
            digit = value.digits[x - 1]
            if hashtable[digit]:
                hashtable[digit].append(value)
            else:
                hashtable[digit] = [value]

        # form hashtable into new array
        lst = []
        for bucket in hashtable:
            if bucket:
                for value in bucket:
                    lst.append(value)

    return [x.val for x in lst]


#########
#TESTING#
#########
def test_numbers(lst):
    return radix_sort(lst)

def test_words(lst):
    lst = padding(lst)
    return radix_sort(lst)
'''
lst = [170, 45, 75, 90, 802, 24, 2, 66, 80, 48, 208]
print(lst)
print(test_numbers(lst))c
print()

import random
lst = [random.randint(0, 1000) for x in range(25)]
print(lst)
print(test_numbers(lst))

lst = "Lorem ipsum dolor sit— amet,.".split()
print(lst)
print(test_words(lst))
'''

sorted_book = radix_a_book()
for word in sorted_book:
    print(word)
