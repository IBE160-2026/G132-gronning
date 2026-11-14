---
title: 'Samlet arbeidsflate for etterspørselsplanlegging'
type: 'feature'
created: '2026-11-14'
status: 'done'
route: 'oneshot'
review_loop_iteration: 0
context: []
baseline_commit: '0b9a469c2e2967da317c068a2621d0ec9be67678'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** Appens separate prognose- og scenariovisninger gjør det vanskelig
å se hvordan valgene påvirker planen. Brukeren har godkjent anbefalingen i
`outputs/designforslag/designgjennomgang.md` og bedt om gjennomføring.

**Approach:** Samle produkt- og metodevalg, historikk/prognose/plan og scenariofelt
i én Streamlit-arbeidsflate med faktisk holdout-MAE og full 12-ukerstabell.
Behold alle prosentgrenser, originaldata, rettelser og beregningsregler.
Vis siste 24 historikkuker i hovedgrafen, hele historikken og alle tre
prognoser i detaljer. Import og lagring samles i et utvidbart felt;
datakilde og importfeil forblir synlige. Scenarioområdet beskrives som en
planleggingsantakelse. Bruk Streamlits tema og responsiv kolonnestabling.
Innlogging, plangodkjenning og planeksport følger som egne leveranser.

</frozen-after-approval>

## Implementation Notes

- Avgrenset visningsendring i `app.py`, eksisterende UI-tester og README.
  Ingen uavklarte brukerbeslutninger eller irreversible endringer.
- Gjenbruk `forecast`, `evaluate`, `calculate_scenarios` og `DatasetStore`
  uendret. Altair finnes allerede i miljøet via Streamlit; registrer det
  som direkte avhengighet når appen importerer det.
- Den uregistrerte designgjennomgangen fra forrige økt er autorisert
  grunnlag for denne oppgaven og skal beholdes.
- Verifiser alle fem produkter, metoder/scenarioer, beholdte prosenter,
  reelle MAE-resultater, kort historikk, importfeil og lagrede rettelser.
- Implementert bred arbeidsflate i `app.py`: ett metodevalg, lagdelt
  Altair-graf med 24 historikkuker og 12 fremtidsuker, scenariofelt,
  uavrundet total, separat holdout og full plantabell. Detaljer og
  historikk kan utvides. Ingen endringer i beregnings- eller lagringsmodulene.
- `requirements.txt` fører nå Altair som direkte avhengighet.
  `README.md` beskriver ny navigasjon og visningsavrunding.
- UI-testene finner tabeller etter innhold fremfor rekkefølge, bruker
  isolerte databaser og kontrollerer i tillegg faktisk grafdata, kort
  historikk, ugyldig import og produktbytte med beholdte prosenter.
- BMad-oppstart og SQLite-tester krevde kjøring utenfor sandkassen på
  grunn av filtilgang. 19 tester bestod før siste gjennomgangsrettelser.
- Visuell kontroll forsøkt i nettleseren: nettleserverten var utilgjengelig;
  Windows-kontrollen kunne ikke lese minimert Edge selv etter startforsøk.
  Mobilvisning og lyst/mørkt tema er derfor ikke visuelt bekreftet.
- Sluttkontroll: `python -m unittest discover -s tests -v` bestod alle
  19 tester etter rettelsene fra gjennomgangen (11,129 sekunder).
  `git diff --check` bestod. Lokal Streamlit-server startet på port 8501.

## Review Triage Log

Uavhengig blind gjennomgang av arbeidskopien: 32,289 kB, N = 6.

- `low`, rettet: Normal uten margin gir overlappende prognose/plan;
  eksplisitt tekst forklarer nå sammenfallet.
- `medium`, rettet parallelt med gjennomgangen: tabelltester alene
  beskyttet ikke hovedgrafen. Ny test inspiserer grafens historikk,
  prognose, plan, scenarioområde og skille mellom historikk/fremtid.
- `low`, rettet: README refererte til fjernet seksjon; beskriver nå
  metodevalget øverst og «Juster planen».
- `low`, rettet: designgjennomgangen oppga ventende godkjenning;
  registrerer nå brukerens «gjør anbefalingen» og implementasjonsstatus.
- `medium`, rettet: kort historikk var bare tilgjengelig i lukket felt;
  inntil 24 tilgjengelige uker vises nå også i hovedområdet.
- `medium`, rettet: advarsel om holdout var skjult i detaljer;
  står nå ved sammenligningen og viser til utviklingsvinduene.

Ingen funn fra kodegjennomgangen utsatt. Visuell brukertest gjenstår.
