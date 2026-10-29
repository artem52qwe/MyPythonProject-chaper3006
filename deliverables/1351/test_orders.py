"""Verify order changes, deletions and exact money calculations."""
import unittest
from decimal import Decimal
from orders import Customer, Product, OrderBook


class OrderTests(unittest.TestCase):
    def setUp(self):
        self.book = OrderBook()
        self.customer = Customer("C1", "Demo")
        self.product = Product("T1", "Torch", Decimal("19.90"))

    def test_lifecycle(self):
        order = self.book.add("O1", self.customer)
        order.set_quantity(self.product, 2)
        self.assertEqual(order.total(), Decimal("39.80"))
        order.set_quantity(self.product, 3)
        self.assertEqual(order.total(), Decimal("59.70"))
        order.set_quantity(self.product, 0)
        self.assertEqual(order.total(), 0)
        self.book.delete("O1")
        self.assertEqual(self.book.report()["orders"], 0)

    def test_paid(self):
        order = self.book.add("O2", self.customer)
        order.set_quantity(self.product, 2)
        order.pay()
        self.assertEqual(self.book.report()["revenue"], "39.80")
        for operation in [lambda: order.pay(),
                          lambda: order.set_quantity(self.product, 4),
                          lambda: self.book.delete("O2")]:
            with self.assertRaises(ValueError):
                operation()

    def test_invalid(self):
        order = self.book.add("O3", self.customer)
        with self.assertRaises(ValueError):
            self.book.add("O3", self.customer)
        with self.assertRaises(ValueError):
            order.pay()
        for quantity in [-1, True, 1.5]:
            with self.assertRaises(ValueError):
                order.set_quantity(self.product, quantity)


if __name__ == "__main__":
    unittest.main()
