import SwiftGUI_Encryption as sge

my_key = "Hallo Welt"

my_file = sge.sg.PasswordJSONDictFile("filetest/hallo.secret", my_key)

#my_file["Hallo"] = "Welt"

print(my_file)
print(my_file.key)


