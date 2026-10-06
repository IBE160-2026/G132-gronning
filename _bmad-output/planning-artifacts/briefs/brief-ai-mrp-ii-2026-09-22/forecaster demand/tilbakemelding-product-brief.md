# Tilbakemelding på product brief

| | |
|---|---|
| **Gruppe** | G132 – G132-gronning |
| **Product brief** | `_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/forecaster demand/brief.md` (commit `4e45446`) |
| **Tilbakemelding fra** | Faglærer i IBE160 (utarbeidet med KI-støtte) |
| **Dato** | 2026-10-06 |

Vurdert fil: `brief.md` i undermappen `forecaster demand`, sammen med `addendum.md` i mappen over (`brief-ai-mrp-ii-2026-09-22`). Det finnes ennå ikke PRD, arkitektur eller epics. Tips: unngå mellomrom i mappenavn (for eksempel `forecaster-demand`), siden det ofte gir problemer i kommandolinjen og lenker.

## Samlet vurdering

- **Godt utgangspunkt med justeringer.** Gruppen kan gå videre og innarbeide punktene under.

**Det som er bra:**

1. Avgrensningen er klok. Av hele MRP II-forslaget velger dere bare modul 4.1 Prognoser og Demand Management som MVP, og resten (MPS, BOM/MRP, kapasitet, detaljplanlegging) er tydelig lagt til senere. Dataflyten i addendumet viser at dere forstår hvordan modulen henger sammen med resten.
2. Evalueringsopplegget er faglig solid og ærlig: KI-kandidaten skal sammenlignes med en enkel baseline (naiv eller sesongnaiv) på de samme historiske testperiodene med MAE, uten å bruke fremtidige observasjoner, og «results are reported even if AI performs no better». Det er akkurat slik KI-bidrag bør kontrolleres.

**De viktigste endringene:**

1. Velg datasett nå, og bruk gjerne syntetiske data. Bransje, bedrift og datasett er ikke valgt, og flere deler av briefen avhenger av det. Lag et syntetisk datasett med kjent trend, sesong og noen innlagte avvik og manglende verdier, for eksempel 5 produkter og 104 uker. Da vet dere hva det riktige svaret er, og kan kontrollere både datavalidering og prognoser. Et reelt eller anonymisert datasett kan komme i tillegg.
2. Avklar hva «AI» er i appen. Briefen snakker om en «AI-based candidate» og om at KI skal støtte metodevalg og finne avvik, men metoden skal velges «after inspecting the dataset». Bestem én konkret kandidat (for eksempel eksponentiell glatting eller en enkel regresjonsmodell med sesongledd fra et kjent bibliotek), og si om en språkmodell skal brukes til forklaringer. Det påvirker arkitektur, testing og kjørbarhet.
3. Forenkle tilgangsstyringen i v1. Tre roller (administrator, planlegger, kun lesetilgang) med tilgangskontroll på serveren gir mye ekstra arbeid for én person. Start med innlogging og én planleggerrolle, og legg til lesetilgang hvis det blir tid.

## Vanskelighetsgrad og gjennomførbarhet

### Vurdert vanskelighetsgrad

- **Vanskelig**

**Sammenlignbart med:** 4) KI-støttet MRP II, avgrenset til 4.1) Prognoser og Demand Management (vanskelig). Avgrensningen til én modul gjør prosjektet mer overkommelig, men prognoser med korrekt tidsserieevaluering, scenarioer, versjonering og rollebasert tilgang holder det på vanskelig nivå.

**Begrunnelse:**

| Faktor | Nivå (lav / middels / høy) | Kommentar |
|---|---|---|
| Domenelogikk – hvor mange og hvor kompliserte regler og beregninger må stemme? | Høy | Prognosemetoder, tidsseriekryssvalidering, MAE, scenarioer, sikkerhetsmargin og forskjellen mellom manglende data og null salg. Må være faglig riktig. |
| Datamodell – antall entiteter og relasjoner mellom dem | Middels | Produkt, periode, salgshistorikk, ordre, signal, datasettversjon, prognose, scenario, godkjent plan og bruker. |
| Brukere, roller og innlogging | Middels til høy | Tre roller med ulike rettigheter, også håndhevet på serveren. |
| KI-funksjonalitet i appen, f.eks. kall til språkmodell, prompts i koden og håndtering av usikre svar | Middels | Maskinlæringsbasert prognose som sammenlignes med baseline. Språkmodell er bare en valgfri utvidelse. |
| Integrasjoner og eksterne tjenester, f.eks. API-er, betaling og e-post | Lav | Ingen eksterne systemer i v1. ERP og leverandørportaler er utelatt. |
| Sanntid, samtidighet eller flere brukere som påvirker hverandre | Lav | Ingen, ut over godkjenning og versjonering. |
| Filhåndtering, f.eks. opplasting, PDF-lesing og eksport | Middels | CSV-import med validering, og CSV-eksport av godkjent plan. |
| Sikkerhet og personvern | Middels | Forretningskritiske data og tilgangskontroll. Med syntetiske data blir risikoen lav i praksis. |

