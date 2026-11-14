"""Kontroller produktvalg mot kildefilen."""

from pathlib import Path
from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

import pandas as pd
from streamlit.testing.v1 import AppTest
from forecasting import evaluate

ROOT = Path(__file__).resolve().parents[1]


class SalesViewTest(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        environment = patch.dict('os.environ', {'FORECAST_DB_PATH': str(Path(directory.name) / 'test.sqlite3')})
        environment.start()
        self.addCleanup(environment.stop)

    def test_each_product_shows_its_history_and_total(self):
        sales = pd.read_csv(ROOT / 'data/synthetic/sales_history_clean.csv')
        app = AppTest.from_file(str(ROOT / 'app.py')).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.selectbox[0].options), 5)
        for product_id in sales.product_id.unique():
            with self.subTest(product=product_id):
                app.selectbox[0].select(product_id).run()
                self.assertFalse(app.exception)
                displayed = next(f.value for f in app.dataframe if 'Antall solgt (stykk)' in f.value)
                expected = sales.loc[sales.product_id == product_id].sort_values('week_start')
                self.assertEqual(len(displayed), 104)
                self.assertTrue(displayed.iloc[:, 0].is_monotonic_increasing)
                self.assertEqual(displayed.iloc[:, 1].tolist(), expected.quantity_sold.tolist())
                total = next(m for m in app.metric if m.label == 'Solgte enheter i perioden')
                self.assertEqual(int(total.value.replace(' ', '')), int(expected.quantity_sold.sum()))
                future = next(f.value for f in app.dataframe if 'Sesongnaiv' in f.value)
                self.assertEqual(len(future), 12)
                self.assertEqual(len(future.columns), 4)
                self.assertEqual(future.iloc[0, 0], pd.Timestamp(expected.week_start.iloc[-1]) + pd.Timedelta(weeks=1))
                scores = next(f.value for f in app.dataframe if list(f.value.columns) == ['Metode', 'MAE (stykk)'])
                expected_scores, _ = evaluate(expected.quantity_sold.tolist())
                self.assertEqual(scores['MAE (stykk)'].tolist(), [s['MAE (stykk)'] for s in expected_scores if s['Holdout']])
                self.assertEqual(len(next(f.value for f in app.dataframe if 'Testperiode' in f.value)), 6)

    def test_short_history_keeps_history_and_explains_missing_results(self):
        sales = pd.read_csv(ROOT / 'data/synthetic/sales_history_clean.csv')
        for weeks in (2, 52):
            with self.subTest(weeks=weeks):
                upload = BytesIO(sales.loc[sales.product_id == 'P01'].head(weeks).to_csv(index=False).encode('utf-8'))
                upload.name = 'kort.csv'
                with patch('streamlit.file_uploader', return_value=upload):
                    app = AppTest.from_file(str(ROOT / 'app.py')).run()
                self.assertFalse(app.exception)
                history = next(f.value for f in app.dataframe if 'Antall solgt (stykk)' in f.value)
                self.assertEqual(len(history), weeks)
                self.assertFalse(any('MAE (stykk)' in f.value for f in app.dataframe))
                messages = [element.value for element in [*app.warning, *app.info]]
                self.assertTrue(any(f'Minst {52 if weeks < 52 else 104}' in message for message in messages))
                plans = [f.value for f in app.dataframe if 'Planlagt mengde (stykk)' in f.value]
                self.assertEqual(len(plans), int(weeks >= 52))
                if weeks < 52:
                    self.assertTrue(any(h.value == 'Salgshistorikk' for h in app.subheader))

    def test_invalid_import_does_not_show_plan(self):
        upload = BytesIO(b'product_id,week_start,quantity_sold,unit\nX,2024-01-01,-1,units\n')
        upload.name = 'feil.csv'
        with patch('streamlit.file_uploader', return_value=upload):
            app = AppTest.from_file(str(ROOT / 'app.py')).run()
        self.assertFalse(app.exception)
        self.assertTrue(any('Importen er avvist' in error.value for error in app.error))
        self.assertFalse(app.dataframe)


if __name__ == '__main__':
    unittest.main()
