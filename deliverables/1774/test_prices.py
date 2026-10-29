"""Check business totals and rejected values."""
import unittest
from decimal import Decimal
from prices import invoice


class PriceTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(invoice([Decimal(12), Decimal(8)]), Decimal("20.00"))

    def test_empty(self):
        self.assertEqual(invoice([]), Decimal("0.00"))

    def test_fraction(self):
        self.assertEqual(invoice([Decimal("0.1"), Decimal("0.2")]),
                         Decimal("0.30"))

    def test_invalid(self):
        for value in [Decimal(-1), Decimal("NaN"), Decimal("Infinity")]:
            with self.assertRaises(ValueError):
                invoice([value])
        with self.assertRaises(TypeError):
            invoice([1.2])


if __name__ == "__main__":
    unittest.main()