**Hva vanskelighetsgraden betyr for dere:**

- _Vanskelig:_ Et vanskelig prosjekt gir større mulighet for toppkarakter, men også større risiko. Definer en minimal versjon som sikkert kan bli ferdig, og legg resten i tydelige trinn etterpå.

### Gjennomførbarhet med BMAD og Claude Code

| Spørsmål | Vurdering (OK / risiko / stor risiko) | Kommentar |
|---|---|---|
| **Tid og omfang** – kan v1 realistisk bli ferdig og stabil i løpet av semesteret, med tid til flere iterasjoner? | Risiko | Én modul er realistisk, men MVP-tabellen har sju områder, inkludert roller og versjonering. For én person bør v1 strammes inn. |
| **BMAD-flyten** – er briefen konkret nok til at PRD, arkitektur og stories kan lages uten store hull, og blir det overkommelig mange stories? | Risiko | Flyten og reglene i addendumet er svært konkrete, men datasett og KI-metode er uavklart, og mange punkter er merket [ASSUMPTION]. Avklar dem før PRD. |
| **Egnet for Claude Code** – bruker løsningen en vanlig, godt dokumentert teknologistakk som Claude Code håndterer godt, eller krever den nisjeteknologi, spesialmaskinvare eller mye manuell konfigurasjon? | OK | En webapp med et kjent bibliotek for tidsserier og diagrammer er godt egnet. Velg en stakk der prognosebiblioteket er godt dokumentert. |
| **Kontroll på KI-ens arbeid** – kan gruppen selv avgjøre om koden gjør det riktige? Krever domenet kunnskap gruppen ikke har, f.eks. avanserte beregninger eller fagregler, så er det vanskelig å kvalitetssikre. | Risiko | Feil i tidsserieevaluering (for eksempel lekkasje av fremtidige data) er lett å gjøre og vanskelig å oppdage. Syntetiske data med kjent fasit og håndregnede baseline-eksempler gjør det kontrollerbart. |
| **Testbarhet** – finnes det tydelige regler og forventede resultater som tester kan skrives mot? | OK | Datavalidering, baseline-prognoser, MAE og tilgangskontroll kan testes med faste forventede verdier. |
| **Kjørbar for sensor** – kan appen kjøres lokalt etter README, uten gruppens nøkler, betalte kontoer eller egen infrastruktur? | OK | Prognosene beregnes lokalt og krever ingen betalt tjeneste. Legg med eksempeldatasett og testbrukere. |
| **Avhengigheter og kostnader** – krever løsningen betalte API-er, f.eks. språkmodeller, og finnes det en plan for kostnad, testmodus eller mock-data? | OK | Ingen betalte API-er er nødvendige. En eventuell språkmodell for forklaringer må kunne slås av. |

**Konklusjon om gjennomførbarhet:**

- **Gjennomførbart med justert omfang.** Se forslagene under.

**Forslag til justering av omfang eller vanskelighetsgrad:**

1. V1: CSV-import av syntetisk salgshistorikk, datavalidering med synlige avvik, sesongnaiv baseline og én ML-kandidat, MAE-sammenligning, tre scenarioer med synlig justering, og godkjenning og eksport av plan. Én innlogget planlegger.
2. Neste trinn: kundeordre og kampanjesignaler som input, flere roller, full versjonering med sporing av alle endringer, og eventuelt språkmodell som forklarer prognosen.

## Hvorfor product brief er viktig for mappen

Product brief er utgangspunktet for PRD, arkitektur, stories og til slutt koden. Del 1 av mappen vurderes blant annet på om sensor kan følge en sporbar vei fra plan til ferdig app. Den vurderes også på om appen gjør det dere har beskrevet, om den er testet, om den er godt designet, og om den kan kjøres etter README. Et uklart, for stort eller for lite brief gjør alt dette vanskeligere senere. Det er mye enklere å rette nå enn sent i semesteret.

## 1. Gjennomgang av briefens deler

