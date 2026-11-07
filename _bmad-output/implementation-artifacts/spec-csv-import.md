---
title: 'CSV-opplasting og datavalidering'
type: 'feature'
created: '2026-11-07'
status: 'done'
route: 'oneshot'
---

<frozen-after-approval>

## Intent

Last opp CSV-salgshistorikk og vis gyldige data i eksisterende produktvelger, graf og tabell. Valider obligatoriske felt, dato, mandagsuker, mengde, enhet, duplikater og manglende interne uker. Skill null fra manglende data. Avvis ugyldig fil samlet og vis feil per rad. Høye avvik gir varsler uten automatisk retting. Ingen permanent lagring eller rettingseditor i dette trinnet; brukeren retter originalfilen og laster opp på nytt.

</frozen-after-approval>

## Implementation Notes

- Validering isolert i sales_data.py; app.py bruker opplastede data kun når hele filen er gyldig.
- README dokumenterer UTF-8, format, grenser og fravær av permanent lagring.
- Tester: ren fil med 520 rader, feilfil, duplikat, manglende uke, ugyldig dato, tom fil/verdi, negativ mengde, NaN, ukestart, enhet, nullsalg og eksisterende produktvisning.

## Review Triage Log

- Medium, rettet: flyttallsparsing kunne runde desimal input til heltall. Erstatter med eksakt siffervalidering og regresjonstest.
