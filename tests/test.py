import SwiftGUI_Encryption as sge

key = sge.random_key()
data = b"Hallo"

try:
    sge.decrypt_full(data, key)
except ValueError:
    print("Failure")
else:
    print("Success!")
