#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

##################
# Wang Zijia 1002885
##################

import array
from io import BytesIO
from present import *
import argparse
from PIL import Image, ImageFile

# from scipy.misc import imread


nokeybits=80
blocksize=64


def ecb(infile, outfile, key, mode):
    with open(key) as keyfile:
        key = int(keyfile.read())
    if mode in ['e', 'E', 'encryption', 'Encryption', 'encrypt', 'Encrypt']:
        with open(infile, 'r') as input_file:
            values = input_file.read()[25:].split()
        print(len(values))

        tux = ['{0:08b}'.format(int(value)) for value in values]  # change each rgb value into 8 bits
        tux.append('{0:08b}'.format(255))
        tux.append('{0:08b}'.format(255))

        tux = ''.join(value for value in tux)  # concatenate them tgt
        print(len(tux))
        tux_chunk = list(int(tux[0+i:64+i], 2) for i in range(0, len(tux), 64))  # split them into fix length with 64 bit
                                                                                 # and convert into int as the input for PRESENT
        print("input list: ", len(tux_chunk))
        # print("encoding: ", encoding, "height: ", height, "width: ", width, "value: ", values[:50])
        encrypted_result = ''
        encrypted_result = []
        for i in range(0, int(len(tux) / 64)):
            new_value = present(int(tux[i * 64:(i + 1) * 64], 2), key)
            encrypted_result.append(str(new_value).zfill(20))
        print(len(encrypted_result))
        encrypted_result_str = ''.join(encrypted_result)
        print(len(encrypted_result_str))
        print("Encryption done !!!")
        # for chunk in tux_chunk:
        #     encrypted_result.append(str(present(chunk, key)))
        #     # encrypted_result += '{0:064b}'.format(present(chunk, key))
        #     # encrypted_result += str(present(chunk, key))
        # print(len(encrypted_result))
        # encrypted_result_str = ''.join(encrypted_result)
        # print(len(encrypted_result_str))

        # encrypted_result_chunk = list(int(encrypted_result[0 + i:8 + i], 2) for i in range(0, len(encrypted_result), 8))
        # print(encrypted_result_chunk)
        # ---------------------
        with open(outfile, 'w') as file:
            file.write(encrypted_result_str)
            # file.write((str(a) for a in encrypted_result_chunk))
        # img = Image.frombytes("RGB", (int(height), int(width)), bytes(encrypted_result_chunk))
        # img.save(outfile, encoding="utf8")
        # img.show()
        # ---------------------
        # print("encrypted list chunk: ", (encrypted_result))

    elif mode in ['d', 'D', 'decryption', 'Decryption', 'decrypt', 'Decrypt']:
        decrypted_list = []
        with open(infile, 'r') as input_file:
            # encoding, encoding_1, encoding_2, encoding_3, height, width, *values = input_file.read().split()
            values = input_file.read()
        for i in range(0, int(len(values) / 20)):
            dec = present_inv(int(values[i * 20: (i + 1) * 20]), key)
            batch = bin(int(dec))[2:].zfill(64)  # decrypted string: 64 bits

            for ll in range(0, 8):  # parse into 8 bit numbers
                decrypted_list.append(str(int(batch[ll * 8:(ll + 1) * 8], 2)))

        del decrypted_list[-1]
        del decrypted_list[-1]
        print(len(decrypted_list))
        decrypted_string = ','.join(decrypted_list)

        with open(outfile, 'w') as file:
            file.write('P3\n# Tux img\n265 314\n255\n' + decrypted_string)
        print("Decryption done !!!")

        # encoding = values[0].decode('utf-8')
        # height = int(values[1])
        # width = int(values[2])
        # maxval = int(values[3])
        # values = values[4:]
        # # values_bin = []
        # # values_bin.append(["{0:08b}".format(int(s.hex(), 16)) for s in values])
        # values_bin = ''.join("{0:08b}".format(int(s.hex(), 16)) for s in values)
        # # print(values_bin)
        #
        # # values = [int.from_bytes(s, byteorder='big')"" for s in values]
        # # values = [s for s in values]
        # print("encoding: ", encoding, "height: ", height, "width: ", width, "maxval: ", maxval, "values: ", values[:50])
        # values_bin_chunk = list(int(values_bin[0 + i:64 + i], 2) for i in range(0, len(values_bin), 64))
        #
        # decrypted_result = ''
        # for chunk in values_bin_chunk:
        #     decrypted_result += '{0:064b}'.format(present_inv(chunk, key))
        # decrypted_result_chunk = list(int(decrypted_result[0 + i:8 + i], 2) for i in range(0, len(decrypted_result), 8))
        # print(len(decrypted_result_chunk))
        #
        # img = Image.frombytes("RGB", (int(height), 280), bytes(decrypted_result_chunk))
        # img.save(outfile, encoding="utf8")
        # img.show()

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

    # infile = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/Tux.ppm"
    # encrypted_file = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/Tux_encrypted.ppm"
    # decrypted_file = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/Tux_decrypted.ppm"
    # keyfile = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/key.txt"

    ecb(infile, outfile, keyfile, mode)

