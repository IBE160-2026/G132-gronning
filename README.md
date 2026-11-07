# Gruppe G132

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

## Medlemmer

- Vilde Gronning

## Kjør appen lokalt

Åpne PowerShell i prosjektmappen. Python 3.11 eller nyere er nødvendig.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Åpne adressen som vises i terminalen, vanligvis http://localhost:8501.
Stopp serveren med `Ctrl+C`. Ved neste oppstart trenger du bare den siste kommandoen.

Første versjon viser en norsk startside. Dataimport, produktvelger og prognoser
er ennå ikke implementert. Eksempeldataene i `data/synthetic/` er konstruerte
øvingsdata, ikke faktisk salgshistorikk fra en bedrift.
