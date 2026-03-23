
from . import Advanced
random_key = Advanced.random_key

from .basics import decrypt_full, encrypt_full, encrypt_with_password, decrypt_with_password, password_to_key, encrypt_multilayer, decrypt_multilayer
from .key_files import KeyFile, KeyHandler, BaseKeyFile

try:
    import SwiftGUI
except ImportError:
    ...
else:
    from . import sg

