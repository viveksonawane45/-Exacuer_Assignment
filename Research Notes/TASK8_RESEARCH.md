# Task 8 - Performance Review Dashboard Research

## Live Calculation & Dynamic UI
- Dashboard calculations are performed purely on the client-side within the `Performance Review` Client Script.
- The UI triggers recalculation on changing specific child table fields inside `Performance Review KPI` (`kpis` field):
  - `target_value`
  - `achieved_value`
  - `score`
  - Row insertion (`kpis_add`) or removal (`kpis_remove`)
- Formulas:
  - Progress percentage per KPI: `(achieved_value / target_value) * 100` (capped at 100%, defaults to 0% if target is 0).
  - Overall Performance Score: Average of all KPI scores (`sum(score) / count(KPIs)`).

## Rating Thresholds
- Rating descriptive labels and colors:
  - **Excellent**: Score >= 4.5 (Green, `#28a745`)
  - **Good**: Score >= 3.0 (Blue, `#007bff`)
  - **Average**: Score >= 2.0 (Orange, `#fd7e14`)
  - **Poor**: Score < 2.0 (Red, `#dc3545`)

## Database Queries & API Design
- To compare performance against the previous period, a single whitelisted server method is called on load:
  - Method: `custom_hr_pro.api.review.get_previous_review_score`
  - Query: Retrieves the `overall_score` from the most recently submitted `tabPerformance Review` record for the same employee, ordered by `creation DESC, modified DESC`.
