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
    num_letters = ord('z') - ord('a') + 1
    for sym in plaintext:
        if sym >= 'a' and sym <= 'z':
            new_ord = ord(sym) + shift
            ciphertext.append(chr(new_ord - (num_letters if new_ord > ord('z') else 0)))
        elif sym >= 'A' and sym <= 'Z':
            new_ord = ord(sym) + shift
            ciphertext.append(chr(new_ord - (num_letters if new_ord > ord('Z') else 0)))
        else:
            ciphertext.append(sym)
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
    NUM_LETTERS = ord('z') - ord('a') + 1
    for sym in ciphertext:
        if sym >= 'a' and sym <= 'z':
            new_ord = ord(sym) - shift
            plaintext.append(chr(new_ord + (NUM_LETTERS if new_ord < ord('a') else 0)))
        elif sym >= 'A' and sym <= 'Z':
            new_ord = ord(sym) - shift
            plaintext.append(chr(new_ord + (NUM_LETTERS if new_ord < ord('A') else 0)))
        else:
            plaintext.append(sym)
    return "".join(plaintext)

