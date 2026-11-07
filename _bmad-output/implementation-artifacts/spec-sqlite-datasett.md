---
title: 'Permanent datalagring med sporbare rettelser'
type: 'feature'
created: '2026-11-07'
status: 'done'
route: 'oneshot'
---

<frozen-after-approval>

## Intent

Lagre validerte originalfiler i lokal SQLite med egen ID, navn og tidspunkt. Brukeren kan åpne lagrede versjoner etter omstart. Rett mengde for én eksisterende produktuke med obligatorisk begrunnelse; lag en ny uforanderlig versjon med forelder, gammel og ny mengde og tidspunkt. Originalens CSV-bytes skal bevares eksakt. Vis versjonshistorikk og aktiv ID. Ingen sletting, innlogging, plangodkjenning eller migrering av eksisterende forretningsdata.

Ugyldige importer avvises fortsatt før lagring. Strukturelle CSV-rettelser må gjøres før import; rettingsskjemaet gjelder mengder på gyldige eksisterende rader. Opplasting har forrang til den fjernes, noe UI forklarer. Lokal database er utenfor Git; README dokumenterer plassering, lokal begrensning og sikkerhetskopi.

</frozen-after-approval>

## Implementation Notes

- storage.py bruker SQLite-standardbibliotek, parameteriserte spørringer og transaksjoner. Bare INSERT, ingen endring av eksisterende datasett.
- Databasesti data/local/datasets.sqlite3, alternativ FORECAST_DB_PATH for isolerte tester.
- UI tilbyr eksplisitt lagring, valg/åpning av gamle versjoner, retur til demo, mengderettelse og nedlasting av kildefil.

## Review Triage Log

- Lav, rettet: utvidet UI-test med opplastede originalbytes og opplastingsforrang frem til fjerning av fil.
- Ingen konkrete lagringsfeil funnet. Alle 16 tester består, inkludert ny appøkt og revisjonskjede.
