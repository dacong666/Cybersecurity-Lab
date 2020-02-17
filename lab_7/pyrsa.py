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
import base64


def generate_RSA(bits=1024):
    key = RSA.generate(bits)
    public_key = key.publickey().exportKey('PEM').decode('ascii')
    private_key = key.exportKey('PEM').decode('ascii')
    # with open('/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/public_key_file.txt', 'w+') as file:
    #     file.write(public_key)
    # with open('/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/private_key_file.txt', 'w+') as file:
    #     file.write(private_key)
    return public_key, private_key


def encrypt_RSA(public_key_file, message):
    key = RSA.importKey(public_key_file)
    rsa = PKCS1_OAEP.new(key)

    encrypted_msg = rsa.encrypt(bytes(message, encoding='utf8'))
    encrypted_msg = base64.b64encode(encrypted_msg)
    return encrypted_msg

def decrypt_RSA(private_key_file, cipher):
    key = RSA.importKey(private_key_file)
    rsa = PKCS1_OAEP.new(key)

    cipher = base64.b64decode(cipher)
    decrypted_msg = rsa.decrypt(cipher)
    return decrypted_msg.decode()

def sign_RSA(private_key_loc, data):
    key = RSA.importKey(private_key_loc)

    hash = SHA256.new()
    hash.update(data.encode())

    signer = PKCS1_PSS.new(key)
    signature = signer.sign(hash)
    signature = base64.b64encode(signature)
    return signature


def verify_sign(public_key_loc, sign, data):
    key = RSA.importKey(public_key_loc)

    hash = SHA256.new()
    hash.update(data.encode())

    verifier = PKCS1_PSS.new(key)
    verification = verifier.verify(hash, base64.b64decode(sign))
    return verification


def demo_protocol_attack(public_key, private_key):
    # Alice sent this 100 to Bob
    plaintext = 100
    ciphertext = encrypt_RSA(public_key, str(plaintext))  # 100 is encrypted by the public key
    s = 2  # Attack pick this 2
    y_s = encrypt_RSA(public_key, str(s))  # x
    m = (unpack_bigint(ciphertext)*unpack_bigint(y_s))  # encryption of modified msg
    m = str(pack_bigint(int(m)))
    # bob verify signature
    x_prime = encrypt_RSA(public_key, str(s))  # Bob verified the signature => x_prime

    print("the message sent with signature by Attacker (Alice): \n", y_s, "\n")
    print("the message Bob get after pub(s): \n", x_prime, "\n")

    # print(decrypt_RSA(private_key, x_prime))
    # print(decrypt_RSA(private_key, y_s))


    decrypted_m = ''
    length = 85
    for i in range(0, len(m), length):
        decrypted_m += encrypt_RSA(private_key, m[i:i+length]).decode()


    # decrypted_m = encrypt_RSA(private_key, (m))  # modified msg

    print("PART III ---------------------")
    print("Encrypting: \n", plaintext, '\n')
    print("Result: \n", ciphertext, '\n')
    print("Modified to: \n", m, '\n')
    print("Decrypted: \n", decrypted_m, '\n')
    print("Is the modified message the same as the target one? {}".format(decrypted_m == s*plaintext))


if __name__ == "__main__":
    message = open('/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/mydata.txt', 'r').read()
    # pub_key = '/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/mykey.pem.pub'
    # priv_key = '/mnt/c/Users/87173/Desktop/term6/CyberSec/lab/lab_7/mykey.pem.priv'

    public_key, private_key = generate_RSA()

    print("----------------- demo of encryption and decryption of RSA ---------------------\n")
    print("Original message: \n", message)
    cipher_text = encrypt_RSA(public_key, message)
    print("Cipher: \n", cipher_text, '\n')
    decrypted_cipher = decrypt_RSA(private_key, cipher_text)
    print("Decrypted cipher: \n", decrypted_cipher)
    print("Decrypted message is matched with the original message: \n", decrypted_cipher == message, '\n')

    print("----------------- demo of signing and verifying message ---------------------\n")
    signature = sign_RSA(private_key, message)
    print("signature: \n", signature, '\n')
    verification = verify_sign(public_key, signature, message)
    print("verification: \n", verification, '\n')

    print("----------------- demo of protocol attack ---------------------\n")
    demo_protocol_attack(public_key, private_key)
    pass
