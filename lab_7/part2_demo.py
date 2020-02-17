#!/usr/bin/env python3

######################
#  Wang Zijia 1002885
######################
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256
import argparse
from pyrsa_sq_mul import *
import textwrap
import sys


# TODO: PART II: Generate the public key and private key and mod
def generate_key(pub_key_file, priv_key_file):
    pub_key = open(pub_key_file, 'r').read()
    priv_key = open(priv_key_file, 'r').read()

    pub_key = RSA.importKey(pub_key)
    priv_key = RSA.importKey(priv_key)

    pub_key_part = pub_key.e  # public key
    priv_key_part = priv_key.d  # private key
    mod_part = pub_key.n

    return pub_key_part, priv_key_part, mod_part


# TODO: PART II: Encrypt the msg using the given key
def encrypt_msg(key_part, mod_part, message):
    encrypted_msg = square_multiply(message, key_part, mod_part)

    # msg = textwrap.wrap(bin(encrypted_msg)[2:], 7)  # in binary format
    # print(msg)
    # msg = ''.join(chr(int(sub_msg, 2)) for sub_msg in msg)  # convert into character by ascii
    # print(msg)
    return encrypted_msg


# TODO: PART II: Decrypt the msg using the given key
def decrypt_msg(key_part, mod_part, message):
    decrypted_msg = square_multiply(message, key_part, mod_part)  # in integer format
    return decrypted_msg


def demo_protocol_attack(public_key_file, private_key_file):
    pub_key, priv_key, mod = generate_key(public_key_file, private_key_file)
    # Alice sent this 100 to Bob
    plaintext = 100
    ciphertext = encrypt_msg(pub_key, mod, plaintext)  # 100 is encrypted by the public key
    s = 2  # Attack pick this 2
    y_s = encrypt_msg(pub_key, mod, s)  # x
    m = (ciphertext*y_s) % mod  # encryption of modified msg

    # bob verify signature
    x_prime = encrypt_msg(pub_key, mod, s)  # Bob verified the signature => x_prime
    print("the message sent with signature by Attacker (Alice): \n", y_s, "\n")
    print("the message Bob get after pub(s): \n", x_prime, "\n")

    decrypted_m = decrypt_msg(priv_key, mod, m)  # modified msg

    print("PART II ---------------------")
    print("Encrypting: ", plaintext, '\n')
    print("Result: \n", ciphertext, '\n')
    print("Modified to: \n", m, '\n')
    print("Decrypted: ", decrypted_m, '\n')

if __name__ == "__main__":
    message = open('/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/message.txt', 'r').read()
    pub_key = '/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/mykey.pem.pub'
    priv_key = '/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/mykey.pem.priv'

    demo_protocol_attack(pub_key, priv_key)

    pass
