"""Persistens, originalbevaring og begrunnede revisjoner."""
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from io import BytesIO
import unittest

from storage import DatasetStore
from sales_data import validate_csv
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
CSV = b'product_id,week_start,quantity_sold,unit\r\nX,2024-01-01,10,units\r\nX,2024-01-08,0,units\r\n'


class StorageTest(unittest.TestCase):
    def test_reopen_and_immutable_correction_chain(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'datasets.sqlite3'
            store = DatasetStore(path)
            original = store.save_original(CSV, 'Test')
            store = DatasetStore(path)
            self.assertEqual(store.get(original)['csv'], CSV)
            changed = store.correct_quantity(original, 'X', '2024-01-01', 12, 'Feilregistrering')
            second = store.correct_quantity(changed, 'X', '2024-01-08', 3, 'Etterslep')
            store = DatasetStore(path)
            self.assertEqual(store.get(original)['csv'], CSV)
            revision = store.get(changed)
            self.assertEqual(revision['parent_id'], original)
            self.assertEqual((revision['old_quantity'], revision['new_quantity']), (10, 12))
            self.assertEqual(revision['reason'], 'Feilregistrering')
            data, errors, _ = validate_csv(store.get(second)['csv'])
            self.assertFalse(errors)
            self.assertEqual(data.quantity_sold.tolist(), [12, 3])
            self.assertEqual(len(store.list_versions()), 3)

    def test_invalid_saves_are_atomic(self):
        with TemporaryDirectory() as directory:
            store = DatasetStore(Path(directory) / 'datasets.sqlite3')
            with self.assertRaises(ValueError):
                store.save_original(b'bad', 'Feil')
            self.assertFalse(store.list_versions())
            original = store.save_original(CSV, 'Test')
            for quantity, reason in [(12, ''), (-1, 'Feil'), (10, 'Ingen endring'), (1.5, 'Feil')]:
                with self.assertRaises(ValueError):
                    store.correct_quantity(original, 'X', '2024-01-01', quantity, reason)
            self.assertEqual(len(store.list_versions()), 1)

    def test_ui_save_reopen_and_correct(self):
        with TemporaryDirectory() as directory, patch.dict('os.environ', {'FORECAST_DB_PATH': str(Path(directory) / 'test.sqlite3')}):
            app = AppTest.from_file(str(ROOT / 'app.py')).run()
            next(b for b in app.button if b.label == 'Lagre datasettet').click().run()
            self.assertFalse(app.exception)
            self.assertEqual(len(DatasetStore(Path(directory) / 'test.sqlite3').list_versions()), 1)
            next(n for n in app.number_input if n.label == 'Ny mengde (stykk)').set_value(123)
            next(t for t in app.text_input if t.label == 'Begrunnelse for rettelsen').set_value('Kontrollert rettelse')
            next(b for b in app.button if b.label == 'Lagre rettelse som ny versjon').click().run()
            self.assertFalse(app.exception)
            self.assertEqual(next(f.value for f in app.dataframe if 'Antall solgt (stykk)' in f.value).iloc[0, 1], 123)
            reopened = AppTest.from_file(str(ROOT / 'app.py')).run()
            next(b for b in reopened.button if b.label == 'Åpne valgt versjon').click().run()
            self.assertFalse(reopened.exception)
            self.assertEqual(next(f.value for f in reopened.dataframe if 'Antall solgt (stykk)' in f.value).iloc[0, 1], 123)

    def test_uploaded_bytes_and_precedence(self):
        with TemporaryDirectory() as directory, patch.dict('os.environ', {'FORECAST_DB_PATH': str(Path(directory) / 'test.sqlite3')}):
            upload = BytesIO(CSV)
            upload.name = 'original.csv'
            with patch('streamlit.file_uploader', return_value=upload):
                app = AppTest.from_file(str(ROOT / 'app.py')).run()
                next(b for b in app.button if b.label == 'Lagre datasettet').click().run()
                self.assertFalse(app.exception)
                store = DatasetStore(Path(directory) / 'test.sqlite3')
                original = store.list_versions()[0]['id']
                self.assertEqual(store.get(original)['csv'], CSV)
                correction = store.correct_quantity(original, 'X', '2024-01-01', 99, 'Rettelse')
                app.run()
                app.selectbox(key='saved_version').select(correction)
                next(b for b in app.button if b.label == 'Åpne valgt versjon').click().run()
                self.assertEqual(next(f.value for f in app.dataframe if 'Antall solgt (stykk)' in f.value).iloc[0, 1], 10)
            with patch('streamlit.file_uploader', return_value=None):
                app.run()
                self.assertFalse(app.exception)
                self.assertEqual(next(f.value for f in app.dataframe if 'Antall solgt (stykk)' in f.value).iloc[0, 1], 99)
