NUM_LETTERS = ord('z') - ord('a') + 1
""" Encrypts plaintext using a Caesar cipher.
>>> encrypt_caesar("PYTHON")
'SBWKRQ'
>>> encrypt_caesar("python")
'sbwkrq'
>>> encrypt_caesar("Python3.6")
'Sbwkrq3.6'
>>> encrypt_caesar("")
''
"""
def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    ciphertext = []
    for sym in plaintext:
        new_ord = ord(sym)
        if 'a' <= sym <= 'z':
            new_ord = ord('a') + (new_ord - ord('a') + shift) % NUM_LETTERS
        elif 'A' <= sym <= 'Z':
            new_ord = ord('A') + (new_ord - ord('A') + shift) % NUM_LETTERS
        ciphertext.append(chr(new_ord))

    return "".join(ciphertext)


""" Decrypts a ciphertext using a Caesar cipher.
>>> decrypt_caesar("SBWKRQ")
'PYTHON'
>>> decrypt_caesar("sbwkrq")
'python'
>>> decrypt_caesar("Sbwkrq3.6")
'Python3.6'
>>> decrypt_caesar("")
''
"""
def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    plaintext = []
    for sym in ciphertext:
        new_ord = ord(sym)
        if 'a' <= sym <= 'z': 
            new_ord = ord('a') + (new_ord - ord('a') - shift) % NUM_LETTERS
        elif 'A' <= sym <= 'Z':
            new_ord = ord('A') + (new_ord - ord('A') - shift) % NUM_LETTERS
        plaintext.append(chr(new_ord))
    return "".join(plaintext)
