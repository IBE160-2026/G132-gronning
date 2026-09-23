---
title: "Module Details: AI-supported MRP II"
status: draft
created: 2026-09-22
updated: 2026-09-22
---

# Module details and input to the PRD

## Original user input

A comprehensive project in which AI supports production planning from demand forecasting to detailed production scheduling. Students will learn how data flows between modules and how AI can support better decisions. Difficulty: high. Authentication is required because the data is business-critical and potentially competitively sensitive. Online purchasing and selling are not directly included in the core modules; supplier portals may be integrated later.

For module 4.1, the user specified historical sales, seasonality/trend signals, campaigns/market data, customer orders, and sales forecasts as inputs. Outputs are demand forecasts by period/product and optimistic, pessimistic, and normal scenarios. Decision points are forecasting methods, safety margin, and outlier treatment.

## Proposed data flow

Sales history + known orders + available market signals → data validation → forecasts and scenarios → planner approval → versioned demand plan **[MVP ends here]** → master production schedule (MPS) → material requirements (MRP, using BOM, inventory, and lead times) → capacity checks → detailed production schedule. In a future version, capacity shortfalls must be able to trigger plan revisions.

This is a proposed educational workflow based on [SAP's description](https://www.sap.com/resources/what-is-material-resource-planning-mrp), rather than a completed architecture. The user has only detailed module 4.1; the functions of the other modules must be specified separately.

## Module 4.1: details to specify

| Topic | Proposed clarification or rule [ASSUMPTION] |
|---|---|
| Sales history | Product ID, period, quantity sold, and unit of measure. Clarify returns and stockout periods; recorded sales do not always equal actual demand. |
| Orders | Product, quantity, delivery period, and status. Clarify how confirmed orders replace parts of the forecast to prevent double-counting demand. |
| External signals | Link campaigns and sales forecasts to product and period, including the source and when the information became known. |
| Missing data and outliers | Distinguish missing data from zero sales. Show anomalies before any correction. Preserve original data and the user's explanation. |
| Methods | Start with a simple naive or seasonal naive baseline and one AI/machine-learning candidate. Select the candidate after inspecting the dataset. Do not promise advanced modeling with limited history. |
| Evaluation | Use time-ordered or rolling validation with the same forecast horizon. Keep the final test period separate from model selection. Mean absolute error (MAE) is expressed in the product's unit of measure; comparisons across different units require separate consideration. |
| Scenarios | In this prototype, normal = baseline forecast, optimistic = higher demand, and pessimistic = lower demand. Show the adjustment; these scenarios are not statistical prediction intervals. |
| Safety margin | Display the margin separately from the baseline forecast. Clarify how it affects the approved plan; safety stock calculation belongs to later material/inventory planning. |
| Approval | Store the method, data version, forecast timestamp, assumptions, changes, approver, and approval timestamp. Export product, period, unit, scenario, and approved quantity. |
| Access | Proposed roles: administrator, planner, and read-only user. Enforce access control on the server as well. Do not place sensitive raw data in openly accessible logs or version control. |

The evaluation proposals draw on [Time series cross-validation](https://otexts.com/fpp3/tscv.html) and [Evaluating point forecast accuracy](https://otexts.com/fpp3/accuracy.html).

## Scope boundaries and future modules

| Stage | Purpose | Status |
|---|---|---|
| Forecasting and Demand Management | Establish and approve the demand basis | User-selected MVP |
| MPS | Translate demand into planned production by period | Future development |
| BOM and MRP | Connect product structure with the production schedule, inventory, scheduled receipts, and lead times | Future development |
| Capacity planning | Check requirements against available machines and personnel | Future development |
| Detailed scheduling | Allocate and sequence production operations | Future development |
| Feedback and finance | Track actual results and show resource and cost implications | Long-term MRP II vision |
| Supplier portals | Support purchasing through integration | Optional extension |

## Questions for the next phase

1. Which manufacturing company or example industry should the prototype represent?
2. Is a dataset available with appropriate usage rights and sufficient history, and does it include campaigns and orders?
3. How many products, what time granularity, and what forecast horizon are realistic?
4. What is the team's timeframe, and what requirements does the course set for AI, testing, and documentation?
5. Who will test the user workflow, and which data and AI services may be used?
