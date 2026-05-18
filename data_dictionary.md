# Data Dictionary

## `data/accounts.csv`

- `account_id`: synthetic account identifier.
- `territory`: sales territory or portfolio.
- `segment`: GTM segment.
- `pipeline_stage`: current funnel stage.
- `estimated_acv`: modeled annual contract value.
- `open_pipeline`: open opportunity value.
- `workload_fit_score`: score for technical fit and likely need.
- `data_completeness_pct`: completeness of required GTM fields.
- `customer_health_score`: health score used for expansion and renewal logic.
- `forecast_category`: pipeline, best case, commit, closed, or renewal risk.
- `rep_capacity_load_pct`: account load relative to sustainable capacity.
- `ai_assist_eligible`: eligibility flag based on fit and data completeness.

## `data/agent_workflows.csv`

- `workflow_id`: AI workflow identifier.
- `workflow_name`: workflow candidate.
- `motion`: GTM motion served by the workflow.
- `business_owner`: accountable operating owner.
- `primary_source`: core data source needed for the workflow.
- `accounts_in_scope`: records in the first modeled rollout cohort.
- `baseline_conversion_pct`: baseline conversion assumption.
- `expected_lift_pct`: modeled lift from the workflow.
- `adoption_pct`: expected human acceptance or usage.
- `data_readiness_pct`: source readiness score.
- `guardrail_score`: governance and control score.
- `model_confidence_pct`: confidence in modeled lift and usage.
- `weekly_hours_saved`: weekly manual effort released.
- `pipeline_influence_usd`: pipeline value influenced by the workflow.
- `annualized_revenue_impact_usd`: modeled revenue impact.
- `deployment_effort_weeks`: estimated implementation effort.
- `payback_multiple`: modeled impact divided by deployment cost.
- `priority_score`: combined scoring formula.
- `recommended_decision`: deploy, pilot, or fix data first.

## `analysis/outputs`

- `agent_workflow_scorecard.csv`: ranked queue for leadership review.
- `pipeline_impact_model.csv`: simplified financial model.
- `territory_capacity_plan.csv`: coverage and capacity planning table.
- `data_quality_queue.csv`: source launch blockers.
- `summary.json`: top-line metrics consumed by the web app.
