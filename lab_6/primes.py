#50.042 FCS Lab 6 template
# Year 2019

##################
# Wang Zijia 1002885
##################

import random
def square_multiply(a, x, n):
    y = 1
    x_bin = "{0:01b}".format(x)
    n_b = len(x_bin)
    # for i in range(n_b-1, -1, -1):
    for i in range(0, n_b):
        y = (y**2) % n
        if x_bin[i] == '1':
            y = (a*y) % n
    return y


def miller_rabin(n, k):
    if n % 2 == 0:
        return False
    if n > 3:
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        for i in range(k):
            a = random.randrange(2, n - 1)
            # x_1 = pow(a, d, n)
            x = square_multiply(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for j in range(r - 1):
                # x_1 = pow(x, 2, n)
                x = square_multiply(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True
    else:
        print("number n has to be larger than 3.")
        return False


def gen_prime_nbits(n):
    found_prime = False
    while not found_prime:
        num = random.randint(2 ** (n - 1), 2 ** n)
        if miller_rabin(num, 2):
            return num


if __name__=="__main__":
    print('Is 561 a prime?')
    print(miller_rabin(561, 2))
    print('Is 27 a prime?')
    print(miller_rabin(27, 2))
    print('Is 61 a prime?')
    print(miller_rabin(61, 2))

    print('Random number (100 bits):')
    print(gen_prime_nbits(100))
    print('Random number (80 bits):')
    print(gen_prime_nbits(80))

# ---------------------------------------
#     print('Is 377 a prime?')
#     print(miller_rabin(377, 2))
#     print('Is 5161 a prime?')
#     print(miller_rabin(5161, 2))
#
#     print('Is 89 a prime?')
#     print(miller_rabin(89, 2))
#     print('Is 31 a prime?')
#     print(miller_rabin(31, 2))
#     print('Is 47 a prime?')
#     print(miller_rabin(47, 2))
#     print('Is 53 a prime?')
#     print(miller_rabin(53, 2))
#     print('Is 59 a prime?')
#     print(miller_rabin(59, 2))
#
    # assert square_multiply(8, 3, 11) == pow(8,3,11)
    # assert square_multiply(89, 11, 81) == pow(89,11,81)
    # assert square_multiply(12,13,14) == pow(12,13,14)
    # assert square_multiply(87,23,99) == pow(87,23,99)
