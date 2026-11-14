"""Startside for prognoseprototypen."""

from pathlib import Path
import os
import sqlite3

import altair as alt
import pandas as pd
import streamlit as st
from sales_data import validate_csv
from forecasting import METHODS, forecast, evaluate
from scenarios import calculate_scenarios
from storage import DatasetStore

st.set_page_config(page_title="Friluft – etterspørselsplanlegging", page_icon="🏕️", layout="wide")

st.title("Fra salgshistorikk til plan")
st.write("En prototype for prognoser og planlegging av salg av friluftsprodukter.")
st.info("Appen er under utvikling. De medfølgende eksempeldataene er syntetiske øvingsdata.")
data_directory = Path(__file__).resolve().parent / "data" / "synthetic"
try:
    products = pd.read_csv(data_directory / "products.csv")
    sales = pd.read_csv(data_directory / "sales_history_clean.csv", parse_dates=["week_start"])
except (OSError, ValueError, pd.errors.ParserError) as error:
    st.error("Kunne ikke lese eksempeldataene. Kontroller filene i data/synthetic/.")
    st.stop()

product_names = products.set_index("product_id")["product_name"].to_dict()
try:
    store = DatasetStore(os.environ.get("FORECAST_DB_PATH", str(data_directory.parent / "local" / "datasets.sqlite3")))
except (OSError, sqlite3.Error):
    st.error("Kunne ikke åpne lokal database. Kontroller skrivetilgang til data/local/.")
    st.stop()
choices = st.container()
data_panel = st.expander("Datagrunnlag og import – lagre, åpne og rette datasett")
with data_panel:
    uploaded = st.file_uploader("Last opp salgshistorikk (CSV)", type=["csv"])
    st.caption("UTF-8, komma, kolonner: product_id,week_start,quantity_sold,unit. Ukestart mandag; unit = units. Nullsalg skrives 0.")
if uploaded is not None:
    source_bytes = uploaded.getvalue()
    source_name = uploaded.name
    active_id = None
    sales, errors, warnings = validate_csv(uploaded.getvalue())
    for warning in warnings:
        st.warning(warning)
    if errors:
        st.error("Importen er avvist. Rett feilene i originalfilen og last opp på nytt. Ingen rader er importert.")
        for error in errors:
            st.error(error)
        st.stop()
    st.success("CSV er kontrollert. Trykk «Lagre datasettet» nedenfor for permanent lagring. Opplasting overstyrer valgt lagret versjon til filen fjernes.")
    product_names = {pid: product_names.get(pid, pid) for pid in sales.product_id.unique()}
else:
    active_id = st.session_state.get("active_dataset_id")
    if active_id:
        try:
            active = store.get(active_id)
            source_bytes, source_name = active['csv'], active['name']
            sales, errors, warnings = validate_csv(source_bytes)
            if errors:
                raise ValueError("Lagret datasett har valideringsfeil.")
            for warning in warnings:
                st.warning(warning)
            product_names = {pid: product_names.get(pid, pid) for pid in sales.product_id.unique()}
            st.caption(f"Viser lagret versjon {active_id} · {source_name}")
        except (ValueError, sqlite3.Error):
            st.error("Kunne ikke åpne valgt datasett. Velg eksempeldata på nytt.")
            if st.button("Bruk eksempeldata"):
                st.session_state.pop("active_dataset_id", None)
                st.rerun()
            st.stop()
    else:
        source_bytes = (data_directory / "sales_history_clean.csv").read_bytes()
        source_name = "Syntetiske eksempeldata"
        st.caption("Viser medfølgende syntetiske eksempeldata.")
with choices:
    product_column, method_column = st.columns(2)
    with product_column:
        selected_product = st.selectbox(
            "Velg produkt", options=list(product_names), format_func=product_names.get,
            key="selected_product",
        )
    with method_column:
        method = st.selectbox("Prognosemetode", METHODS, key="scenario_method")
history = sales.loc[sales["product_id"] == selected_product].sort_values("week_start")

