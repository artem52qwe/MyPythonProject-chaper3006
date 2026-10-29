"""Call a deliberately leaking or fixed native measurement routine."""
import ctypes
from pathlib import Path
import sys

library = ctypes.CDLL(str(Path(__file__).with_name("native.so")))
library.sample_average.argtypes = [ctypes.c_int]
library.sample_average.restype = ctypes.c_double
leak = int(sys.argv[1])
for _ in range(50):
    value = library.sample_average(leak)
assert abs(value - 24.4765625) < 0.000001, value
print("mean:", value, "native calls:", 50)
