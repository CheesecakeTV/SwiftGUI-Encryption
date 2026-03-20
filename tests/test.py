import SwiftGUI_Encryption as sge

pw = "Hallo Welt!"

enc = sge.encrypt_with_password(b"SECRET :D", pw)
print(enc)
dec = sge.decrypt_with_password(enc, pw)
print(dec)


