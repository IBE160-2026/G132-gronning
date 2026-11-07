"""Startside for prognoseprototypen."""

import streamlit as st

st.set_page_config(page_title="Friluft – etterspørselsplanlegging", page_icon="🏕️")

st.title("Friluft – etterspørselsplanlegging")
st.write("En prototype for prognoser og planlegging av salg av friluftsprodukter.")
st.info("Appen er under utvikling. Salgsdataene i prosjektet er syntetiske øvingsdata.")
st.subheader("Neste trinn")
st.write("Koble til eksempeldataene og vis salgshistorikk for valgt produkt.")
