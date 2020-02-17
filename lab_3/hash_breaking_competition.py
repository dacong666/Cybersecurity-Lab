import argparse
import csv
import hashlib
import string
import time
from itertools import product


def part_6(hash_file, csv_file):
    hash_password = {}

    o_file = open(csv_file, 'a')
    writer = csv.writer(o_file)
    with open(hash_file, 'r') as hashes_file:
        hashes = hashes_file.read().splitlines()

    char_in_password = string.printable
    print(char_in_password)
    possible_permutation = (''.join(x) for i in range(1, 20) for x in product(char_in_password, repeat=i))

    # possible_permutation = [''.join(p) if hashlib.md5(''.join(p).encode('utf-8')).hexdigest() in hashes else print(''.join(p)) for i in range(4, 5) for p in product(char_in_password, repeat=i)]
    print(possible_permutation)

    start_time = time.time()
    for permutation in possible_permutation:
        if hashlib.md5(permutation.encode('utf-8')).hexdigest() in hashes:
            hash_password[hashlib.md5(permutation.encode('utf-8')).hexdigest()] = permutation
            writer.writerow([hashlib.md5(permutation.encode('utf-8')).hexdigest(), permutation])
    end_time = time.time()
    #
    time_period = end_time-start_time

    print(hash_password)
    print(time_period)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein', help='input file')
    parser.add_argument('-o', dest='fileout_csv', help='output file')

    args = parser.parse_args()
    filein = args.filein
    fileout_csv = args.fileout_csv

    part_6(filein, fileout_csv)