| Del av brief | Status | Kommentar |
|---|---|---|
| Executive Summary – er det klart hva appen er, og hvilket problem den løser? | OK | Klart: prognoser for etterspørsel som planleggeren kan vurdere, justere og godkjenne, som første modul i MRP II. |
| The Problem – er problemet konkret, med reelle situasjoner og brukere? | Juster | Problemet er forståelig, men markert som antakelse som må valideres. Gi et konkret eksempel, for eksempel et produkt med sesongtopp der feil prognose gir tomt lager. |
| The Solution – beskriver løsningen brukeropplevelsen, ikke bare teknologi? | OK | Beskriver flyten fra import via avvik, prognosesammenligning og scenarioer til godkjent plan. |
| What Makes This Different – er vurderingen ærlig og realistisk? | OK | Ærlig: det finnes ennå ikke bevis for at KI gir bedre prognoser på det valgte datasettet. Verdien ligger i sporbar læring og beslutningsflyt. |
| Who This Serves – er primærbrukerne tydelige, og vet vi hva de trenger? | Juster | Produksjons- eller etterspørselsplanleggeren er tydelig. Salgssjef, studenter og faglærer som brukere gjør bildet uklart. Hold fokus på planleggeren i v1. |
| Success Criteria – kan kriteriene faktisk sjekkes eller testes? | OK | Svært gode og testbare kriterier: lik testperiode for baseline og KI, sporbarhet for godkjent plan og tilgangstest. |
| Scope – er det klart hva som er med i første versjon, og hva som ikke er det? | Juster | Tydelig MVP-tabell og utelatte moduler. Stram inn v1 (roller, signaler og versjonering), og avklar datasettet som avgjør hva som er mulig. |
| Vision – henger visjonen sammen med resten uten å blåse opp omfanget? | OK | Neste moduler er tydelig lagt etter MVP. |

## 2. Utgangspunkt for del 1 av mappen

Punktene følger kriteriene i sensorveiledningen for del 1. Vektene i parentes viser hvor mye hvert kriterium teller i del 1.

| Kriterium i del 1 | Hva briefen bør legge til rette for | Status | Kommentar |
|---|---|---|---|
| **1. Prosess og KI-styring** (30 %) | Brief som er presis nok til at PRD og stories kan bygges direkte på den, slik at krav kan spores fra brief til kode. | Juster | Brief og addendum gir et godt grunnlag, men antakelsene må avklares først. Commit-meldingene («product brief») kan gjerne være mer beskrivende, og lagre promptene. |
| **2. Funksjonalitet og omfang** (20 %) | Realistisk omfang for gruppen og semesteret: en tydelig kjerneflyt som kan bli ferdig og stabil, og nok innhold til å vise reell funksjonalitet. | Juster | Tydelig kjerneflyt med rikelig innhold. Stram inn v1 for å sikre at den blir stabil. |
| **3. Kvalitetssikring og testing** (15 %) | Suksesskriterier og funksjoner som er konkrete nok til å bli testtilfeller. | OK | Evalueringsopplegget og tilgangstesten er gode utgangspunkt. Syntetiske data med kjent fasit vil gjøre dette til en styrke. |
| **4. Design og brukeropplevelse** (10 %) | Tydelige brukere og brukssituasjoner som designet kan bygges rundt, gjerne med de viktigste skjermbildene eller flytene skissert. | Juster | Flyten er tydelig. Skisser hovedvisningen med historikk, prognose, feilmål og scenarioer i ett diagram, og hvordan avvik vises. |
| **5. Kodekvalitet og arkitektur** (10 %) | Teknologivalg som er begrunnet og ikke mer komplekse enn appen trenger. | Juster | Teknologi er ikke valgt. Hold prognose- og evalueringslogikken i en egen, testbar del av koden, og begrunn valget av bibliotek. |
| **6. README og kjørbarhet** (10 %) | Løsning som andre kan kjøre lokalt uten betalte kontoer, og uten tilgang til gruppens egne tjenester og nøkler. | OK | Lokal beregning uten betalte tjenester. Sørg for at eksempeldata og testbrukere følger med. |
| **7. Ryddighet i repoet** (5 %) | En plan for hvor hemmeligheter, testdata og dokumentasjon skal ligge. | Juster | Addendumet sier riktig at sensitive rådata ikke skal i versjonskontroll. Legg syntetiske data i en egen mappe, og unngå mellomrom i mappenavn. |

## 3. Neste steg for gruppen

1. Lag eller velg datasettet (gjerne syntetisk med kjent trend, sesong og avvik), og bestem antall produkter, ukeperioder og 12-ukers horisont.
2. Bestem én konkret KI-/ML-kandidat og om en språkmodell skal brukes, og avklar de viktigste [ASSUMPTION]-punktene.
3. Stram inn v1 (én rolle, salgshistorikk som eneste obligatoriske input), og lag deretter PRD med BMAD.

Oppdater product brief i repoet når dere har gjort endringene, slik at historikken viser hvordan planen utviklet seg. Det er en del av prosessen sensor ser etter.
