"""Planleggingsscenarioer fra punktprognoser; ikke prediksjonsintervaller."""

import math


def calculate_scenarios(forecast_values, high_pct=10.0, low_pct=10.0, margin_pct=0.0):
    """Returner normal/høy/lav og separat marginvirkning uten avrunding."""
    values = [float(value) for value in forecast_values]
    if not values or any(not math.isfinite(value) or value < 0 for value in values):
        raise ValueError('Prognosen må inneholde endelige, ikke-negative verdier.')
    for value, upper in [(high_pct, 1000), (low_pct, 100), (margin_pct, 1000)]:
        if not math.isfinite(value) or not 0 <= value <= upper:
            raise ValueError('Høyjustering og margin må være 0–1000 %, lavjustering 0–100 %.')
    result = {}
    for name, multiplier in [('Normal', 1.0), ('Høy', 1 + high_pct / 100), ('Lav', 1 - low_pct / 100)]:
        quantities = [value * multiplier for value in values]
        additions = [value * margin_pct / 100 for value in quantities]
        result[name] = {
            'scenario': quantities,
            'margin': additions,
            'planned': [value + addition for value, addition in zip(quantities, additions)],
        }
    return result
