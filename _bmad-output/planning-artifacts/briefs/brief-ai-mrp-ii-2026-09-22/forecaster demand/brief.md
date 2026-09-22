---
title: "Product Brief: AI-supported MRP II – Forecasting and Demand Management"
status: draft
created: 2026-09-22
updated: 2026-09-22
---

# Product Brief: AI-supported MRP II

## Executive summary

The product will use AI to support production planning, from demand forecasting to material requirements and detailed production scheduling. The first release is **module 4.1: Forecasting and Demand Management**, selected by the user as the MVP. It will turn historical sales and relevant market signals into understandable forecasts that a planner can review, adjust, and approve.

The project has a high level of difficulty and a clear educational purpose: students will understand how data flows between planning modules and investigate when AI improves decision support. MRP II is the long-term product vision. The bill of materials (BOM) and other production modules are planned for future development.

**[ASSUMPTION]** The first version is a web-based student prototype for a single manufacturing company, demonstrated using synthetic or anonymized data. The industry, company, and dataset have not yet been selected.

## Problem and target users

A production planner must balance expected demand against uncertainty. Incorrect estimates can lead to excess inventory or shortages. **[ASSUMPTION]** The target users currently combine sales, orders, and campaign information manually, with limited support for comparing forecasting methods and explaining adjustments. This problem statement needs validation with a prospective user.

The primary user is a production or demand planner who needs a traceable basis for decisions by product and period. A sales manager contributes customer orders and market knowledge. Students and the course instructor use the solution to demonstrate, test, and assess data quality, forecasts, and the contribution of AI. **[ASSUMPTION]** These roles represent the initial user environment.

## Solution and user experience

The planner imports data, receives visible warnings about missing data and anomalies, and selects a product and planning period. The solution compares a simple baseline forecast with an AI-based candidate and displays historical data, expected demand, and forecast errors. The planner explores normal, optimistic, and pessimistic scenarios, considers a safety margin, and saves an approved demand plan with reasons for any overrides.

AI will support method selection and anomaly identification. Calculated results must be verifiable, and recommendations must be linked to data and measured performance. The user retains control over the method, outlier treatment, and safety margin. An optional language model for explanations is an extension, not a prerequisite for forecast calculation.

The project's value is a clear learning and decision-making workflow with traceability from source data to the approved plan. There is no evidence yet of a competitive advantage or that AI will produce better forecasts on the selected dataset.

## MVP: module 4.1

| Area | First-release scope |
|---|---|
| Inputs | Historical sales and customer orders. Seasonality/trends, campaigns, market data, and sales forecasts are included when suitable data is available; missing inputs must be visible. |
| Data quality | Checks for required fields, periods, duplicates, missing values, and outliers. Corrections must be traceable. |
| Forecasts | Demand forecasts by product and period, comparing a simple baseline model with an AI-based candidate. |
| Scenarios | Normal, optimistic, and pessimistic demand, with visible assumptions. High and low demand are explicitly defined. |
| Decisions | Selection of forecasting method, safety margin, and outlier treatment; manual changes with explanations. |
| Outputs | A versioned demand plan and scenarios that can be exported for subsequent master production scheduling. |
| Access | Authentication and access control for business-critical and potentially competitively sensitive data. |

**[ASSUMPTION]** The MVP uses CSV import and export, weekly periods, and a 12-week forecast horizon. Scope will be adjusted to the available data before implementation. Detailed module information is available in [addendum.md](../addendum.md).

The MVP excludes BOM editing, material requirements calculation, inventory management, capacity planning, detailed production scheduling, a finance module, and integration with ERP systems or supplier portals. Direct online purchasing and selling are outside the core module.

## Success criteria

The following are proposed criteria **[ASSUMPTION]**, to be refined in the product requirements document (PRD):

- A planner can complete data import, anomaly review, forecast comparison, scenario analysis, and approval in a single demonstration without code changes.
- The AI candidate and baseline model are evaluated on the same historical test periods and forecast horizon, using mean absolute error (MAE) per product. No future observations are used for training or method selection. Results are reported even if AI performs no better. This follows the principles of [time series evaluation](https://otexts.com/fpp3/tscv.html) and [forecast accuracy evaluation](https://otexts.com/fpp3/accuracy.html).
- Every approved plan can be traced to its data version, method, scenario assumptions, manual changes, and approver.
- An access test shows that an unauthenticated user cannot read or export data, and that a read-only user cannot change or approve plans.
- Students can explain how exported demand will later feed into master production scheduling and material requirements planning using the BOM, inventory, and lead times.

## Future vision, risks, and open questions

The next stages are master production scheduling (MPS), BOM and material requirements planning (MRP), followed by capacity planning and detailed production scheduling. MRP calculates material requirements using inputs such as the production schedule, BOM, and inventory; MRP II extends this relationship to additional manufacturing and business functions. Capacity must be assessed separately. See [SAP's explanation of MRP and MRP II](https://www.sap.com/resources/what-is-material-resource-planning-mrp).

The main risks are insufficient historical data, misleading forecasts, exposure of sensitive data, and scope exceeding the student team's capacity. Mitigations include a bounded MVP, visible data gaps, evaluation against a baseline model, human approval, and access control.

Before creating the PRD, the team must clarify the industry and user, available dataset and usage rights, project timeframe, number of products, time granularity and history length, and the AI contribution to implement. Selecting an external AI service also requires clarification of which data may be shared externally. This brief is a complete first draft; marked assumptions are not confirmed requirements.
