import string
from itertools import product

possible_permutation = [''.join(x) for x in product('abc', repeat=2)]
LIST = [1,2,3, None, None]
print(LIST.remove(None))

char_in_password = string.printable
print(char_in_password)