---
title: "Module Details: AI-supported MRP II"
status: draft
created: 2026-09-22
updated: 2026-11-07
---

# Module details and input to the PRD

## Original user input and scope decision

The original concept was a comprehensive project in which AI supports production planning from demand forecasting to detailed production scheduling. Students learn how data flows between modules and evaluate AI decision support. Authentication is required. Module 4.1 originally included historical sales, seasonality/trend signals, campaigns/market data, customer orders, and sales forecasts; outputs included demand forecasts and three scenarios. Decision points were method, safety margin, and outlier treatment.

The 2026-11-07 revision applies the [instructor feedback](forecaster%20demand/tilbakemelding-product-brief.md). The [revised brief](forecaster%20demand/brief.md) governs v1: sales history only, moving average, simple exponential smoothing and a seasonal naive reference, and one planner role. Orders and market signals, administrator/read-only roles, automatic method selection, and full edit-history tracking are deferred. This supersedes the broader earlier proposals while preserving the original product vision.

## V1 data flow and screen outline

Login → CSV sales import → validation and explained corrections → SCM200-method comparison → scenarios and optional margin/overrides → approval snapshot → CSV export **[v1 ends here]**.

The main screen places a product selector above a history/forecast chart. Data-quality markers link to a row-level issues table. Beside the chart, show all three methods' MAE and the evaluation windows. Below it, place method/scenario controls, the visible scenario and margin calculations, and a weekly quantity table. Approval requires review of the final quantities and explanations; export refers to the saved snapshot.

Future flow: approved demand → master production schedule (MPS) → material requirements (MRP using BOM, inventory, receipts, and lead times) → capacity checks → detailed scheduling. Capacity shortfalls may require plan revision. These modules need separate specifications.

## Synthetic dataset contract

Use one fictional manufacturer of seasonal outdoor products, with product IDs P01–P05 and unit `units`. Generate 104 consecutive Monday-start weeks, from 2024-01-01 through 2025-12-22. Each clean product series uses a documented base level, linear trend, annual seasonality of period 52, and seeded noise; use seed 132 and record all parameters. Quantities are nonnegative integers. This is a reproducible learning dataset, not evidence about a real company.

Planned artifacts under `data/synthetic/`:

- A generator and parameter manifest, including the seed and expected defect locations.
- A complete clean CSV with 520 product-week rows and fields `product_id`, `week_start`, `quantity_sold`, and `unit`.
- A corrupted CSV derived from that reference, containing documented missing quantities, an omitted week, outliers, duplicates, an invalid date, and a negative quantity. It may contain a different row count because defects are deliberate.
- A reference file for checking validation and demonstrating corrections. This reference must never be used as hidden input to model training or test-period predictions.

Known generating parameters and a clean reference support controlled tests; they do not make noisy future demand a known exact forecast. A future real or anonymized dataset is optional and needs rights and privacy review.

## Forecast and evaluation protocol

| Topic | V1 rule |
|---|---|
| Baseline | Seasonal naive: for forecast week t, use observed quantity at t−52. Require sufficient complete history; otherwise show why a comparison cannot run. |
| Course methods | Four-week moving average: arithmetic mean of the last four training observations, repeated for all 12 future steps. Simple exponential smoothing: initial level = first observation; level = 0.3 * observation + 0.7 * previous level, repeated for all 12 future steps. No tuning or future actuals. Regression is deferred by user decision. |
| Temporal evaluation | On the clean 104-week fixture, use expanding training windows ending at weeks 68, 80, and 92; forecast weeks 69–80, 81–92, and 93–104 respectively. All three methods forecast 12 weeks from each origin. |
| Final holdout | Fix the method specification and preprocessing before evaluating weeks 93–104. Earlier windows support development; keep final-holdout MAE separate. If the final holdout influences changes, disclose that and reserve a new untouched test dataset. |
| MAE | Mean of absolute prediction errors, separately per product and window, in units sold. Display the 12 observations behind each score. Report every method honestly, even when it performs worse than the seasonal reference. |
| Missing data | Zero is an observed value, never a missing marker. Block unresolved gaps. For demonstrations, the planner can supply an explained correction; any automated fill introduced later must use only information available at the forecast origin. |
| Outliers | Flag quantities above the product median plus three interquartile ranges over available history; an all-equal series flags values above its median. This is a review heuristic, not proof of an error. In backtests, calculate the rule from training history only. Keep values unless explicitly corrected with a reason. |
| Forward forecast | After evaluation, fit on all 104 available weeks and forecast weeks 105–116. Label forward forecasts separately from historical test predictions. |

Keep import validation, method calculation, forecasting, and scoring separate from the Streamlit UI. Use hand-calculated seasonal-naive and MAE fixtures as independent checks. For example, actual values 10 and 14 versus predictions 12 and 11 give MAE 2.5. Verify that changing observations after a forecast origin cannot change its predictions.

## Scenarios, approvals, and access

Normal is the planner-selected method's forecast, optimistic is +10%, and pessimistic is −10%. The planner may change the percentages; require optimistic ≥ normal and pessimistic between zero and normal. These are planning assumptions, not statistical prediction intervals. Display the percentage and quantity effect explicitly.

Apply the optional nonnegative safety-margin percentage to the selected scenario, then apply any explained weekly quantity overrides. Retain decimal precision for MAE; round final approved quantities to whole units with a documented, consistent rule. Approval snapshots store the calculation inputs and exact final exported values. Safety stock and inventory optimisation are deferred.

Preserve the original import plus an explained corrected dataset. An immutable approval snapshot links that dataset, method/specification, forecast timestamp, scenario percentages, margin, overrides, approver, and approval time. New approvals create new snapshots. Full event-by-event editing history and rollback tooling are deferred.

One authenticated planner can use the workflow. Enforce authentication on the server, including data reads and exports. Provide a local demonstration account through documented setup, without committing production secrets. Do not place sensitive business data or credentials in public logs or version control.

## Later stages and remaining questions

Orders and campaigns require separate input contracts and rules that prevent double-counting orders and forecast demand. Additional roles, richer version history, language-model explanations, and additional models come after the core flow is stable. MPS, BOM/MRP, capacity, scheduling, finance, and supplier integrations remain future modules.

Before implementation tasks are generated, confirm any course-specific requirement for AI within the app after the user-directed deferral of regression, agree who will try the workflow, and choose authentication details and tested dependency versions. The revised [project plan](forecaster%20demand/prosjektplan.md) follows the reduced v1 and requires a check of actual progress and remaining capacity before its estimates are confirmed.

## Verified course basis and parameter choices

[SCM200 spring 2026](https://www.himolde.no/studier/emner/log/2026/var/scm200.html) explicitly names moving averages and exponential smoothing and evaluation through metrics. Four weeks, alpha 0.3, MAE and the seasonal naive reference are project choices. Formulas follow standard methods; [Forecasting: Principles and Practice](https://otexts.com/fpp3/exponential-smoothing.html) is a supporting method reference, not a claim about assigned HiMolde reading. Simple smoothing assumes no explicit trend/seasonal component and may perform poorly on these synthetic seasonal series.

Forward comparison requires at least 52 consecutive weeks; evaluation requires at least 104. For histories longer than 104, fixed test windows still refer to the first 104 weeks, while forward forecasts use all history. Display the 12 observations and predictions behind each score.
