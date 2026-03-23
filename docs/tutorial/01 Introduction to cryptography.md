
# Getting started
`SwiftGUI_Encryption` is a small package for everyone who wants to encrypt data, but doesn't know a lot about it.

In cryptography, there are many things you can do wrong.
Even a tiny error can make your encryption more vulnerable, or even render it useless.

That's why `SwiftGUI_Encryption` gives you pre-made encryption-schemes, so you don't need to worry about all that complicated stuff in the background.

However, this means less flexibility and a less-optimized code.
So, maybe don't use it at a professional level, even though it would work pretty well.

# You can skip this tutorial
`SwiftGUI_Encryption` is supposed to be useable without too much cryptography-knowledge.

However, just this little bit of knowledge will prevent most errors you might make.

# Basic rules of cryptography
## Always expect a skilled attacker
Can you think of any realistic way an attacker could possibly break into your encrypted data?

If so, you did something wrong.

I don't know what exactly you'd like to keep secure, but it's a good practice to just assume the attacker is your own government (And yes, I know how suspicious that makes me look).

They have access to supercomputers and possible quantum-computers.
I'll talk more about this later.

They could also raid your house.\
Is your harddrive encrypted?
Probably not.\
What if the raid happens while your PC is running?
They sure aren't gonna shut it down for you.

Sure, you probably aren't hiding anything from the police (neither am I, please don't raid my house), but even non-programmers could easily bypass a windows-login on a non-encrypted harddrive.

It doesn't hurt to be extra-secure.

## Always expect the attacker to have access to your program-code (Security by obscurity)
...the most common and most devastating rookie-mistake.

"Security by obscurity" describes a system that is "secure", because people don't know how it works.

You might be old enough to remember DVD-copy-protection.
Some DVDs were encrypted, so that noone can copy its movie.

Unfortunatly, every DVD-player had to be able to decrypt the movie in order to play it.

So, how would your DVD-player be able to decrypt it, but not you?\
How the encryption works was kept secret by NDAs.
Everyone who spilled the secret could have gotten sued.

Needless to say, this was a very bad idea.
How to decrypt these DVDs was leaked very quickly, rendering the copy-protection useless.

Long story short, **always expect an attacker to have all of your program-code!**\
That is the first and most important rule!

An encryption is only secure if you couldn't break it yourself.

## Don't invent new encryptions
Modern encryption-algorithms have all been open source for quite a long time.
Many very smart people reviewed them and (hopefully) found all possible security-issues.

**You will not be able to top such a level of security by yourself**, you are not the main character.

Stick to established algorithms and concepts, even if it doesn't seem as cool.

# Basic concepts of cryptography
This is important to use the python-package correctly.

Incorrect usage might mean less security.

## key-length and brute-force-attacks
One of the best modern encryption-algorithm is AES-256.\
**There are no known vulnerabilities to that algorithm** (at least for AES-256-GCM).

The only thing you can do to break it is to try different keys until you guess the correct one.

This is called "brute-force-attack".

The only thing you can do against such an attack is to increase the number of possible keys.

The total number of combinations is equal to the number of possible characters to the power of the character-count.

Example: "Windows Hello" lets you log into your account with a 4-digit number-code.
You have 10 different possible characters (0-9) and 4 characters in total, meaning $10^4 = 10,000$ different combinations.
Most home-PCs could try all of these in about a second.

Let's say you also include letters (capital and non-capital).
Now, each character can have 26 lowercase letters, 26 uppercase letters and 10 digits, totaling to 62 possible characters.\
That means, there are $62^4 = 14,776,336$ different combinations.

However, if your PC can try 10000 combinations per second, it still only takes around 4 hours to try all of them.

The maximum key-length of AES-256 is 256 bit, hence the name.
Each bit can be either 0 or 1, so 2 combinations per character.\
That means, the total number of combinations is $2^{256} = 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457,584,007,913,129,639,936$.

It would take your PC $366,922,989,192,195,222,424,800,903,141,488,765,764,310,173,965,470,422,940,319,219,712$ YEARS to try all possible combinations.

Quantum-computers act on AES as if the key-length was cut in half, so AES-256 becomes as vulnerable as AES-128.
Don't worry, still takes longer to break than the universe exists right now, even for supercomputers.

Long story short, to our current understanding, AES-256 is invulnerable.\
If anyone tries to break your security, they are going to attack somewhere else.

