import SwiftGUI_Encryption as sge

my_file = sge.sg.PasswordJSONDictFile("secrets/ConfidentialInformation1", "Password")
my_file.set_path("secrets/ConfidentialInformation", reload=True)

#my_file["Hello"] = "Secret world"
print(my_file)

