"""Generate fictional weekly outdoor-product sales; no external dependencies."""
import csv
import json
import math
import random
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ['product_id', 'week_start', 'quantity_sold', 'unit']
PRODUCTS = [
    ('P01', 'Telt, 2 personer', 24, 0.08, 15, 25, 3),
    ('P02', 'Sovepose, 3 sesonger', 35, 0.10, 18, 24, 4),
    ('P03', 'Tursekk, 45 liter', 42, 0.12, 16, 23, 5),
    ('P04', 'Liggeunderlag, oppblaasbart', 30, 0.09, 17, 26, 4),
    ('P05', 'Hodelykt, LED', 48, 0.06, 22, 47, 6),
]


def write_csv(name, fields, rows):
    with (ROOT / name).open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def generate():
    rng = random.Random(132)
    rows = []
    catalog = []
    for pid, name, base, trend, amplitude, peak, noise_sd in PRODUCTS:
        catalog.append(dict(product_id=pid, product_name=name, base_units=base,
                            trend_units_per_week=trend, seasonal_amplitude=amplitude,
                            peak_week_in_cycle=peak, noise_sd=noise_sd))
        for index in range(104):
            mean = base + trend * index + amplitude * math.cos(
                2 * math.pi * ((index + 1) - peak) / 52)
            quantity = max(0, math.floor(mean + rng.gauss(0, noise_sd) + 0.5))
            rows.append(dict(product_id=pid,
                             week_start=(date(2024, 1, 1) + timedelta(weeks=index)).isoformat(),
                             quantity_sold=quantity, unit='units'))
    write_csv('sales_history_clean.csv', FIELDS, rows)
    write_csv('products.csv', list(catalog[0]), catalog)
    # Deliberately invalid fixture; never train on this without reviewing issues.
    corrupted = [dict(row) for row in rows]
    defects = []
    changes = [(10, 'missing_quantity', ''), (135, 'negative_quantity', -5),
               (240, 'outlier', 600), (345, 'invalid_date', '2024-02-30')]
    for index, kind, value in changes:
        row = corrupted[index]
        original = dict(row)
        field = 'week_start' if kind == 'invalid_date' else 'quantity_sold'
        row[field] = value
        defects.append(dict(kind=kind, original=original, changed_field=field, changed_value=value))
    removed = corrupted.pop(430)
    defects.append(dict(kind='missing_week', original=removed))
    corrupted.append(dict(rows[50]))
    defects.append(dict(kind='duplicate', original=dict(rows[50])))
    # Valid zero observation, deliberately distinct from a missing quantity.
    zero = corrupted[60]
    defects.append(dict(kind='valid_zero_for_testing', original=dict(zero), changed_value=0))
    zero['quantity_sold'] = 0
    write_csv('sales_history_validation.csv', FIELDS, corrupted)
    metadata = dict(data_type='synthetic_not_observed_sales', seed=132,
                    weeks_per_product=104, seasonal_period_weeks=52,
                    formula='max(0, floor(base + trend*i + amplitude*cos(2*pi*((i+1)-peak)/52) + Gaussian(0,noise_sd) + 0.5))',
                    products=catalog, validation_cases=defects)
    (ROOT / 'manifest.json').write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    assert len(rows) == 520
    assert len({(r['product_id'], r['week_start']) for r in rows}) == 520
    assert all(isinstance(r['quantity_sold'], int) and r['quantity_sold'] >= 0 for r in rows)
    assert rows[-1]['week_start'] == '2025-12-22'
    print('Validated: 5 products, 104 weeks each, 520 unique clean rows.')
    for product in catalog:
        values = [r['quantity_sold'] for r in rows if r['product_id'] == product['product_id']]
        print(product['product_id'], product['product_name'], 'total=', sum(values), 'min=', min(values), 'max=', max(values))


if __name__ == '__main__':
    generate()
