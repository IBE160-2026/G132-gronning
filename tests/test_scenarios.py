"""Uavhengige beregningseksempler og brukervalg i scenarioflyten."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from streamlit.testing.v1 import AppTest
import pandas as pd
import streamlit as st
from scenarios import calculate_scenarios

ROOT = Path(__file__).resolve().parents[1]


class ScenarioTest(unittest.TestCase):
    def setUp(self):
        directory = TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        environment = patch.dict('os.environ', {'FORECAST_DB_PATH': str(Path(directory.name) / 'test.sqlite3')})
        environment.start()
        self.addCleanup(environment.stop)

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
            table = next(f.value for f in app.dataframe if 'Planlagt mengde (stykk)' in f.value)
            self.assertEqual(len(table), 12)
            future = next(f.value for f in app.dataframe if 'Sesongnaiv' in f.value)
            self.assertEqual(table['Normal (stykk)'].tolist(), future[method].tolist())
            for base, planned in zip(table['Normal (stykk)'], table['Planlagt mengde (stykk)']):
                self.assertAlmostEqual(planned, base * 1.2 * 1.1)
            total = next(m for m in app.metric if m.label == 'Planlagt mengde · neste 12 uker')
            self.assertAlmostEqual(float(total.value.replace(' stk', '').replace(' ', '').replace(',', '.')), table['Planlagt mengde (stykk)'].sum(), delta=0.051)
        app.selectbox[0].select('P05').run()
        self.assertFalse(app.exception)
        self.assertEqual(app.number_input(key='high_pct').value, 20.0)
        self.assertEqual(app.number_input(key='margin_pct').value, 10.0)
        future = next(f.value for f in app.dataframe if 'Sesongnaiv' in f.value)
        scenario = next(f.value for f in app.dataframe if 'Planlagt mengde (stykk)' in f.value)
        self.assertEqual(scenario['Normal (stykk)'].tolist(), future[method].tolist())
        app.number_input(key='low_pct').set_value(100.0)
        app.selectbox(key='selected_scenario').select('Lav').run()
        self.assertTrue((next(f.value for f in app.dataframe if 'Planlagt mengde (stykk)' in f.value)['Planlagt mengde (stykk)'] == 0).all())

    def test_main_chart_matches_selected_product_and_plan(self):
        app = AppTest.from_file(str(ROOT / 'app.py')).run()
        app.selectbox(key='selected_product').select('P05')
        app.selectbox(key='scenario_method').select('Sesongnaiv')
        app.selectbox(key='selected_scenario').select('Høy')
        app.number_input(key='high_pct').set_value(20.0)
        app.number_input(key='margin_pct').set_value(10.0)
        with patch('streamlit.altair_chart', wraps=st.altair_chart) as render:
            app.run()
        self.assertFalse(app.exception)
        chart = next(call.args[0] for call in render.call_args_list if call.kwargs.get('key') == 'planning_chart')
        chart.to_dict()  # Valider at den lagdelte grafen kan serialiseres av Altair.
        band, lines, boundary = chart.layer
        plan = next(f.value for f in app.dataframe if 'Planlagt mengde (stykk)' in f.value)
        pd.testing.assert_frame_equal(band.data, plan)
        series = lines.data
        history = next(f.value for f in app.dataframe if 'Antall solgt (stykk)' in f.value)
        shown_history = series.loc[series.Serie == 'Historikk']
        self.assertEqual(shown_history.Mengde.tolist(), history['Antall solgt (stykk)'].tail(24).tolist())
        for name, column in [('Valgt prognose', 'Normal (stykk)'), ('Plan med margin', 'Planlagt mengde (stykk)')]:
            shown = series.loc[series.Serie == name]
            self.assertEqual(shown.Mengde.tolist(), plan[column].tolist())
            self.assertEqual(shown.Uke.tolist(), plan.Uke.tolist())
        self.assertTrue(history.Uke.iloc[-1] < boundary.data.Uke.iloc[0] < plan.Uke.iloc[0])
