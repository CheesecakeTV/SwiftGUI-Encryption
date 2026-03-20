from pathlib import Path
import json

import SwiftGUI.Files as files
from SwiftGUI_Encryption import encrypt_full, decrypt_full, random_key
from SwiftGUI_Encryption import Advanced as adv

NONCE_LEN = 32
SALT_LEN = 16

class EncryptedJSONDictFile(files.BaseDictFile):
    """
    An encrypted json-dictfile
    """

    def __init__(
            self,
            path: str | Path,
            file_key: bytes,
            *,
            defaults: dict = None,
            add_defaults_to_values: bool = None,
            auto_save: bool = None,
            **kwargs
    ):
        assert not isinstance(file_key, str), "Keys are always in the byte-format.\nIf you tired to pass a password, use PasswordJSONDictFile instead."

        self._filekey = file_key    # Key to encrypt the file with

        super().__init__(
            path=path,
            defaults=defaults,
            add_defaults_to_values=add_defaults_to_values,
            auto_save=auto_save,
            **kwargs
        )

    def change_key(self, new_key: bytes):
        """

        :param new_key:
        :return:
        """
        self._filekey = new_key
        self._do_auto_save()

        return self

    @property
    def key(self) -> bytes:
        return self._filekey

    def _save_to_file(
            self,
            values: dict,
            path: Path,
    ):
        raw = json.dumps(values)

        path.write_bytes(
            encrypt_full(raw.encode(), self._filekey)
        )

    def _load_from_file(
            self,
            path: Path
    ) -> dict:
        raw = path.read_bytes()

        raw = decrypt_full(raw, self._filekey).decode()
        return json.loads(raw)

class PasswordJSONDictFile(EncryptedJSONDictFile):
    """
    An encrypted JSON-dictfile that requires a password instead of a key
    """
    def __init__(
            self,
            path: str | Path,
            password: str,
            *,
            defaults: dict = None,
            add_defaults_to_values: bool = None,
            auto_save: bool = None,
            **kwargs
    ):
        path = Path(path)

        exists = path.exists()
        self._regenerated_key = not exists  # Regenerate the key on next save, if it already exists
        if exists:
            salt = path.read_bytes()[:SALT_LEN]
        else:
            salt = random_key(SALT_LEN)

        self._salt = salt
        self._password = password

        self._filekey = adv.argon2_key_derivation(password.encode(), salt)  # Key to encrypt the file with

        super(EncryptedJSONDictFile, self).__init__(
            path=path,
            #file_key=self._filekey,
            defaults=defaults,
            add_defaults_to_values=add_defaults_to_values,
            auto_save=auto_save,
            **kwargs
        )

    def _regenerate_key(self, new_salt = True):
        if new_salt:
            self._salt = random_key(SALT_LEN)

        self._filekey = adv.argon2_key_derivation(self._password.encode(), self._salt)

    def change_key(self, new_key: bytes):
        """
        NOT IMPLEMENTED!

        :param new_key:
        :return:
        """
        raise NotImplementedError("Setting a key directly on a Password-file is not possible. Use .change_password instead!")

    def change_password(self, new_password: str):
        """
        Specify a new password for this file

        :param new_password:
        :return:
        """
        self._password = new_password
        self._regenerate_key()

    def _save_to_file(
            self,
            values: dict,
            path: Path,
    ):
        raw = json.dumps(values)

        if not self._regenerated_key:
            self._regenerate_key()
            self._regenerated_key = False

        path.write_bytes(
            self._salt + encrypt_full(raw.encode(), self._filekey)
        )

    def _load_from_file(
            self,
            path: Path
    ) -> dict:
        raw = path.read_bytes()

        salt = raw[:SALT_LEN]
        if salt != self._salt:
            self._salt = salt
            self._regenerate_key(new_salt=False)

        raw = decrypt_full(raw[SALT_LEN:], self._filekey).decode()
        return json.loads(raw)


