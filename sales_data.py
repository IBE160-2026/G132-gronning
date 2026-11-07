"""Les og kontroller ukentlige salgsdata uten å endre kilden."""

import csv
import io
import re
from datetime import date, timedelta

import pandas as pd

FIELDS = ['product_id', 'week_start', 'quantity_sold', 'unit']


def validate_csv(content: bytes):
    """Returner data, blokkerende feil og varsler. Radnummer inkluderer header."""
    errors, warnings, records = [], [], []
    try:
        reader = csv.DictReader(io.StringIO(content.decode('utf-8-sig')), strict=True)
        if reader.fieldnames != FIELDS:
            return None, ['Kolonnene må være: ' + ','.join(FIELDS)], []
        seen = set()
        for row_number, row in enumerate(reader, 2):
            prefix = f'Rad {row_number}'
            if None in row or any(value is None for value in row.values()):
                errors.append(f'{prefix}: feil antall felt.')
                continue
            pid = row['product_id'].strip()
            raw_date = row['week_start'].strip()
            raw_quantity = row['quantity_sold'].strip()
            row_errors = []
            if not pid:
                row_errors.append('produkt-ID mangler')
            try:
                if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', raw_date):
                    raise ValueError
                week = date.fromisoformat(raw_date)
                if not 1900 <= week.year <= 2100:
                    row_errors.append('dato må være mellom 1900 og 2100')
                if week.weekday() != 0:
                    row_errors.append('ukestart må være mandag')
            except ValueError:
                week = None
                row_errors.append('ugyldig dato; bruk YYYY-MM-DD')
            try:
                if not re.fullmatch(r'[0-9]{1,10}', raw_quantity):
                    raise ValueError
                quantity = int(raw_quantity)
                if quantity > 1_000_000_000:
                    raise ValueError
            except ValueError:
                quantity = None
                row_errors.append('mengde må være et heltall mellom 0 og 1000000000; tom verdi er ikke nullsalg')
            if row['unit'].strip() != 'units':
                row_errors.append('unit må være units (stykk)')
            key = (pid, week)
            if week and key in seen:
                row_errors.append('duplikat av produkt og uke')
            seen.add(key)
            if row_errors:
                errors.append(f'{prefix} ({pid or "ukjent produkt"}, {raw_date}): ' + '; '.join(row_errors))
            else:
                records.append(dict(product_id=pid, week_start=week, quantity_sold=quantity, unit='units', source_row=row_number))
    except (UnicodeError, csv.Error):
        return None, ['Filen må være en gyldig UTF-8 CSV med komma som skilletegn.'], []
    if not records:
        return None, errors + ['Filen inneholder ingen gyldige salgsrader.'], []
    data = pd.DataFrame(records)
    # Kontroller ukedekning og avvik på gyldige rader, også når andre rader feiler.
    for pid, group in data.groupby('product_id'):
        weeks = set(group.week_start)
        current = min(weeks)
        while current <= max(weeks):
            if current not in weeks:
                errors.append(f'Produkt {pid}: mangler uke {current.isoformat()}.')
            current += timedelta(weeks=1)
        quantities = group.quantity_sold
        threshold = quantities.median() + 3 * (quantities.quantile(.75) - quantities.quantile(.25))
        for row in group.loc[quantities > threshold].itertuples():
            warnings.append(f'Rad {row.source_row} ({pid}, {row.week_start}): uvanlig høy mengde {row.quantity_sold}; verdien er beholdt.')
    if errors:
        return None, errors, warnings
    data['week_start'] = pd.to_datetime(data.week_start)
    return data[FIELDS].sort_values(['product_id', 'week_start']), [], warnings
