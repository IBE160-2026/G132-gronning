"""Enkle, kontrollerbare prognosemetoder for SCM200-prototypen."""

import math

METHODS = ('Glidende gjennomsnitt', 'Eksponensiell glatting', 'Sesongnaiv')
HORIZON = 12
WINDOW = 4
ALPHA = 0.3
ORIGINS = (68, 80, 92)


def forecast(values, horizon=HORIZON):
    """Prognoser fra ett tidspunkt, uten tilgang til fremtidige observasjoner.

    Gjennomsnitt og enkel glatting gir flate flerstegsprognoser.
    Sesongnaiv gjentar siste 52-ukerssyklus.
    """
    values = [float(value) for value in values]
    if not values or any(not math.isfinite(value) or value < 0 for value in values):
        raise ValueError('Salgshistorikken må inneholde endelige, ikke-negative tall.')
    if len(values) < 52:
        raise ValueError('Minst 52 sammenhengende uker kreves for sammenligning av alle tre metoder.')
    if not isinstance(horizon, int) or horizon < 1:
        raise ValueError('Prognosehorisonten må være et positivt heltall.')
    average = sum(values[-WINDOW:]) / WINDOW
    level = values[0]
    for value in values[1:]:
        level = ALPHA * value + (1 - ALPHA) * level
    return {
        METHODS[0]: [average] * horizon,
        METHODS[1]: [level] * horizon,
        METHODS[2]: [values[-52 + (step % 52)] for step in range(horizon)],
    }


def mae(actual, predicted):
    if len(actual) != len(predicted) or not len(actual):
        raise ValueError('MAE krever like lange, ikke-tomme serier.')
    if any(not math.isfinite(float(v)) for v in list(actual) + list(predicted)):
        raise ValueError('MAE krever endelige tall.')
    return sum(abs(a - p) for a, p in zip(actual, predicted)) / len(actual)


def evaluate(values):
    """Faste, felles 12-ukersvinduer. Holdout rapporteres separat."""
    if len(values) < 104:
        raise ValueError('Minst 104 uker kreves for testvinduene 69–80, 81–92 og 93–104.')
    scores, details = [], []
    for origin in ORIGINS:
        predictions = forecast(values[:origin])
        actual = list(values[origin:origin + HORIZON])
        for method, predicted in predictions.items():
            scores.append({'Metode': method, 'Trening til uke': origin,
                           'Testperiode': f'{origin + 1}–{origin + HORIZON}',
                           'Holdout': origin == 92, 'MAE (stykk)': mae(actual, predicted)})
            for step, (observed, estimate) in enumerate(zip(actual, predicted), 1):
                details.append({'Metode': method, 'Trening til uke': origin,
                                'Uke i historikken': origin + step,
                                'Faktisk': observed, 'Prognose': estimate,
                                'Absolutt feil': abs(observed - estimate)})
    return scores, details
