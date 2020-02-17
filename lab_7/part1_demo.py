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


# TODO: PART I: Generate the public key and private key and mod
def generate_key(pub_key_file, priv_key_file):
    pub_key = open(pub_key_file, 'r').read()
    priv_key = open(priv_key_file, 'r').read()

    pub_key = RSA.importKey(pub_key)
    priv_key = RSA.importKey(priv_key)
    pub_key_part = pub_key.e  # public key
    priv_key_part = priv_key.d  # private key
    mod_part = pub_key.n

    return pub_key_part, priv_key_part, mod_part


# TODO: PART I: Encrypt the msg using the given key
def encrypt_msg(key_part, mod_part, message):
    bin_msg = ' '.join('{0:07b}'.format(ord(x)) for x in message).replace(' ', '')
    encrypted_msg = square_multiply(int(bin_msg, 2), key_part, mod_part)

    return encrypted_msg


# TODO: PART I: Decrypt the msg using the given key
def decrypt_msg(key_part, mod_part, message):
    decrypted_msg = square_multiply(message, key_part, mod_part)  # in integer format
    decrypted_msg = textwrap.wrap(bin(decrypted_msg)[2:], 7)  # in binary format
    decrypted_msg = ''.join(chr(int(sub_msg, 2)) for sub_msg in decrypted_msg)  # convert into character by ascii

    return decrypted_msg


# TODO: PART I: Hash the msg
def hash_msg(message):
    hash = SHA256.new()
    hash.update(message.encode())
    hashed_msg = hash.hexdigest()
    return hashed_msg


# TODO: PART I: Sign the hashed message using private key
def sign_msg(key, mod, message):
    signed_msg = encrypt_msg(key, mod, message)  # encrypt the hashed_msg with private key
    return signed_msg


# TODO: PART I: Verify the hashed message using public key
def verify_msg(key, mod, message):
    verified_msg = decrypt_msg(key, mod, message)
    return verified_msg


# TODO: PART I: Demo the whole process of encryption, decryption, sign and verify
def demo_encryption_decryption(public_key_file, private_key_file, message):
    pub_key, priv_key, mod = generate_key(public_key_file, private_key_file)
    encrypted_msg = encrypt_msg(pub_key, mod, message)
    decrypted_msg = decrypt_msg(priv_key, mod, encrypted_msg)

    print("----------------- demo of encryption and decryption of RSA ---------------------\n")
    print("Original message: \n", message, "\n")
    print("Encrypted_msg: \n", encrypted_msg, "\n")
    print("Decrypted_msg: \n", decrypted_msg, "\n")
    print("Decrypted message is matched with the original message: ", decrypted_msg == message, '\n')

    hashed_msg = hash_msg(message)
    signed_msg = sign_msg(priv_key, mod, hashed_msg)
    verified_msg = verify_msg(pub_key, mod, signed_msg)

    print("----------------- demo of signing and verifying message ---------------------\n")
    print("Hashed msg: \n", hashed_msg, "\n")
    print("Signed msg: \n", signed_msg, "\n")
    print("Verified msg: \n", verified_msg, "\n")
    print("Verified message is matched with the hashed message: ", verified_msg == hashed_msg, '\n')


if __name__ == "__main__":
    message = open('/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/message.txt', 'r').read()
    pub_key = '/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/mykey.pem.pub'
    priv_key = '/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/mykey.pem.priv'

    demo_encryption_decryption(pub_key, priv_key, message)
    # encrypted_msg = encrypt_RSA(pub_key, message)

    pass