with data_panel:
    st.caption("Lokal lagring på denne maskinen. Ingen innlogging ennå. Originalfil og tidligere versjoner beholdes; rettelser gjelder mengde på eksisterende produktuker. Strukturelle importfeil må rettes i CSV før lagring.")
    try:
        if active_id is None and st.button("Lagre datasettet"):
            saved_id = store.save_original(source_bytes, source_name)
            st.session_state["active_dataset_id"] = saved_id
            st.success(f"Lagret med ID {saved_id}. Fjern eventuell opplasting for å åpne lagret versjon.")
            if uploaded is None:
                st.rerun()
        versions = store.list_versions()
        if versions:
            version_names = {v['id']: f"{v['name']} · {v['created_at']} · {v['id']}" for v in versions}
            chosen = st.selectbox("Lagrede versjoner", list(version_names), format_func=version_names.get, key="saved_version")
            if st.button("Åpne valgt versjon"):
                st.session_state["active_dataset_id"] = chosen
                if uploaded is not None:
                    st.info("Fjern opplastet fil for å vise valgt lagret versjon.")
                else:
                    st.rerun()
        if st.button("Vis eksempeldata"):
            st.session_state.pop("active_dataset_id", None)
            if uploaded is not None:
                st.info("Fjern opplastet fil for å vise eksempeldata.")
            else:
                st.rerun()
        if active_id:
            st.download_button("Last ned denne versjonens CSV", source_bytes, file_name=f"dataset-{active_id}.csv", mime="text/csv")
            week = st.selectbox("Produktuke som skal rettes", history.week_start.dt.strftime('%Y-%m-%d').tolist(), key=f"correction_week_{active_id}_{selected_product}")
            old_quantity = int(history.loc[history.week_start.dt.strftime('%Y-%m-%d') == week, 'quantity_sold'].iloc[0])
            with st.form(f"correction_{active_id}_{selected_product}_{week}"):
                quantity = st.number_input("Ny mengde (stykk)", min_value=0, max_value=1_000_000_000, value=old_quantity, step=1)
                reason = st.text_input("Begrunnelse for rettelsen")
                if st.form_submit_button("Lagre rettelse som ny versjon"):
                    corrected_id = store.correct_quantity(active_id, selected_product, week, quantity, reason)
                    st.session_state["active_dataset_id"] = corrected_id
                    st.rerun()
        if versions:
            st.write("Versjonshistorikk (tidspunkt i UTC)")
            st.json(versions, expanded=False)
    except (ValueError, sqlite3.Error, OSError) as error:
        st.error(f"Lagring mislyktes: {error}")

if history.empty:
    st.warning("Ingen salgshistorikk finnes for dette produktet.")
    st.stop()

# Opprett grafplassen først; kontrollene til høyre bestemmer innholdet.
graph_column, settings_column = st.columns([2, 1], gap="large")
try:
    forecast_values = forecast(history.quantity_sold.tolist())
except ValueError as error:
    with graph_column:
        st.subheader("Salgshistorikk")
        st.warning(str(error))
        st.caption("Tilgjengelig salgshistorikk · inntil siste 24 uker · stykk. Hele historikken finnes nedenfor.")
        st.line_chart(history.tail(24), x="week_start", y="quantity_sold", x_label="Uke", y_label="Antall solgt (stykk)")
