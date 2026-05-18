import csv
import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"
RANDOM_SEED = 42


def money(value):
    return int(round(value, 0))


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clamp(value, low, high):
    return max(low, min(high, value))


def main():
    random.seed(RANDOM_SEED)
    DATA.mkdir(exist_ok=True)
    OUTPUTS.mkdir(parents=True, exist_ok=True)

    territories = [
        {"territory": "Northeast Enterprise", "segment": "Enterprise", "reps": 7, "quota": 12800000, "accounts": 38},
        {"territory": "Financial Services", "segment": "Strategic", "reps": 5, "quota": 11200000, "accounts": 24},
        {"territory": "Digital Native West", "segment": "Enterprise", "reps": 6, "quota": 9800000, "accounts": 42},
        {"territory": "Central Commercial", "segment": "Mid-Market", "reps": 8, "quota": 7600000, "accounts": 64},
        {"territory": "Healthcare and Public", "segment": "Enterprise", "reps": 4, "quota": 7200000, "accounts": 27},
        {"territory": "Expansion Portfolio", "segment": "Customer Growth", "reps": 6, "quota": 10400000, "accounts": 51},
    ]

    industries = ["Fintech", "Retail", "Gaming", "Healthcare", "SaaS", "Media", "Logistics", "Cybersecurity"]
    products = ["Cloud Basic", "Cloud Standard", "Cloud Advanced", "Self-Hosted", "BYOC Evaluation"]
    stages = ["Target", "Engaged", "Stage 1", "Stage 2", "Stage 3", "Commit", "Customer"]
    accounts = []
    account_id = 1
    for t in territories:
        for _ in range(t["accounts"]):
            stage = random.choices(stages, weights=[18, 18, 16, 15, 12, 8, 13])[0]
            segment_multiplier = {"Strategic": 2.0, "Enterprise": 1.45, "Mid-Market": 0.65, "Customer Growth": 1.1}[t["segment"]]
            acv = random.triangular(65000, 720000, 210000) * segment_multiplier
            workload_fit = random.randint(48, 96)
            data_completeness = random.randint(58, 99)
            health = random.randint(42, 94)
            if stage == "Customer":
                health = random.randint(55, 98)
            open_pipeline = 0 if stage in ["Target", "Customer"] else acv * random.uniform(0.7, 1.9)
            accounts.append(
                {
                    "account_id": f"ACCT{account_id:04d}",
                    "account_name": f"Account {account_id:04d}",
                    "territory": t["territory"],
                    "segment": t["segment"],
                    "industry": random.choice(industries),
                    "product_motion": random.choice(products),
                    "pipeline_stage": stage,
                    "estimated_acv": money(acv),
                    "open_pipeline": money(open_pipeline),
                    "workload_fit_score": workload_fit,
                    "data_completeness_pct": data_completeness,
                    "customer_health_score": health,
                    "forecast_category": random.choices(["Pipeline", "Best Case", "Commit", "Closed", "Renewal Risk"], weights=[38, 24, 13, 15, 10])[0],
                    "rep_capacity_load_pct": random.randint(62, 118),
                    "ai_assist_eligible": "Yes" if workload_fit >= 62 and data_completeness >= 68 else "Watch",
                }
            )
            account_id += 1

    workflows = [
        ("WF01", "Agentic account prioritization", "Pipeline Creation", "Sales Strategy", "Accounts", 0.16, 0.19, 3),
        ("WF02", "Technical trigger enrichment", "Pipeline Creation", "Marketing Ops", "Accounts", 0.11, 0.15, 2),
        ("WF03", "Personalized enterprise outreach", "Pipeline Creation", "SDR Leadership", "Contacts", 0.10, 0.18, 4),
        ("WF04", "Pipeline inspection assistant", "Deal Acceleration", "Revenue Operations", "Opportunities", 0.09, 0.13, 3),
        ("WF05", "Mutual action plan risk reader", "Deal Acceleration", "Sales Leadership", "Opportunities", 0.08, 0.10, 4),
        ("WF06", "Forecast commit anomaly review", "Forecasting", "GTM Operations", "Opportunities", 0.07, 0.09, 2),
        ("WF07", "Expansion health scoring", "Customer Growth", "Customer Success", "Customers", 0.10, 0.14, 3),
        ("WF08", "Renewal risk intervention queue", "Customer Growth", "Customer Success", "Customers", 0.08, 0.12, 3),
        ("WF09", "Territory whitespace recommender", "Planning", "GTM Operations", "Territories", 0.05, 0.11, 5),
        ("WF10", "Rep capacity relief planner", "Planning", "Sales Operations", "Territories", 0.04, 0.08, 4),
        ("WF11", "Data quality triage copilot", "Governance", "Data Engineering", "Source Tables", 0.03, 0.07, 2),
        ("WF12", "Executive narrative generator", "Leadership Cadence", "Revenue Strategy", "Metrics", 0.02, 0.05, 2),
    ]

    workflow_rows = []
    run_rows = []
    action_rows = []
    quality_rows = []
    priority_rows = []
    total_pipeline = sum(a["open_pipeline"] for a in accounts)

    for workflow_id, name, motion, owner, source, base_conv, lift, effort_weeks in workflows:
        scope_accounts = random.randint(38, 156)
        adoption = random.randint(43, 91)
        data_ready = random.randint(54, 97)
        guardrail = random.randint(55, 96)
        confidence = random.randint(52, 92)
        weekly_hours = random.randint(14, 86)
        pipeline_influence = total_pipeline * random.uniform(0.025, 0.14)
        revenue_impact = pipeline_influence * lift * (adoption / 100) * (confidence / 100)
        cost = effort_weeks * random.randint(16000, 28000)
        payback = revenue_impact / max(cost, 1)
        readiness_penalty = (100 - data_ready) * 0.16 + (100 - guardrail) * 0.11
        priority = (revenue_impact / 45000) + lift * 145 + adoption * 0.22 + confidence * 0.18 - readiness_penalty - effort_weeks
        decision = "Deploy next" if priority >= 55 and data_ready >= 70 and guardrail >= 70 else "Pilot with guardrails" if priority >= 42 else "Fix data first"
        workflow_rows.append(
            {
                "workflow_id": workflow_id,
                "workflow_name": name,
                "motion": motion,
                "business_owner": owner,
                "primary_source": source,
                "accounts_in_scope": scope_accounts,
                "baseline_conversion_pct": round(base_conv * 100, 1),
                "expected_lift_pct": round(lift * 100, 1),
                "adoption_pct": adoption,
                "data_readiness_pct": data_ready,
                "guardrail_score": guardrail,
                "model_confidence_pct": confidence,
                "weekly_hours_saved": weekly_hours,
                "pipeline_influence_usd": money(pipeline_influence),
                "annualized_revenue_impact_usd": money(revenue_impact),
                "deployment_effort_weeks": effort_weeks,
                "payback_multiple": round(payback, 1),
                "priority_score": round(priority, 1),
                "recommended_decision": decision,
            }
        )
        priority_rows.append(workflow_rows[-1])
        for week in range(1, 13):
            run_rows.append(
                {
                    "workflow_id": workflow_id,
                    "week": f"2026-W{week + 4:02d}",
                    "eligible_records": int(scope_accounts * random.uniform(0.55, 1.05)),
                    "agent_recommendations": int(scope_accounts * random.uniform(0.24, 0.72)),
                    "human_acceptance_pct": clamp(round(random.gauss(adoption, 9), 1), 18, 97),
                    "measured_lift_pct": clamp(round(random.gauss(lift * 100, 3.1), 1), -4, 32),
                    "qa_exception_rate_pct": clamp(round(random.gauss((100 - guardrail) / 5, 1.5), 1), 0.2, 16),
                }
            )
        for action_number in range(1, 4):
            action_rows.append(
                {
                    "action_id": f"{workflow_id}-A{action_number}",
                    "workflow_id": workflow_id,
                    "action": random.choice(
                        [
                            "Confirm source ownership and SLA",
                            "Launch two-week pilot cohort",
                            "Add manager review checkpoint",
                            "Backtest against previous quarter",
                            "Create enablement brief for field leaders",
                            "Move into weekly revenue operating review",
                        ]
                    ),
                    "owner": owner,
                    "effort": random.choice(["Low", "Medium", "High"]),
                    "expected_outcome": random.choice(
                        [
                            "Higher stage conversion",
                            "Cleaner forecast calls",
                            "Faster account review",
                            "Reduced manual inspection time",
                            "Earlier renewal intervention",
                        ]
                    ),
                }
            )
        for field in ["account fit", "opportunity stage", "contact role", "usage signal", "manager note"]:
            quality_rows.append(
                {
                    "workflow_id": workflow_id,
                    "source_table": source,
                    "field_group": field,
                    "freshness_hours": random.randint(2, 72),
                    "completeness_pct": clamp(random.randint(data_ready - 18, data_ready + 7), 35, 100),
                    "definition_owner": random.choice(["RevOps", "Sales", "Marketing Ops", "CS Ops", "Data Engineering"]),
                    "launch_blocker": "Yes" if data_ready < 68 and random.random() > 0.45 else "No",
                }
            )

    pipeline_rows = []
    capacity_rows = []
    for t in territories:
        base_pipeline = t["quota"] * random.uniform(1.55, 3.05)
        closed_won = t["quota"] * random.uniform(0.12, 0.34)
        coverage = base_pipeline / t["quota"]
        automation_hours = random.randint(80, 310)
        productivity_gain = automation_hours * random.uniform(850, 2100)
        capacity_rows.append(
            {
                "territory": t["territory"],
                "segment": t["segment"],
                "sales_reps": t["reps"],
                "named_accounts": t["accounts"],
                "annual_quota_usd": t["quota"],
                "open_pipeline_usd": money(base_pipeline),
                "pipeline_coverage": round(coverage, 2),
                "capacity_load_pct": random.randint(76, 122),
                "weekly_admin_hours_releasable": automation_hours,
                "modeled_productivity_gain_usd": money(productivity_gain),
                "planning_recommendation": "Add coverage" if coverage < 2.2 else "Shift automation here" if automation_hours > 185 else "Monitor",
            }
        )
        for week in range(1, 17):
            pipeline_rows.append(
                {
                    "territory": t["territory"],
                    "week": f"2026-W{week:02d}",
                    "pipeline_created_usd": money(base_pipeline * random.uniform(0.025, 0.075)),
                    "stage_2_plus_usd": money(base_pipeline * random.uniform(0.25, 0.62)),
                    "closed_won_usd": money(closed_won * random.uniform(0.05, 0.13)),
                    "forecast_commit_usd": money(t["quota"] * random.uniform(0.18, 0.42)),
                    "deal_velocity_days": random.randint(58, 142),
                    "forecast_risk_pct": random.randint(9, 38),
                }
            )

    priority_rows = sorted(priority_rows, key=lambda row: float(row["priority_score"]), reverse=True)
    impact_rows = []
    for row in priority_rows:
        impact_rows.append(
            {
                "workflow_id": row["workflow_id"],
                "workflow_name": row["workflow_name"],
                "motion": row["motion"],
                "annualized_revenue_impact_usd": row["annualized_revenue_impact_usd"],
                "pipeline_influence_usd": row["pipeline_influence_usd"],
                "expected_lift_pct": row["expected_lift_pct"],
                "payback_multiple": row["payback_multiple"],
                "recommended_decision": row["recommended_decision"],
            }
        )

    blocker_rows = [row for row in quality_rows if row["launch_blocker"] == "Yes"]
    blocker_rows = sorted(blocker_rows, key=lambda row: (row["workflow_id"], int(row["freshness_hours"])))

    write_csv(DATA / "accounts.csv", accounts, list(accounts[0].keys()))
    write_csv(DATA / "agent_workflows.csv", workflow_rows, list(workflow_rows[0].keys()))
    write_csv(DATA / "workflow_runs.csv", run_rows, list(run_rows[0].keys()))
    write_csv(DATA / "pipeline_snapshots.csv", pipeline_rows, list(pipeline_rows[0].keys()))
    write_csv(DATA / "territory_capacity.csv", capacity_rows, list(capacity_rows[0].keys()))
    write_csv(DATA / "data_quality_checks.csv", quality_rows, list(quality_rows[0].keys()))
    write_csv(DATA / "recommended_actions.csv", action_rows, list(action_rows[0].keys()))

    write_csv(OUTPUTS / "agent_workflow_scorecard.csv", priority_rows, list(priority_rows[0].keys()))
    write_csv(OUTPUTS / "pipeline_impact_model.csv", impact_rows, list(impact_rows[0].keys()))
    write_csv(OUTPUTS / "territory_capacity_plan.csv", capacity_rows, list(capacity_rows[0].keys()))
    write_csv(OUTPUTS / "data_quality_queue.csv", blocker_rows, list(quality_rows[0].keys()))

    deploy_next = [r for r in priority_rows if r["recommended_decision"] == "Deploy next"]
    summary = {
        "random_seed": RANDOM_SEED,
        "account_count": len(accounts),
        "workflow_count": len(workflow_rows),
        "workflow_run_rows": len(run_rows),
        "pipeline_snapshot_rows": len(pipeline_rows),
        "data_quality_checks": len(quality_rows),
        "launch_blockers": len(blocker_rows),
        "top_workflow": priority_rows[0]["workflow_name"],
        "top_workflow_score": priority_rows[0]["priority_score"],
        "deploy_next_count": len(deploy_next),
        "modeled_annualized_revenue_impact_usd": sum(int(r["annualized_revenue_impact_usd"]) for r in priority_rows),
        "modeled_releasable_hours_per_week": sum(int(r["weekly_hours_saved"]) for r in priority_rows),
        "average_data_readiness_pct": round(sum(int(r["data_readiness_pct"]) for r in priority_rows) / len(priority_rows), 1),
        "average_pipeline_coverage": round(sum(float(r["pipeline_coverage"]) for r in capacity_rows) / len(capacity_rows), 2),
    }
    (OUTPUTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    print(f"Generated {len(accounts)} accounts, {len(workflow_rows)} workflows, and {len(blocker_rows)} launch blockers.")
    print(f"Top workflow: {summary['top_workflow']} with score {summary['top_workflow_score']}.")


if __name__ == "__main__":
    main()
