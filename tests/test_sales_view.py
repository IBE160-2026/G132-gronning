"""Kontroller produktvalg mot kildefilen."""

from pathlib import Path
import unittest

import pandas as pd
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]


class SalesViewTest(unittest.TestCase):
    def test_each_product_shows_its_history_and_total(self):
        sales = pd.read_csv(ROOT / 'data/synthetic/sales_history_clean.csv')
        app = AppTest.from_file(str(ROOT / 'app.py')).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.selectbox[0].options), 5)
        for product_id in sales.product_id.unique():
            with self.subTest(product=product_id):
                app.selectbox[0].select(product_id).run()
                self.assertFalse(app.exception)
                displayed = app.dataframe[0].value
                expected = sales.loc[sales.product_id == product_id].sort_values('week_start')
                self.assertEqual(len(displayed), 104)
                self.assertTrue(displayed.iloc[:, 0].is_monotonic_increasing)
                self.assertEqual(displayed.iloc[:, 1].tolist(), expected.quantity_sold.tolist())
                self.assertEqual(int(app.metric[0].value.replace(' ', '')), int(expected.quantity_sold.sum()))
                future = app.dataframe[1].value
                self.assertEqual(len(future), 12)
                self.assertEqual(len(future.columns), 4)
                self.assertEqual(future.iloc[0, 0], pd.Timestamp(expected.week_start.iloc[-1]) + pd.Timedelta(weeks=1))
                self.assertEqual(len(app.dataframe[2].value), 6)
                self.assertEqual(len(app.dataframe[3].value), 3)


if __name__ == '__main__':
    unittest.main()
