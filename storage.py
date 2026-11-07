"""Uforanderlige datasettversjoner i lokal SQLite."""
from contextlib import closing
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from uuid import uuid4

from sales_data import validate_csv


class DatasetStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self.connect()) as db, db:
            db.execute('''CREATE TABLE IF NOT EXISTS datasets (
                id TEXT PRIMARY KEY, parent_id TEXT REFERENCES datasets(id),
                name TEXT NOT NULL, created_at TEXT NOT NULL,
                csv BLOB NOT NULL, reason TEXT NOT NULL,
                product_id TEXT, week_start TEXT, old_quantity INTEGER, new_quantity INTEGER
            )''')

    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys = ON')
        return db

    def list_versions(self):
        with closing(self.connect()) as db:
            return [dict(row) for row in db.execute(
                'SELECT id,parent_id,name,created_at,reason,product_id,week_start,old_quantity,new_quantity FROM datasets ORDER BY created_at DESC,id')]

    def get(self, version_id):
        with closing(self.connect()) as db:
            row = db.execute('SELECT * FROM datasets WHERE id=?', (version_id,)).fetchone()
        if row is None:
            raise ValueError('Datasettversjonen finnes ikke.')
        return dict(row)

    def _insert(self, content, name, parent=None, reason='', change=(None, None, None, None)):
        _, errors, _ = validate_csv(content)
        if errors:
            raise ValueError('Datasettet kan ikke lagres: ' + '; '.join(errors))
        version_id = str(uuid4())
        with closing(self.connect()) as db, db:
            db.execute('INSERT INTO datasets VALUES (?,?,?,?,?,?,?,?,?,?)',
                       (version_id, parent, name, datetime.now(timezone.utc).isoformat(),
                        content, reason, *change))
        return version_id

    def save_original(self, content, name):
        if not name.strip():
            raise ValueError('Datasettet må ha et navn.')
        return self._insert(bytes(content), name.strip())

    def correct_quantity(self, parent_id, product_id, week_start, quantity, reason):
        if not reason.strip():
            raise ValueError('Rettelsen må ha en begrunnelse.')
        if isinstance(quantity, bool) or not isinstance(quantity, int) or not 0 <= quantity <= 1_000_000_000:
            raise ValueError('Mengden må være et heltall fra 0 til 1000000000.')
        parent = self.get(parent_id)
        data, errors, _ = validate_csv(parent['csv'])
        if errors:
            raise ValueError('Lagret datasett kan ikke valideres.')
        mask = (data.product_id == product_id) & (data.week_start.dt.strftime('%Y-%m-%d') == week_start)
        if mask.sum() != 1:
            raise ValueError('Velg én eksisterende produktuke.')
        old = int(data.loc[mask, 'quantity_sold'].iloc[0])
        if old == quantity:
            raise ValueError('Ny mengde er lik eksisterende mengde.')
        data.loc[mask, 'quantity_sold'] = quantity
        content = data.to_csv(index=False, date_format='%Y-%m-%d', lineterminator='\n').encode('utf-8')
        return self._insert(content, parent['name'], parent_id, reason.strip(),
                            (product_id, week_start, old, quantity))
