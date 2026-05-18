# Analysis Plan

## Operating question

Which AI-assisted GTM workflows should revenue leadership deploy, pilot, or hold until the source data is trustworthy enough?

## Method

1. Build a synthetic source layer for accounts, workflow candidates, workflow telemetry, pipeline snapshots, territory capacity, and data quality checks.
2. Score each workflow on modeled annualized revenue impact, expected conversion lift, adoption, confidence, source readiness, guardrail strength, and deployment effort.
3. Separate high-upside pilots from deployable workflows by requiring clean readiness and guardrail thresholds.
4. Size territory coverage and capacity release so the recommendation connects to planning, not only workflow enthusiasm.
5. Produce a data quality queue that explains launch blockers before an AI workflow is scaled.

## Decision outputs

- `agent_workflow_scorecard.csv`: ranked workflow recommendation queue.
- `pipeline_impact_model.csv`: financial impact model by workflow.
- `territory_capacity_plan.csv`: territory planning and coverage view.
- `data_quality_queue.csv`: source blockers that prevent safe workflow scaling.
- `summary.json`: headline metrics used by the browser artifact.
