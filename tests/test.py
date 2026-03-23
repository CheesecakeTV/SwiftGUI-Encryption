import SwiftGUI_Encryption as sge

keys = [
    sge.random_key(),
    sge.random_key(),
    sge.random_key(),
    sge.random_key(),
    sge.random_key(),
    sge.random_key(),
    sge.random_key(),
]

data = b"Hallo Welt"

encr = sge.encrypt_multilayer(data, *keys)
print(encr, len(encr))
decr = sge.decrypt_multilayer(encr, *keys)
print(decr)

