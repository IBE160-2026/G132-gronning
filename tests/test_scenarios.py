"""Uavhengige beregningseksempler og brukervalg i scenarioflyten."""

from pathlib import Path
import unittest

from streamlit.testing.v1 import AppTest
from scenarios import calculate_scenarios

ROOT = Path(__file__).resolve().parents[1]


class ScenarioTest(unittest.TestCase):
    def test_hand_calculation(self):
        result = calculate_scenarios([100, 0, 25.5], 20, 30, 10)
        for actual, expected in zip(result['Høy']['scenario'], [120, 0, 30.6]):
            self.assertAlmostEqual(actual, expected)
        self.assertAlmostEqual(result['Lav']['scenario'][0], 70)
        self.assertAlmostEqual(result['Lav']['planned'][0], 77)
        self.assertAlmostEqual(result['Høy']['margin'][0], 12)
        self.assertAlmostEqual(result['Høy']['planned'][0], 132)
        self.assertEqual(result['Normal']['planned'][1], 0)

    def test_boundaries(self):
        result = calculate_scenarios([100], 0, 100, 0)
        self.assertEqual(result['Lav']['planned'], [0])
        self.assertEqual(result['Høy']['planned'], [100])
        for args in [([-1],), ([float('nan')],), ([],), ([1], -1),
                     ([1], 10, 101), ([1], 10, 10, -1), ([1], 10, 10, float('inf'))]:
            with self.subTest(args=args), self.assertRaises(ValueError):
                calculate_scenarios(*args)

    def test_ui_recomputes_for_choices(self):
        app = AppTest.from_file(str(ROOT / 'app.py')).run()
        self.assertFalse(app.exception)
        for method in app.selectbox(key='scenario_method').options:
            app.selectbox(key='scenario_method').select(method).run()
            app.selectbox(key='selected_scenario').select('Høy')
            app.number_input(key='high_pct').set_value(20.0)
            app.number_input(key='margin_pct').set_value(10.0).run()
            self.assertFalse(app.exception)
            table = app.dataframe[-1].value
            self.assertEqual(len(table), 12)
            self.assertEqual(table['Normal (stykk)'].tolist(), app.dataframe[1].value[method].tolist())
            for base, planned in zip(table['Normal (stykk)'], table['Planlagt mengde (stykk)']):
                self.assertAlmostEqual(planned, base * 1.2 * 1.1)
        app.selectbox[0].select('P05').run()
        self.assertFalse(app.exception)
        future = app.dataframe[1].value
        scenario = app.dataframe[-1].value
        self.assertEqual(scenario['Normal (stykk)'].tolist(), future[method].tolist())
        app.number_input(key='low_pct').set_value(100.0)
        app.selectbox(key='selected_scenario').select('Lav').run()
        self.assertTrue((app.dataframe[-1].value['Planlagt mengde (stykk)'] == 0).all())
