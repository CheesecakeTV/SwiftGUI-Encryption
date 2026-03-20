import SwiftGUI_Encryption as sge


pw = b" " * 32

my_file = sge.KeyFile("Keys/my_key.key", file_key=pw)#, saved_key=b"SECRET :D")
#my_file.change_file_key(new_password="Hi")

print(my_file.key)


