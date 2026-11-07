---
title: "Product Brief: AI-supported MRP II – Forecasting and Demand Management"
status: draft
created: 2026-09-22
updated: 2026-11-07
---

# Product Brief: AI-supported MRP II

## Executive summary

A web-based student prototype will help a demand planner import weekly sales, review data quality, compare forecasts, explore scenarios, and approve and export a demand plan. The first release covers **module 4.1: Forecasting and Demand Management** for one fictional manufacturing company. MRP II remains the long-term vision; other planning modules are outside v1.

This revision applies the instructor feedback dated 2026-10-06. V1 uses synthetic data for five products over 104 weeks, a 12-week forecast horizon, a seasonal naive baseline, moving average and simple exponential smoothing, and one authenticated planner role. These are planning decisions for the prototype, not claims about an implemented app or validated customer needs. The project plan sets the delivery deadline at **week 51 (14–20 December 2026)**.

## Problem and primary user

The primary user is a production or demand planner who needs an understandable basis for weekly demand decisions. For example, a fictional manufacturer of seasonal outdoor products risks shortages if it plans a summer peak using winter sales; an excessive forecast can instead leave unsold stock. The prototype lets the planner inspect seasonality, compare measured errors, and explain adjustments before approving demand.

**[ASSUMPTION]** This example represents a useful real planning problem; it still needs validation with a prospective planner. Students and the instructor evaluate the prototype, but are not additional product roles. Sales managers and other contributors are outside v1.

## Solution and user experience

The planner logs in, imports a sales CSV, and reviews errors and warnings with product, week, and row references. Missing values are distinguished from zero sales. Corrections require an explanation and preserve the original import; suspicious values are flagged rather than silently removed.

The main workspace provides a product selector, a chart of history and the three 12-week forecasts, a per-product MAE comparison, and visible data-quality markers. A linked scenario panel and table show normal, optimistic, and pessimistic quantities and the exact adjustments. The planner chooses a method, reviews changes, approves a saved plan, and exports it as CSV.

The forecasting foundation is [SCM200, spring 2026](https://www.himolde.no/studier/emner/log/2026/var/scm200.html), whose learning outcomes name moving averages and exponential smoothing and evaluating forecasts through metrics. V1 uses a four-week moving average and simple exponential smoothing with alpha 0.3, initial level equal to the first observation. Both produce flat fixed-origin 12-week forecasts. A seasonal naive method with period 52 is retained as a reference for seasonal data. These fixed parameters and MAE are project choices, not verified prescriptions from the course textbook.

At the user's direction, these classical statistical methods replace the regression candidate in v1; regression is deferred. No trained ML model, automatic tuning, language model or paid API is required. AI is used for development, while the application's forecasts remain inspectable classical calculations. This changes the earlier AI-candidate scope and does not claim instructor approval of that change. All methods run locally; warnings use explicit validation rules.
## First-release scope

| Area | V1 commitment |
|---|---|
| Data | CSV sales history only: product ID, week start, quantity sold, unit. Five synthetic products, 104 weekly observations per product, and a 12-week forecast horizon. |
| Data quality | Validate fields, weekly coverage, duplicates, missing values, negative quantities, and rule-based outlier warnings. Preserve zero sales. Unresolved blocking errors prevent forecasting. |
| Forecasts | Four-week moving average, simple exponential smoothing and seasonal naive reference; history, forecasts, and MAE displayed per product. No automatic tuning or method selection. |
| Scenarios | Normal = selected forecast; optimistic = normal × 1.10; pessimistic = normal × 0.90. Display these as editable planning assumptions, not confidence intervals. |
| Decisions | Select method and scenario; optionally apply a separately displayed percentage safety margin, default 0%, and explained quantity overrides. Quantities cannot be negative. Safety-stock calculation is outside v1. |
| Approval and export | Save an immutable approval snapshot linking the imported data and corrections, method, scenario, margin, overrides, approver, and timestamp. Export product, week, unit, scenario, and approved quantity. Full edit-history tracking is deferred. |
| Access | Login and one planner role, enforced on the server for data, forecast, approval, and export operations. Include a local demonstration account; no role-management interface. |

The chosen development direction is a Python web application with Streamlit, pandas and SQLite for local persistence. This keeps the data workflow and forecasting in one language. Forecasting, validation, and evaluation must be separate from the UI and independently testable. Authentication details and dependency versions belong in architecture work. Example data and a local setup guide must allow assessment without personal keys or paid accounts.

Dataset construction, evaluation windows, and calculation rules are specified in [addendum.md](../addendum.md). Synthetic data, sales views, CSV validation and forecasting are implemented; scenarios, local permanent imports and explained quantity corrections are also implemented; authentication and approval/export still remain. Tests document the implemented behavior.

## Success criteria

- A planner completes login, import, anomaly review, forecast comparison, scenario adjustment, approval, and export using the supplied demonstration data without code changes.
- A reproducible generator produces five products × 104 weeks with documented trend, 52-week seasonality, and a fixed random seed. A clean reference and an intentionally corrupted import fixture expose known missing values, outliers, and invalid rows. Tests check known data defects and hand-calculated baseline/MAE examples. The generating process is known; future random demand is not perfectly predictable.
- All three methods use the same historical 12-week evaluation windows and available observations. Training and any missing-value treatment use only information available at each forecast origin. MAE is shown per product, with results reported even when a method performs worse. See the local evaluation protocol in the addendum.
- Every exported plan matches its approved snapshot and can be traced to source data, corrections, method, scenario assumptions, margin, overrides, and approver. A new approval creates a new snapshot rather than replacing a prior approval.
- Tests show that unauthenticated users cannot read data, run forecasts, change plans, approve, or export, including direct server requests. No read-only or administrator role is required in v1.
- An assessor can follow README instructions to run locally, load the bundled data, use the demonstration account, and reproduce the comparison without paid services. A peer or prospective planner tries the core workflow and confusing steps are recorded for improvement.

## Boundaries, risks, and next steps

Customer orders, campaign and market signals, additional roles, full change-history tracking, additional models, and optional language-model explanations are later extensions. BOM editing, MPS, MRP, inventory management, capacity planning, detailed scheduling, finance, ERP/supplier integrations, and purchasing/selling are outside v1. Exported demand may feed future MPS and MRP modules; this prototype does not calculate material or capacity requirements.

The main risks are scope exceeding the remaining time, leakage of future data into evaluation, and synthetic results being mistaken for real-world evidence. Mitigations are the bounded core workflow, fixed temporal tests, human approval, and clearly labelled demonstration data. Synthetic raw data can be version controlled in `data/synthetic/`; secrets and any future sensitive business data must stay outside version control and public logs.

Next, create the dataset fixtures and PRD from these commitments, document the user-directed replacement of regression with SCM200 methods and confirm any course-specific application-AI requirements, and validate the workflow with a prospective planner. The named real company and external dataset are no longer prerequisites. The [project plan](prosjektplan.md) reflects this scope reduction and starts with a check of actual implementation status and remaining capacity. The revised brief governs v1 scope.

## Capacity and course boundary

The user has about four hours per week and targets completion in week 51 of 2026. This prototype covers the demand-forecasting part of SCM200 only; EOQ, MRP and other inventory/production modules are outside v1. The course description is the verified source; the detailed textbook and 2027 syllabus have not been checked.