## key derivation
Having a key-length of 256 bit is pretty cool, but that doesn't do jack, if your actual password is only 4 characters long.

Including uppercase, lowercase and digits, your password would need to be around 43 characters long for the same level of security.
Not quite realistic.

Here is where key-derivation comes in handy.
Key-derivation is the process of generating a key from a password.
(Note that a "key" is actually used in encrypting/decrypting data, while a "password" is the thing you know yourself.)

Instead of adding more combinations (making the password longer), we simply increase how long it takes to try each password.

Remember that puny 4-digit number-code you could break in about a second before?
If every test took one second, you'd need 3 hours to try out all combinations.\
Still not good, but a lot better.

We can achieve this by adding a lot of "unnecessary" calculations to the key-derivation-algorithm.

Sure, every time you log in, all of these calculations need to be done, but the attacker has to do them for every (most) possible password.
One additional second for you means 10000 additional seconds for the attacker (in case of the 4-digit number-code).

`SwiftGUI_Encryption` relies on the `argon2` key-derivation algorithm, which is state-of-the-art.
The algorithm even allows you to specify, how heavy it is on cpu- and ram-usage.

Also, if used correctly, you can create many different keys from a single password.
So, even if a key gets broken, the others are still intact.

## Cryptographic hashing
Hashing is a concept used in many different fields, so let's only focus on cryptographic hashing.

Let's say, you run a server with different user-accounts.
Each account has a username and a password.

How would you save these passwords?\
If you just put them in a database and someone manages to break into that database, all of these passwords are out in the open.
Also, users might not like it, if you know their actual password.

So instead, "hash" the password and save that value.

A cryptographic hash-function is an algorithm which takes some input and converts it to its hash-value.

The trick is that this function only works one-way.
You can't convert the hash-value back to its input.

That means, an attacker can't use the hash-value to recreate the used passwords.

To check if the user entered the correct password, just calculate its hash-value and compare it to the saved one.
(Zero knowledge-testing is a better alternative for servers)

## Pre-calculation-attacks
One way to attack hash-values is to calculate all possible hashes.
Then, you could just look up which input generates the stolen hash-value.

This makes hashing quite unsecure.

However, the pre-calculated hash-values only work for a single hash-algorithm.\
So, why not just use a different hash-algorithm for every hash-value?

We can do this by adding some random "text" to the input before hashing it.
Now, the output of the hash-function depends on the input AND the random text.

That random text holds no secrets, so it can be saved unsecure.

In practice, this is done a bit more complicated.
The random text (number) isn't just added to the input, but integrated into the hashing-algorithm in different places.

That random number is called "salt" for most algorithms.
Some even allow a second random number called "pepper", to avoid some very specific attacks on the hash-value.

# AES-256
Finally, let's talk about encryption.

However, AES is very complex, so I won't cover how the actual algorithm works here. 

AES has different "modes" of operations, some more, some less relevant.

Each mode has its advantages and disadvantages, but you'll probably only use GCM, or CTR.

Theoretically, these modes work for all symmetric block-encryption-algorithms, but only AES is relevant for us.

## ECB-Mode
ECB is "pure" AES.
You take some data and a key, plug both into the function and voila, you'll get your encrypted data.

But sadly, it's not that simple.

What do you think happens, when you encrypt the same data with the same key again?\
You'll get the same output.

In ECB-Mode, the same input always generates the same output (with the same key, of course).

This is a lot worse than it sounds, because AES is a block-encryption.
The input-data is divided into blocks, that are encrypted separately.

So, if you encrypt an image that is mostly black/transparent, all black area will have the same encrypted value.

This image shows the problem it very well: https://www.researchgate.net/figure/An-example-of-image-encrypted-using-ECB-mode_fig1_356357239

So, don't use ECB.

## CTR-Mode
Remember how we talked about a simmilar problem with hashing before.
What did we do so the same input doesn't always generate the same hash-value?\
Correct, we added "salt".

It's basically the same here.\
We pass a pseudo-random number to every encryption-block, changing its output.
Pseudo-random, because the number for the next block is calculated from the current block.

The first block receives an actual random number called "nonce" ("number used once").

Like with hashing, the nonce doesn't need to be kept secret.

## GCM-Mode
This is the most popular mode, for a good reason.

It works very simmilar to CTR-Mode, but has a builtin "tampering-detection".

If anyone modifies the encrypted data, any other mode would just decrypt it wrong.
GCM-Mode lets you test for modifications.

