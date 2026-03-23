
# Basic usage of SwiftGUI_Encryption
This tutorial gives you an overview over the basic, general functionality of `SwiftGUI_Encryption`.

# bytes datatype
(If you already know the `bytes`-type in Python, you can skip this part)

You'll find that many functions of `SwiftGUI_Encryption` take/return data of type `bytes`.

`bytes` is simmilar to a string, but every character represents a single byte.

One way to create `bytes` is adding `b` in front of a normal string:
```py
my_bytes = b"Hello World"
```

You can convert strings to bytes by encoding them:
```py
my_string = "Hello World"
my_bytes = my_string.encode()
```

Simmilarely, decoding bytes gives you a string:
```py
my_bytes = b"Hello World"
my_string = my_bytes.decode()
```

It's also possible to save bytes directly to a file.
Instead of the usual `"w"`-argument in the `open(...)`-function, use `"wb"` (as in "write bytes"):
```py
my_bytes = b"Hello World"

with open("tutorial.txt", "wb") as f:
    f.write(my_bytes)
```
Or the opposite, using `"rb"` ("read bytes"):
```py
with open("tutorial.txt", "rb") as f:
    my_bytes = f.read()
```

# Key-generation
## Random key
Generate a random key like this:
```py
import SwiftGUI_Encryption as sge

key = sge.random_key()
```
If you encrypt with this key, make sure to save it somehow, or you won't be able to decrypt your data in the future...

## Key-derivation
You can't encrypt with a password, you need a key.

To turn a password into a key, use `sge.password_to_key`:
```py
import SwiftGUI_Encryption as sge

password = "password"
key = sge.password_to_key(password)
```
**NOTE THAT THIS IS NOT AS SECURE AS IT COULD BE.**\
This type of key-derivation uses the very good `argon2`-algorithm, but without salt.
It might be vulnerable to pre-calculation-attacks, if the attacker has a supercomputer at hand.

For extra-security, you can increase the calculation (and ram)-cost of the function by increasing the parameter `security_multiplier` (default is `1`):
```py
import SwiftGUI_Encryption as sge

password = "password"
key = sge.password_to_key(password, security_multiplier=50)
```
Why/how this increases security was explained in the previous tutorial.

# Encryption/decryption
All of the following encryption-methods generate a nonce and add it to the encrypted data.

## With a key
Here is an example on how to encrypt/decrypt data with AES-256-GCM:
```py
import SwiftGUI_Encryption as sge

key = sge.random_key()  # You can generate that key from a password, as explained earlier
data = b"Secret hello World"    # You can load this data from a file, as explained earlier

encrypted = sge.encrypt_full(data, key) # This is the secure data you may save to a file
```
Decryption:
```py
decrypted = sge.decrypt_full(encrypted, key)
```

## With a password
To make it as easy for you as possible, there is a function for encryption/decryption that includes key-derivation:
```py
import SwiftGUI_Encryption as sge

password = "Password"   # This is a normal string
data = b"Secret hello World"

encrypted = sge.encrypt_with_password(data, password)
```
Decryption:
```py
decrypted = sge.decrypt_with_password(encrypted, password)
```
**Keep in mind that the key-derivation is slow on purpose.**
It's not designed to be used 5 times in a row.

On the other hand, these functions include salt for the key-derivation, unlike `sge.password_to_key`.
This means, every encrypted data has its own semi-unique key and pre-calculation-attacks are useless.

## Multi-layer-encryption
There are functions to encrypt/decrypt with multiple keys in a row:
```py
import SwiftGUI_Encryption as sge

key1 = sge.random_key()
key2 = sge.random_key()
key3 = sge.random_key()

data = b"Insanely secure hello world"

encrypted = sge.encrypt_multilayer(data, key1, key2, key3)
```
Decryption:
```py
decrypted = sge.decrypt_multilayer(encrypted, key1, key2, key3)
```
Every additional key applies another AES-256-CTR encryption, with the innermost being AES-256-GCM.
You can add as many keys as you want.

As I explained in the previous tutorial, AES-256 is already stupendously secure.
Using multiple layers of encryption does increase the security of something that doesn't need better security.

However, there is a reason I used AES-256-CTR instead of GCM in the outer layers, explained in the function's docstring.
The multilayer-function is more secure than just stacking `sge.encrypt_full`-calls and the encrypted data is shorter.

## Decryption-failure
If the used key is wrong, or the encrypted data was modified, decryption "fails".
It is not possible to differentiate the cases without additional code.

This results in a value-error when decrypting.

If you don't know how to handle such exceptions, here is a quick example:
```py
try:
    sge.decrypt_full(data, key)
except ValueError:
    print("Failure")
else:
    print("Success")
```
This example prints `Failure`, or `Success` depending on if `sge.decrypt_full` was able to properly decrypt the data.


