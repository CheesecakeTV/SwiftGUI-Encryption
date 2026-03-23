from abc import abstractmethod
from os import PathLike
from pathlib import Path

from SwiftGUI_Encryption import Advanced as adv
from SwiftGUI_Encryption import encrypt_full, decrypt_full

SALT_LEN = 16
SECURITY_MULTIPLIER = 8


class BaseKeyFile:

    def __init__(self, file_password: str = None, file_key: bytes = None, saved_key: bytes = None):
        """
        Abstract base class so you could implement a different read/write-method.

        Create/read a single file containing a key.
        The file can be encrypted by a password, or a key directly

        :param file_password:   Password to unlock the file
        :param file_key:    Key to unlock the file
        :param saved_key:   The key that is to be stored inside the file. Leave empty for random key
        """
        # Create folders containing this file
        assert file_key or file_password, "You need to specify either a file_password, or a file_key for every KeyFile!"

        self._salt: bytes = adv.random_key(SALT_LEN) # Placeholder if a key is used instead of a password
        self._key: bytes | None = saved_key  # Key stored in the file
        self._file_password: str | None = file_password
        self._file_key: bytes | None = file_key # Key to unlock the file

        if self.exists():
            self._init_exists()
        else:
            self._init_not_exists()

    def _do_key_derivation(self):
        """
        Generate or re-generate the file-key
        """
        if self._file_password is None:
            return

        self._salt = adv.random_key(SALT_LEN)
        file_key = adv.argon2_key_derivation(self._file_password.encode(), self._salt, multiplier=SECURITY_MULTIPLIER)

        self._file_key = file_key

    def _init_exists(self):
        """init if the file already exists"""
        raw = self._read()

        if self._file_key is None:
            self._salt = raw[:SALT_LEN]
            self._file_key = adv.argon2_key_derivation(self._file_password.encode(), self._salt, multiplier=SECURITY_MULTIPLIER)

        assert self._key is None, "The file already exists, yet you tried to define its secret key"
        # if self._key is not None:
        #     self.save()
        #     return

        raw = raw[SALT_LEN:]
        self._key = decrypt_full(raw, self._file_key)

    def _init_not_exists(self):
        """init if the file doesn't already exist"""
        self._do_key_derivation()

        if self._key is None:
            self._key = adv.random_key()

        self.save()

    def save(self):
        """
        Save the content of the "file" to whereever

        :return: Self (Not typehinted for compatability-reasons)
        """
        raw = encrypt_full(self._key, self._file_key)
        self._write(self._salt + raw)
        return self

    @abstractmethod
    def _read(self) -> bytes:
        """Pure read from whereever"""
        ...

    @abstractmethod
    def _write(self, data: bytes):
        """Pure write the data to whereever"""
        ...

    @abstractmethod
    def exists(self) -> bool:
        """True, if the file (or whatever) exists"""
        ...

    @property
    def key(self) -> bytes:
        return self._key

    @key.setter
    def key(self, val):
        self.change_key(val)

    def change_key(self, new_key: bytes = None):
        """
        Overwrite the saved key.
        :param new_key:
        :return:
        """
        if new_key is None:
            new_key = adv.random_key()

        self._do_key_derivation()

        self._key = new_key
        self.save()
        return self

    def change_file_key(self, new_password: str | None = None, new_key: bytes | None = None):
        """
        Change the key/password which unlocks the file

        :param new_password:
        :param new_key:
        :return:
        """
        self._file_password = new_password
        self._file_key = new_key
        self._do_key_derivation()
        self.save()

class KeyFile(BaseKeyFile):

    def __init__(self, path: str | PathLike | Path, file_password: str = None, file_key: bytes = None,
                 saved_key: bytes = None):
        """
        Create/read a single file containing a key.
        The file can be encrypted by a password, or a key directly

        :param path: Path to the file
        :param file_password:   Password to unlock the file
        :param file_key:    Key to unlock the file
        :param saved_key:   The key that is to be stored inside the file. Leave empty for random key
        """
        # Create folders containing this file
        self.path = Path(path)

        super().__init__(file_password=file_password, file_key=file_key, saved_key=saved_key)

    def _init_not_exists(self, *args, **kwargs):
        self.path.parent.mkdir(exist_ok=True, parents=True)
        super()._init_not_exists(*args, **kwargs)

    def _read(self) -> bytes:
        """Pure read"""
        return self.path.read_bytes()

    def _write(self, data: bytes):
        """Pure write"""
        self.path.write_bytes(data)

    def exists(self) -> bool:
        """True, if the file (or whatever) exists"""
        return self.path.exists()


class KeyHandler:

    def __init__(self):
        ...


