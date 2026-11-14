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

Arbeidsflaten samler produkt- og metodevalg øverst. Hovedgrafen viser siste
24 historikkuker, valgt prognose, lav–høy scenario uten margin og plan med
margin for de neste 12 ukene. Juster scenario og prosenter ved siden av grafen;
tabellen viser alle 12 planuker. Holdout-MAE beregnes for valgt produkt og
vises separat fra utviklingsvinduene. Kort historikk gir forklaring når
prognoser eller evaluering ikke kan beregnes.

«Datagrunnlag og import» samler opplasting, lagring og rettelser. Aktiv
datakilde og importfeil vises utenfor det sammenfoldede feltet.
«Alle beregninger og testvinduer» viser alle tre prognoser, formler og feil
bak MAE; «Hele salgshistorikken» viser alle uker og salgssummen.
Total planlagt mengde og planrader vises med én desimal; beregningene bruker
uavrundede verdier, så summen av avrundede rader kan avvike fra vist total.
Appen bruker Streamlits tema, som velges under menyen øverst til høyre →
Settings → Theme. Kolonnene stables på smal skjerm.

CSV-opplasting krever UTF-8, komma og kolonnene i denne rekkefølgen:
`product_id,week_start,quantity_sold,unit`. Dato er mandag i format
`YYYY-MM-DD` mellom 1900 og 2100, mengde et heltall fra 0 til 1000000000,
og enhet `units`. Duplikater og manglende uker mellom første og siste registrering
per produkt avvises. Manglende verdi er forskjellig fra nullsalg.
Uvanlig høye verdier gir varsel uten automatisk endring. Rett feil i originalfilen
og last opp på nytt. Ingen automatisk retting utføres.

## Lokal lagring og rettelser

Åpne «Lagre, åpne og rette datasett» og trykk «Lagre datasettet» for å lagre
gyldig CSV eller eksempeldata. Originalfilen bevares byte for byte med UUID og
tidspunkt. Velg en lagret versjon og «Åpne valgt versjon» for å bruke den igjen,
også etter at appen er startet på nytt. Opplastet fil har forrang til den fjernes.
«Vis eksempeldata» går tilbake til demo når opplastingen er fjernet.

På en lagret versjon kan du velge produkt og uke, angi ny heltallsmengde og
begrunnelse, og lagre rettelsen som en ny versjon. Historikken viser forelder,
gammel/ny mengde, begrunnelse og tidspunkt i UTC. Tidligere versjoner og originalen
overskrives ikke av appen. Originalen kan åpnes og lastes ned fra versjonslisten.
Feil i CSV-struktur eller manglende uker må fortsatt rettes før import.

Databasen ligger i `data/local/datasets.sqlite3` og er ignorert av Git. For en
annen lokal plassering kan `FORECAST_DB_PATH` settes før oppstart. Ta sikkerhetskopi
av databasefilen når appen er stoppet. Filer synkroniseres ikke gjennom GitHub.
Dette er lokal lagring uten innlogging; ikke publiser appen med sensitive data
før tilgangsstyring er implementert. Lagring av godkjente planer er et senere trinn.

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

Velg prognosemetode øverst i arbeidsflaten og scenario under «Juster planen». Normal bruker
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
