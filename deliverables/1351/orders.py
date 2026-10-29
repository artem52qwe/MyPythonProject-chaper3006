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
