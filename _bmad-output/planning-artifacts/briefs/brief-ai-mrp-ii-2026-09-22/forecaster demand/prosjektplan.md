---
title: "Prosjektplan – Forecasting and Demand Management"
status: draft
created: 2026-09-23
updated: 2026-11-07
start_date: 2026-09-23
replanned_from: 2026-11-07
deadline: 2026-12-01
---

# Prosjektplan – Forecasting and Demand Management

Målet er en fungerende nettprototype for modul 4.1: Prognoser og etterspørselsstyring innen **1. desember 2026**. Planen er revidert 7. november etter [faglærerens tilbakemelding](tilbakemelding-product-brief.md) og følger [produktbriefen](brief.md) og [modulvedlegget](../addendum.md).

Revisjonen erstatter tidligere omfang og fremtidige arbeidsoppgaver i septemberplanen. Tidligere datoer er ikke dokumentasjon på fullført arbeid. Implementasjonsstatus og faktisk tidsbruk er ikke bekreftet; første kontrollpunkt er derfor å kartlegge hva som faktisk virker. Planen starter ingen implementasjon automatisk.

## 1. Omfang og forutsetninger

V1 er en nettprototype for én fiktiv produsent av sesongbaserte friluftsprodukter. Én innlogget planlegger gjennomfører import → datakontroll → prognosesammenligning → scenario → godkjenning → eksport.

| Område | Forpliktelse i v1 |
|---|---|
| Datasett | Fem produkter, 104 uker fra 2024-01-01 til 2025-12-22, ukestart mandag, enhet `units`, seed 132. Ren referanse med 520 rader og en separat fil med kjente feil. |
| Import | Kun salgshistorikk fra CSV med `product_id`, `week_start`, `quantity_sold`, `unit`. |
| Datakvalitet | Valider felter, datoer, ukedekning, duplikater, negative og manglende verdier. Skill nullsalg fra manglende data. Vis regelbaserte avviksvarsler og bevar originaldata og begrunnede rettelser. |
| Prognoser | Sesongnaiv referanse med 52 ukers sesong og én scikit-learn lineær regresjon med trend og årlige sinus-/cosinusledd. Horisont 12 uker. |
| Evaluering | Felles testvinduer, MAE per produkt og vindu, ingen fremtidige observasjoner i trening eller databehandling. Svakere regresjonsresultater rapporteres også. |
| Scenarioer | Normal = valgt prognose, optimistisk = +10 %, pessimistisk = −10 %. Justerbare, synlige prosentsatser; separat sikkerhetsmargin, standard 0 %, og begrunnede overstyringer. |
| Godkjenning | Uforanderlig godkjenningsøyeblikksbilde med datagrunnlag, rettelser, metode, scenario, margin, overstyringer, godkjenner og tidspunkt. Ny godkjenning gir nytt øyeblikksbilde. |
| Tilgang | Innlogging og én planleggerrolle, håndhevet på serveren også for lesing, beregning og eksport. Lokal demonstrasjonskonto. |
| Teknisk retning | Python, Streamlit, scikit-learn og SQLite. Validering, prognoser og evaluering holdes adskilt fra brukergrensesnittet. |
| Kjørbarhet | README, eksempeldata og lokalt oppsett uten personlige nøkler, betalte API-er eller kontoer. Publisert demonstrasjon klargjøres etter avklaring av emnets leveringskrav. |

Kundeordre, kampanjer, markedssignaler, administrator-/leseroller, full endringshistorikk, flere modeller og språkmodellforklaringer er senere utvidelser. BOM, MPS/MRP, lagerstyring, kapasitet, detaljplanlegging, økonomi, kjøp/salg og eksterne integrasjoner er utenfor v1.

**[ANTAKELSE]** Én student har 12–15 timer per full uke. Fra 9. november til fristen gir dette omtrent 36–45 timer over tre fulle uker, med eventuell kapasitet på de siste to dagene i tillegg. Dette erstatter ikke en konkret arbeidskalender. Det tidligere budsjettet på 142 timer kan ikke behandles som gjenstående kapasitet. Helgearbeid er ikke en forutsetning.

## 2. Revidert tidsplan

Estimatene under er et foreløpig budsjett på **36 timer arbeid + 6 timer reserve**. Det er realistisk bare dersom statuskontrollen viser at vesentlige deler allerede finnes, eller at oppgavene kan gjennomføres innen estimatene. Hvis hele appen gjenstår, må kapasitet og leveranse avklares med faglærer; tabellen er ikke et løfte om at alt kan bygges fra grunnen på 36 timer.

