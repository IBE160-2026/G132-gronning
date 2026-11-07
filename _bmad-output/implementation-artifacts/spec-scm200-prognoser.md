---
title: 'SCM200-prognoser og MAE'
type: 'feature'
created: '2026-11-07'
status: 'done'
route: 'oneshot'
---

<frozen-after-approval>

## Intent

Implementer prognosedelen med SCM200 våren 2026 som faglig input. Bruk fire ukers glidende gjennomsnitt, enkel eksponensiell glatting med alfa 0,3 og første observasjon som startnivå, samt sesongnaiv referanse med periode 52. Faste parametere uten tuning og 12 ukers punktprognoser. Regresjon utsettes etter brukerens valg.

Vis historikk og prognoser i graf, fremtidstabell, MAE per metode/vindu og underliggende observasjoner. Bruk utvidende treningsvinduer som slutter ved 68, 80 og 92, med påfølgende 12 ukers evaluering; siste vindu vises separat. Ingen fremtidige data brukes til prognoser eller parameterbestemmelse. Krev 52 uker for sammenligning og 104 for denne evalueringen. Oppdater brief, addendum og plan med faglig forankring og brukerens avklarte tid/frist. Andre SCM200-moduler er utenfor dette trinnet.

</frozen-after-approval>

## Implementation Notes

- forecasting.py isolerer alle beregninger fra UI; ingen nye avhengigheter.
- Klassiske metoder beskrives korrekt, uten påstand om trent ML-modell eller verifisert lærebokinnhold.
- Glidende gjennomsnitt og enkel glatting gir flate flerstegsprognoser; ingen reelle fremtidstall brukes til å oppdatere dem innen testvinduet.
- For lengre import brukes første 104 uker til faste tester og hele historikken til fremtidsprognose.

## Review Triage Log

- Lav, rettet: styrket lekkasjetesten til å endre alle observasjoner fra første testuke (indeks 68), slik at også umiddelbar testperiode dekkes.

- Sluttkontroll: ni tester bestod. UI-test verifiserer 12 fremtidsuker, tre metoder og separate MAE-vinduer for alle fem produkter.
