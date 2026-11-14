# Designgjennomgang – fra salgshistorikk til plan

Dato: 14. november 2026. Status: designretning godkjent av brukeren;
overføring til Streamlit gjennomføres i `spec-samlet-arbeidsflate.md`.

## Formål og grunnlag

Gjennomgangen gjelder `samlet-oversikt.html`, introdusert i commit
`13265b4`. Commiten la til prototypen og fire linjer i endringsloggen:
to filer, 41 nye linjer. Prototypen samler produktvalg, prognose,
scenario og plan i samme arbeidsflate. Dagens funksjoner i `app.py`
er sammenligningsgrunnlag. Dette dokumentet registrerer anbefalinger,
opprinnelig som grunnlag for brukerens designbeslutning.

## Gjennomgang

1. **Velg produkt og metode.** `outputs/designforslag/samlet-oversikt.html:17`
   samler valgene øverst. Anbefaling: ett metodevalg skal styre både graf,
   scenario og plantabell. Produktbytte skal beholde prosentvalgene,
   slik dagens app gjør.
2. **Se konsekvensen av valgene.** `outputs/designforslag/samlet-oversikt.html:19`
   viser historikk, prognose og plan i samme graf.
   Anbefaling: vis siste 24 historikkuker og alle 12 fremtidsuker,
   med faktiske datoer, tydelig skille og tilgang til hele historikken.
3. **Juster scenario og margin.** `outputs/designforslag/samlet-oversikt.html:20`
   plasserer kontrollene ved grafen. Behold dette oppsettet på bred skjerm;
   bruk én kolonne på smal skjerm. Behold dagens justerbare høy-/lavsatser
   og gyldige prosentområder. Skissens faste ±10 % og margin 0–30 %
   skal ikke innskrenke appens eksisterende funksjoner.
4. **Vurder metode og plan.** `outputs/designforslag/samlet-oversikt.html:22`
   viser MAE og planutdrag. Erstatt faste eksempeltall med beregnet MAE
   for valgt produkt og separat holdout. Vis alle 12 planuker i full tabell.
   Manglende evalueringsgrunnlag skal gi forklaring, aldri illustrativ score.
5. **Undersøk grunnlaget.** `outputs/designforslag/samlet-oversikt.html:23`
   samler import og beregningsdetaljer i utvidbare felt. Behold tilgjengelig
   import, datasettversjoner, rettelser, full MAE-tabell og observasjoner.
   Aktiv datakilde og viktige importfeil må fortsatt være synlige.

## Forhold som må vurderes før overføring

- Prototypens graf genererer egne illustrasjonstall, og MAE-stolpene er faste.
  De sier derfor ingenting om metodens kvalitet på valgt produkt.
- Scenariobåndet er en planleggingsantakelse. Det må omtales slik og ha
  tekstforklaring; farge alene skal ikke formidle betydningen.
- Totalen i skissen avrundes til heltall, mens radene viser én desimal.
  Visningsavrunding må forklares. Beregningsverdiene beholdes uten avrunding;
  regel for godkjente heltallsmengder avklares med plangodkjenningen.
- Lyst/mørkt tema er demonstrert i HTML. Bruk Streamlits tilgjengelige
  temafunksjoner ved overføring og kontroller lesbarhet i begge temaer.
- Ingen visuell nettlesertest eller brukertest er utført i denne økten.
  Vurderingene bygger på kildekoden og eksisterende dokumentasjon.

## Forslag til første implementasjonsleveranse

Overfør den samlede arbeidsflaten til Streamlit med eksisterende data,
prognoseberegninger og lagring. Produkt- og metodevalg øverst, samlet graf
med scenariofelt ved siden av, MAE og 12-ukerstabell under, utdypende
datagrunnlag i utvidbare felt. Behold eksisterende validering og beregningsregler.

Innlogging, uforanderlig plangodkjenning og eksport av den godkjente planen
følger som egne leveranser. De skal ikke fremstå som ferdige funksjoner i
arbeidsflaten før de er implementert.

## Slik kan designet prøves av brukeren

Åpne `samlet-oversikt.html` i nettleseren:

- Bytt produkt og metode. Graf, totalsum og planutdrag skal oppdateres.
  MAE-feltet er fortsatt faste eksempeltall i denne skissen.
- Velg høy etterspørsel og margin 10 %. Planen skal bli 1,21 ganger
  normalprognosen før visningsavrunding.
- Bytt lyst/mørkt tema og gjør vinduet smalt. Vurder lesbarhet og om
  rekkefølgen graf → justering → MAE → tabell er forståelig.

Ved implementasjon kontrolleres også CSV-feil, gjenåpning av lagret datasett,
produktbytte med beholdte prosenter, kort historikk og samsvar mellom
graf, tabell og total. Eksisterende relevante tester kjøres da.

## Beslutning

Brukeren godkjente retningen med «gjør anbefalingen» 14. november 2026.
Den samlede arbeidsflaten og tilpasningene ovenfor overføres til Streamlit.
Visuell kontroll av smal skjerm og lyst/mørkt tema gjenstår; nettlesertilgangen
var blokkert under implementasjonsøkten.
