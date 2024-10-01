from math import floor
import random
import typing as tp

"""
Tests to see if a number is prime.
>>> is_prime(2)
True
>>> is_prime(11)
True
>>> is_prime(8)
False
"""
def is_prime(n: int) -> bool:
    if not (n > 0):
        raise ValueError("Number must be natural")
    for div in range(2, floor(n ** 0.5) + 1):
        if n % div == 0:
            return False
    return True

"""
Euclid's algorithm for determining the greatest common divisor.
>>> gcd(12, 15)
3
>>> gcd(3, 7)
1
"""
def gcd(a: int, b: int) -> int:
    while a > 0:
        a, b = b % a, a
    return b

"""
Euclid's extended algorithm for finding the multiplicative
inverse of two numbers.
>>> multiplicative_inverse(7, 40)
23
"""
def multiplicative_inverse(e: int, phi: int) -> int:
    if e < 0 or phi < 0:
        raise ValueError("Both numbers must be positive")
    phi_ = phi
    x0, x1 = 1, 0
    y0, y1 = 0, 1

    while e > 0:
        q = phi_ // e 
        phi_, e = e, phi_ % e  
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    if phi_ != 1:
        raise ValueError("e and phi aren't coprime")
    return y0 + (phi if y0 < 0 else 0)

print(multiplicative_inverse(95, 391))

def generate_keypair(p: int, q: int) -> tp.Tuple[tp.Tuple[int, int], tp.Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p < 17 or q < 17:
        raise ValueError("Îne of the numbers is too small, choose numbers greater than 16")
    elif p == q:
        raise ValueError("p and q cannot be equal")

    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    return ((e, n), (d, n))


def encrypt(pk: tp.Tuple[int, int], plaintext: str) -> tp.List[int]:
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk: tp.Tuple[int, int], ciphertext: tp.List[int]) -> str:
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    p = int(input("Enter a prime number (17, 19, 23, etc): "))
    q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(p, q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(lambda x: str(x), encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
