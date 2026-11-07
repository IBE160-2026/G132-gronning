# Endringsoversikt fra prosjektstart

Oversikten bygger på lokal Git-historikk fra første commit 15. september 2026 til og med b8cea5b (7. november 2026). Datoer og klokkeslett nedenfor er fra commitene med tidssone. Dette er tidspunktet endringen ble registrert i Git, ikke nødvendigvis tidspunktet arbeidet startet.

Git er fasiten for historiske filversjoner. Hver lenke åpner den eksakte endringen på GitHub. Oversikten dokumenterer committede endringer; ignorerte filer som .venv, lokal PATH og arbeid før første commit er ikke rekonstruerbare fra Git alene. Testresultater er historiske opplysninger fra specs/sesjonslogg, ikke en ny testkjøring.

## Finn riktig område ved feil

| Symptom eller område | Se først i | Første relevante commit |
|---|---|---|
| Oppstart eller avhengigheter | app.py, requirements.txt, README.md | c3ecc75 |
| Salgstall, produktnavn og sesongmønster | data/synthetic/ og manifest.json | f542a10 |
| Produktvalg, graf og historikktabell | app.py, tests/test_sales_view.py | f53104e |
| CSV avvises eller godtas feil | sales_data.py, tests/test_sales_data.py | 4a0f6bb |
| Feil prognose, sesongforskyvning eller MAE | forecasting.py, tests/test_forecasting.py | 5971ea2 |
| Feil scenario eller sikkerhetsmargin | scenarios.py, tests/test_scenarios.py | e3487f5 |
| BMAD eller Codex-skills | _bmad/, .agents/skills/ | 6d118b9 |
| Scope, kapasitet og frist | brief.md, addendum.md, prosjektplan.md under _bmad-output/ | e403e66 og 5971ea2 |

## Viktige beslutninger og kontrollbevis

- e403e66: Innarbeidet faglærertilbakemelding; avgrenset v1, syntetisk datasett, én planleggerrolle og konkret regresjonskandidat i daværende plan.
- f542a10: Fem generiske friluftsprodukter, 104 uker hver og seed 132. Alle salgstall er syntetiske, ikke hentet fra en virkelig butikk. Ren fil og separat feilfil.
- c3ecc75: Kjørbar Streamlit-startside; oppstartstest og avhengighetskontroll dokumentert i spec og sesjonslogg.
- 4a0f6bb: Samlet avvisning av ugyldig CSV, radfeil og avviksvarsler; nullsalg skilles fra manglende data. Desimalverdier valideres uten stille flyttallsavrunding. Fire tester dokumentert som bestått.
- 5971ea2: SCM200 våren 2026 ble faglig grunnlag. MA(4), enkel eksponensiell glatting med alfa 0,3 og sesongnaiv 52-ukersreferanse erstattet regresjon etter brukerbeslutning. Tolvukers testvinduer og separat holdout. Ni tester dokumentert som bestått. Planen endret til fire timer per uke og uke 51.
- e3487f5: Normal, høy og lav etterspørsel; margin anvendes separat på valgt scenario. Desimaler beholdes. Tolv tester dokumentert som bestått. Ingen permanent lagring eller godkjenning i dette trinnet.

## Full kronologisk commitoversikt

A = lagt til, M = endret, D = slettet, R = omdøpt. Filene er oppgitt med hele repo-relative stier. BMAD-installasjonen har mange leverandørfiler og er derfor også samlet i en sammenleggbar filliste. Loggcommits endrer dokumentasjon, ikke appfunksjonalitet.

### 2026-09-15T21:29:53+02:00 | Initialiser gruppeprosjekt for IBE160