else:
    future_dates = pd.date_range(history.week_start.iloc[-1] + pd.Timedelta(weeks=1), periods=12, freq="7D")
    future = pd.DataFrame(forecast_values, index=future_dates)
    future.index.name = "Uke"
    with settings_column:
        st.subheader("Juster planen")
        selected_scenario = st.selectbox("Scenario for planlagt mengde", ["Normal", "Høy", "Lav"], key="selected_scenario")
        high_pct = st.number_input("Høy etterspørsel – økning (%)", min_value=0.0, max_value=1000.0, value=10.0, step=1.0, key="high_pct")
        low_pct = st.number_input("Lav etterspørsel – reduksjon (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0, key="low_pct")
        margin_pct = st.number_input("Separat sikkerhetsmargin (%)", min_value=0.0, max_value=1000.0, value=0.0, step=1.0, key="margin_pct")
        st.caption("Prosentvalgene beholdes ved produktbytte. Planen er et utkast uten godkjenning eller permanent planlagring.")
    scenarios = calculate_scenarios(forecast_values[method], high_pct, low_pct, margin_pct)
    scenario_table = pd.DataFrame({
        "Uke": future_dates,
        "Normal (stykk)": scenarios["Normal"]["scenario"],
        "Høy (stykk)": scenarios["Høy"]["scenario"],
        "Lav (stykk)": scenarios["Lav"]["scenario"],
        "Valgt scenario (stykk)": scenarios[selected_scenario]["scenario"],
        "Sikkerhetsmargin (stykk)": scenarios[selected_scenario]["margin"],
        "Planlagt mengde (stykk)": scenarios[selected_scenario]["planned"],
    })
    with settings_column:
        total = scenario_table["Planlagt mengde (stykk)"].sum()
        st.metric("Planlagt mengde · neste 12 uker", f"{total:,.1f}".replace(",", " ").replace(".", ",") + " stk")
        st.caption("Total og tabell vises med én desimal. Summen beregnes før visningsavrunding; underliggende verdier beholdes.")

    with graph_column:
        st.subheader("Salg og plan i samme graf")
        st.caption("Siste 24 historikkuker og neste 12 prognoseuker · stykk. Prognosen starter uken etter siste salg, ikke etter dagens dato.")
        past = history.tail(24).rename(columns={"week_start": "Uke", "quantity_sold": "Mengde"})[["Uke", "Mengde"]].assign(Serie="Historikk")
        estimates = pd.DataFrame({"Uke": future_dates, "Valgt prognose": forecast_values[method], "Plan med margin": scenarios[selected_scenario]["planned"]})
        lines = pd.concat([past, estimates.melt("Uke", var_name="Serie", value_name="Mengde")], ignore_index=True)
        series = ["Historikk", "Valgt prognose", "Plan med margin"]
        line_chart = alt.Chart(lines).mark_line(point=True).encode(
            x=alt.X("Uke:T", title="Uke", axis=alt.Axis(format="%d.%m.%Y", labelOverlap=True)),
            y=alt.Y("Mengde:Q", title="Antall (stykk)", scale=alt.Scale(zero=True)),
            color=alt.Color("Serie:N", scale=alt.Scale(domain=series, range=["#89978f", "#508ee3", "#28a875"]), legend=alt.Legend(orient="top", title=None)),
            strokeDash=alt.StrokeDash("Serie:N", scale=alt.Scale(domain=series, range=[[1, 0], [6, 4], [2, 2]]), legend=None),
            tooltip=[alt.Tooltip("Uke:T", format="%d.%m.%Y"), "Serie:N", alt.Tooltip("Mengde:Q", format=".2f")],
        )
        band = alt.Chart(scenario_table).mark_area(color="#d89342", opacity=0.18).encode(
            x="Uke:T", y=alt.Y("Lav (stykk):Q", title="Antall (stykk)"), y2="Høy (stykk):Q",
            tooltip=[alt.Tooltip("Uke:T", format="%d.%m.%Y"), "Lav (stykk):Q", "Høy (stykk):Q"],
        )
        boundary = alt.Chart(pd.DataFrame({"Uke": [history.week_start.iloc[-1] + pd.Timedelta(days=3.5)]})).mark_rule(strokeDash=[4, 4], color="#89978f").encode(x="Uke:T")
        st.altair_chart((band + line_chart + boundary).properties(height=340), width="stretch", key="planning_chart")
        st.caption(f"{product_names[selected_product]} · {method} · {selected_scenario}. Høy: +{high_pct:g} %, lav: −{low_pct:g} %, separat margin: +{margin_pct:g} %.")
        st.caption("Det oransje området viser lav–høy scenario uten margin: planleggingsantakelser, ikke statistiske intervaller eller sikkerhetslager. Linjemønstrene skiller historikk, prognose og plan også uten farge.")
        if scenario_table["Normal (stykk)"].equals(scenario_table["Planlagt mengde (stykk)"]):
            st.caption("Valgt prognose og plan har identiske verdier og ligger oppå hverandre i grafen.")

    score_column, table_column = st.columns(2, gap="large")
    scores = details = None
    with score_column:
        st.subheader("Hvilken metode bommer minst?")
        st.caption("MAE · separat holdout (historikkens uke 93–104) · stykk · lavere er bedre. Ingen automatisk metodevalg.")
        st.caption("Holdout er sluttkontroll. Bruk utviklingsvinduene under «Alle beregninger og testvinduer» til metodevurdering; endringer etter holdout krever et nytt urørt testsett.")
        try:
            scores, details = evaluate(history.quantity_sold.tolist())
        except ValueError as error:
            st.info(str(error))
        else:
            score_table = pd.DataFrame(scores)
            holdout = score_table.loc[score_table.Holdout, ["Metode", "MAE (stykk)"]]
            bars = alt.Chart(holdout).mark_bar().encode(
                x=alt.X("MAE (stykk):Q", title="MAE (stykk)", scale=alt.Scale(zero=True)),
                y=alt.Y("Metode:N", sort=None, title=None),
                tooltip=["Metode:N", alt.Tooltip("MAE (stykk):Q", format=".2f")],
            )
            st.altair_chart(bars.properties(height=160), width="stretch")
            st.dataframe(holdout, hide_index=True, key="holdout_scores")
    with table_column:
        st.subheader("Planens 12 uker")
        st.caption("Normal er valgt prognose. Tabellen viser scenario, separat margin og planlagt mengde uten heltallsavrunding.")
        st.dataframe(scenario_table, hide_index=True, key="plan_table", column_config={
            "Uke": st.column_config.DateColumn(format="DD.MM.YYYY"),
            **{name: st.column_config.NumberColumn(format="%.1f") for name in scenario_table.columns if name != "Uke"},
        })

    with st.expander("Alle beregninger og testvinduer"):
        st.write("Glidende gjennomsnitt: siste 4 uker. Enkel eksponensiell glatting: α = 0,3, startnivå = første salgstall. Sesongnaiv: samme uke i forrige 52-ukerssyklus.")
        st.caption("Faste pedagogiske parametere, ikke optimalisert på testdata. Glidende gjennomsnitt og enkel glatting gir flate 12-ukersprognoser og modellerer ikke sesong eller trend eksplisitt.")
        st.markdown("Faglig grunnlag: [SCM200 våren 2026](https://www.himolde.no/studier/emner/log/2026/var/scm200.html). Metodene er klassiske statistiske metoder, ikke en trent KI-modell.")
        st.write("Normal = prognose. Høy = normal × (1 + økning/100). Lav = normal × (1 − reduksjon/100). Planlagt mengde = valgt scenario × (1 + margin/100).")
        st.caption("Desimaler beholdes i beregningen; godkjent heltallsmengde kommer i et senere trinn.")
        st.write("Alle tre metoders fremtidsprognoser")
        st.dataframe(future.reset_index(), hide_index=True, key="all_forecasts")
        if scores is not None:
            st.write("Utviklingsvinduer (historikkens uke 69–80 og 81–92)")
            st.dataframe(score_table.loc[~score_table.Holdout].drop(columns="Holdout"), hide_index=True, key="development_scores")
            st.caption("Alle metodene bruker samme testuker og 12-ukershorisont. For lengre datasett brukes fortsatt de første 104 ukene. Ikke juster etter holdout uten et nytt urørt testsett.")
            observations = pd.DataFrame(details)
            observations["Dato"] = observations["Uke i historikken"].map(lambda week: history.week_start.iloc[week - 1])
            st.write("Observasjoner og feil bak MAE, inkludert separat holdout")
            st.dataframe(observations, hide_index=True, key="evaluation_details")

with st.expander("Hele salgshistorikken"):
    st.metric("Solgte enheter i perioden", f"{history['quantity_sold'].sum():,}".replace(",", " "))
    st.line_chart(history, x="week_start", y="quantity_sold", x_label="Uke", y_label="Antall solgt (stykk)")
    st.dataframe(
        history[["week_start", "quantity_sold"]].rename(columns={"week_start": "Uke", "quantity_sold": "Antall solgt (stykk)"}),
        hide_index=True, key="sales_history",
        column_config={"Uke": st.column_config.DateColumn(format="DD.MM.YYYY")},
    )
