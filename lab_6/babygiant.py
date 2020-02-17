#50.042 FCS Lab 6 template
#Year 2019

##################
# Wang Zijia 1002885
##################

import math
import primes


def baby_step(alpha, beta, p, fname):
    m = math.ceil(math.sqrt(p))
    with open(fname, 'w') as baby_file:
        for x_b in range(m):
            baby_file.write(str((alpha**x_b*beta) % p) + ',' + str(x_b) + '\n')

    baby_list = [line.strip().split(',') for line in open(fname, 'r').readlines()]

    return baby_list


def giant_step(alpha, p, fname):
    m = math.ceil(math.sqrt(p))
    with open(fname, 'w') as giant_file:
        for x_g in range(m):
            # giant_file.write(str((alpha**(m*x_g)) % p)+'\n')
            giant_file.write(str(primes.square_multiply(alpha, m*x_g, p)) + ',' + str(x_g) + '\n')

    giant_list = [line.strip().split(',') for line in open(fname, 'r').readlines()]

    return giant_list


def baby_giant(alpha, beta, p):
    m = math.ceil(math.sqrt(p))

    baby_file = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_6/baby_step_file.txt"
    giant_file = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_6/giant_step_file.txt"
    baby_list = baby_step(alpha, beta, p, baby_file)
    giant_list = giant_step(alpha, p, giant_file)
    # result = []
    for x_b in baby_list:
        for x_g in giant_list:
            if x_b[0] == x_g[0]:
                x = int(x_g[1])*m - int(x_b[1])
                # result.append(int(x_g[1])*m - int(x_b[1]))
    # print(result)
    return x


if __name__ == "__main__":
    """
    test 1
    My private key is:  264
    Test other private key is:  7265
    """
    p = 17851  # known to attacker
    alpha = 17511  # known to attacker
    A = 2945  # known to attacker, shared public key
    B = 11844  # known to attacker, shared public key
    sharedkey = 1671  # real shared key
    a = baby_giant(alpha, A, p)  # attack 猜的private key
    b = baby_giant(alpha, B, p)  # attack 猜的private key
    guesskey1 = primes.square_multiply(A, b, p)
    guesskey2 = primes.square_multiply(B, a, p)
    print('Guess key 1:', guesskey1)
    print('Guess key 2:', guesskey2)
    print('Actual shared key :', sharedkey)

    # print("------------ 16 bit shared key ----------------")
    # """
    # test 2
    # 16 bit
    # Generate 16-bit shared keys using the DHKE protocol and
    # calculate the shared key based on the known p, alpha, and public keys.
    # My private key is:  6949
    # Test other private key is:  29088
    # """
    # p = 44269
    # alpha = 38219
    # A = 22065
    # B = 39294
    # sharedkey = 37775
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 20 bit shared key ----------------")
    # """
    # test 3
    # 20 bit
    # Increase the number of bits to break slowly.
    # My private key is:  112861
    # Test other private key is:  174141
    # """
    # p = 607931
    # alpha = 607606
    # A = 604645
    # B = 382386
    # sharedkey = 606440
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 22 bit shared key ----------------")
    # """
    # test 4
    # 22 bit
    # Increase the number of bits to break slowly.
    # My private key is:  1981385
    # Test other private key is:  390158
    # """
    # p = 2897491
    # alpha = 517938
    # A = 111949
    # B = 2337571
    # sharedkey = 2368502
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 25 bit shared key ----------------")
    # """
    # test 5
    # 25 bit
    # Increase the number of bits to break slowly.
    # My private key is:  11364600
    # Test other private key is:  4901346
    # """
    # p = 26779043
    # alpha = 17734426
    # A = 25933339
    # B = 16079414
    # sharedkey = 22463770
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 26 bit shared key ----------------")
    # """
    # test 6
    # 26 bit
    # Increase the number of bits to break slowly.
    # My private key is:  54100700
    # Test other private key is:  8388164
    # """
    # p = 110868977
    # alpha = 75088189
    # A = 65690974
    # B = 87841942
    # sharedkey = 43173922
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 27 bit shared key ----------------")
    # """
    # test 7
    # 27 bit
    # Increase the number of bits to break slowly.
    # My private key is:  90627283
    # Test other private key is:  94855164
    # """
    # p = 101193283
    # alpha = 11504000
    # A = 29001880
    # B = 86819146
    # sharedkey = 95395979
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 28 bit shared key ----------------")
    # """
    # test 8
    # 28 bit
    # Increase the number of bits to break slowly.
    # My private key is:  94926249
    # Test other private key is:  126925542
    # """
    # p = 239964047
    # alpha = 206982294
    # A = 170764433
    # B = 197623801
    # sharedkey = 191241416
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 29 bit shared key ----------------")
    # """
    # test 9
    # 29 bit
    # Increase the number of bits to break slowly.
    # My private key is:  186273391
    # Test other private key is:  499781853
    # """
    # p = 501499819
    # alpha = 87517001
    # A = 482617195
    # B = 30696475
    # sharedkey = 494105317
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    # print("------------ 30 bit shared key ----------------")
    # """
    # test 10
    # 30 bit
    # Increase the number of bits to break slowly.
    # My private key is:  17288237
    # Test other private key is:  783777913
    # """
    # p = 980751853
    # alpha = 923069052
    # A = 236759625
    # B = 665118501
    # sharedkey = 932215468
    # a = baby_giant(alpha, A, p)
    # b = baby_giant(alpha, B, p)
    # guesskey1 = primes.square_multiply(A, b, p)
    # guesskey2 = primes.square_multiply(B, a, p)
    # print('Guess key 1:', guesskey1)
    # print('Guess key 2:', guesskey2)
    # print('Actual shared key :', sharedkey)
    #
    #
    #
    #
