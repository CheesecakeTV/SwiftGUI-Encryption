
# SwiftGUI-Logging: Motivation
A small package ment to extend logging to better fit actual applications.

Before getting into the logging-package, I usually implemented 
something like this (but more complicated):
```py
def main():
    ...

if __name__ == "__main__":
    try:
        main()  # Run the main program
    except Exception as ex: # An exception occured
        with open("Crashlog.txt", "w") as f:    # Save exception to file
            f.write(str(ex))
```
If `main()` causes an exception, the file `Crashlog.txt` is created
containing information about the exception.
That means, only "the interesting logs" take up storage space.

Unfortunately, you can't implement such a functionality using the 
logging-package.

Until now.

SwiftGUI-Logging provides a very easy way to set up crashlogs that 
are fully compatible with the logging-package.

# Basic usage
## Installation
Install the package by running this on your terminal:
```bash
pip install SwiftGUI_Logging
```

## Crashlogging to a file
Simply call `SwiftGUI_Logging.Configs.exceptions_to_file(filepath)` 
to set up the crashlogger.

That's all.

Example:
```py
import time
import SwiftGUI_Logging as sgl
import logging

def main():
    for i in range(10):
        logging.debug(f"Test {i}")
        print(i)
        time.sleep(0.25)

    logging.info("Crashing the program now")

    1 / 0   # Cause a ZeroDivisionError, which crashes the program

if __name__ == '__main__':
    sgl.Configs.exceptions_to_file("Crashlogs/Crash.log") # Set up the crash-log
    main()  # Execute program
```

You'll find that the directory `Crashlogs` was created.
After the program executes, the directory contains a file like
`Crash_2026-02-24_16-33-52.log`.

As you can see, the time of the crash was inserted into the 
filename, so that multiple crashlogs don't overwrite each other.

The file contains the most recent log-entries (from `logging.debug` and `logging.info`)
and the exception with full traceback:
```log
2026-02-24 16:33:49,940 - root - DEBUG - Test 0
2026-02-24 16:33:50,197 - root - DEBUG - Test 1
2026-02-24 16:33:50,451 - root - DEBUG - Test 2
2026-02-24 16:33:50,704 - root - DEBUG - Test 3
2026-02-24 16:33:50,958 - root - DEBUG - Test 4
2026-02-24 16:33:51,214 - root - DEBUG - Test 5
2026-02-24 16:33:51,469 - root - DEBUG - Test 6
2026-02-24 16:33:51,723 - root - DEBUG - Test 7
2026-02-24 16:33:51,979 - root - DEBUG - Test 8
2026-02-24 16:33:52,235 - root - DEBUG - Test 9
2026-02-24 16:33:52,490 - root - INFO - Crashing the program now
2026-02-24 16:33:52,490 - root - ERROR - Traceback (most recent call last):
  File "C:\Users\chees\PycharmProjects\SwiftGUI-Logging\tests\test.py", line 17, in <module>
    main()  # Execute program
  File "C:\Users\chees\PycharmProjects\SwiftGUI-Logging\tests\test.py", line 13, in main
    1 / 0   # Cause a ZeroDivisionError, which crashes the program
ZeroDivisionError: division by zero
```

`sgl.Configs.exceptions_to_file` can do a bit more, but for most programs,
the default configuration is fine.

## Other functionality
`SwiftGUI_Logging` provides some other functionality, but these
aren't nearly as important as the `exceptions_to_file`-function.

A detailed documentation will follow.

# SwiftGUI
This package was written as an addition to 
my Python GUI-package `SwiftGUI`:
https://github.com/CheesecakeTV/SwiftGUI

Since `SwiftGUI_Logging` itself has nothing to to with GUIs, 
it is its own package.

Consider checking out `SwiftGUI` if you want to easily create 
user-interfaces for python.
If you already know the package `PySimpleGUI`, you'll learn the 
basics of`SwiftGUI` with little to no effort.


