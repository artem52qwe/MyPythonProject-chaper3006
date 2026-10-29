"""Calculate the greatest common divisor using a structured loop."""


def gcd(a, b):
    """Return a nonnegative GCD; gcd(0, 0) is defined here as 0."""
    if type(a) is not int or type(b) is not int:
        raise TypeError("Integer arguments required")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


if __name__ == "__main__":
    try:
        first, second = map(int, input("Two integers: ").split())
        print(gcd(first, second))
    except ValueError:
        print("Enter exactly two integers")
