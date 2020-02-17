#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

##################
# Wang Zijia 1002885
##################

import argparse
import operator
from collections import Counter


def getInfo(headerfile):
    header = open(headerfile).read().split()
    return header[0], header[1], header[2], header[3]
    pass


def extract(infile, outfile, headerfile):
    dtype, comment, height, width = getInfo(headerfile)
    print("dtype: ", dtype, "comment: ", comment, "height: ", height, "width: ", width)
    input_data = open(infile, "rb").read()
    # read file looping bytes
    # data =[]
    # with open(infile, "rb") as f:
    #     byte = f.read(8)
    #     while byte:
    #         # Do stuff with byte.
    #         byte = f.read(8)
    #         data.append(byte)
    # print(data)
    data = list((input_data[0 + i:8 + i] for i in range(0, len(input_data), 8)))  # split them into fix length with 8 bytes => one block

    frequency = dict(Counter(data))
    sorted_freq = dict(sorted(frequency.items(), key=operator.itemgetter(1), reverse=True))
    print(sorted_freq)
    max_freq_rgb = list(sorted_freq.keys())[0]
    print(max_freq_rgb)
    data = ['11111111' if i == max_freq_rgb else '00000000' for i in data]
    # print(sorted_freq)
    # print(data)
    output_data = "".join(data for data in data)
    # print("output data: ", output_data)
    output_img = open(outfile, 'w')
    output_img.write('{}\n{}\n{} {}\n'.format(dtype, comment, height, width) + output_data)
    print("Decryption done !!!")
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile', help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile', help='output PBM file')
    parser.add_argument('-hh', dest='headerfile', help='known header file')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    headerfile = args.headerfile

    print('Reading from: %s' % infile)
    print('Reading header file from: %s' % headerfile)
    print('Writing to: %s' % outfile)

    success = extract(infile, outfile, headerfile)




