"""Kontroller at import ikke skjuler ugyldige salgstall."""

from pathlib import Path
import unittest
from sales_data import validate_csv

ROOT = Path(__file__).resolve().parents[1]
HEADER = 'product_id,week_start,quantity_sold,unit\n'


class ImportTest(unittest.TestCase):
    def test_bundled_files(self):
        clean, errors, _ = validate_csv((ROOT / 'data/synthetic/sales_history_clean.csv').read_bytes())
        self.assertFalse(errors)
        self.assertEqual(len(clean), 520)
        dirty, errors, warnings = validate_csv((ROOT / 'data/synthetic/sales_history_validation.csv').read_bytes())
        self.assertIsNone(dirty)
        self.assertTrue(any('duplikat' in error for error in errors))
        self.assertTrue(any('ugyldig dato' in error for error in errors))
        self.assertTrue(any('mangler uke' in error for error in errors))
        self.assertTrue(warnings)

    def test_zero_is_valid(self):
        data, errors, _ = validate_csv((HEADER + 'X,2024-01-01,0,units\n').encode())
        self.assertFalse(errors)
        self.assertEqual(data.quantity_sold.iloc[0], 0)

    def test_invalid_files_are_rejected(self):
        for content in ['', HEADER, 'wrong\n', HEADER + 'X,2024-01-01,,units\n',
                        HEADER + 'X,2024-01-01,-1,units\n', HEADER + 'X,2024-01-01,nan,units\n',
                        HEADER + 'X,2024-01-01,0.99999999999999999,units\n',
                        HEADER + 'X,2024-01-02,2,units\n', HEADER + 'X,2024-01-01,2,kg\n']:
            with self.subTest(content=content):
                data, errors, _ = validate_csv(content.encode())
                self.assertIsNone(data)
                self.assertTrue(errors)
