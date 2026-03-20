import argon2pure
from Crypto.Cipher import AES
import os
import hashlib

def random_key(n: int = 32) -> bytes:
    """
    Generate a new random key
    :param n: Length of the key in bytes
    :return:
    """
    return os.urandom(n)

def readable_hash(data: bytes, n: int = 6) -> str:
    """
    Create a humanly-readable string that can be used to compare data without knowing the data.
    Only use it if the user himself needs to read/compare this

    :param data:
    :param n: Length of the checksum
    :return:
    """
    return hashlib.sha256(data).hexdigest()[:n].upper()

def make_hash(data: bytes) -> bytes:
    """
    Generate the hash-value of some data
    Raises a value-error if no text was supplied
    :param data:
    :return:
    """
    return hashlib.sha256(data).digest()

def argon2_key_derivation(derive_from: bytes, salt: bytes, multiplier: int = 1, n: int = 32) -> bytes:
    """
    If you don't know what key-derivation is, don't use this function.

    :param derive_from:
    :param salt:
    :param multiplier: You may increase this to increase calculation-time and therefore security
    :param n: How many characters the generated key should have
    :return:
    """
    salt = salt[:16]    # clip it to the needed length

    return argon2pure.argon2(derive_from, salt, multiplier, 8 * multiplier, parallelism=1, tag_length=n)

def encrypt(data: bytes, key: bytes, nonce: bytes, mac_len: int = 8) -> bytes:
    """
    Encrypt some data.
    The tag is appended to the end, fitting the decryption-function.

    :param data:
    :param key:
    :param nonce: A random number, which you should definetly remember
    :param mac_len:
    :return: Encrypted
    """
    crypter = AES.new(key, AES.MODE_GCM, mac_len=mac_len, nonce=nonce)

    enc_data, tag = crypter.encrypt_and_digest(data)  # tag is always 16 bytes

    return tag + enc_data

def decrypt(enc_data:bytes, key:bytes, nonce:bytes, mac_len: int = 8) -> bytes:
    """
    Decrypt some data.
    The tag needs to be appended to the data.

    Raises a value-error if the data was manipulated (tag is invalid)

    :param mac_len: This needs to be the same as with the encryption
    :param enc_data: Encrypted data
    :param key: This needs to be the same as with the encryption
    :param nonce: This needs to be the same as with the encryption
    :return:
    """
    tag = enc_data[:mac_len]
    enc_data = enc_data[mac_len:]
    crypter = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=mac_len)

    data = crypter.decrypt(enc_data)

    crypter.verify(tag)

    return data

