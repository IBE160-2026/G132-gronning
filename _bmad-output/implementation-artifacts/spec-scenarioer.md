---
title: 'Scenarioer og separat sikkerhetsmargin'
type: 'feature'
created: '2026-11-07'
status: 'done'
route: 'oneshot'
---

<frozen-after-approval>

## Intent

Brukeren velger en eksisterende prognosemetode og ser normal, høy (+10 %) og lav (-10 %) etterspørsel for 12 uker. Prosentsatser kan endres. Et valgt scenario kan få en separat sikkerhetsmargin med startverdi 0 %. Vis beregningene og mengdevirkningen i graf og tabell; mengder kan aldri bli negative. Scenarioer er planleggingsantakelser, ikke statistiske intervaller, og marginen er ikke sikkerhetslager.

Produktbytte beholder forutsetningene og beregner mengdene på nytt. Ingen eksport, permanent lagring, manuelle mengdeoverstyringer eller godkjenning i dette trinnet.

</frozen-after-approval>

## Implementation Notes

- scenarios.py beregner uten UI eller endring av grunnprognose. Lavjustering 0–100 %, høyjustering/margin 0–1000 % for praktiske inndatagrenser.
- app.py plasserer scenarioer etter eksisterende MAE-visning slik at den eksisterende flyten bevares.
- Desimalpresisjon beholdes; heltallsavrunding av godkjent plan er et senere trinn.

## Review Triage Log

- Lav, rettet: test hver valgt metodes grunnprognose mot riktig kildekolonne.
- Lav, rettet: legg til håndkontroll av ikke-null lavscenario med margin (100 * 0,7 * 1,1 = 77).
- Alle 12 tester består; ingen funksjonsfeil funnet.
