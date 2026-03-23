from typing import Hashable, Callable
from string import ascii_uppercase, ascii_lowercase, digits, ascii_letters, punctuation

ascii_letters: set = set(ascii_letters)
ascii_uppercase: set = set(ascii_uppercase)
ascii_lowercase: set = set(ascii_lowercase)
digits: set = set(digits)
punctuation: set = set(punctuation)

import SwiftGUI as sg
from SwiftGUI import ValueDict

# This class was originally created as an example for new SwiftGUI users.
# That's why it has so many comments.
class popup_create_password(sg.BasePopup, str):
    def __init__(
            self,
            title: str = "Create your password",
            min_length: int = None,
            must_include_upper: bool = None,
            must_include_lower: bool = None,
            must_include_special: bool = None,
            must_include_digits: bool = None,
            additional_check_function: Callable = None,
            additional_check_text: str = None,
            wrong_password_color: str | sg.Color = "#A52A2A",
            **kwargs
    ):
        self.min_length = min_length
        self.must_include_upper = must_include_upper
        self.must_include_lower = must_include_lower
        self.must_include_special = must_include_special
        self.must_include_digits = must_include_digits

        self.additional_check_function = additional_check_function
        self.additional_check_text = additional_check_text

        self.wrong_password_color = wrong_password_color

        layout = [
            [
                sg.T("Password:", width= 10),
                password := sg.In(
                    key= "PW",
                    default_event= True,
                    pass_char= "*", # Hidden characters
                ).bind_event(
                    sg.Event.KeyEnter,
                    key_function= lambda w:w["Confirm"].set_focus() # Jump to next input-element
                ),
                sg.Spacer(width=5),
                sg.Checkbox(
                    "Show password",
                    default_event= True,
                    key_function= lambda val: password.update(pass_char = "" if val else "*"),  # If the box is checked, reveal characters. Else hide them
                    takefocus= False,   # Pressing tab should ignore this element
                )
            ],[
                sg.T("Confirm:", width= 10),
                confirm := sg.In(
                    key= "Confirm",
                    default_event= True,
                    pass_char= "*", # Also hidden characters
                ).bind_event(
                    sg.Event.KeyEnter,  # Same as clicking "Confirm"
                    key= "Done",
                ),
                sg.T(expand=True)
            ],[
                sg.HSep(),
            ], [
                sg.Button(
                    "Confirm",
                    key= "Done",
                ),
                sg.Button(
                    "Cancel",
                    key_function= lambda :self.done()   # Call self.done() so the popup "returns" None
                )
            ]
        ] + self._additional_layout()
        self.password = password    # Save these two for later
        self.confirm = confirm

        super().__init__(layout, title=title, **kwargs)
        password.set_focus()    # Start with the focus on the password-input-field

    def _additional_layout(self) -> list[list[sg.BaseElement]]:
        new_texts = []

        if self.additional_check_text:
            new_texts.append(self.additional_check_text)

        if self.min_length:
            new_texts.append(f"Must be at least {self.min_length} characters long")

        if self.must_include_upper:
            new_texts.append(f"Must include uppercase letters")

        if self.must_include_lower:
            new_texts.append(f"Must include lowercase letters")

        if self.must_include_special:
            new_texts.append(f"Must include special characters")

        if self.must_include_digits:
            new_texts.append(f"Must include digits")

        new_layout = []
        if new_texts:
            new_layout.append([sg.HSep()])
            new_layout.append([sg.T("The password...", expand=True)])

            new_layout += [
                [sg.T(text)] for text in new_texts
            ]

        return new_layout

    def _is_valid_password(self) -> bool:
        """Check if the entered password follows the rules"""

        current_pw = self.password.value

        if self.additional_check_function and not self.additional_check_function(current_pw):
            return False

        if self.min_length and len(current_pw) < self.min_length:
            return False

        current_pw: set = set(current_pw)

        if self.must_include_upper and not (current_pw & ascii_uppercase):
            return False

        if self.must_include_lower and not (current_pw & ascii_lowercase):
            return False

        if self.must_include_special and not (current_pw & punctuation):
            return False

        if self.must_include_digits and not (current_pw & digits):
            return False

        return True

    def _event_loop(self, e: Hashable, v: sg.ValueDict):
        pw_match = self.password.value == self.confirm.value

        if e == "Done" and pw_match and self._is_valid_password():
            self.done(self.password.value)  # "Return" the password

        if self._is_valid_password():
            self.password.update_to_default_value("background_color")
        else:
            self.password.update(background_color=self.wrong_password_color)

        # If any other key happened, check if the two input-values match
        if pw_match:
            # If they do, use the default background-color for the confirm-field
            self.confirm.update_to_default_value("background_color")
        else:
            # Else, set it to red
            self.confirm.update(background_color=self.wrong_password_color)




