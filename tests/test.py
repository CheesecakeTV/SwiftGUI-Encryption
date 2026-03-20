import SwiftGUI_Encryption as sge
import SwiftGUI as sg

sg.Themes.FourColors.Emerald()
print(sge.sg.popup_create_password(
    "PW erstellen",
    #min_length= 10,
    must_include_special=True,
    must_include_lower=True,
    must_include_upper=True,
    must_include_digits=True,
    min_length=5,
))


