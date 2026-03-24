from typing import Hashable

import SwiftGUI as sg


#########################################################################
# A small tool to calculate how long it would take to break a password. #
# You need to install SwiftGUI, then run this script.                   #
#########################################################################



_timeunits = {
    "milliseconds": 0.001,
    "seconds": 1,
    "minutes": 60,
    "hours": 3600,
    "days": 24 * 3600,
    "month": 30 * 24 * 3600,
    "years": 365 * 24 * 3600,
}

class PWSecurityEstimator(sg.BasePopupNonblocking):

    def __init__(self):
        sg.GlobalOptions.Text.padding = 3

        layout = [
            [
                sg.T("How long is the password?")
            ], [
                sg.T("Character-count: "),
                sg.Button("-", key= "-"),
                sg.In(
                    "8",
                    width= 5,
                    key= "CharCount",
                    default_event= True,
                    key_function=self._calculate,
                ),
                sg.Button("+", key= "+"),
            ],[
                sg.HSep(),
            ], [
                sg.T("Which types of characters are allowed?")
            ], [
                sg.Checkbox(
                    "Digits",
                    key= "Digits",
                    default_event= True,
                    default_value= True,
                ),
                sg.Checkbox(
                    "Letters lowercase",
                    key= "LettersL",
                    default_event= True,
                    default_value=True,
                ),
                sg.Checkbox(
                    "Letters uppercase",
                    key= "LettersU",
                    default_event= True,
                    default_value=True,
                ),
                sg.Checkbox(
                    "Special chars (21)",
                    key= "Specials",
                    default_event= True,
                )
            ],[
                sg.HSep()
            ], [
                sg.T("How long does it take one processing unit to try out a single password?")
            ], [
                sg.T("Calculation time per try: "),
                sg.In("0.2", width= 5, key= "CPS", default_event= True),
                sg.T(" s")
            ],[
                sg.T()
            ], [
                sg.T("0.2s seams a bit long, but not with key derivation.")
            ], [
                sg.T("It artificially increases the calculation-time.")
            ], [
                sg.T("For my processor, one calculation takes around 0.2s.")
            ], [
                sg.HSep()
            ], [
                sg.T("How many processing-units does the computer have?")
            ], [
                sg.T("Processing-units: "),
                sg.In("100_000", key= "CPUs", default_event= True),
            ],[
                sg.T("Modern supercomputers can have hundreds of thousands.\nYour computer probably has around 8.")
            ], [
                sg.HSep(),
            ],[
                sg.T("It takes the computer")
            ], [
                sg.Input(
                    readonly= True,
                    key= "Output",
                    width= 25,
                    justify= "right",
                ),
                sg.Combobox(
                    _timeunits.keys(),
                    default_value= "years",
                    key= "Timeunit",
                    default_event= True,
                )
            ], [
                sg.T("to try out all possible passwords.")
            ], [
                sg.T()    # Placeholder
            ], [
                sg.T("It takes half that time for a 50% chance of success.")
            ]
        ]
        
        super().__init__(layout, title= "Brute-Force-attack calculator")

        sg.GlobalOptions.Text.padding = None

        self._calculate()

    def _event_loop(self, e: Hashable, v: sg.ValueDict):
        try:
            if e == "+":
                v["CharCount"] = int(v["CharCount"]) + 1
            if e == "-":
                v["CharCount"] = int(v["CharCount"]) - 1
        except ValueError:
            ...

        self._calculate()

    def _calculate(self):
        v = self.w.value

        try:
            possible_chars = v["Digits"] * 10 + v["LettersL"] * 24 + v["LettersU"] * 24 + v["Specials"] * 21
            char_count = int(v["CharCount"])
            CPS = float(v["CPS"])  # Yeah, this should be calculation-time, not CPS. Don't really care.
            CPUs = float(v["CPUs"])

            calculations = 0
            for i in range(1, char_count):
                calculations += possible_chars ** i

            total_time = CPS * calculations / (CPUs * _timeunits[v["Timeunit"]])

            v["Output"] = f"{round(total_time, 5):_}"
        except (ValueError, ZeroDivisionError):
            v["Output"] = " Error "


if __name__ == '__main__':
    sg.Themes.FourColors.TransgressionTown()
    PWSecurityEstimator().w.loop()



