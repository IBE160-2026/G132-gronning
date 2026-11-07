# Syntetisk salgshistorikk for friluftsprodukter

**Alle salgstall er konstruerte øvingsdata. Ingen tall er hentet fra en butikk, produsent eller virkelig kunde.** Produktene er generiske kategorier, ikke bestemte merkevarer. Bruk dette som teknisk grunnlag for prototypen, ikke som dokumentasjon på faktisk marked eller modellnøyaktighet i en bedrift.

## Filer

- `sales_history_clean.csv`: hovedfil for import og prognoser. Fem produkter × 104 mandagsuker = 520 rader, fra 2024-01-01 til 2025-12-22.
- `products.csv`: produktnavn og alle antatte generatorparametere. Koble produktnavn via `product_id`.
- `sales_history_validation.csv`: separat testfil med manglende verdi/uke, duplikat, negativ mengde, ugyldig dato, et høyt avvik og ett gyldig nullsalg. Ikke bruk denne som ren treningsfil.
- `manifest.json`: seed, genereringsformel og eksakte feilsteder med originalverdier. Kun til kontroll, ikke skjult input til modellen.
- `generate_data.py`: gjenskaper filene med Python-standardbiblioteket og seed 132. Kjør fra prosjektroten med `python data/synthetic/generate_data.py`.

## Produkter og antakelser

| ID | Produkt | Konstruert sesongmønster |
|---|---|---|
| P01 | Telt, 2 personer | Topp omkring uke 25 i 52-ukerssyklusen |
| P02 | Sovepose, 3 sesonger | Topp omkring uke 24 |
| P03 | Tursekk, 45 liter | Topp omkring uke 23 |
| P04 | Liggeunderlag, oppblåsbart | Topp omkring uke 26 |
| P05 | Hodelykt, LED | Topp omkring uke 47 |

Sesongtopper, volum, vekst og støy er pedagogiske antakelser, ikke målte norske kjøpsmønstre. Modellen bruker en 52-ukers syklus, ikke en nøyaktig kalenderårsmodell. Datasettene har ingen priser, personopplysninger, lagerbegrensninger eller kundeordre. Salg brukes som en forenklet representasjon av etterspørsel.

## CSV-format

UTF-8, komma som skilletegn, datoformat `YYYY-MM-DD`. `product_id` er tekst; `quantity_sold` er heltall; `unit` er alltid `units` (stykk). Null betyr observert nullsalg; tom verdi betyr manglende registrering. Ikke legg prognoseukene inn i historikkfilen: de neste 12 ukene skal beregnes av appen.

## Evaluering

Bruk ukenummer 1–104 per produkt. Tren til og med uke 68, 80 og 92, og prognostiser henholdsvis 69–80, 81–92 og 93–104. Rapporter MAE per produkt og vindu. Siste vindu er holdout; bestem modell og databehandling før det vurderes. Ingen testobservasjoner eller kontrollverdier fra manifestet kan brukes til trening. Den glatte syntetiske sesongen passer bevisst den enkle modellen og kan gi mer optimistiske resultater enn reelle data.

## Kildeundersøkelse

Undersøkt 2026-11-07. REIs campingutvalg bekrefter at kategoriene er relevante friluftsprodukter: https://www.rei.com/c/camping-and-hiking . Dette er kun kategorireferanse, ikke kilde til tall eller sesongmønstre.

UCI Online Retail tilbyr reelle transaksjoner, men det er ikke her verifisert fem passende friluftsprodukter med den nødvendige historikken: https://archive.ics.uci.edu/dataset/352/online+retail . IBM beskriver selv Great Outdoors som fiktive eksempeldata: https://www.ibm.com/docs/en/planning-analytics/2.0.0?topic=applications-introduction . Ingen av disse datasettene er kopiert inn i våre filer.
