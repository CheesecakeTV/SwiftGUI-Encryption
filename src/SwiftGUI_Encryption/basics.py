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

def encrypt_multilayer(data: bytes, *keys: bytes) -> bytes:
    """
    Encrypt some data multiple times.
    Pass a key for every layer of encryption.

    This is overkill for most applications.
    A single AES-256-GCM-encryption is already very secure, even against quantumcomputers.

    VERY IMPORTANT:
    Don't correlate the keys in any way.
    If you calculate key2 from key1, you can just leave out key2.
    DON'T DO SECURITY-BY-OBSCURITY!

    KINDA IMPORTANT:
    Using two keys is only a little more secure than one key, because someone could do a "meet-in-the-middle-attack".
    As a general rule, you should only use an odd number of keys.

    TECHNICALITIES:
    Only the innermost encryption is using AES-GCM Mode. All other layers are AES-CTR.
    That's because full AES-GCM allows guessing, if the decryption was successful.
    Especially for short data, you could brute-force through layer by layer, leaving only a few possible keys per layer.

    So, this function disables that verification-step for the outer layers.
    You can only check if the full decryption was a success, but not separate layers.

    :return:
    """
    # GCM encryption
    first_nonce = adv.random_key(NONCE_LEN)
    nonce = first_nonce
    data = adv.encrypt(data, keys[0], nonce)

    # CTR encryptions
    for key in keys[1:]:
        nonce = adv.make_hash(nonce)[:12]
        data = adv.encrypt_CTR(data, key, nonce)

    return first_nonce + data

def decrypt_multilayer(data: bytes, *keys: bytes) -> bytes:
    """
    Read the description of encrypt_multilayer.

    The keys have to be in the same order as with the encryption.

    :return:
    """
    first_nonce = data[:NONCE_LEN]
    data = data[NONCE_LEN:]

    nonce = first_nonce
    nonces = list()

    for i in range(len(keys) - 1):
        nonce = adv.make_hash(nonce)[:12]
        nonces.append(nonce)

    # CTR encryptions
    for nonce, key in zip(nonces[::-1], keys[1:][::-1]):
        data = adv.decrypt_CTR(data, key, nonce)

    # GCM encryption
    return adv.decrypt(data, keys[0], first_nonce)

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

