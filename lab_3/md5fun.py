#!/usr/bin/env python3
import argparse
import random
import string
import hashlib
from itertools import permutations, product
import time


def break_hash_brute_force(hash_file, password_file, salted_hash_file):
    hash_password = {}
    with open(hash_file) as f:
        hashes = f.read().splitlines()

    char_in_password = string.ascii_lowercase + string.digits
    # possible_permutation = [''.join(p) for p in permutations(char_in_password, 5)]
    possible_permutation = [''.join(p) for p in product(char_in_password, repeat=5)]

    start_time = time.time()
    for permutation in possible_permutation:
        if hashlib.md5(permutation.encode('utf-8')).hexdigest() in hashes:
            hash_password[hashlib.md5(permutation.encode('utf-8')).hexdigest()] = permutation
    end_time = time.time()

    time_period = end_time-start_time

    print(hash_password)
    print("total time: ", time_period)

    # part 5 ----------------------------------------------------
    password_list = list(hash_password.values())
    pass6 = open(password_file, 'w')
    salted6 = open(salted_hash_file, 'w')
    print(password_list)

    for password in password_list:
        salt_value = random.choice(string.ascii_lowercase)
        password += salt_value

        pass6.write(password+'   ' + salt_value + '\n')
        salted6.write("{}\n".format(hashlib.md5(password.encode('utf-8')).hexdigest()))

    pass6.close()
    salted6.close()
    # -----------------------------------------------------------


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein', help='input file')
    parser.add_argument('-op', dest='fileout_password', help='input file')
    parser.add_argument('-oh', dest='fileout_hash', help='input file')

    args = parser.parse_args()
    filein = args.filein
    fileout_password = args.fileout_password
    fileout_hash = args.fileout_hash

    # hash5 = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_3/hash5.txt"
    # break_hash_brute_force(hash5)
    break_hash_brute_force(filein, fileout_password, fileout_hash)

    # py md5fun.py -i hash5.txt -op pass6.txt -oh salted6.txt
    # ./md5fun.py -i hash5.txt -op pass6.txt -oh salted6.txt
    # rcrack.exe . -l C:\Users\87173\Desktop\term6\CyberSec\lab\lab_3\salted6.txt
