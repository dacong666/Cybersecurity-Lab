#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# Import libraries
import sys
import argparse


def doStuff(filein, fileout, key, mode):
    # open file handles to both files
    fin = open(filein, mode='r', encoding='utf-8', newline='\n')       # read mode
    fin_b = open(filein, mode='rb')  # binary read mode
    fout = open(fileout, mode='w', encoding='utf-8', newline='\n')      # write mode
    fout_b = open(fileout, mode='wb')  # binary write mode
    c = fin.read()         # read in file into c as a str
    # and write to fileout
    # --------------------------------------------------------------------
    if mode == 'e' or mode == 'E':
        mode = "encrypt"
    elif mode == 'd' or mode == 'D':
        mode = 'decrypt'
    else:
        print("Mode is no valid.")
    if 1 <= key <= (len(c) - 1):
        print("checking mode: {}".format(mode))
        if mode == 'encrypt':
            print("doing encryption ...")
            for char in c:
                index = ord(char)
                new_char = chr(index + key)
                fout.write(new_char)
        elif mode == 'decrypt':
            for char in c:
                index = ord(char)
                new_char = chr(index - key)
                fout.write(new_char)
    else:
        print("Key length is not valid.")




    # --------------------------------------------------------------------
    # close all file streams
    fin.close()
    fin_b.close()
    fout.close()
    fout_b.close()

    # # PROTIP: pythonic way
    # with open(filein, mode="r", encoding='utf-8', newline='\n') as fin:
    #     text = fin.read()
    #
    #     # do stuff
    #
    #     # file will be closed automatically when interpreter reaches end of the block


# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='filein', help='input file')
    parser.add_argument('-o', dest='fileout', help='output file')

    # parse our arguments
    args = parser.parse_args()
    filein = args.filein
    fileout = args.fileout

    # doStuff(filein, fileout)
    # doStuff('C:/Users/87173/Desktop/term6/cybersecurity/lab_1/sherlock.txt',
    #         'C:/Users/87173/Desktop/term6/cybersecurity/lab_1/sherlock_encrypted.txt', key=3, mode='e')

    doStuff('C:/Users/87173/Desktop/term6/cybersecurity/lab_1/sherlock_encrypted.txt',
            'C:/Users/87173/Desktop/term6/cybersecurity/lab_1/sherlock_decrypted.txt', key=3, mode='d')
    # all done


