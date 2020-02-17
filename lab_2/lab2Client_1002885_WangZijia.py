#!/usr/bin/python3
# -*- coding: utf-8 -*-
# DA+Nils 2018
# Andrei + Z.TANG + Bowen, 2019

"""
Lab2: Breaking Ciphers

Pwntool client for python3

Install: see install.sh

Documentation: https://python3-pwntools.readthedocs.io/en/latest/
"""

from pwn import remote
import operator

# pass two bytestrings to this function
def XOR(a, b):
    r = b''
    for x, y in zip(a, b):
        r += (x ^ y).to_bytes(1, 'big')
    return r


def sol1():
    conn = remote(URL, PORT)
    message = conn.recvuntil('-Pad')  # receive TCP stream until end of menu
    conn.sendline("1")  # select challenge 1

    dontcare = conn.recvuntil(':')
    challenge = conn.recvline()
    # print("*************** challenge is: ", challenge.decode("ascii"))
    # decrypt the challenge here
    # ————————————————————————————————————————————
    char_freq_result = get_freq_result_from_cipher(challenge)
    char_mapping = get_char_mapping(char_freq_result)
    char_mapping = {50: 32, 79: 101, 46: 116, 73: 97, 99: 111, 116: 104, 12: 114, 75: 110, 124: 100, 62: 105, 69: 115,
                    45: 108, 59: 119, 9: 10, 32: 103, 112: 44, 70: 117, 89: 99, 95: 109, 39: 121, 101: 102, 88: 112,
                    87: 46, 60: 98, 86: 107, 115: 118, 51: 34, 117: 45, 118: 39, 82: 106, 123: 113, 102: 63, 10: 10}

    solution = ''
    for char in challenge.decode("ascii"):
        solution += chr(int(char_mapping[ord(char)]))

    # solution = solution.encode()
    print(solution)
    # ————————————————————————————————————————————
    # solution = int(0).to_bytes(7408, 'big')
    conn.send(solution)
    message = conn.recvline()
    message = conn.recvline()

    print("*************** message is: ", message)
    if b'Congratulations' in message:
        print("*************** message is: ", message)
    conn.close()


def sol2():
    conn = remote(URL, PORT)
    message = conn.recvuntil('-Pad')  # receive TCP stream until end of menu
    conn.sendline("2")  # select challenge 2

    dontcare = conn.recvuntil(':')
    challenge = conn.recvline()
    print("*************** challenge is: ", challenge.decode("ascii"))
    # some all zero mask.
    # TODO: find the magic mask!
    # -----------------------
    mask = XOR('Student ID 1000000 gets 0 points'.encode(), "Student ID 1002885 gets 0 points".encode())
    # -----------------------
    # mask = int(0).to_bytes(len(message), 'big')
    print("*************** mask is: ", mask)
    message = XOR(challenge, mask)
    conn.send(message)
    message = conn.recvline()
    message = conn.recvline()
    print("*************** message is: ", message)
    if b'points' in message:
        print(message)
    conn.close()


def get_freq_result_from_cipher(challenge):
    char_freq = {}
    challenge = challenge.decode("ascii")
    for char in challenge:
        char_freq[ord(char)] = challenge.count(char)
    sorted_char_freq = dict(sorted(char_freq.items(), key=operator.itemgetter(1), reverse=True))
    char_freq_result = list(sorted_char_freq.keys())
    print(char_freq_result)
    return char_freq_result


def get_char_mapping(char_freq_result):
    char_mapping = {}
    # online resource
    std_freq_result = ['101', '116', '111', '97', '110', '105', '115', '114', '108', '104', '100', '99', '117', '32',
                       '109', '103', '112', '46', '45', '102', '119', '121', '98', '118', '44', '107', '149', '48',
                       '49', '58', '83', '67', '77', '50', '84', '73', '68', '65', '69', '80', '87', '82', '39', '34',
                       '72', '41', '40', '66', '78', '120', '76', '71', '51', '79', '74', '53', '47', '63', '70', '52',
                       '62', '60', '59', '95', '54', '56', '55', '57', '86', '106', '85', '113', '75', '42', '122',
                       '36', '88', '81', '89', '61', '38', '43', '35', '37', '93', '91', '90', '64', '33', '9', '123',
                       '125', '92', '183', '96', '124', '94', '126', '23', '131', '223', '226', '229', '230', '237']
    # online resource
    std_freq_result = [97, 101, 125, 111, 114, 105, 115, 110, 49, 116, 108, 50, 109, 100, 99, 112, 51, 104, 98, 117, 107, 52, 53, 103, 57, 54, 56, 55, 121, 102, 119, 48, 106, 118, 122, 120, 113, 65, 83, 69, 82, 66, 84, 77, 76, 78, 80, 79, 73, 68, 67, 72, 71, 75, 70, 74, 85, 87, 46, 33, 89, 42, 64, 86, 45, 90, 81, 88, 95, 36, 35, 44, 47, 43, 63, 59, 94, 37, 126, 61, 38, 96, 92, 41, 93, 91, 58, 60, 40, 62, 34, 124, 123, 39, 195]
    # sherlock.txt
    std_freq_result = [32, 101, 116, 111, 97, 110, 104, 105, 114, 115, 100, 108, 117, 10, 109, 99, 119, 102, 121, 103, 112, 44, 46, 98, 34, 118, 107, 73, 72, 45, 84, 83, 87, 63, 66, 39, 65, 120, 77, 67, 68, 89, 78, 76, 69, 106, 113, 79, 71, 33, 80, 70, 82, 122, 49, 85, 59, 48, 58, 74, 86, 42, 56, 51, 40, 41, 47, 50, 52, 55, 53, 75, 54, 57, 81, 64, 91, 93, 60, 62, 95, 88, 36, 35, 37]

    # std_freq_result = ['e', 't', 'o', 'a', 'n', 'i', 's', 'r', 'l', 'h', 'd', 'c', 'u', 'space', 'm', 'g', 'p', '.',
    #                    '-', 'f', 'w', 'y', 'b', 'v', ',', 'k', '0', '1', ':', 'S', 'C', 'M', '2', 'T', 'I', 'D', 'A',
    #                    'E', 'P', 'W', 'R', "'", '"', 'H', ')', '(', 'B', 'N', 'x', 'L', 'G', '3', 'O', 'J', '5', '/',
    #                    '?', 'F', '4', '>', '<', ';', '_', '6', '8', '7', '9', 'V', 'j', 'U', 'q', 'K', '*', 'z', '$',
    #                    'X', 'Q', 'Y', '=', '&', '+', '#', '%', ']', '[', 'Z', '@', '!', 'tab', '{', '}', '\\', '`', '|',
    #                    '^', '~', 'etb', 'ï¿½']
    for idx in range(0, len(char_freq_result)):
        char_mapping[char_freq_result[idx]] = std_freq_result[idx]
    return char_mapping


if __name__ == "__main__":

    # NOTE: UPPERCASE names for constants is a (nice) Python convention
    URL = '34.239.117.115'
    PORT = 1337

    sol1()
    sol2()