| Periode | Arbeid | Ferdig når | Timer |
|---|---|---|---:|
| 9.–10. november | Kartlegg kjørbar kode, data, tester og dokumentasjon. Lag korte PRD-krav og oppgaver fra revidert brief. Bekreft at regresjonen møter emnets KI-forventninger. Avklar autentisering og leveringsform. | Faktisk status, avhengigheter, estimert restarbeid og arbeidskalender er dokumentert. Kapasitet er sammenlignet med restarbeidet. | 4 |
| 11.–13. november | Lag eller ferdigstill datagenerator, ren referanse og feilfil. Få innlogging, lagring og salgsimport til å virke. Test manglende verdier, nullsalg og kjente feil. | Demo kan startes lokalt. Innlogget planlegger kan importere og kontrollere data; uautorisert tilgang avvises. | 8 |
| 16.–18. november | Ferdigstill sesongnaiv metode, fast regresjon og tidsordnet evaluering. Vis historikk, begge prognoser og MAE. | Begge modeller kan kjøres fra UI. Håndregnede tester og kontroll mot datalekkasje består. | 8 |
| 19.–20. november | Ferdigstill scenarioer, margin, forklarte overstyringer, godkjenningsøyeblikksbilder og CSV-eksport. | Hele hovedflyten virker med eksempelfilen. Eksport samsvarer med lagrede godkjente mengder. | 6 |
| 23.–25. november | La en annen person prøve hovedflyten. Rett blokkerende feil. Kontroller direkte servertilgang, oppstart og gjenoppretting av demo. Klargjør publisert demo dersom påkrevd. | Alle må-krav har kontrollbevis; ingen kjente feil blokkerer hovedflyten eller bryter tilgangskrav. | 6 |
| 26.–27. november | Fullfør README, modell-/databeskrivelse, testresultater og kjente begrensninger. Gjenta installasjon i et rent miljø og øv på demonstrasjonen. | Leveringskandidat med identifisert kodeversjon og reproduserbar lokal kjøring. | 4 |
| 30. november–1. desember | Bruk gjenværende reserve til konkrete feil og sluttkontroll. Lever etter emnets krav innen 1. desember. | Leveringspakken er kontrollert, og innleveringen er bekreftet. | Inntil 6 reserve |

Reserven kan brukes tidligere ved behov. Registrer brukt og gjenstående reserve; ikke legg inn nye funksjoner i bufferen. Dersom statuskontrollen viser at noe allerede er ferdig, bruk frigjort tid til nødvendige kontroller og feilretting.

## 3. Oppgaver og arbeidsmetode

Bruk en tavle med **Planlagt → Klar → Pågår → Til kontroll → Ferdig**. Begrens pågående arbeid til én større oppgave per person. Hver oppgave får ID, kravreferanse, ansvarlig, estimat, avhengigheter, akseptansekriterier og kontrollbevis. Del opp arbeid som tar mer enn én arbeidsdag.

Prioritert rekkefølge:

1. Bekreft status, kapasitet og testbare krav fra briefen.
2. Lag datasett og kontrollerbare feiltilfeller i `data/synthetic/`.
3. Sikre innlogging, lagring og validering av salgsimport.
4. Koble inn sesongnaiv metode, regresjon og felles evaluering.
5. Fullfør scenarioer, godkjenning og eksport.
6. Gjennomfør brukertest, lokal installasjon, eventuell publiseringskontroll og levering.

Lag små, beskrivende commits. Før en kort logg over vesentlig KI-bruk, egne vurderinger og kontrollresultater. Oppbevar syntetiske data i Git, men hold hemmeligheter og eventuelle senere sensitive rådata utenfor Git og offentlige logger.

Bruk eventuelt `bmad-prd`, `bmad-ux` og `bmad-architecture` til korte krav og beslutninger, og `bmad-build` til avgrensede implementasjonsoppgaver. Planlegging og dokumentasjon inngår i timebudsjettet. Ingen av disse arbeidsflytene er utført bare fordi de er nevnt her.

## 4. Testplan og definisjon av ferdig

Lagre dato, kravreferanse, forventet resultat, faktisk resultat og eventuell feilreferanse for hver kontroll.

