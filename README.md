# Gruppe G132

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

Se [endringsoversikten](ENDRINGSLOGG.md) for historikk fra prosjektstart,
commit-lenker, berørte filer og hjelp til å finne endringer ved feil.

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

Appen viser en produktvelger, salgsgraf, tabell og total solgt mengde for fem
friluftsprodukter over 104 uker. Du kan også laste opp egen CSV og sammenligne
tre prognosemetoder med historisk MAE. Eksempeldataene i `data/synthetic/` er konstruerte
øvingsdata, ikke faktisk salgshistorikk fra en bedrift.

CSV-opplasting krever UTF-8, komma og kolonnene i denne rekkefølgen:
`product_id,week_start,quantity_sold,unit`. Dato er mandag i format
`YYYY-MM-DD` mellom 1900 og 2100, mengde et heltall fra 0 til 1000000000,
og enhet `units`. Duplikater og manglende uker mellom første og siste registrering
per produkt avvises. Manglende verdi er forskjellig fra nullsalg.
Uvanlig høye verdier gir varsel uten automatisk endring. Rett feil i originalfilen
og last opp på nytt; ingen automatisk retting eller permanent import utføres.
Fjerner du opplastingen, vises eksempeldataene igjen.

## Prognoser og faglig grunnlag

[SCM200 våren 2026](https://www.himolde.no/studier/emner/log/2026/var/scm200.html)
nevner glidende gjennomsnitt, eksponensiell glatting og vurdering gjennom måltall.
Appen bruker glidende gjennomsnitt over fire uker og enkel glatting med alfa 0,3,
initialisert med første observasjon. Flerstegsprognosene er flate. Sesongnaiv
referanse gjentar siste 52-ukerssyklus. Dette er klassiske metoder; regresjon er
utsatt. Parametere og MAE er prosjektvalg, ikke bekreftede krav fra pensumboken.
Se [metodereferansen](https://otexts.com/fpp3/exponential-smoothing.html).

Minst 52 uker trengs for treveis sammenligning, og 104 for evaluering.
Trening avsluttes ved uke 68, 80 og 92 med påfølgende 12-ukers testvinduer.
Holdout 93–104 vises separat. Ingen automatisk tuning eller metodevalg.
For lengre historikk beholdes disse testvinduene, mens fremtidsprognosen bruker
hele historikken. MAE måles per produkt i stykk uten heltallsavrunding.
Ingen av metodene garanterer gode resultater på reelle sesongdata.

## Scenarioer

Velg prognosemetode under «Scenarioer og sikkerhetsmargin». Normal bruker
punktprognosen; høy og lav starter på henholdsvis +10 % og −10 %.
Lavjustering kan være 0–100 %, høyjustering og margin 0–1000 %.
Velg et scenario og legg eventuelt til en separat margin (standard 0 %).
Eksempel: prognose 100, høy +20 % og margin +10 % gir 120 + 12 = 132.
Graf og tabell viser antakelser og mengdevirkning. Produktbytte beholder
prosentvalgene, men beregner verdiene på nytt. Dette er planleggingsantakelser,
ikke statistiske intervaller eller sikkerhetslager. Verdiene lagres ikke
permanent og er ennå ikke en godkjent plan eller eksport.

Kjør alle beregnings-, import- og visningstester:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```
