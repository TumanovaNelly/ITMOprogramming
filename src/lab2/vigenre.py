NUM_LETTERS = ord('z') - ord('a') + 1

def check_key(keyword: str) -> str:
    if not keyword:
        raise ValueError("Empty keyword")

    correct_key = "".join(filter(str.isalpha, keyword))
    if not correct_key:
        raise ValueError("keyword must contain at least one letter")

    if correct_key != keyword:
        print(f"Keyword was modified to: {correct_key}")
    return correct_key

"""
Encrypts plaintext using a Vigenere cipher.
>>> encrypt_vigenere("PYTHON", "A")
'PYTHON'
>>> encrypt_vigenere("python", "a")
'python'
>>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
'LXFOPVEFRNHR'
"""
def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    keyword = check_key(keyword)
    ciphertext = []
    for i in range(len(plaintext)):
        new_ord = ord(plaintext[i])
        if 'a' <= plaintext[i] <= 'z':
            new_ord = ord('a') + (new_ord + ord(keyword[i % len(keyword)].lower()) - ord('a') * 2) % NUM_LETTERS
        elif 'A' <= plaintext[i] <= 'Z':
            new_ord = ord('A') + (new_ord + ord(keyword[i % len(keyword)].upper()) - ord('A') * 2) % NUM_LETTERS

        ciphertext.append(chr(new_ord))

    return "".join(ciphertext)

"""
Decrypts a ciphertext using a Vigenere cipher.
>>> decrypt_vigenere("PYTHON", "A")
'PYTHON'
>>> decrypt_vigenere("python", "a")
'python'
>>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
'ATTACKATDAWN'
"""
def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    keyword = check_key(keyword)
    plaintext = []
    for i in range(len(ciphertext)):
        new_ord = ord(ciphertext[i])
        if 'a' <= ciphertext[i] <= 'z':
            new_ord = ord('a') + (new_ord - ord(keyword[i % len(keyword)].lower())) % NUM_LETTERS
        elif 'A' <= ciphertext[i] <= 'Z':
            new_ord = ord('A') + (new_ord - ord(keyword[i % len(keyword)].upper())) % NUM_LETTERS

        plaintext.append(chr(new_ord))
    return "".join(plaintext)