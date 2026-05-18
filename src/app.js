const paths = {
  summary: "analysis/outputs/summary.json",
  scorecard: "analysis/outputs/agent_workflow_scorecard.csv",
  impact: "analysis/outputs/pipeline_impact_model.csv",
  capacity: "analysis/outputs/territory_capacity_plan.csv",
  blockers: "analysis/outputs/data_quality_queue.csv",
};

const currency = new Intl.NumberFormat("en-US", {
  style: "currency",
  currency: "USD",
  maximumFractionDigits: 0,
});

function parseCsv(text) {
  const rows = [];
  const lines = text.trim().split(/\r?\n/);
  const headers = lines.shift().split(",");
  for (const line of lines) {
    const values = [];
    let value = "";
    let insideQuote = false;
    for (const char of line) {
      if (char === '"') {
        insideQuote = !insideQuote;
      } else if (char === "," && !insideQuote) {
        values.push(value);
        value = "";
      } else {
        value += char;
      }
    }
    values.push(value);
    rows.push(Object.fromEntries(headers.map((header, index) => [header, values[index] ?? ""])));
  }
  return rows;
}

async function getCsv(path) {
  const response = await fetch(path);
  return parseCsv(await response.text());
}

function numberValue(value) {
  return Number(String(value).replace(/[$,]/g, ""));
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function badgeClass(decision) {
  if (decision === "Deploy next") return "deploy";
  if (decision === "Pilot with guardrails") return "pilot";
  return "fix";
}

function renderPriorityTable(rows) {
  const table = document.getElementById("priority-table");
  table.innerHTML = rows.slice(0, 7).map((row) => `
    <tr>
      <td><strong>${row.workflow_name}</strong><span>${row.business_owner}</span></td>
      <td>${row.motion}</td>
      <td>${row.priority_score}</td>
      <td>${currency.format(numberValue(row.annualized_revenue_impact_usd))}</td>
      <td><mark class="${badgeClass(row.recommended_decision)}">${row.recommended_decision}</mark></td>
    </tr>
  `).join("");
}

function renderImpactBars(rows) {
  const holder = document.getElementById("impact-bars");
  const topRows = rows.slice(0, 6);
  const max = Math.max(...topRows.map((row) => numberValue(row.annualized_revenue_impact_usd)));
  holder.innerHTML = topRows.map((row) => {
    const width = Math.max(8, (numberValue(row.annualized_revenue_impact_usd) / max) * 100);
    return `
      <div class="bar-row">
        <div class="bar-label">
          <strong>${row.workflow_name}</strong>
          <span>${currency.format(numberValue(row.annualized_revenue_impact_usd))}</span>
        </div>
        <div class="bar-track"><div class="bar-fill impact" style="width:${width}%"></div></div>
      </div>
    `;
  }).join("");
}

function renderWorkflowCards(rows) {
  const holder = document.getElementById("workflow-cards");
  holder.innerHTML = rows.map((row) => `
    <article class="workflow-card">
      <div class="card-top">
        <span>${row.motion}</span>
        <mark class="${badgeClass(row.recommended_decision)}">${row.recommended_decision}</mark>
      </div>
      <h3>${row.workflow_name}</h3>
      <dl>
        <div><dt>Impact</dt><dd>${currency.format(numberValue(row.annualized_revenue_impact_usd))}</dd></div>
        <div><dt>Lift</dt><dd>${row.expected_lift_pct}%</dd></div>
        <div><dt>Adoption</dt><dd>${row.adoption_pct}%</dd></div>
        <div><dt>Readiness</dt><dd>${row.data_readiness_pct}%</dd></div>
      </dl>
      <div class="meter" aria-label="Priority score">
        <span style="width:${Math.min(100, Number(row.priority_score) * 1.5)}%"></span>
      </div>
      <p>${row.business_owner} owns the source-to-action path across ${row.accounts_in_scope} scoped records.</p>
    </article>
  `).join("");
}

function renderCoverage(capacity) {
  const holder = document.getElementById("coverage-bars");
  const max = Math.max(...capacity.map((row) => Number(row.pipeline_coverage)));
  holder.innerHTML = capacity.map((row) => {
    const width = (Number(row.pipeline_coverage) / max) * 100;
    return `
      <div class="bar-row">
        <div class="bar-label">
          <strong>${row.territory}</strong>
          <span>${row.pipeline_coverage}x</span>
        </div>
        <div class="bar-track"><div class="bar-fill coverage" style="width:${width}%"></div></div>
      </div>
    `;
  }).join("");
}

function renderCapacityTable(capacity) {
  const table = document.getElementById("capacity-table");
  table.innerHTML = capacity.map((row) => `
    <tr>
      <td><strong>${row.territory}</strong><span>${row.sales_reps} reps, ${row.named_accounts} accounts</span></td>
      <td>${row.capacity_load_pct}%</td>
      <td>${row.weekly_admin_hours_releasable}</td>
      <td>${row.planning_recommendation}</td>
    </tr>
  `).join("");
}

function renderBlockers(blockers) {
  const holder = document.getElementById("blocker-list");
  holder.innerHTML = blockers.slice(0, 8).map((row) => `
    <article>
      <span>${row.workflow_id}</span>
      <strong>${row.field_group}</strong>
      <p>${row.source_table} is ${row.completeness_pct}% complete with ${row.freshness_hours} hour freshness. Owner: ${row.definition_owner}.</p>
    </article>
  `).join("");
}

async function init() {
  const [summary, scorecard, impact, capacity, blockers] = await Promise.all([
    fetch(paths.summary).then((response) => response.json()),
    getCsv(paths.scorecard),
    getCsv(paths.impact),
    getCsv(paths.capacity),
    getCsv(paths.blockers),
  ]);

  const deployable = scorecard.find((row) => row.recommended_decision === "Deploy next") || scorecard[0];
  setText("hero-decision", `Deploy ${deployable.workflow_name}`);
  setText("hero-context", `${deployable.business_owner} has the best mix of readiness, guardrails, modeled impact, and executive measurability.`);
  setText("metric-impact", currency.format(summary.modeled_annualized_revenue_impact_usd));
  setText("metric-workflows", summary.workflow_count);
  setText("metric-hours", summary.modeled_releasable_hours_per_week);
  setText("metric-blockers", summary.launch_blockers);

  renderPriorityTable(scorecard);
  renderImpactBars(impact);
  renderWorkflowCards(scorecard);
  renderCoverage(capacity);
  renderCapacityTable(capacity);
  renderBlockers(blockers);
}

init();
