"""Exercise real file boundaries and processing edge cases."""
import tempfile
import unittest
from pathlib import Path
from reader import read_values
from processor import transform, save_result


class MeasurementTests(unittest.TestCase):
    def test_transform(self):
        self.assertEqual(transform([12, -3, 12, 8, 25]), [-3, 8, 12, 25])

    def test_empty(self):
        self.assertEqual(transform([]), [])

    def test_invalid_file(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "input.json"
            file.write_text('[true]', encoding="utf-8")
            with self.assertRaises(ValueError):
                read_values(file)
            with self.assertRaises(OSError):
                read_values(Path(directory) / "missing")

    def test_output(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "out.json"
            save_result(file, [3, 7])
            self.assertEqual(file.read_text(), "[3, 7]")


if __name__ == "__main__":
    unittest.main()
