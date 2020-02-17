from present import *
import argparse


def chunk_encrypt(msg, key):
    msg = msg[25:]
    print(len(msg))
    split_msg = msg.split()
    binary_list = []
    byte_list = []
    split_msg.append(255)  # + 2 number padding ==> 249632 numbers
    split_msg.append(255)  # length(split_msg) = 249632
    for i in split_msg:
        binary_i = '{0:08b}'.format(int(str(i)))  # max 255, 8 bits, 2 bytes
        binary_list.append(binary_i)
    binary_string = ''.join(binary_list)  # a long string containing 11111111(255)1111..., length = 1997056 (31204*8)
    print(len(binary_string))
    # a 64 bit block requires 8 numbers
    for i in range(0, int(len(binary_string) / 64)):
        new_value = present(int(binary_string[i * 64:(i + 1) * 64], 2), key)
        byte_list.append(str(new_value).zfill(20))
    print(len(byte_list))
    new_msg = ''.join(byte_list)
    print(len(new_msg))
    return new_msg


# 249632 numbers, 31204 * 8 numbers==> 624080 digits in output file

def chunk_decrypt(msg, key):
    numbers = []
    print(len(msg))

    for i in range(0, int(len(msg) / 20)):
        dec = present_inv(int(msg[i * 20: (i + 1) * 20]), key)
        batch = bin(int(dec))[2:].zfill(64)  # decrypted string: 64 bits

        for ll in range(0, 8):  # parse into 8 bit numbers
            numbers.append(str(int(batch[ll * 8:(ll + 1) * 8], 2)))

    del numbers[-1]
    del numbers[-1]
    print(len(numbers))
    number_string = ','.join(numbers)
    return number_string


def ecb(infile, outfile, keyfile, mode):
    keyf = open(keyfile, "r")
    key = int(keyf.read())
    outf = open(outfile, "w")
    f = open(infile, "r")
    msg = f.read()

    if (mode.lower() == 'e'):
        outmsg = chunk_encrypt(msg, key)
        outf.write(outmsg)
    elif (mode.lower() == 'd'):
        outmsg = chunk_decrypt(msg, key)
        outf.write('P3\n# Tux img\n265 314\n255\n' + outmsg)

    print("Finished!!!!")



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

    infile = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/Tux.ppm"
    encrypted_file = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/Tux_encrypted_test.ppm"
    decrypted_file = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/Tux_decrypted_test.ppm"
    keyfile = "C:/Users/87173/Desktop/term6/CyberSec/lab/lab_4/key.txt"

    # mode = 'd'
    ecb(infile, encrypted_file, keyfile, 'e')
    ecb(encrypted_file, decrypted_file, keyfile, 'd')

