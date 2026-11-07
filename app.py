"""Startside for prognoseprototypen."""

from pathlib import Path
import os
import sqlite3

import pandas as pd
import streamlit as st
from sales_data import validate_csv
from forecasting import forecast, evaluate
from scenarios import calculate_scenarios
from storage import DatasetStore

st.set_page_config(page_title="Friluft – etterspørselsplanlegging", page_icon="🏕️")

st.title("Friluft – etterspørselsplanlegging")
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
selected_product = st.selectbox(
    "Velg produkt", options=list(product_names), format_func=product_names.get
)
history = sales.loc[sales["product_id"] == selected_product].sort_values("week_start")

with st.expander("Lagre, åpne og rette datasett"):
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

st.subheader("Salgshistorikk")
st.caption("Salgstall per uke. Mengder er oppgitt i stykk.")
if history.empty:
    st.warning("Ingen salgshistorikk finnes for dette produktet.")
    st.stop()

st.metric("Solgte enheter i perioden", f"{history['quantity_sold'].sum():,}".replace(",", " "))
st.line_chart(history, x="week_start", y="quantity_sold", x_label="Uke", y_label="Antall solgt (stykk)")
st.dataframe(
    history[["week_start", "quantity_sold"]].rename(
        columns={"week_start": "Uke", "quantity_sold": "Antall solgt (stykk)"}
    ),
    hide_index=True,
    column_config={"Uke": st.column_config.DateColumn(format="DD.MM.YYYY")},
)

st.subheader("Etterspørselsprognoser – SCM200")
st.write("Glidende gjennomsnitt: siste 4 uker. Enkel eksponensiell glatting: α = 0,3, startnivå = første salgstall. Sesongnaiv: samme uke i forrige 52-ukerssyklus.")
st.caption("Faste pedagogiske parametere, ikke optimalisert på testdata. Glidende gjennomsnitt og enkel glatting gir flate 12-ukersprognoser og modellerer ikke sesong eller trend eksplisitt.")
st.markdown("Faglig grunnlag: [SCM200 våren 2026](https://www.himolde.no/studier/emner/log/2026/var/scm200.html). Metodene er klassiske statistiske metoder, ikke en trent KI-modell.")
try:
    forecast_values = forecast(history.quantity_sold.tolist())
except ValueError as error:
    st.warning(str(error))
else:
    future_dates = pd.date_range(history.week_start.iloc[-1] + pd.Timedelta(weeks=1), periods=12, freq="7D")
    future = pd.DataFrame(forecast_values, index=future_dates)
    future.index.name = "Uke"
    st.caption("Neste 12 uker etter siste registrerte uke, ikke etter dagens dato. Verdiene er punktprognoser i stykk og beholdes uten heltallsavrunding.")
    chart = pd.DataFrame({"Historikk": history.set_index("week_start").quantity_sold})
    st.line_chart(chart.join(future, how="outer"), x_label="Uke", y_label="Antall (stykk)")
    st.dataframe(future.reset_index(), hide_index=True)

    st.subheader("Historisk kontroll – MAE")
    st.caption("MAE er gjennomsnittlig absolutt feil i stykk; lavere er bedre. Alle metodene bruker samme testuker og 12-ukershorisont. Parametere er fastsatt før evalueringen; ingen automatisk metodevalg.")
    try:
        scores, details = evaluate(history.quantity_sold.tolist())
    except ValueError as error:
        st.warning(str(error))
    else:
        score_table = pd.DataFrame(scores)
        st.write("Utviklingsvinduer (historikkens uke 69–80 og 81–92)")
        st.dataframe(score_table.loc[~score_table.Holdout].drop(columns="Holdout"), hide_index=True)
        st.write("Separat holdout (historikkens uke 93–104)")
        st.dataframe(score_table.loc[score_table.Holdout].drop(columns="Holdout"), hide_index=True)
        st.caption("For lengre datasett brukes fortsatt de første 104 ukene til disse testene. Ikke juster metoder etter holdout-resultater uten et nytt urørt testsett.")
        with st.expander("Se observasjoner og feil bak MAE"):
            observations = pd.DataFrame(details)
            observations["Dato"] = observations["Uke i historikken"].map(lambda week: history.week_start.iloc[week - 1])
            st.dataframe(observations, hide_index=True)

    st.subheader("Scenarioer og sikkerhetsmargin")
    st.caption("Planleggingsantakelser, ikke statistiske konfidens- eller prediksjonsintervaller. Sikkerhetsmargin er et tillegg til mengden, ikke beregnet sikkerhetslager.")
    method = st.selectbox("Prognosemetode for scenarioer", list(forecast_values), key="scenario_method")
    high_pct = st.number_input("Høy etterspørsel – økning (%)", min_value=0.0, max_value=1000.0, value=10.0, step=1.0, key="high_pct")
    low_pct = st.number_input("Lav etterspørsel – reduksjon (%)", min_value=0.0, max_value=100.0, value=10.0, step=1.0, key="low_pct")
    selected_scenario = st.selectbox("Scenario for planlagt mengde", ["Normal", "Høy", "Lav"], key="selected_scenario")
    margin_pct = st.number_input("Separat sikkerhetsmargin (%)", min_value=0.0, max_value=1000.0, value=0.0, step=1.0, key="margin_pct")
    st.caption("Prosentvalgene beholdes ved produktbytte og beregnes på nytt for valgt produkt. Ingen godkjenning eller permanent lagring utføres her.")
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
    st.write(f"{product_names[selected_product]} · {method} · {selected_scenario}. Høy: +{high_pct:g} %, lav: −{low_pct:g} %, separat margin: +{margin_pct:g} %.")
    st.caption("Normal = prognose. Høy = normal × (1 + økning/100). Lav = normal × (1 − reduksjon/100). Planlagt mengde = valgt scenario × (1 + margin/100). Desimaler beholdes i beregningen; godkjent heltallsmengde kommer i et senere trinn.")
    st.line_chart(scenario_table.set_index("Uke")[["Normal (stykk)", "Høy (stykk)", "Lav (stykk)", "Planlagt mengde (stykk)"]], x_label="Uke", y_label="Antall (stykk)")
    st.dataframe(scenario_table, hide_index=True)
