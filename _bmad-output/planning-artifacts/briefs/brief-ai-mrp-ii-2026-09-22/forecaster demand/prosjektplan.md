---
title: "Prosjektplan – Forecasting and Demand Management"
status: draft
created: 2026-09-23
updated: 2026-11-07
deadline_week: 2026-W51
capacity_hours_per_week: 4
---

# Prosjektplan – videre utvikling

**Mål: ferdigstillelse i uke 51, 14.–20. desember 2026. Kapasitet: omtrent fire timer per uke.** Nøyaktig innleveringsdato i uken må bekreftes mot emnets krav. Dette erstatter tidligere frist 1. desember og anslaget 12–15 timer per uke.

Planen følger [produktbriefen](brief.md), [addendum](../addendum.md) og brukerens valg av SCM200 våren 2026 som faglig grunnlag for prognosene. Seks uker à fire timer gir et planleggingsbudsjett på omtrent 24 timer; faktisk tidsbruk er ikke registrert her og må føres separat. Ferdigstillelse av hele MVP-en er fortsatt usikker innen denne kapasiteten.

## Faglig grunnlag og omfang

[Emnebeskrivelsen for SCM200 våren 2026](https://www.himolde.no/studier/emner/log/2026/var/scm200.html) nevner glidende gjennomsnitt, eksponensiell glatting og evaluering av prognoser gjennom måltall. Vi bruker MA(4), enkel glatting med alfa 0,3 og sesongnaiv referanse med periode 52. MAE, parameterverdiene og 12 ukers horisont er prosjektvalg, ikke bekreftede krav fra pensumboken. Regresjon er utsatt etter brukerens beslutning. Utviklingen er KI-assistert; prognosemetodene er klassiske statistiske metoder.

Kun etterspørselsstyring inngår. EOQ, MRP, lagerstyring, kapasitet og detaljplanlegging er utenfor v1. Kundeordre, markedssignaler, ekstra roller og språkmodeller er også utsatt.

## Verifisert status

- Syntetiske data: fem friluftsprodukter, 104 uker hver; generator, manifest og testfil med kjente feil.
- Streamlit med produktvelger, historikkgraf, tabell og totalsum.
- CSV-opplasting med formatkontroll, radfeil, duplikater, interne ukehull og avviksvarsler. Gyldig opplasting kan nå lagres eksplisitt i SQLite med uforanderlige versjoner og begrunnede mengderettelser.
- SCM200-prognoser med graf og fremtidstabell, historisk MAE og separat holdout er implementert i denne leveransen.
- Scenarioer, sikkerhetsmargin, permanent datalagring og begrunnede mengderettelser er implementert. Innlogging, godkjenning og planeksport gjenstår. Dette er planlagte funksjoner, ikke fullført arbeid.

## Prioritert arbeidsplan

Ukene er målperioder, ikke påstander om registrert tidsbruk. Funksjoner som er ferdige før målperioden, frigjør kapasitet til gjenstående arbeid og kontroll.

| Uke | Prioritet | Kontrollpunkt | Budsjett |
|---|---|---|---:|
| 46, 9.–15. november | Kontroller lokal app, eksempeldata og salgsvisning | En annen person kan starte appen etter README | 4 t |
| 47, 16.–22. november | CSV-import og datakvalitet; planlegg permanent lagring og sporbare rettelser | Gyldig fil vises, feilfil avvises; avklar resterende lagringsarbeid | 4 t |
| 48, 23.–29. november | Kontroller og forklar prognoser, MAE og tidsserieevaluering | Håndregnede eksempler, ingen datalekkasje, alle fem produkter virker | 4 t |
| 49, 30. november–6. desember | Scenarioer, synlig margin og CSV-eksport | Beregningene er synlige og eksport kan kontrolleres mot skjermen | 4 t |
| 50, 7.–13. desember | Prioriter innlogging, SQLite og uforanderlig godkjenning; innhent hjelp ved kapasitetsgap | Tilgang håndheves; godkjent plan og datagrunnlag kan spores | 4 t |
| 51, 14.–20. desember | Feilretting, brukertest, README og leveringskontroll | Gjentakbar demonstrasjon og dokumenterte begrensninger | 4 t |

Uke 51 skal brukes til testing og feilretting fremfor nye funksjoner. Lagre oppgaver med kravreferanse, estimat, ansvarlig og kontrollbevis. Ikke fjern sikkerhet, korrekt evaluering eller sporbarhet uten en uttrykkelig dokumentert omfangsendring. Hvis fire timer ikke dekker ukens arbeid, prioriter og avklar konsekvensene tidlig.

## Test- og leveringskrav

- Prognoser: MA(4) er gjennomsnittet av siste fire treningsverdier. Enkel glatting starter i første observasjon og oppdaterer nivået med alfa 0,3. Begge gir flate 12-stegsprognoser fra hvert starttidspunkt.
- Sesongnaiv: riktig forskyvning 52 uker; krever minst 52 sammenhengende observasjoner.
- Evaluering: tren til uke 68, 80 og 92; test 69–80, 81–92 og 93–104. Vis holdout separat og de faktiske verdiene bak MAE. Minst 104 uker kreves. Lengre historikk endrer ikke disse testvinduene.
- Ikke velg parametere etter holdout. Hvis det skjer, opplys om det og reserver nytt urørt testsett. Rapporter også svake resultater.
- Data: nullsalg er gyldig; manglende registrering er ikke null. Original og rettelser skal kunne spores når permanent import innføres.
- Tilgang og godkjenning: test uautorisert tilgang og at eksporterte mengder er identiske med lagret godkjenning når disse funksjonene er bygget.
- Lever README, data-/metodebeskrivelse, tester, brukerveiledning og kjent-feil-liste sammen med identifisert kodeversjon. Lokal kjøring skal ikke kreve betalte kontoer eller personlige nøkler. Avklar publiseringskrav før valg av vertstjeneste.

## Neste utviklingsoppgave

Bygg innlogging og sporbar godkjenning av planer, og koble deretter eksport til godkjenningslagringen. Før ukentlig status med utført arbeid, testbevis, faktisk tidsbruk, gjenstående timer og risiko mot uke 51.
