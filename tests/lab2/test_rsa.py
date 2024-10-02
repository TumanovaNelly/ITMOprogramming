import unittest
import sys
sys.path.append('C:/Users/Admin/Desktop/ITMO/Programming/src')
from lab2.rsa import is_prime, gcd, multiplicative_inverse, generate_keypair

class TestNumberTheory(unittest.TestCase):
    def test_is_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(11))
        self.assertFalse(is_prime(8))
        with self.assertRaises(ValueError):
            is_prime(-5)
            is_prime(-1)
            is_prime(0)

    def test_gcd(self):
        self.assertEqual(gcd(12, 15), 3)
        self.assertEqual(gcd(3, 7), 1)
        self.assertEqual(gcd(24, 30), 6)
        with self.assertRaises(ValueError):
            gcd(0, 0)
            gcd(5, 0)
            gcd(-2, 5)
        

    def test_multiplicative_inverse(self):
        self.assertEqual(multiplicative_inverse(7, 40), 23)
        self.assertEqual(multiplicative_inverse(11, 26), 19)
        with self.assertRaises(ValueError):
            multiplicative_inverse(-1, 40)
        with self.assertRaises(ValueError):
            multiplicative_inverse(7, -40)

    def test_generate_keypair(self):
        p, q = 17, 19
        public_key, private_key = generate_keypair(p, q)
        self.assertEqual(len(public_key), 2)
        self.assertEqual(len(private_key), 2)
        self.assertEqual(public_key[1], private_key[1])
        self.assertNotEqual(public_key[0], private_key[0])

        with self.assertRaises(ValueError):
            generate_keypair(4, 6)
        with self.assertRaises(ValueError):
            generate_keypair(17, 17)
        with self.assertRaises(ValueError):
            generate_keypair(16, 17)

if __name__ == "__main__":
    unittest.main()

