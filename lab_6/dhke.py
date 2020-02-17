#!/usr/bin/env python3

#50.042 FCS Lab 6 template
#Year 2019

##################
# Wang Zijia 1002885
##################

import argparse

import primes 
import random
import ecb


def dhke_setup(nb):
    p = primes.gen_prime_nbits(nb)
    alpha = random.randint(2, p-2)
    return p, alpha


def gen_priv_key(p):
    private_key = random.randint(2, p-2)
    return private_key


def get_pub_key(alpha, a, p):
    public_key = primes.square_multiply(alpha, a, p)
    return public_key


def get_shared_key(keypub, keypriv, p):
    shared_key = primes.square_multiply(keypub, keypriv, p)
    return shared_key

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile', help='input file')
    parser.add_argument('-o', dest='outfile', help='output file')
    parser.add_argument('-k', dest='keyfile', help='key file')
    parser.add_argument('-m', dest='mode', help='mode')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    keyfile = args.keyfile
    mode = args.mode

    if mode in ['e', 'E', 'encryption', 'Encryption', 'encrypt', 'Encrypt']:
        p, alpha = dhke_setup(80)
        print('Generate P and alpha:')
        print('P:', p)
        print('alpha:', alpha)
        a = gen_priv_key(p)
        b = gen_priv_key(p)
        print('My private key is: ', a)
        print('Test other private key is: ', b)

        A = get_pub_key(alpha, a, p)
        B = get_pub_key(alpha, b, p)
        print('My public key is: ', A)
        print('Test other public key is: ', B)

        sharedKeyA = get_shared_key(B, a, p)
        sharedKeyB = get_shared_key(A, b, p)
        print('My shared key is: ', sharedKeyA)
        print('Test other shared key is: ', sharedKeyB)
        print('Length of key is %d bits.' % sharedKeyA.bit_length())

        print("--------------------------- doing encryption below -----------------------------------------")

        with open(keyfile, 'w') as key_file:
            key_file.write(str(sharedKeyA))

        ecb.ecb(infile, outfile, keyfile, mode)

    elif mode in ['d', 'D', 'decryption', 'Decryption', 'decrypt', 'Decrypt']:
        print("--------------------------- doing decryption below -----------------------------------------")

        ecb.ecb(infile, outfile, keyfile, mode)

# ./dhke.py -i Tux.ppm -o Tux_encrypted.ppm  -k key_file.txt -m e
# ./dhke.py -i Tux_encrypted.ppm -o Tux_decrypted.ppm  -k key_file.txt -m d

