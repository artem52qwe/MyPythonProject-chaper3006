"""Verify cost arithmetic and validation."""
import unittest
from pricing import batch_cost


class CostTests(unittest.TestCase):
    def test_cost(self):
        self.assertEqual(batch_cost(2750, 4), 11000)

    def test_zero(self):
        self.assertEqual(batch_cost(2750, 0), 0)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            batch_cost(1, -1)
        with self.assertRaises(TypeError):
            batch_cost(True, 2)


if __name__ == "__main__":
    unittest.main()
