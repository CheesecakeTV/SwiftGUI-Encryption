import argon2pure
from Crypto.Cipher import AES
import os
import hashlib

from SwiftGUI_Encryption import Advanced as adv

# This should not be chanced, it just doesn't feel right to add magic numbers...
NONCE_LEN = 32
SALT_LEN = 16

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

def encrypt_with_password(data: bytes, password: str, security_multiplier: int = 1) -> bytes:
    """
    IMPORTANT:
    This needs to be decrypted with decrypt_with_password.
    It is not compatible with decrypt_full.

    But this function is very secure, because each encryption generates its own key.

    :param data: What to encrypt
    :param password:
    :param security_multiplier:
    :return:
    """
    salt = adv.random_key(SALT_LEN)
    key = adv.argon2_key_derivation(password.encode(), salt, multiplier=security_multiplier)

    return salt + encrypt_full(data, key)

def decrypt_with_password(data: bytes, password: str, security_multiplier: int = 1) -> bytes:
    """
    IMPORTANT:
    This needs data from encrypt_with_password.
    encrypt_full doesn't work on this.

    :param data: What to decrypt
    :param password:
    :param security_multiplier: Needs to be the same as with the encryption
    :return:
    """
    salt = data[:SALT_LEN]
    key = adv.argon2_key_derivation(password.encode(), salt, multiplier=security_multiplier)

    return decrypt_full(data[SALT_LEN:], key)

def password_to_key(password: str, security_multiplier: int = 1) -> bytes:
    """
    WARNING!
    If anyone finds out what this function returned (the key), he might be able to find your password.
    It's still quite secure, but not against people with supercomputers.
    The attack is called pre-calculation-attack, or rainbow-table-attack.

    Increasing the security_multiplier helps, but not as much as it does normally.

    :param password:
    :param security_multiplier: Needs to be the same as with the encryption
    :return:
    """
    return adv.argon2_key_derivation(password.encode(), salt=b"", multiplier=security_multiplier)

