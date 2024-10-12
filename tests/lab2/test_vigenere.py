import unittest
import sys
sys.path.append('../../src')
from lab2.vigenre import encrypt_vigenere, decrypt_vigenere, check_key


class TestVigenereCipher(unittest.TestCase):
    def test_encrypt_vigenere(self):
        self.assertEqual(encrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(encrypt_vigenere("python", "a"), "python")
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR")
        self.assertEqual(encrypt_vigenere("ATTACKATDAWN", "12LE##M$O37--N LEMON!!!"), "LXFOPVEFRNHR")
        self.assertEqual(encrypt_vigenere("Hello, World!", "KEY"), "Rijvs, Ambpb!")
        self.assertEqual(encrypt_vigenere("abcdefghijklmnopqrstuvwxyz", "ABC"), "acedfhgikjlnmoqprtsuwvxzya")
        self.assertEqual(encrypt_vigenere("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "AbC"), "ACEDFHGIKJLNMOQPRTSUWVXZYA")

    def test_decrypt_vigenere(self):
        self.assertEqual(decrypt_vigenere("PYTHON", "A"), "PYTHON")
        self.assertEqual(decrypt_vigenere("python", "a"), "python")
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "LEMON"), "ATTACKATDAWN")
        self.assertEqual(decrypt_vigenere("LXFOPVEFRNHR", "12LE##M$O37--N LEMON!!!"), "ATTACKATDAWN")
        self.assertEqual(decrypt_vigenere("Rijvs, Ambpb!", "KEY"), "Hello, World!")
        self.assertEqual(decrypt_vigenere("acedfhgikjlnmoqprtsuwvxzya", "ABC"), "abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(decrypt_vigenere("ACEDFHGIKJLNMOQPRTSUWVXZYA", "AbC"), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")


    def test_check_key(self):
        self.assertRaises(ValueError, check_key, "")
        self.assertRaises(ValueError, check_key, "123")
        self.assertEqual(check_key("hello"), "hello")
        self.assertEqual(check_key("HeLLo"), "HeLLo")
        self.assertEqual(check_key("123Hello!!!"), "Hello")

    def test_encrypt_vigenere_edge_cases(self):
        self.assertEqual(encrypt_vigenere("", "A"), "")
        self.assertEqual(encrypt_vigenere(" ", "A"), " ")
        self.assertEqual(encrypt_vigenere("!", "A"), "!")

    def test_decrypt_vigenere_edge_cases(self):
        self.assertEqual(decrypt_vigenere("", "A"), "")
        self.assertEqual(decrypt_vigenere(" ", "A"), " ")
        self.assertEqual(decrypt_vigenere("!", "A"), "!")

if __name__ == "__main__":
    unittest.main()