Commit: [5acb653](https://github.com/IBE160-2026/G132-gronning/commit/5acb65353a476bd163d00e7d19ba78701bb118bc)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	.gitignore
A	README.md
```

</details>

### 2026-09-22T17:24:33+02:00 | product brief

Commit: [4e45446](https://github.com/IBE160-2026/G132-gronning/commit/4e454462d0ef3534e9828e49f641701500a70f62)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/forecaster demand/brief.md
```

</details>

### 2026-09-23T11:40:01+02:00 | product brief

Commit: [0e2aca5](https://github.com/IBE160-2026/G132-gronning/commit/0e2aca5f112532da3b3fbc5f11f35211a605e1ec)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/.memlog.md
A	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/addendum.md
```

</details>

### 2026-10-06T12:03:19+02:00 | Legg til tilbakemelding på product brief

Commit: [b5f6bc6](https://github.com/IBE160-2026/G132-gronning/commit/b5f6bc6e2a71a5d3290011c35cf6ea4abf58183e)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/forecaster demand/tilbakemelding-product-brief.md
```

</details>

### 2026-10-26T18:08:40+01:00 | Legg til sesjonslogg-skill

Commit: [017858a](https://github.com/IBE160-2026/G132-gronning/commit/017858a41ad2df235848dbc26da52d35b47cbe56)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	.claude/skills/sesjonslogg/SKILL.md
```

</details>

### 2026-10-26T19:37:06+01:00 | Oppdater sesjonslogg-skill og instruks

Commit: [d84d1b6](https://github.com/IBE160-2026/G132-gronning/commit/d84d1b6e6a0624d2f996cfd3241ee49923923ec1)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.claude/skills/sesjonslogg/SKILL.md
A	CLAUDE.md
```

</details>

### 2026-11-07T12:04:39+01:00 | Innarbeid tilbakemelding i produktbrief og prosjektplan

Commit: [e403e66](https://github.com/IBE160-2026/G132-gronning/commit/e403e668045c8e71e82fa976fb9ecbf88b1c3449)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/addendum.md
M	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/forecaster demand/brief.md
A	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/forecaster demand/prosjektplan.md
```

</details>

### 2026-11-07T12:16:08+01:00 | Logg: friluftsdata

Commit: [efe0c44](https://github.com/IBE160-2026/G132-gronning/commit/efe0c44c57f5a96cc1b3322aee962e0a66e6f265)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
A	.logs/vsalte/issues.md
```

</details>

### 2026-11-07T12:19:40+01:00 | Legg til syntetiske salgsdata for fem friluftsprodukter

Commit: [f542a10](https://github.com/IBE160-2026/G132-gronning/commit/f542a10ef27b4be5b2ddc393a5b8abc9097bc37f)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	data/synthetic/README.md
A	data/synthetic/generate_data.py
A	data/synthetic/manifest.json
A	data/synthetic/products.csv
A	data/synthetic/sales_history_clean.csv
A	data/synthetic/sales_history_validation.csv
```

</details>

### 2026-11-07T12:21:29+01:00 | Logg: friluftsdata

Commit: [ab5e423](https://github.com/IBE160-2026/G132-gronning/commit/ab5e423a272f78a2d8ef98ea3152170e26bf6ad1)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
```

</details>

### 2026-11-07T12:28:29+01:00 | Logg: BMAD-reparasjon

Commit: [00b7837](https://github.com/IBE160-2026/G132-gronning/commit/00b783740afc705317af7c029107c1b37a9dffbc)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
M	.logs/vsalte/issues.md
```

</details>

### 2026-11-07T12:33:28+01:00 | feat: opprett kjørbar Streamlit-startside

Commit: [c3ecc75](https://github.com/IBE160-2026/G132-gronning/commit/c3ecc7561b10f84e2c8b09e5eac54cb5fa581d05)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	README.md
A	_bmad-output/implementation-artifacts/spec-streamlit-oppstart.md
A	app.py
A	requirements.txt
```

</details>

### 2026-11-07T12:33:32+01:00 | Logg: Streamlit-oppstart

Commit: [c9d5f44](https://github.com/IBE160-2026/G132-gronning/commit/c9d5f44fbb26f6933f264cb6ac8f73493f53e2c4)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
M	.logs/vsalte/issues.md
```

</details>

### 2026-11-07T12:36:38+01:00 | chore: legg til reparert BMAD-oppsett og Codex-skills

Commit: [6d118b9](https://github.com/IBE160-2026/G132-gronning/commit/6d118b93ba352a10ea6236c7a5002088a63cfca4)

<details>
<summary>Berørte filer og endringstype</summary>

```text
A	.agents/skills/bmad-advanced-elicitation/SKILL.md
A	.agents/skills/bmad-advanced-elicitation/assets/methods.csv
A	.agents/skills/bmad-advanced-elicitation/customize.toml
A	.agents/skills/bmad-advanced-elicitation/scripts/pick_methods.py
A	.agents/skills/bmad-advanced-elicitation/scripts/tests/test_pick_methods.py
A	.agents/skills/bmad-agent-analyst/SKILL.md
A	.agents/skills/bmad-agent-analyst/customize.toml
A	.agents/skills/bmad-agent-architect/SKILL.md
A	.agents/skills/bmad-agent-architect/customize.toml
A	.agents/skills/bmad-agent-dev/SKILL.md
A	.agents/skills/bmad-agent-dev/customize.toml
A	.agents/skills/bmad-agent-pm/SKILL.md
A	.agents/skills/bmad-agent-pm/customize.toml
A	.agents/skills/bmad-agent-ux-designer/SKILL.md
A	.agents/skills/bmad-agent-ux-designer/customize.toml
A	.agents/skills/bmad-architecture/SKILL.md
A	.agents/skills/bmad-architecture/assets/spine-template.md
A	.agents/skills/bmad-architecture/customize.toml
A	.agents/skills/bmad-architecture/references/headless.md
A	.agents/skills/bmad-architecture/references/reviewer-gate.md
A	.agents/skills/bmad-architecture/scripts/lint_spine.py
A	.agents/skills/bmad-architecture/scripts/tests/test_lint_spine.py
A	.agents/skills/bmad-brainstorming/SKILL.md
A	.agents/skills/bmad-brainstorming/assets/brain-icons.json
A	.agents/skills/bmad-brainstorming/assets/brain-methods.csv
A	.agents/skills/bmad-brainstorming/assets/brain-selector.html
A	.agents/skills/bmad-brainstorming/customize.toml
A	.agents/skills/bmad-brainstorming/references/converge.md
A	.agents/skills/bmad-brainstorming/references/finalize.md
A	.agents/skills/bmad-brainstorming/references/headless.md
A	.agents/skills/bmad-brainstorming/references/in-chat-techniques.md
A	.agents/skills/bmad-brainstorming/references/mode-autonomous.md
A	.agents/skills/bmad-brainstorming/references/mode-facilitator.md
A	.agents/skills/bmad-brainstorming/references/mode-partner.md
A	.agents/skills/bmad-brainstorming/references/resume.md
A	.agents/skills/bmad-brainstorming/scripts/brain.py
A	.agents/skills/bmad-brainstorming/scripts/tests/test_brain.py
A	.agents/skills/bmad-build-auto/SKILL.md
A	.agents/skills/bmad-build-auto/compile-epic-context.md
A	.agents/skills/bmad-build-auto/customize.toml
A	.agents/skills/bmad-build-auto/references/claims-check.md
A	.agents/skills/bmad-build-auto/references/deletion-check.md
A	.agents/skills/bmad-build-auto/review-prompts/edge-case-hunter.md
A	.agents/skills/bmad-build-auto/review-prompts/verification-gap.md
A	.agents/skills/bmad-build-auto/spec-template.md
A	.agents/skills/bmad-build-auto/step-01-clarify-and-route.md
A	.agents/skills/bmad-build-auto/step-02-plan.md
A	.agents/skills/bmad-build-auto/step-03-implement.md
A	.agents/skills/bmad-build-auto/step-04-review.md
A	.agents/skills/bmad-build-auto/workflow.md
A	.agents/skills/bmad-build/SKILL.md
A	.agents/skills/bmad-build/compile-epic-context.md
A	.agents/skills/bmad-build/customize.toml
A	.agents/skills/bmad-build/references/claims-check.md
A	.agents/skills/bmad-build/references/deletion-check.md
A	.agents/skills/bmad-build/review-prompts/edge-case-hunter.md
A	.agents/skills/bmad-build/review-prompts/verification-gap.md
A	.agents/skills/bmad-build/spec-template.md
A	.agents/skills/bmad-build/step-01-clarify-and-route.md
A	.agents/skills/bmad-build/step-02-plan.md
A	.agents/skills/bmad-build/step-03-implement.md
A	.agents/skills/bmad-build/step-04-review.md
A	.agents/skills/bmad-build/step-05-present.md
A	.agents/skills/bmad-build/step-oneshot.md
A	.agents/skills/bmad-build/sync-sprint-status.md
A	.agents/skills/bmad-build/workflow.md
A	.agents/skills/bmad-code-review/SKILL.md
A	.agents/skills/bmad-code-review/customize.toml
A	.agents/skills/bmad-code-review/references/claims-check.md
A	.agents/skills/bmad-code-review/references/deletion-check.md
A	.agents/skills/bmad-code-review/review-prompts/edge-case-hunter.md
A	.agents/skills/bmad-code-review/review-prompts/verification-gap.md
A	.agents/skills/bmad-code-review/steps/step-01-gather-context.md
A	.agents/skills/bmad-code-review/steps/step-02-review.md
A	.agents/skills/bmad-code-review/steps/step-03-triage.md
A	.agents/skills/bmad-code-review/steps/step-04-present.md
A	.agents/skills/bmad-correct-course/SKILL.md
A	.agents/skills/bmad-correct-course/checklist.md
A	.agents/skills/bmad-correct-course/customize.toml
A	.agents/skills/bmad-create-epics-and-stories/SKILL.md
A	.agents/skills/bmad-create-epics-and-stories/customize.toml
A	.agents/skills/bmad-create-epics-and-stories/steps/step-01-validate-prerequisites.md
A	.agents/skills/bmad-create-epics-and-stories/steps/step-02-design-epics.md
A	.agents/skills/bmad-create-epics-and-stories/steps/step-03-create-stories.md
A	.agents/skills/bmad-create-epics-and-stories/steps/step-04-final-validation.md
A	.agents/skills/bmad-create-epics-and-stories/templates/epics-template.md
A	.agents/skills/bmad-customize/SKILL.md
A	.agents/skills/bmad-customize/scripts/list_customizable_skills.py
A	.agents/skills/bmad-customize/scripts/tests/test_list_customizable_skills.py
A	.agents/skills/bmad-deep-recon/SKILL.md
A	.agents/skills/bmad-deep-recon/assets/research.template.md
A	.agents/skills/bmad-deep-recon/customize.toml
A	.agents/skills/bmad-deep-recon/references/draft.md
A	.agents/skills/bmad-deep-recon/references/finalize.md
A	.agents/skills/bmad-deep-recon/references/html-briefing.md
A	.agents/skills/bmad-deep-recon/references/lifecycle.md
A	.agents/skills/bmad-deep-recon/references/process.md
A	.agents/skills/bmad-deep-recon/references/run.md
A	.agents/skills/bmad-deep-recon/references/selection.md
A	.agents/skills/bmad-deep-recon/references/synthesis.md
A	.agents/skills/bmad-deep-recon/references/verification.md
A	.agents/skills/bmad-deep-recon/scripts/recon_kit.py
A	.agents/skills/bmad-deep-recon/scripts/tests/test_recon_kit.py
A	.agents/skills/bmad-deep-recon/types/academic-lit.md
A	.agents/skills/bmad-deep-recon/types/competitive.md
A	.agents/skills/bmad-deep-recon/types/domain.md
A	.agents/skills/bmad-deep-recon/types/market.md
A	.agents/skills/bmad-deep-recon/types/technical.md
A	.agents/skills/bmad-deep-recon/types/user-voice.md
A	.agents/skills/bmad-forge-idea/SKILL.md
A	.agents/skills/bmad-forge-idea/customize.toml
A	.agents/skills/bmad-forge-idea/scripts/resolve_personas.py
A	.agents/skills/bmad-forge-idea/scripts/tests/test_resolve_personas.py
A	.agents/skills/bmad-help/SKILL.md
A	.agents/skills/bmad-party-mode/SKILL.md
A	.agents/skills/bmad-party-mode/customize.toml
A	.agents/skills/bmad-party-mode/references/create-party.md
A	.agents/skills/bmad-party-mode/references/mode-agent-team.md
A	.agents/skills/bmad-party-mode/references/mode-auto.md
A	.agents/skills/bmad-party-mode/references/mode-subagent.md
A	.agents/skills/bmad-party-mode/references/party-memory.md
A	.agents/skills/bmad-party-mode/scripts/resolve_party.py
A	.agents/skills/bmad-party-mode/scripts/tests/test_resolve_party.py
A	.agents/skills/bmad-prd/SKILL.md
A	.agents/skills/bmad-prd/assets/headless-schemas.md
A	.agents/skills/bmad-prd/assets/prd-template.md
A	.agents/skills/bmad-prd/assets/prd-validation-checklist.md
A	.agents/skills/bmad-prd/assets/validation-report-template.html
A	.agents/skills/bmad-prd/customize.toml
A	.agents/skills/bmad-prd/references/headless.md
A	.agents/skills/bmad-prd/references/validate.md
A	.agents/skills/bmad-prfaq/SKILL.md
A	.agents/skills/bmad-prfaq/agents/artifact-analyzer.md
A	.agents/skills/bmad-prfaq/agents/web-researcher.md
A	.agents/skills/bmad-prfaq/assets/prfaq-template.md
A	.agents/skills/bmad-prfaq/bmad-manifest.json
A	.agents/skills/bmad-prfaq/customize.toml
A	.agents/skills/bmad-prfaq/references/customer-faq.md
A	.agents/skills/bmad-prfaq/references/internal-faq.md
A	.agents/skills/bmad-prfaq/references/press-release.md
A	.agents/skills/bmad-prfaq/references/verdict.md
A	.agents/skills/bmad-product-brief/SKILL.md
A	.agents/skills/bmad-product-brief/assets/brief-template.md
A	.agents/skills/bmad-product-brief/customize.toml
A	.agents/skills/bmad-project-context/SKILL.md
A	.agents/skills/bmad-project-context/customize.toml
A	.agents/skills/bmad-project-context/references/best-practices.md
A	.agents/skills/bmad-project-context/references/template.md
A	.agents/skills/bmad-qa-generate-e2e-tests/SKILL.md
A	.agents/skills/bmad-qa-generate-e2e-tests/checklist.md
A	.agents/skills/bmad-qa-generate-e2e-tests/customize.toml
A	.agents/skills/bmad-retrospective/SKILL.md
A	.agents/skills/bmad-retrospective/customize.toml
A	.agents/skills/bmad-retrospective/references/acceptance-verdict.md
A	.agents/skills/bmad-retrospective/references/aggregate-views.md
A	.agents/skills/bmad-retrospective/references/evidence-gathering.md
A	.agents/skills/bmad-retrospective/references/retro-document.md
A	.agents/skills/bmad-retrospective/references/team-discussion.md
A	.agents/skills/bmad-retrospective/scripts/git_evidence.py
A	.agents/skills/bmad-retrospective/scripts/sprint_status.py
A	.agents/skills/bmad-retrospective/scripts/tests/fixtures/sprint-status-template.yaml
A	.agents/skills/bmad-retrospective/scripts/tests/test_git_evidence.py
A	.agents/skills/bmad-retrospective/scripts/tests/test_sprint_status.py
A	.agents/skills/bmad-review/SKILL.md
A	.agents/skills/bmad-review/customize.toml
A	.agents/skills/bmad-review/references/editorial-common.md
A	.agents/skills/bmad-review/references/lens-adversarial.md
A	.agents/skills/bmad-review/references/lens-edge-case-hunter.md
A	.agents/skills/bmad-review/references/lens-prose.md
A	.agents/skills/bmad-review/references/lens-structure.md
A	.agents/skills/bmad-review/references/lens-verification-gap.md
A	.agents/skills/bmad-review/references/structure-models.md
A	.agents/skills/bmad-review/scripts/tests/test_word_metrics.py
A	.agents/skills/bmad-review/scripts/word_metrics.py
A	.agents/skills/bmad-spec/SKILL.md
A	.agents/skills/bmad-spec/assets/headless-schemas.md
A	.agents/skills/bmad-spec/assets/spec-template.md
A	.agents/skills/bmad-spec/assets/stories-schema.md
A	.agents/skills/bmad-spec/customize.toml
A	.agents/skills/bmad-sprint-planning/SKILL.md
A	.agents/skills/bmad-sprint-planning/customize.toml
A	.agents/skills/bmad-sprint-planning/references/fix-sprint-status.md
A	.agents/skills/bmad-sprint-planning/references/generate-tracking.md
A	.agents/skills/bmad-sprint-planning/references/readiness-gate.md
A	.agents/skills/bmad-sprint-planning/references/status-view.md
A	.agents/skills/bmad-sprint-planning/references/validate.md
A	.agents/skills/bmad-sprint-planning/scripts/sprint_plan.py
A	.agents/skills/bmad-sprint-planning/scripts/tests/test_sprint_plan.py
A	.agents/skills/bmad-sprint-planning/sprint-status-template.yaml
A	.agents/skills/bmad-ux/SKILL.md
A	.agents/skills/bmad-ux/assets/color-themes.md
A	.agents/skills/bmad-ux/assets/design-directions.md
A	.agents/skills/bmad-ux/assets/design-example-editorial.md
A	.agents/skills/bmad-ux/assets/design-example-mobile.md
A	.agents/skills/bmad-ux/assets/design-example-shadcn.md
A	.agents/skills/bmad-ux/assets/excalidraw-wireframe.md
A	.agents/skills/bmad-ux/assets/experience-example-mobile.md
A	.agents/skills/bmad-ux/assets/experience-example-shadcn.md
A	.agents/skills/bmad-ux/assets/headless-schemas.md
A	.agents/skills/bmad-ux/assets/key-screens.md
A	.agents/skills/bmad-ux/assets/validation-report-template.html
A	.agents/skills/bmad-ux/customize.toml
A	.agents/skills/bmad-ux/references/creative-tools.md
A	.agents/skills/bmad-ux/references/design-md-spec.md
A	.agents/skills/bmad-ux/references/headless.md
A	.agents/skills/bmad-ux/references/validate.md
A	.agents/skills/bmad-walkthrough/SKILL.md
A	.agents/skills/bmad-walkthrough/customize.toml
A	.agents/skills/bmad-walkthrough/generate-trail.md
A	.agents/skills/bmad-walkthrough/step-01-orientation.md
A	.agents/skills/bmad-walkthrough/step-02-walkthrough.md
A	.agents/skills/bmad-walkthrough/step-03-detail-pass.md
A	.agents/skills/bmad-walkthrough/step-04-testing.md
A	.agents/skills/bmad-walkthrough/step-05-wrapup.md
A	_bmad/_config/bmad-help.csv
A	_bmad/_config/files-manifest.csv
A	_bmad/_config/manifest.yaml
A	_bmad/_config/skill-manifest.csv
A	_bmad/bmm/config.yaml
A	_bmad/bmm/module-help.csv
A	_bmad/bmm/v6-shims/README.md
A	_bmad/config.toml
A	_bmad/core/config.yaml
A	_bmad/core/module-help.csv
A	_bmad/core/v6-shims/README.md
A	_bmad/custom/.gitignore
A	_bmad/custom/config.toml
A	_bmad/scripts/config_utils.py
A	_bmad/scripts/memlog.py
A	_bmad/scripts/render_skill.py
A	_bmad/scripts/resolve_config.py
A	_bmad/scripts/resolve_customization.py
```

</details>

### 2026-11-07T12:37:02+01:00 | Logg: push av alle prosjektendringer

Commit: [0959354](https://github.com/IBE160-2026/G132-gronning/commit/09593542516830b16bb2405e618fe2d8fe13b677)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
```

</details>

### 2026-11-07T12:42:06+01:00 | feat: vis salgshistorikk for valgt friluftsprodukt

Commit: [f53104e](https://github.com/IBE160-2026/G132-gronning/commit/f53104e63f41bbb32f32c88367a8d088f660c092)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	README.md
A	_bmad-output/implementation-artifacts/spec-salgshistorikk.md
M	app.py
M	requirements.txt
A	tests/test_sales_view.py
```

</details>

### 2026-11-07T12:42:09+01:00 | Logg: produktvelger og salgshistorikk

Commit: [611eea8](https://github.com/IBE160-2026/G132-gronning/commit/611eea89109c39ef43dff25218ccb81ff5871da7)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
M	.logs/vsalte/issues.md
```

</details>

### 2026-11-07T12:43:35+01:00 | Logg: push salgshistorikk

Commit: [63bfa82](https://github.com/IBE160-2026/G132-gronning/commit/63bfa828b4102b32f880e7f06c3c51cff4eef2c8)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
```

</details>

### 2026-11-07T12:50:42+01:00 | feat: last opp og valider ukentlige salgsdata

Commit: [4a0f6bb](https://github.com/IBE160-2026/G132-gronning/commit/4a0f6bb2a9191154900d4aa68870fbb0ed7db858)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	README.md
A	_bmad-output/implementation-artifacts/spec-csv-import.md
M	app.py
A	sales_data.py
A	tests/test_sales_data.py
```

</details>

### 2026-11-07T12:50:43+01:00 | Logg: CSV-import

Commit: [f251a41](https://github.com/IBE160-2026/G132-gronning/commit/f251a41930772399ab8cd19afbfea3698a443892)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
M	.logs/vsalte/issues.md
```

</details>

### 2026-11-07T12:52:24+01:00 | Logg: push CSV-import

Commit: [a2fb0e3](https://github.com/IBE160-2026/G132-gronning/commit/a2fb0e37435c32d9841e001ab693433c86287211)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
```

</details>

### 2026-11-07T13:02:35+01:00 | feat: implementer SCM200-prognoser og MAE-evaluering

Commit: [5971ea2](https://github.com/IBE160-2026/G132-gronning/commit/5971ea29805a654f09c358f37ca9dfa6d80644e9)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	README.md
A	_bmad-output/implementation-artifacts/spec-scm200-prognoser.md
M	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/.memlog.md
M	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/addendum.md
M	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/forecaster demand/brief.md
M	_bmad-output/planning-artifacts/briefs/brief-ai-mrp-ii-2026-09-22/forecaster demand/prosjektplan.md
M	app.py
A	forecasting.py
A	tests/test_forecasting.py
M	tests/test_sales_view.py
```

</details>

### 2026-11-07T13:02:38+01:00 | Logg: SCM200-prognoser

Commit: [9b42b1f](https://github.com/IBE160-2026/G132-gronning/commit/9b42b1f36e3002c0a8ff86a618f599bbc7f18a5f)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
M	.logs/vsalte/issues.md
```

</details>

### 2026-11-07T13:03:29+01:00 | Logg: push SCM200

Commit: [9ae2be9](https://github.com/IBE160-2026/G132-gronning/commit/9ae2be9b1c373f8fa5557e1713976a637411bff2)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
```

</details>

### 2026-11-07T13:12:21+01:00 | feat: legg til scenarioer og separat sikkerhetsmargin

Commit: [e3487f5](https://github.com/IBE160-2026/G132-gronning/commit/e3487f59bcb52f0ddbae415148cdac341100cfa3)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	README.md
A	_bmad-output/implementation-artifacts/spec-scenarioer.md
M	app.py
A	scenarios.py
A	tests/test_scenarios.py
```

</details>

### 2026-11-07T13:12:23+01:00 | Logg: scenarioer og sikkerhetsmargin

Commit: [de4f0c3](https://github.com/IBE160-2026/G132-gronning/commit/de4f0c34b7bcbbad032568566fbf1432048c4089)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
M	.logs/vsalte/issues.md
```

</details>

### 2026-11-07T13:13:04+01:00 | Logg: push scenarioer

Commit: [b8cea5b](https://github.com/IBE160-2026/G132-gronning/commit/b8cea5b8c5e010de6addb6ab640292b05ed7270c)

<details>
<summary>Berørte filer og endringstype</summary>

```text
M	.logs/vsalte/999-2026-11-07-00-00-00-friluftsdata.md
```

</details>

## Slik undersøker du en feil uten å endre filer

Kjør fra prosjektroten i PowerShell. Bytt commit eller filsti etter behov:

```powershell
git log --oneline -- app.py
git show e3487f5 -- scenarios.py
git diff 5971ea2 e3487f5 -- app.py
git blame -L 1,80 -- forecasting.py
git show 5971ea2:forecasting.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

git log viser filhistorikk; git show viser en endring eller gammel fil; git diff sammenligner to versjoner; git blame viser siste commit som endret hver linje. Siste linjeendring er ikke i seg selv bevis på hvor en feil oppstod. For filstier med mellomrom må stien settes i anførselstegn.

## Vedlikehold videre

### Nytt arbeid etter historikkgrensen: SQLite-datasett

- `storage.py`: lokal SQLite, uforanderlige datasett-ID-er, eksakte originalbytes,
  mengderettelser med forelder, gammel/ny verdi, begrunnelse og UTC-tidspunkt.
- `app.py`: lagre og åpne versjon, returnere til demo, vise historikk og rette
  eksisterende produktuke. Opplasting har forrang til filen fjernes.
- `tests/test_storage.py`: gjenåpning, originalbevaring, kjede av rettelser,
  atomisk avvisning og UI-test gjennom ny appøkt. Alle 16 tester bestod, inkludert opplastede originalbytes og opplastingsforrang.
- `.gitignore` utelater `data/local/`; README dokumenterer lokal lagring og backup.
- Finn den eksakte commiten med `git log --oneline -- storage.py`.
- Ingen innlogging eller lagring av godkjente planer i denne endringen.

Ved hver ferdig funksjonsendring: legg til commit-lenke, dato, formål, berørte filer, kontrollresultat og eventuelle kjente begrensninger. Bruk git log og git show som grunnlag; ikke før planlagt funksjonalitet som implementert. Nye logg- og pushcommits kan samles under en dokumentasjonsoppføring, men behold commitreferansene.

Denne oversikten kan ikke inneholde hashen til sin egen commit før den er opprettet. For endringer etter avgrensningen ovenfor, inkludert opprettelsen av denne filen, bruk:

```powershell
git log --oneline b8cea5b..HEAD
```

Utfyllende begrunnelser og arbeidsøkter finnes i .logs/vsalte/; gjenstående arbeid finnes i .logs/vsalte/issues.md. Implementasjonsspesifikasjoner og reviewnotater finnes i _bmad-output/implementation-artifacts/.

## Designprototype med fargetema

`outputs/designforslag/samlet-oversikt.html` viser et samlet, interaktivt designforslag med illustrative tall. Fargetema kan settes til lyst, mørkt eller systemets valg, og huskes lokalt i nettleseren når lokal lagring er tilgjengelig. Dette er en selvstendig prototype, ikke en endring av Streamlit-appen. Finn commit med `git log --oneline -- outputs/designforslag/samlet-oversikt.html`.
