-- Representative warehouse checks for the synthetic GTM operations source layer.
-- These are written to show the analytical queries the artifact is modeling.

-- 1. Find AI workflow candidates with high impact but weak launch readiness.
select
  workflow_id,
  workflow_name,
  motion,
  annualized_revenue_impact_usd,
  data_readiness_pct,
  guardrail_score,
  recommended_decision
from agent_workflows
where annualized_revenue_impact_usd >= 500000
  and (data_readiness_pct < 70 or guardrail_score < 70)
order by annualized_revenue_impact_usd desc;

-- 2. Summarize adoption telemetry by workflow.
select
  workflow_id,
  avg(human_acceptance_pct) as avg_acceptance_pct,
  avg(measured_lift_pct) as avg_measured_lift_pct,
  avg(qa_exception_rate_pct) as avg_exception_rate_pct
from workflow_runs
group by workflow_id
order by avg_measured_lift_pct desc;

-- 3. Identify capacity planning pressure by territory.
select
  territory,
  sales_reps,
  named_accounts,
  pipeline_coverage,
  capacity_load_pct,
  weekly_admin_hours_releasable,
  planning_recommendation
from territory_capacity
where pipeline_coverage < 2.25
   or capacity_load_pct > 105
order by capacity_load_pct desc;

-- 4. Count launch blockers by source table and owner.
select
  source_table,
  definition_owner,
  count(*) as blocker_count,
  avg(completeness_pct) as avg_completeness_pct,
  max(freshness_hours) as worst_freshness_hours
from data_quality_checks
where launch_blocker = 'Yes'
group by source_table, definition_owner
order by blocker_count desc, worst_freshness_hours desc;
