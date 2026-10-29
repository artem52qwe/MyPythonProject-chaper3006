# ООП: заказы магазина туристического снаряжения

Макаров Артем Александрович · 3427А

Product и Customer — неизменяемые справочники; Order хранит состав и состояние, OrderBook управляет заказами и отчётом. Изменение количества заменяет строку, 0 удаляет её. Черновик можно удалить, оплаченный заказ сохраняется для отчётности. Выручка учитывает только оплаченные заказы. Decimal исключает двоичную погрешность денежных сумм. Хранилище учебное, в памяти одного процесса; сетевые платежи не выполняются.

## orders.py
```python
"""Order registry with immutable products and validated transitions."""
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True)
class Product:
    code: str
    title: str
    price: Decimal

    def __post_init__(self):
        if not self.code or not self.title:
            raise ValueError("Product code and title required")
        if not isinstance(self.price, Decimal):
            raise TypeError("Use Decimal for money")
        if not self.price.is_finite() or self.price < 0:
            raise ValueError("Invalid price")


@dataclass(frozen=True)
class Customer:
    code: str
    name: str


@dataclass
class Order:
    code: str
    customer: Customer
    lines: dict = field(default_factory=dict)
    paid: bool = False

    def set_quantity(self, product, quantity):
        """Create/update a line; zero deletes it before payment."""
        if self.paid:
            raise ValueError("Paid order is immutable")
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Quantity must be a nonnegative integer")
        if quantity == 0:
            self.lines.pop(product.code, None)
        else:
            self.lines[product.code] = (product, quantity)

    def total(self):
        return sum((p.price * q for p, q in self.lines.values()), Decimal(0))

    def pay(self):
        if self.paid or not self.lines:
            raise ValueError("Order must be unpaid and nonempty")
        self.paid = True


class OrderBook:
    """Manage orders and count paid sales separately from drafts."""

    def __init__(self):
        self.orders = {}

    def add(self, code, customer):
        if not code or code in self.orders:
            raise ValueError("Unique nonempty order code required")
        order = Order(code, customer)
        self.orders[code] = order
        return order

    def delete(self, code):
        if self.orders[code].paid:
            raise ValueError("Paid orders stay in sales history")
        del self.orders[code]

    def report(self):
        paid = [order for order in self.orders.values() if order.paid]
        return {"orders": len(self.orders), "paid": len(paid),
                "revenue": str(sum((o.total() for o in paid), Decimal(0)))}


if __name__ == "__main__":
    book = OrderBook()
    order = book.add("R-301", Customer("C-1", "Учебный клиент"))
    order.set_quantity(Product("P-1", "Фонарь", Decimal("450.50")), 2)
    order.pay()
    print(book.report())
```

## test_orders.py
```python
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
```

## Проверка
```text
test_invalid (test_orders.OrderTests.test_invalid) ... ok
test_lifecycle (test_orders.OrderTests.test_lifecycle) ... ok
test_paid (test_orders.OrderTests.test_paid) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
{'orders': 1, 'paid': 1, 'revenue': '901.00'}

flake8: 0 замечаний.
```
