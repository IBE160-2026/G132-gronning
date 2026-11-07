"""Håndregnede kontroller og tidsordnet evaluering."""
import unittest
from forecasting import forecast, evaluate, mae, METHODS


class ForecastTest(unittest.TestCase):
    def test_hand_calculations(self):
        values = [10] * 50 + [20, 30]
        result = forecast(values)
        self.assertEqual(result[METHODS[0]], [17.5] * 12)
        self.assertAlmostEqual(result[METHODS[1]][0], 18.1)
        self.assertEqual(result[METHODS[2]], [10] * 12)
        self.assertEqual(mae([10, 14], [12, 11]), 2.5)

    def test_seasonal_alignment(self):
        result = forecast(list(range(104)))
        self.assertEqual(result[METHODS[2]], list(range(52, 64)))

    def test_no_future_leakage(self):
        values = list(range(104))
        _, before = evaluate(values)
        values[68:] = [999] * 36
        _, after = evaluate(values)
        first = lambda rows: [r['Prognose'] for r in rows if r['Trening til uke'] == 68]
        self.assertEqual(first(before), first(after))

    def test_constant_and_zero(self):
        for value in [0, 7]:
            scores, details = evaluate([value] * 104)
            self.assertEqual(len(scores), 9)
            self.assertEqual(len(details), 108)
            self.assertTrue(all(abs(row['MAE (stykk)']) < 1e-10 for row in scores))

    def test_short_and_invalid(self):
        for values in [[], [1] * 51, [float('nan')] * 52, [-1] * 52]:
            with self.assertRaises(ValueError):
                forecast(values)
        with self.assertRaises(ValueError):
            evaluate([1] * 103)
        with self.assertRaises(ValueError):
            mae([], [])
