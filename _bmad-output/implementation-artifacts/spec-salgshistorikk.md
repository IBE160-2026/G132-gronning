---
title: 'Produktvelger og salgshistorikk'
type: 'feature'
created: '2026-11-07'
status: 'done'
route: 'oneshot'
---

<frozen-after-approval>

## Intent

Koble medfølgende syntetisk salgshistorikk og produktkatalog til Streamlit-siden. Brukeren velger ett av fem produkter og ser ukentlig salg i en kronologisk graf og tabell, samt totalen for perioden. Dataene merkes tydelig som syntetiske. CSV-opplasting, prognoser og innlogging er utenfor dette trinnet.

</frozen-after-approval>

## Implementation Notes

- app.py leser filer relativt til egen filsti, uavhengig av arbeidsmappe.
- pandas er eksplisitt avhengighet. Ingen datafiler endres.
- Manglende/uleselige filer gir en norsk feilmelding; manglende historikk gir et varsel.

- Test i tests/test_sales_view.py bestod for alle fem produkter, samtlige verdier, kronologi og summer. pip check bestod.

## Review Triage Log

- Uavhengig review fant ingen konkrete feil. Ingen funn utsatt.
