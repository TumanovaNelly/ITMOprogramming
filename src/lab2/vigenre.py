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
    ciphertext = []
    num_letters = ord('z') - ord('a') + 1
    for i in range(len(plaintext)):
        if plaintext[i] >= 'a' and plaintext[i] <= 'z':
            new_ord = ord(plaintext[i]) + ord(keyword[i % len(keyword)]) - ord('a')
            ciphertext.append(chr(new_ord - (num_letters if new_ord > ord('z') else 0)))
        elif plaintext[i] >= 'A' and plaintext[i] <= 'Z':
            new_ord = ord(plaintext[i]) + ord(keyword[i % len(keyword)]) - ord('A')
            ciphertext.append(chr(new_ord - (num_letters if new_ord > ord('Z') else 0)))
        else:
            ciphertext.append(plaintext[i])

    return "".join(ciphertext)
print(encrypt_vigenere("PYTHON", "A"))
print(encrypt_vigenere("python", "a"))
print(encrypt_vigenere("ATTACKATDAWN", "LEMON"))

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
    plaintext = []
    num_letters = ord('z') - ord('a') + 1
    for i in range(len(ciphertext)):
        if ciphertext[i] >= 'a' and ciphertext[i] <= 'z':
            new_ord = ord(ciphertext[i]) - ord(keyword[i % len(keyword)]) + ord('a')
            plaintext.append(chr(new_ord + (num_letters if new_ord < ord('a') else 0)))
        elif ciphertext[i] >= 'A' and ciphertext[i] <= 'Z':
            new_ord = ord(ciphertext[i]) - ord(keyword[i % len(keyword)]) + ord('A')
            plaintext.append(chr(new_ord + (num_letters if new_ord < ord('A') else 0)))
        else:
            plaintext.append(ciphertext[i])
    return "".join(plaintext)

print(decrypt_vigenere("PYTHON", "A"))
print(decrypt_vigenere("python", "a"))
print(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"))