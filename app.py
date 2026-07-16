import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

st.set_page_config(page_title="IBM Bob Acquisition Speed Command Center", layout="wide")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f2f4f8;
    }
    [data-testid="stTabs"] button {
        background-color: #ffffff;
        border: 1px solid #dfe3e8;
        border-radius: 10px 10px 0 0;
        margin-right: 6px;
        padding: 10px 18px;
        color: #525252;
        font-weight: 600;
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        color: #0f62fe;
        border-bottom: 3px solid #0f62fe;
    }
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid #dfe3e8;
    }
    [data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #dfe3e8;
        padding: 16px;
        border-radius: 12px;
    }
    [data-testid="stMetricLabel"] {
        color: #525252;
        font-weight: 600;
    }
    [data-testid="stMetricValue"] {
        color: #0f62fe;
        font-weight: 700;
    }
    .executive-banner {
        background: linear-gradient(135deg, #0f62fe 0%, #0043ce 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 14px;
        margin-bottom: 20px;
    }
    .executive-card {
        background-color: #ffffff;
        border: 1px solid #dfe3e8;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
    }
    .badge-complete {
        background-color: #d4edda; color: #155724;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600;
    }
    .badge-inprogress {
        background-color: #fff3cd; color: #856404;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600;
    }
    .badge-atrisk {
        background-color: #f8d7da; color: #721c24;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600;
    }
    .badge-notstarted {
        background-color: #e2e3e5; color: #383d41;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600;
    }
    .badge-critical {
        background-color: #6f0000; color: #ffffff;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600;
    }
    .badge-high {
        background-color: #f8d7da; color: #721c24;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600;
    }
    .badge-medium {
        background-color: #fff3cd; color: #856404;
        padding: 3px 10px; border-radius: 12px;
        font-size: 12px; font-weight: 600;
    }
    .risk-row {
        background-color: #ffffff;
        border: 1px solid #dfe3e8;
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("IBM Bob Acquisition Speed Command Center")
workspace_name = st.text_input("Acquisition Workspace Name", value="Company X Integration")
integration_lead = st.text_input("Integration Lead", value="Priya Nair")
region = st.selectbox("Region", ["APAC", "Americas", "EMEA", "Japan"])
date_col1, date_col2 = st.columns(2)
with date_col1:
    day_1_date = st.date_input("Day 1 Target Date", value=date.today())
with date_col2:
    day_100_date = st.date_input("Day 100 Target Date", value=day_1_date + timedelta(days=100))
st.subheader(f"Prototype Dashboard - {workspace_name}")
st.write("Bob is the single front door for acquisition integration — combining uploaded data, IBM knowledge, live metrics and agentic guidance to accelerate Day 1 to Day 100 execution.")


def recommend_legal_entity_action(entity):
    if entity["regulatory_required"] == "Yes":
        return "Retain"
    if entity["employees"] == 0 and entity["annual_revenue"] == 0 and entity["active_contracts"] == "No":
        return "Dissolve"
    if entity["duplicate_ibm_presence"] == "Yes" and entity["regulatory_required"] == "No":
        return "Merge"
    return "Further Assessment"


def get_legal_entity_reason(entity):
    if entity["regulatory_required"] == "Yes":
        return "Regulatory requirement exists"
    if entity["employees"] == 0 and entity["annual_revenue"] == 0 and entity["active_contracts"] == "No":
        return "No employees, no revenue, no active contracts"
    if entity["duplicate_ibm_presence"] == "Yes" and entity["regulatory_required"] == "No":
        return "Duplicate IBM presence exists"
    return "Requires further assessment"


def get_legal_entity_confidence(entity):
    if entity["regulatory_required"] == "Yes":
        return "High"
    if entity["employees"] == 0 and entity["annual_revenue"] == 0 and entity["active_contracts"] == "No":
        return "High"
    if entity["duplicate_ibm_presence"] == "Yes" and entity["regulatory_required"] == "No":
        return "Medium"
    return "Low"


def get_legal_entity_required_approval(entity):
    if entity["recommended_action"] == "Retain":
        return "Legal"
    if entity["recommended_action"] == "Dissolve":
        return "Legal / Tax"
    if entity["recommended_action"] == "Merge":
        return "Legal / Treasury"
    return "Legal / Tax / Treasury"


def get_legal_entity_compliance_risk(entity):
    if entity["regulatory_required"] == "Yes":
        return "High"
    if entity["active_contracts"] == "Yes":
        return "Medium"
    return "Low"


def calculate_readiness_score(status_series):
    score_map = {
        "Complete": 100,
        "In Progress": 60,
        "At Risk": 30,
        "Not Started": 0,
    }
    total_score = status_series.map(score_map).fillna(0).sum()
    return round(total_score / len(status_series)) if len(status_series) else 0


def status_badge(status):
    mapping = {
        "Complete": "badge-complete",
        "In Progress": "badge-inprogress",
        "At Risk": "badge-atrisk",
        "Not Started": "badge-notstarted",
    }
    css = mapping.get(status, "badge-notstarted")
    return f"<span class='{css}'>{status}</span>"


def severity_badge(severity):
    mapping = {
        "Critical": "badge-critical",
        "High": "badge-high",
        "Medium": "badge-medium",
    }
    css = mapping.get(severity, "badge-medium")
    return f"<span class='{css}'>{severity}</span>"


def render_tab_header(title, summary):
    st.caption("Private and Confidential")
    st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
    st.header(title)
    st.write(summary)
    st.markdown("</div>", unsafe_allow_html=True)


st.sidebar.header("Data Upload Center")
st.sidebar.caption("Upload your own files to replace the sample data below.")
uploaded_integration_status = st.sidebar.file_uploader("Integration status CSV", type="csv")
uploaded_risks = st.sidebar.file_uploader("Risks CSV", type="csv")
uploaded_budget = st.sidebar.file_uploader("Budget CSV", type="csv")
uploaded_legal_entities = st.sidebar.file_uploader("Legal entities CSV", type="csv")
uploaded_sme_directory = st.sidebar.file_uploader("SME directory CSV", type="csv")
uploaded_knowledge_library = st.sidebar.file_uploader("Knowledge library TXT", type="txt")
uploaded_sod_matrix = st.sidebar.file_uploader("SoD matrix CSV", type="csv")
st.sidebar.markdown("---")
st.sidebar.caption("IBM Bob Acquisition Speed Command Center v1.0")


try:
    integration_status = pd.read_csv(uploaded_integration_status or "sample_data/integration_status.csv")
    risks = pd.read_csv(uploaded_risks or "sample_data/risks.csv")
    budget = pd.read_csv(uploaded_budget or "sample_data/budget.csv")
    legal_entities = pd.read_csv(uploaded_legal_entities or "sample_data/legal_entities.csv")
    sme_directory = pd.read_csv(uploaded_sme_directory or "sample_data/sme_directory.csv")
    sod_matrix = pd.read_csv(uploaded_sod_matrix if uploaded_sod_matrix is not None else "sample_data/sod_matrix.csv")

    if uploaded_knowledge_library is not None:
        knowledge_library_text = uploaded_knowledge_library.getvalue().decode("utf-8")
    else:
        with open("sample_data/knowledge_library.txt", encoding="utf-8") as knowledge_file:
            knowledge_library_text = knowledge_file.read()

    legal_entities["recommended_action"] = legal_entities.apply(recommend_legal_entity_action, axis=1)
    legal_entities["recommendation_reason"] = legal_entities.apply(get_legal_entity_reason, axis=1)
    legal_entities["confidence_level"] = legal_entities.apply(get_legal_entity_confidence, axis=1)
    legal_entities["required_approval"] = legal_entities.apply(get_legal_entity_required_approval, axis=1)
    legal_entities["compliance_risk"] = legal_entities.apply(get_legal_entity_compliance_risk, axis=1)
    legal_entities["estimated_recurring_savings_example"] = legal_entities["saving_if_action_is_taken"]

    completed_areas = (integration_status["status"] == "Complete").sum()
    at_risk_areas = (integration_status["status"] == "At Risk").sum()
    not_started_areas = (integration_status["status"] == "Not Started").sum()
    total_areas = len(integration_status)
    readiness_percent = calculate_readiness_score(integration_status["status"])
    critical_risks = (risks["severity"] == "Critical").sum()
    high_risks = (risks["severity"] == "High").sum()
    medium_risks = (risks["severity"] == "Medium").sum()
    total_budget = budget["budget"].sum()
    actual_spend = budget["actual_spend"].sum()
    forecast_spend = budget["forecast_spend"].sum()
    estimated_savings = budget["estimated_savings"].sum()
    merge_or_dissolve_entities = legal_entities[
        legal_entities["recommended_action"].isin(["Merge", "Dissolve"])
    ]
    annual_admin_cost_reduction = merge_or_dissolve_entities["annual_admin_cost"].sum()
    total_action_savings = merge_or_dissolve_entities["saving_if_action_is_taken"].sum()
    total_value_opportunity = estimated_savings + total_action_savings
    cash_release_opportunity = annual_admin_cost_reduction
    sme_actions_required = len(risks)
    knowledge_files_loaded = 1 if knowledge_library_text.strip() else 0
    budget_variance_pct = round(((forecast_spend - total_budget) / total_budget) * 100, 1) if total_budget else 0

    budget_totals = pd.DataFrame(
        [
            {
                "category": "Total",
                "budget": budget["budget"].sum(),
                "actual_spend": budget["actual_spend"].sum(),
                "forecast_spend": budget["forecast_spend"].sum(),
                "estimated_savings": budget["estimated_savings"].sum(),
            }
        ]
    )
    legal_entity_totals = pd.DataFrame(
        [
            {
                "entity_name": "Total",
                "annual_admin_cost": legal_entities["annual_admin_cost"].sum(),
                "annual_audit_fees": legal_entities["annual_audit_fees"].sum(),
                "saving_if_action_is_taken": legal_entities["saving_if_action_is_taken"].sum(),
            }
        ]
    )
    japan_payroll_sme = sme_directory[
        (sme_directory["function"] == "Payroll") & (sme_directory["geography"] == "Japan")
    ]
    budget_chart_data = budget.set_index("category")[["budget", "actual_spend", "forecast_spend"]]
    legal_action_counts = legal_entities["recommended_action"].value_counts()
    status_counts = integration_status["status"].value_counts()

    dashboard_tab, status_tab, risks_tab, budget_tab, legal_tab, sme_tab, knowledge_tab, bob_tab = st.tabs(
        [
            "Dashboard",
            "Integration Status",
            "Risks",
            "Budget",
            "Legal Entities",
            "SME Directory",
            "Knowledge Library",
            "IBM Bob Q&A",
        ]
    )

    # ── DASHBOARD TAB ──────────────────────────────────────────────────────────
    with dashboard_tab:
        st.caption("Private and Confidential")

        # ── Title banner ──
        st.markdown(
            f"""
            <div class="executive-banner">
                <div style="font-size: 24px; font-weight: 700; margin-bottom: 4px;">
                    Live Prototype Dashboard — {workspace_name}
                </div>
                <div style="font-size: 13px; opacity: 0.85; margin-bottom: 12px;">
                    The prototype is live — and the outcomes are measurable, not aspirational.
                </div>
                <div style="display:flex; gap:32px; font-size:13px; flex-wrap:wrap;">
                    <span><b>Integration Lead:</b> &nbsp;{integration_lead}</span>
                    <span><b>Region:</b> &nbsp;{region}</span>
                    <span><b>Day 1 Target:</b> &nbsp;{day_1_date}</span>
                    <span><b>Day 100 Target:</b> &nbsp;{day_100_date}</span>
                    <span><b>Open Risk Actions:</b> &nbsp;{len(risks)}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── 5 top metric cards ──
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("Overall Readiness", f"{readiness_percent}%",
                   delta=f"{int(completed_areas)} of {total_areas} areas complete")
        mc2.metric("Critical / High Risks", f"{critical_risks} / {high_risks}",
                   delta=f"{critical_risks} Critical · {high_risks} High · {medium_risks} Medium",
                   delta_color="inverse")
        mc3.metric("Forecast Spend", f"${forecast_spend/1e6:.2f}M",
                   delta=f"{budget_variance_pct:+.1f}% vs ${total_budget/1e6:.2f}M budget",
                   delta_color="inverse")
        mc4.metric("Total Value Opportunity", f"${total_value_opportunity/1000:.0f}K",
                   delta=f"Cash Release: ${cash_release_opportunity/1000:.0f}K")
        mc5.metric("Legal Entities to Simplify", f"{len(merge_or_dissolve_entities)} / {len(legal_entities)}",
                   delta=f"{round(len(merge_or_dissolve_entities)/len(legal_entities)*100)}% targeted for action")

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Main 2-column layout: Journey (left) | Panels (right) ──
        journey_col, panels_col = st.columns([1.5, 1])

        with journey_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.markdown("**Integration Journey — 7 Workstreams**")
            journey_steps = [
                ("Due Diligence",             "Complete"),
                ("Day 1 Readiness",           "In Progress"),
                ("Accounting & Process Mapping", "In Progress"),
                ("Workforce Alignment",       "Not Started"),
                ("Systems & Controls",        "At Risk"),
                ("Legal Entity Simplif.",     "In Progress"),
                ("Steady State",              "Not Started"),
            ]
            bar_colors = {
                "Complete":    "#42be65",
                "In Progress": "#00b0ff",
                "At Risk":     "#fa4d56",
                "Not Started": "#3a3a3a",
            }
            bar_widths = {
                "Complete":    100,
                "In Progress": 55,
                "At Risk":     35,
                "Not Started": 5,
            }
            for step, s in journey_steps:
                bw   = bar_widths.get(s, 10)
                bc   = bar_colors.get(s, "#555")
                lbl_color = {"Complete":"#42be65","In Progress":"#00b0ff","At Risk":"#fa4d56","Not Started":"#888"}.get(s,"#aaa")
                st.markdown(
                    f"""<div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                        <div style="width:130px;font-size:13px;color:#1f2328;font-weight:500;">{step}</div>
                        <div style="flex:1;background:#e5e7eb;border-radius:4px;height:14px;">
                            <div style="width:{bw}%;background:{bc};height:14px;border-radius:4px;"></div>
                        </div>
                        <div style="width:90px;text-align:right;font-size:12px;font-weight:600;color:{bc};">{s}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)


        with panels_col:
            # Budget overview panel
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.markdown("**Budget Overview**")
            budget_items = list(zip(budget["category"], budget["forecast_spend"]))
            total_fc = budget["forecast_spend"].sum()
            for cat, val in budget_items:
                pct = int(val / total_fc * 100) if total_fc else 0
                st.markdown(
                    f"""<div style="display:flex;align-items:center;gap:8px;margin-bottom:5px;">
                        <div style="width:120px;font-size:12px;color:#444;">{cat}</div>
                        <div style="flex:1;background:#e5e7eb;border-radius:3px;height:10px;">
                            <div style="width:{pct}%;background:#0f62fe;height:10px;border-radius:3px;"></div>
                        </div>
                        <div style="width:55px;text-align:right;font-size:12px;color:#444;">${val/1000:.0f}K</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            st.markdown(
                f"""<div style="display:flex;align-items:center;gap:8px;margin-top:8px;border-top:1px solid #e5e7eb;padding-top:6px;">
                    <div style="width:120px;font-size:12px;font-weight:700;">Forecast Total</div>
                    <div style="flex:1;background:#e5e7eb;border-radius:3px;height:10px;">
                        <div style="width:100%;background:#42be65;height:10px;border-radius:3px;"></div>
                    </div>
                    <div style="width:55px;text-align:right;font-size:12px;font-weight:700;color:#0f62fe;">${total_fc/1e6:.2f}M</div>
                </div>""",
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)

            # Legal entity donut panel
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.markdown("**Legal Entity Actions**")
            simplify_count = len(merge_or_dissolve_entities)
            retain_count   = len(legal_entities) - simplify_count
            total_ent      = len(legal_entities)
            fig_donut = go.Figure(data=[go.Pie(
                labels=["Simplify / Dissolve", "Retain"],
                values=[simplify_count, retain_count],
                hole=0.6,
                marker_colors=["#00b0ff", "#42be65"],
                textinfo="none",
            )])
            fig_donut.update_layout(
                showlegend=False, margin=dict(t=0,b=0,l=0,r=0),
                height=140, paper_bgcolor="rgba(0,0,0,0)",
            )
            dc1, dc2 = st.columns([1, 1.2])
            with dc1:
                st.plotly_chart(fig_donut, use_container_width=True)
            with dc2:
                st.markdown(
                    f"""<div style="font-size:12px;padding-top:20px;">
                        <div style="margin-bottom:4px;"><span style="color:#00b0ff;">●</span> Simplify / Dissolve &nbsp;<b>{simplify_count}</b></div>
                        <div style="margin-bottom:4px;"><span style="color:#42be65;">●</span> Retain &nbsp;<b>{retain_count}</b></div>
                        <div style="margin-bottom:4px;"><span style="color:#888;">●</span> Total Entities &nbsp;<b>{total_ent}</b></div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # Live alerts panel
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.markdown("**Live Command Center Alerts**")
            alerts = []
            if critical_risks > 0:
                alerts.append(("🔴", f"{critical_risks} Critical risk needs immediate escalation"))
            if high_risks > 0:
                alerts.append(("🔴", f"{high_risks} High risks need owner within 48h"))
            if at_risk_areas > 0:
                at_risk_names = integration_status[integration_status["status"] == "At Risk"]["area"].tolist()
                alerts.append(("🟠", f"{at_risk_areas} workstreams At Risk — {', '.join(at_risk_names)}"))
            if not_started_areas > 0:
                alerts.append(("⚫", f"{not_started_areas} workstreams Not Started"))
            alerts.append(("🟢", f"Forecast ${forecast_spend/1e6:.2f}M vs ${total_budget/1e6:.2f}M budget ({budget_variance_pct:+.1f}%)"))
            for icon, msg in alerts:
                st.markdown(
                    f'<div style="font-size:12px;margin-bottom:5px;">{icon} {msg}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Ask Bob full-width below columns ──
        st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
        st.markdown("**Ask IBM Bob**")
        st.write("Ask anything about this acquisition integration.")
        dashboard_bob_question = st.text_area(
            "",
            value="Multi-layer processes are not harmonized — where do we even start?",
            height=100,
            key="dashboard_bob_question",
        )
        dashboard_ask = st.button("Ask Bob", key="dashboard_ask_bob")
        st.markdown("</div>", unsafe_allow_html=True)

        # ── Bob response full-width below ──
        if dashboard_ask and dashboard_bob_question:
            q = dashboard_bob_question.lower()

            # ── Intent scoring: pick the highest-confidence topic ──
            scores = {
                "sod":        sum([q.count(k) for k in ["sod", "segregation of duties", "separation of duties", "sod risk", "sod conflict", "dual approval", "dual authorization", "conflicting role", "conflicting roles", "controls conflict", "access conflict", "fraud risk", "misappropriation"]]),
                "legal":      sum([q.count(k) for k in ["legal entity", "legal entities", "merge", "dissolve", "dissolution", "entity simplif", "simplification", "retain", "entity structure", "subsidiary", "holding company"]]),
                "payroll":    sum([q.count(k) for k in ["payroll", "japan", "salary", "compensation payroll", "pay run", "employee pay", "payroll sme"]]),
                "budget":     sum([q.count(k) for k in ["budget", "spend", "forecast", "cost", "savings", "variance", "overspend", "cash release", "cash impact", "value opportunity", "cash flow", "underspend", "capex", "opex"]]),
                "coa":        sum([q.count(k) for k in ["coa", "chart of accounts", "erp", "accounting mapping", "account mapping", "close", "consolidated close", "system cutover", "cutover", "mapping gap", "account structure"]]),
                "risk":       sum([q.count(k) for k in ["risk", "risks", "critical risk", "high risk", "open risk", "escalate", "all risks", "open risks", "risk register", "risk status", "unresolved risk", "outstanding risk"]]),
                "tax":        sum([q.count(k) for k in ["tax", "gst", "vat", "tax registration", "malaysia", "tax compliance", "tax gap", "tax risk", "withholding"]]),
                "hr":         sum([q.count(k) for k in ["hr", "workforce", "employee", "headcount", "org design", "reporting line", "org structure", "people", "talent", "benefits", "compensation", "change management"]]),
                "sme":        sum([q.count(k) for k in ["sme", "who can help", "contact", "expert", "specialist", "subject matter", "who owns", "who is responsible", "find an sme", "subject matter expert"]]),
                "readiness":  sum([q.count(k) for k in ["readiness", "day 1", "day one", "day1", "ready", "not started", "at risk workstream", "systems access", "it access", "access provisioning", "systems integration", "it integration", "systems readiness", "day 100"]]),
                "harmonize":  sum([q.count(k) for k in ["harmonize", "harmonized", "harmonisation", "harmonization", "where do we", "multi-layer", "not harmonized", "process gap", "process layer", "process alignment", "process design", "target operating model", "tom"]]),
                "finance":    sum([q.count(k) for k in ["finance", "financial", "accounting", "controller", "cfo", "ap ", "ar ", "accounts payable", "accounts receivable", "general ledger", "fixed asset", "bank payment", "procurement", "vendor", "invoice", "journal", "reconcil", "bank reconcil", "treasury"]]),
                "timeline":   sum([q.count(k) for k in ["timeline", "milestone", "when", "schedule", "integration plan", "integration timeline", "plan", "target date", "deadline", "roadmap", "100 day", "hundred day"]]),
                "controls":   sum([q.count(k) for k in ["controls gap", "controls framework", "internal control", "control assessment", "ibm controls", "controls standard", "audit", "internal audit", "gap assessment", "controls review"]]),
            }
            # SoD hard-boost — always wins when the question is clearly about SoD
            if ("sod" in q or "segregation" in q or "separation of duties" in q or "sod conflict" in q or "sod risk" in q):
                scores["sod"] += 10
            # "open risks" / "all risks" boost — boost risk score so it beats the general case
            if any(k in q for k in ["open risk", "all risk", "risk register", "outstanding risk", "unresolved risk"]):
                scores["risk"] += 5
            # cash release → budget, not general
            if any(k in q for k in ["cash release", "cash impact", "cash flow", "value opportunity"]):
                scores["budget"] += 5
            topic = max(scores, key=scores.get) if max(scores.values()) > 0 else "general"

            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("IBM Bob Response")
            st.subheader("Executive Summary")

            if topic == "sod":
                sod_critical = sod_matrix[sod_matrix["severity"] == "Critical"]
                sod_high     = sod_matrix[sod_matrix["severity"] == "High"]
                sod_open_risks = risks[risks["risk"].str.lower().str.contains("sod")]
                st.write(
                    f"IBM Bob identified **{len(sod_critical)} Critical** and **{len(sod_high)} High** Segregation of Duties (SoD) conflicts across {sod_matrix['process'].nunique()} processes. "
                    f"Critical conflicts include bank payment authorization, payroll bank detail custody, and vendor master management — all requiring immediate remediation before Day 1."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Risk & Controls Agent\n- SoD Assessment Agent\n- Integration Navigator Agent")
                st.subheader("Critical SoD Conflicts")
                st.dataframe(sod_critical[["process", "task", "sod_role", "assigned_to", "conflicts_with", "sod_risk", "mitigation"]], use_container_width=True)
                st.subheader("High SoD Conflicts")
                st.dataframe(sod_high[["process", "task", "sod_role", "assigned_to", "conflicts_with", "sod_risk", "mitigation"]], use_container_width=True)
                if len(sod_open_risks) > 0:
                    st.subheader("SoD Risks in Risk Register")
                    st.dataframe(sod_open_risks[["risk_id", "severity", "risk", "owner", "status", "mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions")
                st.write(
                    "1. Immediately separate bank payment authorization from custody — implement dual authorization for all payments.\n"
                    "2. Remove payroll team access to employee bank details — assign a dedicated custodian.\n"
                    "3. Restrict vendor master management to Finance Controls team only; AP to process payments only.\n"
                    "4. Require secondary approval for all manual journal entries in the General Ledger.\n"
                    "5. Assign an independent reconciler for AP, AR, and Bank — not involved in posting.\n"
                    "6. Complete a full IBM controls gap assessment for all acquired entities before Day 100."
                )
                st.subheader("Owners")
                st.write(f"{integration_lead}, Finance Controller, Treasury, HR, Internal Audit")
                st.subheader("Risks")
                st.write(f"{len(sod_critical)} Critical SoD conflicts create direct fraud, misappropriation, and financial misstatement exposure. All Critical items must be resolved before Day 1.")
                st.subheader("Next Steps")
                st.write("Open the Risks tab → SoD Assessment section to review all conflicts by process and role. Escalate Critical items to the CFO and Internal Audit immediately.")

            elif topic == "legal":
                st.write(f"IBM Bob identified {len(merge_or_dissolve_entities)} legal entities recommended for merge or dissolve, with total action savings of ${total_action_savings:,.0f} and annual admin cost reduction of ${annual_admin_cost_reduction:,.0f}.")
                st.subheader("Agent Capabilities Used"); st.write("- Legal Entity Optimization Agent\n- Budget & Value Tracking Agent")
                st.subheader("Entities Recommended for Action"); st.dataframe(merge_or_dissolve_entities[["entity_name","country","recommended_action","compliance_risk","approval_required","action_savings","annual_admin_cost_reduction"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write("1. Review entity-level recommendations and confirm approval requirements.\n2. Validate compliance risk, active contracts, and tax dependencies.\n3. Obtain Legal, Tax, and Treasury sign-off before executing any action.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Legal, Tax, Treasury")
                st.subheader("Risks"); st.write("Active contracts or regulatory gaps may block dissolution or merger actions.")
                st.subheader("Budget / Savings / Cash Impact"); st.write(f"Action savings: ${total_action_savings:,.0f}  |  Admin cost reduction: ${annual_admin_cost_reduction:,.0f}")
                st.subheader("Next Steps"); st.write("Open the Legal Entities tab and validate candidates for merge or dissolve.")

            elif topic == "payroll":
                payroll_smes = sme_directory[sme_directory["function"].str.lower().str.contains("payroll", na=False)]
                payroll_risks = risks[risks["risk"].str.lower().str.contains("payroll", na=False)]
                st.write("IBM Bob identified the payroll SME routing path and highlighted Day 1 employee continuity as a critical dependency.")
                st.subheader("Agent Capabilities Used"); st.write("- SME Discovery Agent\n- Workforce & Organization Mapping Agent\n- Risk & Controls Agent")
                if len(payroll_smes) > 0:
                    st.subheader("Payroll SMEs"); st.dataframe(payroll_smes[["function","geography","primary_sme","backup_sme","escalation_path"]], use_container_width=True)
                if len(payroll_risks) > 0:
                    st.subheader("Payroll Risks"); st.dataframe(payroll_risks[["risk_id","severity","risk","owner","status","mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write("1. Contact the primary payroll SME immediately.\n2. Confirm payroll setup timeline and Day 1 continuity plan.\n3. Resolve all open payroll SoD conflicts before processing the first payroll run.\n4. Track payroll readiness as a Critical Day 1 dependency.")
                st.subheader("Owners"); st.write("HR Director, Payroll Team, Integration Lead")
                st.subheader("Next Steps"); st.write("Open the SME Directory tab and engage the payroll SME. Review SoD conflicts in the Risks tab.")

            elif topic == "budget":
                st.write(f"IBM Bob reviewed integration spend: forecast of ${forecast_spend:,.0f} against a total budget of ${total_budget:,.0f}, with estimated savings of ${estimated_savings:,.0f}. Budget variance is {budget_variance_pct:+.1f}%.")
                st.subheader("Agent Capabilities Used"); st.write("- Budget & Value Tracking Agent")
                bm1, bm2, bm3, bm4 = st.columns(4)
                bm1.metric("Total Budget", f"${total_budget/1e6:.2f}M")
                bm2.metric("Forecast Spend", f"${forecast_spend/1e6:.2f}M", delta=f"{budget_variance_pct:+.1f}% vs budget", delta_color="inverse")
                bm3.metric("Estimated Savings", f"${estimated_savings/1000:.0f}K")
                bm4.metric("Cash Release Opportunity", f"${cash_release_opportunity/1000:.0f}K")
                st.subheader("Budget by Category"); st.dataframe(budget[["category","budget","actual_spend","forecast_spend","estimated_savings"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write("1. Review current spend by category against plan.\n2. Validate forecast assumptions and savings targets.\n3. Escalate any overspend categories to the Integration Lead.\n4. Confirm cash release timeline with Treasury.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance")
                st.subheader("Risks"); st.write("Forecast variance may indicate scope creep or unplanned integration costs.")
                st.subheader("Next Steps"); st.write("Open the Budget tab to review detailed spend by category.")

            elif topic == "coa":
                st.write("IBM Bob identified accounting and process mapping as the first priority. Chart of accounts alignment, process design, and ERP mapping must all be completed before the first consolidated close.")
                st.subheader("Agent Capabilities Used"); st.write("- Accounting & Process Mapping Agent\n- Integration Navigator Agent\n- Systems & Process Mapping Agent")
                st.subheader("Recommended Actions"); st.write("1. Upload and validate chart of accounts and process mapping files.\n2. Map key accounts and business processes to the IBM target structure.\n3. Identify unresolved mapping gaps and assign owners.\n4. Confirm ERP and system integration points for each mapped process.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance, APAC Controller")
                st.subheader("Risks"); st.write("Unresolved COA and process mapping blocks the first consolidated close, ERP cutover, and financial reporting.")
                st.subheader("Next Steps"); st.write("Coordinate with Finance SME to validate COA and process mapping. Confirm close calendar and ERP cutover timeline.")

            elif topic == "tax":
                tax_risks = risks[risks["risk"].str.lower().str.contains("tax", na=False)]
                st.write("IBM Bob identified tax registration gaps as a Critical Day 1 blocker. Incomplete tax registration prevents revenue recognition and increases compliance risk.")
                st.subheader("Agent Capabilities Used"); st.write("- Risk & Controls Agent\n- Integration Navigator Agent")
                if len(tax_risks) > 0:
                    st.subheader("Tax Risks"); st.dataframe(tax_risks[["risk_id","severity","risk","owner","status","mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write("1. Identify all entities with incomplete tax registration.\n2. Engage Regional Tax Lead immediately to resolve gaps.\n3. Do not recognize revenue in any entity with unresolved tax registration.")
                st.subheader("Owners"); st.write("Regional Tax Lead, Legal, Integration Lead")
                st.subheader("Next Steps"); st.write("Open the Risks tab and review R006. Escalate to the Regional Tax Lead today.")

            elif topic == "hr":
                hr_risks = risks[risks["risk"].str.lower().str.contains("hr|workforce|employee|headcount|org", na=False, regex=True)]
                st.write(f"IBM Bob identified workforce alignment as a key Day 100 dependency. HR integration covers headcount, compensation, benefits, reporting lines, and change management.")
                st.subheader("Agent Capabilities Used"); st.write("- Workforce & Organization Mapping Agent\n- SME Discovery Agent")
                if len(hr_risks) > 0:
                    st.subheader("HR & Workforce Risks"); st.dataframe(hr_risks[["risk_id","severity","risk","owner","status","mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write(f"1. Upload headcount and compensation data.\n2. Confirm reporting lines before Day 100.\n3. Ensure all employees receive communications within Week 1.\n4. Engage HR SME for change management.")
                st.subheader("Owners"); st.write(f"{integration_lead}, HR, Regional HR Leadership")
                st.subheader("Next Steps"); st.write("Open the SME Directory and engage the HR Integration SME. Confirm payroll continuity plan for Day 1.")

            elif topic == "sme":
                st.write(f"IBM Bob identified {len(sme_directory)} SME records across {sme_directory['function'].nunique()} functions and {sme_directory['geography'].nunique()} geographies.")
                st.subheader("Agent Capabilities Used"); st.write("- SME Discovery Agent")
                st.subheader("SME Directory"); st.dataframe(sme_directory[["function","geography","primary_sme","backup_sme","escalation_path"]], use_container_width=True)
                st.subheader("Next Steps"); st.write("Open the SME Directory tab and search for your function or geography.")

            elif topic == "readiness":
                st.write(f"Current integration readiness is {readiness_percent}%. {int(completed_areas)} of {total_areas} workstreams complete. {int(at_risk_areas)} At Risk, {int(not_started_areas)} Not Started.")
                st.subheader("Agent Capabilities Used"); st.write("- Integration Readiness Agent\n- Risk & Controls Agent")
                st.subheader("Readiness by Workstream"); st.dataframe(integration_status[["area","status","owner"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write(f"1. Resolve all {int(at_risk_areas)} At Risk workstreams before Day 1.\n2. Assign owners to all {int(not_started_areas)} Not Started workstreams.\n3. Schedule Day 1 readiness review 2 weeks before target.")
                st.subheader("Next Steps"); st.write("Open the Integration Status tab and address all At Risk items before the next checkpoint.")

            elif topic == "harmonize":
                st.write(f"IBM Bob recommends a structured process harmonization approach across {total_areas} workstreams. Start by mapping acquired entity processes against IBM's target operating model, then identify divergence points and assign workstream owners.")
                st.subheader("Agent Capabilities Used"); st.write("- Integration Navigator Agent\n- Accounting & Process Mapping Agent\n- Risk & Controls Agent\n- Integration Readiness Agent")
                st.subheader("Current Workstream Status"); st.dataframe(integration_status[["area","status","owner"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write("1. Run a full process inventory across Finance, HR, Legal, Tax, and Operations.\n2. Map each acquired process to the IBM target process layer.\n3. Prioritize divergence gaps by Day 1 risk and impact.\n4. Assign a workstream owner and SME to each gap.\n5. Build a harmonization roadmap with milestones to Day 1 and Day 100.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance, HR, Legal, Tax, Operations")
                st.subheader("Risks"); st.write(f"Unharmonized processes across {total_areas} workstreams increase the risk of reporting errors, compliance gaps, and delayed milestones. {int(at_risk_areas)} workstreams currently At Risk.")
                st.subheader("Next Steps"); st.write("Open the Integration Status tab and assign owners to all At Risk and Not Started workstreams. Use the Accounting & Process Mapping tab to begin the process gap analysis.")

            elif topic == "risk":
                # If user asks for open/all risks show the relevant filtered set
                if any(k in q for k in ["open risk", "all risk", "risk register", "outstanding", "unresolved", "full risk"]):
                    display_risks = risks[risks["status"] == "Open"] if "open" in q else risks
                    risk_label = "Open Risks" if "open" in q else "Full Risk Register"
                    open_count = (risks["status"] == "Open").sum()
                    st.write(f"IBM Bob found {open_count} open risks across the risk register. {critical_risks} Critical and {high_risks} High severity items require immediate attention.")
                    st.subheader("Agent Capabilities Used"); st.write("- Risk & Controls Agent\n- Integration Navigator Agent")
                    st.subheader(risk_label); st.dataframe(display_risks[["risk_id","severity","risk","owner","status","mitigation"]], use_container_width=True)
                else:
                    top_risks = risks[risks["severity"].isin(["Critical", "High"])].head(5)
                    st.write(f"IBM Bob identified {critical_risks} Critical and {high_risks} High risks. Top priority: '{risks.iloc[0]['risk']}' — owned by {risks.iloc[0]['owner']}.")
                    st.subheader("Agent Capabilities Used"); st.write("- Risk & Controls Agent\n- Integration Navigator Agent")
                    st.subheader("Top Critical & High Risks"); st.dataframe(top_risks[["risk_id","severity","risk","owner","status","mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write(f"1. Escalate all {critical_risks} Critical risks to the executive sponsor immediately.\n2. Assign mitigation plans to all {high_risks} High risks within 48 hours.\n3. Schedule a weekly risk review.")
                st.subheader("Risk Owners Summary")
                owner_summary = risks[risks["severity"].isin(["Critical","High"])].groupby("owner")["risk_id"].count().reset_index()
                owner_summary.columns = ["Owner", "Open Risk Count"]
                st.dataframe(owner_summary, use_container_width=True)
                st.subheader("Next Steps"); st.write("Open the Risks tab to review the full register. Check the SoD Assessment section for controls-related conflicts.")

            elif topic == "finance":
                finance_risks = risks[risks["risk"].str.lower().str.contains("finance|account|coa|close|erp|ap|ar|journal|ledger|bank|treasury|vendor|procurement", na=False, regex=True)]
                st.write("IBM Bob reviewed the Finance integration workstream. Key priorities are COA mapping, AP/AR controls, bank payment authorization, and consolidated close readiness.")
                st.subheader("Agent Capabilities Used"); st.write("- Accounting & Process Mapping Agent\n- Risk & Controls Agent\n- SoD Assessment Agent\n- Budget & Value Tracking Agent")
                if len(finance_risks) > 0:
                    st.subheader("Finance Risks"); st.dataframe(finance_risks[["risk_id","severity","risk","owner","status","mitigation"]], use_container_width=True)
                st.subheader("SoD Controls — Finance Processes"); st.dataframe(sod_matrix[["process","task","sod_role","assigned_to","conflicts_with","severity","mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write("1. Complete COA mapping and validate against IBM target structure.\n2. Resolve all Critical SoD conflicts in AP, AR, Payroll, and Bank & Treasury.\n3. Assign independent reconcilers for AP, AR, and Bank.\n4. Confirm close calendar and ERP cutover timeline.\n5. Implement dual authorization for all bank payments.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance Controller, CFO, Treasury, Internal Audit")
                st.subheader("Next Steps"); st.write("Open the Risks tab SoD section and the Accounting & Process Mapping tab. Escalate Critical SoD items to CFO and Internal Audit immediately.")

            elif topic == "timeline":
                st.write(f"IBM Bob reviewed the integration timeline. Day 1 target is {day_1_date} and Day 100 target is {day_100_date}. Current readiness is {readiness_percent}% — {int(at_risk_areas)} workstreams are At Risk and {int(not_started_areas)} have not started.")
                st.subheader("Agent Capabilities Used"); st.write("- Integration Navigator Agent\n- Integration Readiness Agent\n- Risk & Controls Agent")
                st.subheader("Workstream Status vs Timeline"); st.dataframe(integration_status[["area","status","owner","day1_dependency" if "day1_dependency" in integration_status.columns else "status"]], use_container_width=True)
                col_t1, col_t2, col_t3 = st.columns(3)
                col_t1.metric("Day 1 Target", str(day_1_date))
                col_t2.metric("Day 100 Target", str(day_100_date))
                col_t3.metric("Overall Readiness", f"{readiness_percent}%")
                st.subheader("Recommended Actions"); st.write(f"1. Confirm Day 1 date with the executive sponsor — currently {day_1_date}.\n2. Resolve all {int(at_risk_areas)} At Risk workstreams before Day 1.\n3. Assign owners and start dates to all {int(not_started_areas)} Not Started workstreams immediately.\n4. Build a detailed Day 1 to Day 100 milestone plan with fortnightly checkpoints.\n5. Schedule a final Day 1 readiness review 2 weeks before target.")
                st.subheader("Owners"); st.write(f"{integration_lead}, workstream leads, executive sponsor")
                st.subheader("Next Steps"); st.write("Open the Integration Status tab to review workstream owners and statuses. Update the dashboard as milestones are completed.")

            elif topic == "controls":
                controls_risks = risks[risks["risk"].str.lower().str.contains("control|audit|framework|assessment|standard|gap", na=False, regex=True)]
                sod_critical = sod_matrix[sod_matrix["severity"] == "Critical"]
                st.write(f"IBM Bob assessed the controls framework for the acquired entity. {len(sod_critical)} Critical SoD conflicts and {len(controls_risks)} controls-related risks have been identified against IBM standards.")
                st.subheader("Agent Capabilities Used"); st.write("- Risk & Controls Agent\n- SoD Assessment Agent\n- Integration Navigator Agent")
                if len(controls_risks) > 0:
                    st.subheader("Controls & Audit Risks"); st.dataframe(controls_risks[["risk_id","severity","risk","owner","status","mitigation"]], use_container_width=True)
                st.subheader("Critical SoD Controls Gaps"); st.dataframe(sod_critical[["process","task","sod_role","assigned_to","conflicts_with","sod_risk","mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write("1. Conduct a full IBM controls gap assessment for all acquired entities before Day 100.\n2. Remediate all Critical SoD conflicts before Day 1.\n3. Implement IBM standard controls framework across Finance, HR, and Operations.\n4. Assign Internal Audit to validate controls remediation.\n5. Document all accepted residual risks with CFO sign-off.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance Controller, Internal Audit, CFO")
                st.subheader("Next Steps"); st.write("Open the Risks tab → SoD Assessment section. Escalate R017 (Controls Framework Assessment) to the Integration Lead and Internal Audit immediately.")

            else:
                st.write(f"IBM Bob reviewed the current workspace: readiness at {readiness_percent}%, {critical_risks} critical and {high_risks} high-risk items open, forecast spend of ${forecast_spend:,.0f}, legal entity savings of ${total_action_savings:,.0f}.")
                st.subheader("Agent Capabilities Used"); st.write("- Integration Navigator\n- Risk & Controls Agent\n- Budget & Value Tracking Agent\n- Legal Entity Optimization Agent\n- SME Discovery Agent")
                st.subheader("Workspace Summary")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Overall Readiness", f"{readiness_percent}%")
                    st.metric("Critical Risks", critical_risks)
                    st.metric("Forecast Spend", f"${forecast_spend/1e6:.2f}M")
                with col_b:
                    st.metric("High Risks", high_risks)
                    st.metric("Entities to Simplify", f"{len(merge_or_dissolve_entities)}/{len(legal_entities)}")
                    st.metric("Value Opportunity", f"${total_value_opportunity/1000:.0f}K")
                st.subheader("Recommended Actions"); st.write("1. Validate all uploaded acquisition data.\n2. Review and assign owners to all Critical and High risks.\n3. Confirm COA, workforce, and legal entity mapping.\n4. Assign SMEs to all open workstreams.\n5. Schedule Day 1 readiness review 2 weeks before target.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
                st.subheader("Timeline"); st.write(f"Day 1: {day_1_date}  |  Day 100: {day_100_date}")
                st.subheader("Cash Release & Value Opportunity"); st.write(f"Cash Release: ${cash_release_opportunity/1000:.0f}K  |  Total Value Opportunity: ${total_value_opportunity/1000:.0f}K  |  Legal Entity Savings: ${total_action_savings/1000:.0f}K")
                st.subheader("Next Steps"); st.write(f"{integration_lead} to review open risks, legal entity candidates, and readiness gaps before next checkpoint.")
            st.markdown("</div>", unsafe_allow_html=True)

        # ── Target outcomes ──
        st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
        st.subheader("Target Outcomes")
        outcome_col1, outcome_col2, outcome_col3, outcome_col4, outcome_col5 = st.columns(5)
        outcome_col1.metric("Planning Time Reduced", "45%")
        outcome_col2.metric("SME Search Time Reduced", "60%")
        outcome_col3.metric("Mapping Effort Reduced", "35%")
        outcome_col4.metric("Readiness Review Accelerated", "50%")
        outcome_col5.metric("Estimated Value Opportunity", "$1.3M")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── INTEGRATION STATUS TAB ─────────────────────────────────────────────────
    with status_tab:
        render_tab_header(
            "Integration Status",
            "Review current progress across all tracked integration workstreams. Identify blockers, confirm Day 1 dependencies, and assign owners to drive readiness.",
        )
        status_metric_col1, status_metric_col2, status_metric_col3, status_metric_col4, status_metric_col5 = st.columns(5)
        status_metric_col1.metric("Tracked Workstreams", total_areas)
        status_metric_col2.metric("Complete", int(completed_areas))
        status_metric_col3.metric("In Progress", int((integration_status["status"] == "In Progress").sum()))
        status_metric_col4.metric("At Risk", int(at_risk_areas))
        status_metric_col5.metric("Readiness Score", f"{readiness_percent}%")
        st.progress(readiness_percent / 100)
        st.caption(f"Day 1 Dependencies: {int((integration_status['day1_dependency'] == 'Yes').sum()) if 'day1_dependency' in integration_status.columns else 'N/A'} workstreams must be complete before Day 1")
        st.markdown("---")

        # Filter controls
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            status_filter = st.selectbox("Filter by status", ["All", "Complete", "In Progress", "At Risk", "Not Started"], key="status_filter")
        with filter_col2:
            day1_filter = st.selectbox("Filter by Day 1 dependency", ["All", "Day 1 Required", "Day 100 Only"], key="day1_filter")

        filtered_status = integration_status.copy()
        if status_filter != "All":
            filtered_status = filtered_status[filtered_status["status"] == status_filter]
        if day1_filter == "Day 1 Required" and "day1_dependency" in integration_status.columns:
            filtered_status = filtered_status[filtered_status["day1_dependency"] == "Yes"]
        elif day1_filter == "Day 100 Only" and "day1_dependency" in integration_status.columns:
            filtered_status = filtered_status[filtered_status["day1_dependency"] == "No"]

        st.caption(f"Showing {len(filtered_status)} workstreams")
        st.markdown("---")

        has_details = "description" in integration_status.columns

        for _, row in filtered_status.iterrows():
            status_val   = row["status"]
            owner_val    = row["owner"]
            area_val     = row["area"]
            day1_val     = row.get("day1_dependency", "—") if has_details else "—"
            desc_val     = row.get("description", "") if has_details else ""
            tasks_val    = row.get("key_tasks", "") if has_details else ""
            blockers_val = row.get("blockers", "") if has_details else ""

            # Colour coding
            border_color = {"Complete": "#42be65", "In Progress": "#0f62fe", "At Risk": "#fa4d56", "Not Started": "#8d8d8d"}.get(status_val, "#e5e7eb")
            day1_html = (
                f'<span style="background:#fee2e2;color:#991b1b;font-size:11px;font-weight:700;padding:2px 8px;border-radius:8px;">Day 1 Required</span>'
                if day1_val == "Yes"
                else f'<span style="background:#f0fdf4;color:#166534;font-size:11px;font-weight:600;padding:2px 8px;border-radius:8px;">Day 100</span>'
            )
            blocker_html = (
                f'<div style="margin-top:6px;background:#fff7ed;border-left:3px solid #f97316;padding:6px 10px;border-radius:4px;font-size:12px;color:#9a3412;">⚠ <b>Blocker:</b> {blockers_val}</div>'
                if blockers_val and blockers_val.lower() != "none — workstream complete"
                else ""
            )

            st.markdown(
                f"""<div style="border:1px solid #e5e7eb;border-left:4px solid {border_color};border-radius:10px;
                    padding:14px 18px;margin-bottom:10px;background:#ffffff;">
                    <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                        <div>
                            <span style="font-size:15px;font-weight:700;color:#1f2328;">{area_val}</span>
                            &nbsp;&nbsp;{status_badge(status_val)}&nbsp;&nbsp;{day1_html}
                        </div>
                        <div style="font-size:12px;color:#57606a;">Owner: <b>{owner_val}</b></div>
                    </div>
                    <div style="font-size:13px;color:#444;margin-top:8px;">{desc_val}</div>
                    <div style="font-size:12px;color:#57606a;margin-top:6px;">
                        <b>Key Tasks:</b> {tasks_val}
                    </div>
                    {blocker_html}
                </div>""",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.subheader("Full Data Table")
        st.dataframe(integration_status, use_container_width=True)

    # ── RISKS TAB ──────────────────────────────────────────────────────────────
    with risks_tab:
        sod_critical = (sod_matrix["severity"] == "Critical").sum() if "severity" in sod_matrix.columns else 0
        sod_high = (sod_matrix["severity"] == "High").sum() if "severity" in sod_matrix.columns else 0

        render_tab_header(
            "Risks & Controls",
            "Monitor all integration risks and separation of duties (SoD) conflicts. No single individual should be able to Authorize, Record, Verify, and hold Custody for the same process.",
        )
        risk_metric_col1, risk_metric_col2, risk_metric_col3, risk_metric_col4, risk_metric_col5 = st.columns(5)
        risk_metric_col1.metric("Total Risks", len(risks))
        risk_metric_col2.metric("Critical Risks", int(critical_risks))
        risk_metric_col3.metric("High Risks", int(high_risks))
        risk_metric_col4.metric("SoD Critical Conflicts", int(sod_critical))
        risk_metric_col5.metric("SoD High Conflicts", int(sod_high))
        st.markdown("---")

        if critical_risks > 0:
            st.subheader("Critical Risks — Immediate Escalation Required")
            for _, row in risks[risks["severity"] == "Critical"].iterrows():
                mitigation = row.get("mitigation", "No mitigation plan assigned")
                status_val = row.get("status", "Open")
                st.markdown(
                    f"<div class='risk-row'>{severity_badge(row['severity'])} &nbsp; <b>{row['risk_id']}</b>: {row['risk']}<br>"
                    f"<small>Owner: {row['owner']} &nbsp;|&nbsp; Status: {status_val} &nbsp;|&nbsp; Mitigation: {mitigation}</small></div>",
                    unsafe_allow_html=True,
                )

        st.subheader("High Risks")
        for _, row in risks[risks["severity"] == "High"].iterrows():
            mitigation = row.get("mitigation", "No mitigation plan assigned")
            status_val = row.get("status", "Open")
            st.markdown(
                f"<div class='risk-row'>{severity_badge(row['severity'])} &nbsp; <b>{row['risk_id']}</b>: {row['risk']}<br>"
                f"<small>Owner: {row['owner']} &nbsp;|&nbsp; Status: {status_val} &nbsp;|&nbsp; Mitigation: {mitigation}</small></div>",
                unsafe_allow_html=True,
            )

        st.subheader("Medium Risks")
        for _, row in risks[risks["severity"] == "Medium"].iterrows():
            mitigation = row.get("mitigation", "No mitigation plan assigned")
            status_val = row.get("status", "Open")
            st.markdown(
                f"<div class='risk-row'>{severity_badge(row['severity'])} &nbsp; <b>{row['risk_id']}</b>: {row['risk']}<br>"
                f"<small>Owner: {row['owner']} &nbsp;|&nbsp; Status: {status_val} &nbsp;|&nbsp; Mitigation: {mitigation}</small></div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.subheader("Full Risk Register")
        st.dataframe(risks, use_container_width=True)

        # ── SoD SECTION ───────────────────────────────────────────────────────
        st.markdown("---")
        st.subheader("Separation of Duties (SoD) Assessment")
        st.markdown(
            """<div class='executive-card'>
            <b>SoD Definition:</b> No single individual should be able to perform more than one of the following roles for the same process or transaction:<br><br>
            &nbsp;&nbsp;🔴 <b>Authorize</b> — Approve or sanction a transaction, action, or access<br>
            &nbsp;&nbsp;📝 <b>Record</b> — Enter, post, or maintain data in systems or ledgers<br>
            &nbsp;&nbsp;✅ <b>Verify</b> — Reconcile, review, or validate transactions or balances<br>
            &nbsp;&nbsp;🔒 <b>Custody</b> — Hold, safeguard, or control assets or privileged system access<br><br>
            A person holding two or more of these roles for the same process represents an <b>SoD conflict</b> that could enable financial loss, fraud, or undetected errors.
            </div>""",
            unsafe_allow_html=True,
        )

        sod_col1, sod_col2 = st.columns(2)
        with sod_col1:
            st.subheader("SoD by Process")
            process_filter = st.selectbox("Filter by process", ["All"] + sorted(sod_matrix["process"].dropna().unique().tolist()), key="sod_process_filter")
        with sod_col2:
            st.subheader("SoD by Role")
            role_filter = st.selectbox("Filter by SoD role", ["All", "Authorize", "Record", "Verify", "Custody"], key="sod_role_filter")

        sod_filtered = sod_matrix.copy()
        if process_filter != "All":
            sod_filtered = sod_filtered[sod_filtered["process"] == process_filter]
        if role_filter != "All":
            sod_filtered = sod_filtered[sod_filtered["sod_role"] == role_filter]

        st.caption(f"Showing {len(sod_filtered)} SoD tasks — {(sod_filtered['severity'] == 'Critical').sum()} Critical, {(sod_filtered['severity'] == 'High').sum()} High")

        if sod_critical > 0:
            st.markdown("#### Critical SoD Conflicts")
            for _, row in sod_filtered[sod_filtered["severity"] == "Critical"].iterrows():
                st.markdown(
                    f"<div class='risk-row'>{severity_badge('Critical')} &nbsp; <b>{row['process']}</b> — {row['task']}<br>"
                    f"<small><b>SoD Role:</b> {row['sod_role']} &nbsp;|&nbsp; <b>Assigned To:</b> {row['assigned_to']} &nbsp;|&nbsp; <b>Conflicts With:</b> {row['conflicts_with']}</small><br>"
                    f"<small><b>Risk:</b> {row['sod_risk']}</small><br>"
                    f"<small><b>Mitigation:</b> {row['mitigation']}</small>"
                    f"</div>",
                    unsafe_allow_html=True,
                )

        st.markdown("#### High SoD Conflicts")
        for _, row in sod_filtered[sod_filtered["severity"] == "High"].iterrows():
            st.markdown(
                f"<div class='risk-row'>{severity_badge('High')} &nbsp; <b>{row['process']}</b> — {row['task']}<br>"
                f"<small><b>SoD Role:</b> {row['sod_role']} &nbsp;|&nbsp; <b>Assigned To:</b> {row['assigned_to']} &nbsp;|&nbsp; <b>Conflicts With:</b> {row['conflicts_with']}</small><br>"
                f"<small><b>Risk:</b> {row['sod_risk']}</small><br>"
                f"<small><b>Mitigation:</b> {row['mitigation']}</small>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("#### Medium SoD Items")
        for _, row in sod_filtered[sod_filtered["severity"] == "Medium"].iterrows():
            st.markdown(
                f"<div class='risk-row'>{severity_badge('Medium')} &nbsp; <b>{row['process']}</b> — {row['task']}<br>"
                f"<small><b>SoD Role:</b> {row['sod_role']} &nbsp;|&nbsp; <b>Assigned To:</b> {row['assigned_to']} &nbsp;|&nbsp; <b>Conflicts With:</b> {row['conflicts_with']}</small><br>"
                f"<small><b>Risk:</b> {row['sod_risk']}</small><br>"
                f"<small><b>Mitigation:</b> {row['mitigation']}</small>"
                f"</div>",
                unsafe_allow_html=True,
            )

        st.markdown("---")
        st.subheader("Full SoD Matrix")
        st.dataframe(sod_matrix, use_container_width=True)

    # ── BUDGET TAB ─────────────────────────────────────────────────────────────
    with budget_tab:
        render_tab_header(
            "Budget",
            "Compare budget, actual spend, forecast, and expected savings across all integration categories. Identify variance and validate savings assumptions.",
        )
        budget_metric_col1, budget_metric_col2, budget_metric_col3, budget_metric_col4 = st.columns(4)
        budget_metric_col1.metric("Total Budget", f"${total_budget:,.0f}")
        budget_metric_col2.metric("Actual Spend", f"${actual_spend:,.0f}")
        budget_metric_col3.metric("Forecast Spend", f"${forecast_spend:,.0f}", delta=f"{budget_variance_pct:+.1f}% vs budget", delta_color="inverse")
        budget_metric_col4.metric("Estimated Savings", f"${estimated_savings:,.0f}")
        st.markdown("---")
        st.subheader("Budget by Category")
        fig_budget_tab = px.bar(
            budget,
            x="category",
            y=["budget", "actual_spend", "forecast_spend", "estimated_savings"],
            barmode="group",
            title="Budget vs Actual vs Forecast vs Savings by Category (USD)",
            labels={"value": "Amount (USD)", "category": "Category", "variable": "Type"},
            color_discrete_map={"budget": "#0f62fe", "actual_spend": "#42be65", "forecast_spend": "#f1c21b", "estimated_savings": "#8a3ffc"},
        )
        fig_budget_tab.update_layout(legend_title_text="", xaxis_title="Category", yaxis_title="Amount (USD)", yaxis_tickformat="$,.0f")
        st.plotly_chart(fig_budget_tab, use_container_width=True)
        st.subheader("Detail")
        st.dataframe(budget, use_container_width=True)
        st.subheader("Totals")
        st.dataframe(budget_totals, use_container_width=True)

    # ── LEGAL ENTITIES TAB ────────────────────────────────────────────────────
    with legal_tab:
        render_tab_header(
            "Legal Entities",
            "Review legal entity simplification recommendations. Retain regulatory-required entities, merge duplicates, and dissolve inactive entities to reduce admin cost and audit fees.",
        )
        legal_metric_col1, legal_metric_col2, legal_metric_col3, legal_metric_col4 = st.columns(4)
        legal_metric_col1.metric("Entities Tracked", len(legal_entities))
        legal_metric_col2.metric("Merge/Dissolve Candidates", len(merge_or_dissolve_entities))
        legal_metric_col3.metric("Action Savings", f"${total_action_savings:,.0f}")
        legal_metric_col4.metric("Admin Cost Reduction", f"${annual_admin_cost_reduction:,.0f}")
        st.markdown("---")
        st.subheader("Entity Recommendations")
        st.dataframe(
            legal_entities[[
                "entity_name",
                "country",
                "recommended_action",
                "recommendation_reason",
                "confidence_level",
                "required_approval",
                "compliance_risk",
                "estimated_recurring_savings_example",
                "external_auditors",
                "annual_audit_fees",
                "annual_admin_cost",
                "saving_if_action_is_taken",
            ]],
            use_container_width=True,
        )
        st.subheader("Totals")
        st.dataframe(legal_entity_totals, use_container_width=True)

    # ── SME DIRECTORY TAB ─────────────────────────────────────────────────────
    with sme_tab:
        render_tab_header(
            "SME Directory",
            "Identify the right functional owner for every integration question. Search by function, geography, job profile, or skills to find the best-matched SME.",
        )
        sme_metric_col1, sme_metric_col2, sme_metric_col3 = st.columns(3)
        sme_metric_col1.metric("SME Records", len(sme_directory))
        sme_metric_col2.metric("Functions Covered", sme_directory["function"].nunique())
        sme_metric_col3.metric("Geographies Covered", sme_directory["geography"].nunique())
        st.markdown("---")

        st.subheader("Find the Right SME")
        search_col1, search_col2 = st.columns(2)
        with search_col1:
            search_keyword = st.text_input("Search by function, geography, job profile or skill", "", placeholder="e.g. SAP, IFRS, chart of accounts, Singapore, Controller")
        with search_col2:
            function_filter = st.selectbox("Filter by function", ["All"] + sorted(sme_directory["function"].dropna().unique().tolist()))

        has_skills = "skills" in sme_directory.columns
        has_job_profile = "job_profile" in sme_directory.columns

        if search_keyword or function_filter != "All":
            mask = pd.Series([True] * len(sme_directory))
            if function_filter != "All":
                mask = mask & (sme_directory["function"] == function_filter)
            if search_keyword:
                keyword_mask = (
                    sme_directory["function"].str.contains(search_keyword, case=False, na=False) |
                    sme_directory["geography"].str.contains(search_keyword, case=False, na=False) |
                    sme_directory["primary_sme"].str.contains(search_keyword, case=False, na=False)
                )
                if has_job_profile:
                    keyword_mask = keyword_mask | sme_directory["job_profile"].str.contains(search_keyword, case=False, na=False)
                if has_skills:
                    keyword_mask = keyword_mask | sme_directory["skills"].str.contains(search_keyword, case=False, na=False)
                mask = mask & keyword_mask
            filtered_sme = sme_directory[mask]
            st.caption(f"{len(filtered_sme)} SME(s) matched")
            if filtered_sme.empty:
                st.warning("No SMEs matched your search. Try a different keyword or clear the filter.")
            else:
                for _, row in filtered_sme.iterrows():
                    job = row.get("job_profile", "") if has_job_profile else ""
                    skills_val = row.get("skills", "") if has_skills else ""
                    st.markdown(
                        f"<div class='risk-row'>"
                        f"<b>{row['primary_sme']}</b> &nbsp;|&nbsp; {row['function']} &nbsp;|&nbsp; {row['geography']}<br>"
                        f"<small><b>Job Profile:</b> {job}</small><br>"
                        f"<small><b>Skills:</b> {skills_val}</small><br>"
                        f"<small>Backup: {row['backup_sme']} &nbsp;|&nbsp; Escalation: {row['escalation_path']}</small>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
        else:
            st.markdown("---")
            st.subheader("All SMEs")
            for _, row in sme_directory.iterrows():
                job = row.get("job_profile", "") if has_job_profile else ""
                skills_val = row.get("skills", "") if has_skills else ""
                st.markdown(
                    f"<div class='risk-row'>"
                    f"<b>{row['primary_sme']}</b> &nbsp;|&nbsp; {row['function']} &nbsp;|&nbsp; {row['geography']}<br>"
                    f"<small><b>Job Profile:</b> {job}</small><br>"
                    f"<small><b>Skills:</b> {skills_val}</small><br>"
                    f"<small>Backup: {row['backup_sme']} &nbsp;|&nbsp; Escalation: {row['escalation_path']}</small>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        st.markdown("---")
        st.subheader("Full SME Table")
        st.dataframe(sme_directory, use_container_width=True)

    # ── KNOWLEDGE LIBRARY TAB ─────────────────────────────────────────────────
    with knowledge_tab:
        render_tab_header(
            "Knowledge Library",
            "Reference approved knowledge, lessons learned, and reusable guidance to accelerate acquisition decisions and avoid repeating past mistakes.",
        )
        sections = knowledge_library_text.split("===")
        if len(sections) > 1:
            for section in sections:
                section = section.strip()
                if not section:
                    continue
                lines = section.split("\n", 1)
                if len(lines) == 2:
                    title_text = lines[0].strip()
                    body_text = lines[1].strip()
                    if title_text:
                        with st.expander(title_text, expanded=False):
                            st.write(body_text)
        else:
            st.text_area("Approved knowledge and lessons learned", knowledge_library_text, height=400)

    # ── IBM BOB Q&A TAB ───────────────────────────────────────────────────────
    with bob_tab:
        render_tab_header(
            "IBM Bob Q&A",
            "Use structured IBM Bob responses to guide integration actions, identify owners, and accelerate acquisition decision-making from Day 1 to Day 100.",
        )
        st.write("Select a sample question or type your own below.")
        question = st.selectbox(
            "Sample questions",
            [
                "What should we do first after acquiring Company X?",
                "Multi-layer processes are not harmonized — where do we even start?",
                "Which legal entities can be merged or dissolved and what is the cash impact?",
                "Who can help with payroll integration in Japan?",
            ],
        )

        if question == "What should we do first after acquiring Company X?":
            st.subheader("Executive Summary")
            st.write(
                f"Start by creating the {workspace_name} workspace for {region}, uploading core data, and addressing the {critical_risks} critical and {high_risks} high-risk items. Current readiness is {readiness_percent}% — Day 1 target is {day_1_date}."
            )
            st.subheader("Agent Capabilities Used")
            st.write("- Integration Navigator")
            st.write("- Risk & Controls")
            st.write("- Budget & Value Tracking")
            st.write("- Legal Entity Optimization")
            st.subheader("Recommended Actions")
            st.write(f"1. Create the {workspace_name} workspace and confirm Day 1 / Day 100 targets.")
            st.write("2. Upload chart of accounts, headcount, legal entity, risk, and budget files.")
            st.write(f"3. Assign owners to all {critical_risks} critical and {high_risks} high-risk items.")
            st.write("4. Confirm payroll continuity and systems access provisioning timelines.")
            st.write("5. Schedule Day 1 readiness review 2 weeks before target date.")
            st.subheader("Owners")
            st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
            st.subheader("Timeline")
            st.write(f"Immediate start in Week 1. Day 1 target: {day_1_date}. Day 100 target: {day_100_date}.")
            st.subheader("Risks")
            st.write("Incomplete mappings, missing SMEs, and unresolved legal entity issues may delay readiness.")
            st.subheader("Budget / Savings / Cash Impact")
            st.write(f"Forecast spend: ${forecast_spend:,.0f}  |  Estimated savings: ${estimated_savings:,.0f}  |  Cash release opportunity: ${cash_release_opportunity:,.0f}")
            st.subheader("Readiness Impact")
            st.write(f"Current readiness is {readiness_percent}% with {critical_risks} critical and {high_risks} high-risk items requiring immediate action.")
            st.subheader("Next Steps")
            st.write(f"{integration_lead} to review all open risks and readiness gaps before next checkpoint.")

        elif question == "Multi-layer processes are not harmonized — where do we even start?":
            st.subheader("Executive Summary")
            st.write(
                f"Start by launching the {workspace_name} workspace for {region}. Validate chart of accounts mapping, review {len(legal_entities)} legal entities for simplification, and align the 500-employee workforce structure to target Day 1 ({day_1_date}) and Day 100 ({day_100_date})."
            )
            st.subheader("Agent Capabilities Used")
            st.write("- Integration Navigator")
            st.write("- Finance & Account Mapping")
            st.write("- Workforce & Organization Mapping")
            st.write("- Legal Entity Optimization")
            st.subheader("Recommended Actions")
            st.write("1. Upload COA, legal entity, workforce, risk, and budget files.")
            st.write("2. Review accounting and process mapping gaps and assign APAC Controller as Finance SME.")
            st.write(f"3. Review {len(merge_or_dissolve_entities)} legal entities flagged for merge or dissolve — estimated savings ${total_action_savings:,.0f}.")
            st.write("4. Confirm workforce reporting lines and identify role changes before Day 100.")
            st.write(f"5. Assign {integration_lead} and functional owners to the highest-priority actions.")
            st.subheader("Owners")
            st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
            st.subheader("Timeline")
            st.write(f"Immediate mobilization. Day 1: {day_1_date}. Day 100: {day_100_date}.")
            st.subheader("Risks")
            st.write("COA misalignment, unresolved entity structure, and workforce mapping issues may delay readiness.")
            st.subheader("Budget / Savings / Cash Impact")
            st.write(f"Forecast spend: ${forecast_spend:,.0f}  |  Estimated savings: ${estimated_savings:,.0f}  |  Total value opportunity: ${total_value_opportunity:,.0f}")
            st.subheader("Readiness Impact")
            st.write("Accounting and process mapping, workforce alignment, and legal entity simplification are the three critical readiness drivers for Day 100.")
            st.subheader("Next Steps")
            st.write("Complete data uploads, confirm SME coverage for all functions, and refresh the dashboard to validate integration readiness.")

        elif question == "Which legal entities can be merged or dissolved and what is the cash impact?":
            st.subheader("Executive Summary")
            st.write(
                f"IBM Bob identified {len(merge_or_dissolve_entities)} of {len(legal_entities)} legal entities as candidates for merge or dissolve. Estimated annual admin cost reduction: ${annual_admin_cost_reduction:,.0f}. Total action savings: ${total_action_savings:,.0f}."
            )
            st.subheader("Agent Capabilities Used")
            st.write("- Legal Entity Optimization")
            st.write("- Budget & Value Tracking")
            st.subheader("Merge / Dissolve Candidates")
            st.dataframe(
                merge_or_dissolve_entities[[
                    "entity_name",
                    "country",
                    "recommended_action",
                    "confidence_level",
                    "required_approval",
                    "external_auditors",
                    "annual_audit_fees",
                    "annual_admin_cost",
                    "saving_if_action_is_taken",
                ]],
                use_container_width=True,
            )
            st.subheader("Owners")
            st.write("Legal, Tax, Treasury, Integration Lead")
            st.subheader("Timeline")
            st.write("Assess in the current integration planning cycle. Target completion by Day 100.")
            st.subheader("Risks")
            st.write("Active contracts, regulatory requirements, and incomplete information may block action.")
            st.subheader("Budget / Savings / Cash Impact")
            st.write(f"Annual admin cost reduction: ${annual_admin_cost_reduction:,.0f}")
            st.write(f"Total action savings: ${total_action_savings:,.0f}")
            st.write(f"Cash release opportunity: ${cash_release_opportunity:,.0f}")
            st.subheader("Readiness Impact")
            st.write("Entity simplification reduces operational complexity and improves Day 100 stabilization.")
            st.subheader("Next Steps")
            st.write("Validate candidates with Legal and Tax. Confirm whether estimated admin cost reductions can be realized before initiating any action.")

        elif question == "Who can help with payroll integration in Japan?":
            st.subheader("Executive Summary")
            if not japan_payroll_sme.empty:
                payroll_row = japan_payroll_sme.iloc[0]
                st.write(
                    f"The primary payroll SME for Japan is {payroll_row['primary_sme']}, with backup support from {payroll_row['backup_sme']}. Escalation path: {payroll_row['escalation_path']}."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- SME Discovery")
                st.write("- Workforce & Organization Mapping")
                st.subheader("SME Contact Details")
                st.dataframe(japan_payroll_sme, use_container_width=True)
                st.subheader("Recommended Actions")
                st.write("1. Contact the primary SME to confirm payroll setup timeline.")
                st.write("2. Use the backup SME if the primary is unavailable.")
                st.write("3. Escalate via the escalation path if payroll continuity is at risk.")
                st.subheader("Owners")
                st.write("HR Director Japan, Integration Lead")
                st.subheader("Timeline")
                st.write("Immediate — payroll continuity is a non-negotiable Day 1 requirement.")
                st.subheader("Risks")
                st.write("Delays in payroll setup can affect Day 1 readiness and employee confidence.")
                st.subheader("Budget / Savings / Cash Impact")
                st.write("Payroll delays may increase transition costs and readiness risk if unresolved before Day 1.")
                st.subheader("Readiness Impact")
                st.write("Payroll SME alignment is a critical dependency for Day 1 employee continuity.")
                st.subheader("Next Steps")
                st.write(f"Contact {payroll_row['primary_sme']} today. Escalate via {payroll_row['escalation_path']} if not resolved within 24 hours.")
            else:
                st.warning("No Japan payroll SME was found in the SME Directory. Please upload an updated SME directory or assign a payroll SME for Japan immediately.")

except Exception as e:
    st.error(f"Could not load data: {e}")
    st.info("Please check that all sample data files are present in the sample_data/ folder, or upload replacement files using the sidebar.")