| Område | Påkrevd kontroll |
|---|---|
| Datasett | Generator gir samme resultat med seed 132; ren fil har fem produkter × 104 uker. Feilmanifest beskriver alle innlagte avvik. Referansefil brukes ikke som skjult modellinput. |
| Import | Gyldig og tom fil, manglende felt/verdi/uke, ugyldig dato, duplikat, negativ mengde og nullsalg. Avvist import skal ikke ødelegge eksisterende data. Rettelser bevarer original og begrunnelse. |
| Referanse og MAE | Kontroller sesongnaiv prognose mot håndregnede verdier. Faktisk 10 og 14 mot prognose 12 og 11 gir MAE 2,5. |
| Tidsserieevaluering | Trening slutter ved uke 68, 80 og 92; prognoser gjelder henholdsvis 69–80, 81–92 og 93–104. Endringer etter en prognoseopprinnelse skal ikke endre dens prognose. Siste vindu holdes separat fra modellvalg. |
| Regresjon | Kun trend og årlige sinus-/cosinusledd; ingen automatisk tuning. Negative prognoser settes til null. Samme horisont og testobservasjoner som referansen. |
| Scenarioer | Kontroller +10 % og −10 %, endrede prosentsatser, separat margin og begrunnede overstyringer. Ikke-negative mengder og konsistent avrunding av godkjente heltallsverdier. Scenarioer merkes som antakelser, ikke prediksjonsintervaller. |
| Godkjenning/eksport | Eksportverdier er identiske med godkjenningsøyeblikksbildet. Alle valg og datagrunnlag er sporbare. En ny godkjenning endrer ikke tidligere godkjenninger. |
| Tilgang | Uten innlogging avvises lesing, beregning, endring, godkjenning og eksport, også gjennom direkte serverforespørsler. Ingen ekstra roller kreves. |
| Brukeropplevelse | En annen person gjennomfører hovedflyten. Kontroller forståelige avviksmeldinger, tastaturnavigasjon og etiketter. Noter og prioriter problemer. |
| Kjørbarhet | Følg README i et rent miljø uten personlige nøkler eller betalte tjenester. Last eksempeldata, bruk demokonto og gjenskap sammenligningen. Kontroller publisert demo dersom den inngår i leveransen. |

Leveransen er ferdig når alle må-krav har bestått relevante kontroller, hovedflyten virker, godkjente mengder er riktige, data bevares og tilgangskravene håndheves. Modellresultater skal være dokumentert selv når regresjonen er dårligere enn referansen. Kodeversjon, oppsett, testbevis og kjente mindre feil følger leveransen.

## 5. Risiko og kontrollpunkter

| Kontrollpunkt / risiko | Handling |
|---|---|
| 10. november: Restarbeid overstiger tilgjengelig tid | Reestimer og avklar kapasitet og eventuell leveranseendring med faglærer. Ikke marker uferdig arbeid som fullført. |
| 13. november: Import og tilgang virker ikke | Stopp annet arbeid og løs grunnflyten. Bruk reserve ved konkrete hindringer. |
| 18. november: Modellene kan ikke sammenlignes korrekt | Prioriter den fastsatte, enkle regresjonen og evalueringslogikken. Ikke bruk tid på flere modeller eller å tvinge fram bedre MAE. |
| 20. november: Hovedflyten er ufullstendig | Rett integrasjonsfeil før brukertest. Dokumenter og avklar eventuelle endringer i må-krav. |
| 27. november: Leveringskandidat mangler | Bruk gjenværende reserve på blokkerende feil; behold siste fungerende kodeversjon. |
| Syntetiske resultater mistolkes | Merk demonstrasjonsdata og begrensninger tydelig. Ikke hev effekt hos en virkelig bedrift. |
| Full holdout påvirker modellendringer | Opplys om det, og reserver et nytt urørt testdatasett som beskrevet i addendumet. |
| Omfang vokser eller publisering tar for lang tid | Hold utvidelser utenfor v1. Test nødvendig publisering tidlig og behold reproduserbar lokal kjøring. |

Tilgangskontroll, korrekt evaluering og sporbar godkjenning skal ikke fjernes for å møte datoen. Endringer i må-krav krever en dokumentert beslutning og oppdaterte krav; de skal ikke skjules i implementasjonen.

## 6. Leveringspakke 1. desember

1. Kodeversjon med README, lokalt oppsett og demonstrasjonskonto uten produksjonshemmeligheter.
2. Generator, syntetiske filer, parameter-/feilmanifest og dataformatbeskrivelse.
3. Brief, addendum, krav og prosjektplan med faktisk status.
4. Modellbeskrivelse, MAE-resultater, evalueringsvinduer og begrensninger.
5. Testoversikt, brukerveiledning og kjente feil.
6. Repeterbar demonstrasjon av import → prognose → scenario → godkjenning → eksport.
7. Nettadresse dersom emnet krever publisering, samt refleksjon over KI-bruk og avvik fra planen.

## 7. Statusmal

```text
Uke / dato:
Mål:
Fullført og kontrollert (med krav- og kodehenvisning):
Planlagte / faktiske timer:
Reserve brukt / igjen:
Feil eller hindringer:
Endringer i omfang og estimat:
Neste tre oppgaver:
Status mot 01.12.2026: i rute / risiko / forsinket
```

**Første praktiske steg:** Kartlegg faktisk implementasjonsstatus og gjenstående kapasitet ved neste arbeidsøkt. Bruk dette til å bekrefte eller justere estimatene før videre utvikling.
