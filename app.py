"""Startside for prognoseprototypen."""

from pathlib import Path

import pandas as pd
import streamlit as st
from sales_data import validate_csv

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
uploaded = st.file_uploader("Last opp salgshistorikk (CSV)", type=["csv"])
st.caption("UTF-8, komma, kolonner: product_id,week_start,quantity_sold,unit. Ukestart mandag; unit = units. Nullsalg skrives 0.")
if uploaded is not None:
    sales, errors, warnings = validate_csv(uploaded.getvalue())
    for warning in warnings:
        st.warning(warning)
    if errors:
        st.error("Importen er avvist. Rett feilene i originalfilen og last opp på nytt. Ingen rader er importert.")
        for error in errors:
            st.error(error)
        st.stop()
    st.success("CSV er kontrollert og vises nedenfor. Filen er ikke lagret permanent.")
    product_names = {pid: product_names.get(pid, pid) for pid in sales.product_id.unique()}
else:
    st.caption("Viser medfølgende syntetiske eksempeldata.")
selected_product = st.selectbox(
    "Velg produkt", options=list(product_names), format_func=product_names.get
)
history = sales.loc[sales["product_id"] == selected_product].sort_values("week_start")

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
