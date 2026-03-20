import argon2pure
from Crypto.Cipher import AES
import os
import hashlib

from SwiftGUI_Encryption import Advanced as adv

NONCE_LEN = 32  # This should not be chanced, but who am I to judge

def encrypt_full(data: bytes, key: bytes) -> bytes:
    """
    Encrypt some data

    :param key:
    :param data:
    :return:
    """
    nonce = adv.random_key(NONCE_LEN)

    return nonce + adv.encrypt(data, key, nonce)

def decrypt_full(data: bytes, key: bytes) -> bytes:
    """
    Decrypt some data with its key

    :param data:
    :param key:
    :return:
    """
    nonce = data[:NONCE_LEN]
    data = data[NONCE_LEN:]

    return adv.decrypt(data, key, nonce)


