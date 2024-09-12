def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    num_letters = ord('z') - ord('a') + 1
    for sim in plaintext:
        if sim >= 'a' and sim <= 'z':
            new_ord = ord(sim) + shift
            ciphertext += chr(new_ord - (num_letters if new_ord > ord('z') else 0))
        elif sim >= 'A' and sim <= 'Z':
            new_ord = ord(sim) + shift
            ciphertext += chr(new_ord - (num_letters if new_ord > ord('Z') else 0))
        else:
            ciphertext += sim
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    NUM_LETTERS = ord('z') - ord('a') + 1
    for sim in ciphertext:
        if sim >= 'a' and sim <= 'z':
            new_ord = ord(sim) - shift
            plaintext += chr(new_ord + (NUM_LETTERS if new_ord < ord('a') else 0))
        elif sim >= 'A' and sim <= 'Z':
            new_ord = ord(sim) - shift
            plaintext += chr(new_ord + (NUM_LETTERS if new_ord < ord('A') else 0))
        else:
            plaintext += sim
    return plaintext

