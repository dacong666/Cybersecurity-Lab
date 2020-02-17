######################
# Wang Zijia 1002885
######################
from Crypto.PublicKey import RSA
from base64 import b64encode, b64decode
import random

def square_multiply(a,x,n):
    y = 1
    x_bin = "{0:01b}".format(x)
    n_b = len(x_bin)
    # for i in range(n_b-1, -1, -1):
    for i in range(0, n_b):
        y = (y**2) % n
        if x_bin[i] == '1':
            y = (a*y) % n
    return y

    pass

# function to convert long int to byte string
def pack_bigint(i):
    b=bytearray()
    while i:
        b.append(i&0xFF)
        i>>=8
    return b

# function to convert byte string to long int
def unpack_bigint(b):
    b=bytearray(b)
    return sum((1<<(bi*8))* bb for (bi,bb) in enumerate(b))

if __name__=="__main__":
    pass
