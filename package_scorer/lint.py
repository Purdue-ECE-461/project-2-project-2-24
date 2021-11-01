import string

SHIFT = 3
CHOICE = input("would you like to encode or decode?")
WORD = input("Please enter text")
LETTERS = string.ascii_letters + string.punctuation + string.digits
ENCODED = ''
if CHOICE == "encode":
    for letter in WORD:
        if letter == ' ':
            ENCODED = ENCODED + ' '
        else:
            x = LETTERS.index(letter) + SHIFT
            ENCODED = ENCODED + LETTERS[x]

if CHOICE == "decode":
    for letter in WORD:
        if letter == ' ':
            ENCODED = ENCODED + ' '
        else:
            x = LETTERS.index(letter) - SHIFT
            ENCODED = ENCODED + LETTERS[x]

print(ENCODED)
