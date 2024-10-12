import unittest
import sys
sys.path.append('../../src')
from lab2.caesar import encrypt_caesar, decrypt_caesar



class TestCaesarCipher(unittest.TestCase):

    def test_encrypt_caesar_uppercase(self):
        self.assertEqual(encrypt_caesar("PYTHON"), "SBWKRQ")
        self.assertEqual(encrypt_caesar("HELLO"), "KHOOR")
    
    def test_encrypt_caesar_lowercase(self):
        self.assertEqual(encrypt_caesar("python"), "sbwkrq")
        self.assertEqual(encrypt_caesar("hello"), "khoor")
    
    def test_encrypt_caesar_mixed(self):
        self.assertEqual(encrypt_caesar("Python3.6"), "Sbwkrq3.6")
        self.assertEqual(encrypt_caesar("Hello123"), "Khoor123")
    
    def test_encrypt_caesar_empty(self):
        self.assertEqual(encrypt_caesar(""), "")
    
    def test_encrypt_caesar_custom_shift(self):
        self.assertEqual(encrypt_caesar("PYTHON", shift=5), "UDYMTS")
        self.assertEqual(encrypt_caesar("hello", shift=1), "ifmmp")

    def test_decrypt_caesar_uppercase(self):
        self.assertEqual(decrypt_caesar("SBWKRQ"), "PYTHON")
        self.assertEqual(decrypt_caesar("KHOOR"), "HELLO")
    
    def test_decrypt_caesar_lowercase(self):
        self.assertEqual(decrypt_caesar("sbwkrq"), "python")
        self.assertEqual(decrypt_caesar("khoor"), "hello")
    
    def test_decrypt_caesar_mixed(self):
        self.assertEqual(decrypt_caesar("Sbwkrq3.6"), "Python3.6")
        self.assertEqual(decrypt_caesar("Khoor123"), "Hello123")
    
    def test_decrypt_caesar_empty(self):
        self.assertEqual(decrypt_caesar(""), "")
    
    def test_decrypt_caesar_custom_shift(self):
        self.assertEqual(decrypt_caesar("UDYMTS", shift=5), "PYTHON")
        self.assertEqual(decrypt_caesar("ifmmp", shift=1), "hello")

if __name__ == '__main__':
    unittest.main()
