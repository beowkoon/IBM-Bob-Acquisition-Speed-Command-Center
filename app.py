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
integration_lead = st.text_input("Integration Lead", value="BEOW KOON HENG")
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
st.sidebar.markdown("---")
st.sidebar.caption("IBM Bob Acquisition Speed Command Center v1.0")


try:
    integration_status = pd.read_csv(uploaded_integration_status or "sample_data/integration_status.csv")
    risks = pd.read_csv(uploaded_risks or "sample_data/risks.csv")
    budget = pd.read_csv(uploaded_budget or "sample_data/budget.csv")
    legal_entities = pd.read_csv(uploaded_legal_entities or "sample_data/legal_entities.csv")
    sme_directory = pd.read_csv(uploaded_sme_directory or "sample_data/sme_directory.csv")

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
        st.markdown(
            f"""
            <div class="executive-banner">
                <div style="font-size: 28px; font-weight: 700; margin-bottom: 6px;">Executive Integration Dashboard</div>
                <div style="font-size: 15px;">{workspace_name} &nbsp;|&nbsp; {region} &nbsp;|&nbsp; Integration Lead: {integration_lead}</div>
                <div style="font-size: 14px; margin-top: 6px; opacity: 0.85;">Day 1: {day_1_date} &nbsp;&nbsp; Day 100: {day_100_date}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.header("Executive Scorecard")
        st.write(
            "Live integration metrics across readiness, risk, budget, legal entity simplification, and SME coverage."
        )

        metric_row_1 = st.columns(4)
        metric_row_2 = st.columns(4)

        metric_row_1[0].metric("Overall Readiness", f"{readiness_percent}%", delta=f"{completed_areas}/{total_areas} areas complete")
        metric_row_1[1].metric("Critical / High Risks", f"{critical_risks} / {high_risks}", delta=f"{medium_risks} medium risks", delta_color="inverse")
        metric_row_1[2].metric("Forecast Spend", f"${forecast_spend:,.0f}", delta=f"{budget_variance_pct:+.1f}% vs budget", delta_color="inverse")
        metric_row_1[3].metric("Total Value Opportunity", f"${total_value_opportunity:,.0f}")

        metric_row_2[0].metric("Cash Release Opportunity", f"${cash_release_opportunity:,.0f}")
        metric_row_2[1].metric("Legal Entities to Simplify", len(merge_or_dissolve_entities), delta=f"of {len(legal_entities)} total entities")
        metric_row_2[2].metric("Open Risk Actions", sme_actions_required)
        metric_row_2[3].metric("Knowledge Files Loaded", knowledge_files_loaded)
        st.caption(f"Total Budget: ${total_budget:,.0f}  |  Actual Spend to Date: ${actual_spend:,.0f}  |  Estimated Savings: ${estimated_savings:,.0f}")

        # Readiness progress bar
        st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
        st.subheader("Integration Readiness Progress")
        st.progress(readiness_percent / 100)
        rcol1, rcol2, rcol3, rcol4 = st.columns(4)
        rcol1.metric("Complete", int(completed_areas))
        rcol2.metric("In Progress", int((integration_status["status"] == "In Progress").sum()))
        rcol3.metric("At Risk", int(at_risk_areas))
        rcol4.metric("Not Started", int(not_started_areas))
        st.markdown("</div>", unsafe_allow_html=True)

        left_col, center_col, right_col = st.columns([1, 1.2, 1])

        with left_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Integration Journey")
            journey_steps = [
                ("1", "Due Diligence", "Complete"),
                ("2", "Day 1 Readiness", "In Progress"),
                ("3", "Finance Mapping", "In Progress"),
                ("4", "Workforce Alignment", "Not Started"),
                ("5", "Systems and Controls", "At Risk"),
                ("6", "Legal Entity Simplification", "In Progress"),
                ("7", "Steady State", "Not Started"),
            ]
            for num, step, status in journey_steps:
                st.markdown(f"{num}. {step} &nbsp; {status_badge(status)}", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with center_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Ask IBM Bob")
            st.write("Ask IBM Bob anything about this acquisition integration.")
            dashboard_bob_question = st.text_area(
                "",
                value="We acquired a company with different COA, 12 legal entities, 500 employees and incomplete tax registration. What should we do first?",
                height=120,
                key="dashboard_bob_question",
            )
            dashboard_ask = st.button("Ask Bob", key="dashboard_ask_bob")
            st.markdown("</div>", unsafe_allow_html=True)

        # Bob response rendered full-width below the 3-column layout
        if dashboard_ask and dashboard_bob_question:
            question_lower = dashboard_bob_question.lower()
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("IBM Bob Response")
            st.subheader("Executive Summary")
            if "legal entity" in question_lower or "entities" in question_lower:
                st.write(
                    f"IBM Bob identified {len(merge_or_dissolve_entities)} legal entities for merge or dissolve review, with total action savings of ${total_action_savings:,.0f} and annual admin cost reduction of ${annual_admin_cost_reduction:,.0f}."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Legal Entity Optimization Agent")
                st.write("- Budget & Value Tracking Agent")
                st.subheader("Recommended Actions")
                st.write("1. Review entity-level recommendations and confirm approval requirements.")
                st.write("2. Validate compliance risk, active contracts, and tax dependencies.")
                st.write("3. Obtain Legal, Tax, and Treasury sign-off before executing any action.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, Legal, Tax, Treasury")
                st.subheader("Risks")
                st.write("Active contracts or regulatory gaps may block dissolution or merger actions.")
                st.subheader("Budget / Savings / Cash Impact")
                st.write(f"Action savings: ${total_action_savings:,.0f}  |  Admin cost reduction: ${annual_admin_cost_reduction:,.0f}")
                st.subheader("Next Steps")
                st.write("Open the Legal Entities tab and validate candidates for merge or dissolve.")
            elif "payroll" in question_lower or "japan" in question_lower:
                st.write(
                    "IBM Bob identified the payroll SME routing path for Japan and highlighted the readiness dependency for Day 1 employee continuity."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- SME Discovery Agent")
                st.write("- Workforce & Organization Mapping Agent")
                st.subheader("Recommended Actions")
                st.write("1. Contact the primary Japan payroll SME immediately.")
                st.write("2. Confirm payroll setup timeline and Day 1 continuity plan.")
                st.write("3. Track payroll readiness as a Critical Day 1 dependency.")
                st.subheader("Owners")
                st.write("HR Director Japan, Integration Lead")
                st.subheader("Risks")
                st.write("Delays in payroll setup can affect Day 1 readiness and employee experience.")
                st.subheader("Next Steps")
                st.write("Open the SME Directory tab and engage the Japan payroll SME immediately.")
            elif "budget" in question_lower:
                st.write(
                    f"IBM Bob reviewed integration spend: forecast of ${forecast_spend:,.0f} against a total budget of ${total_budget:,.0f}, with estimated savings of ${estimated_savings:,.0f}. Budget variance is {budget_variance_pct:+.1f}%."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Budget & Value Tracking Agent")
                st.subheader("Recommended Actions")
                st.write("1. Review current spend by category against plan.")
                st.write("2. Validate forecast assumptions and savings targets.")
                st.write("3. Escalate any overspend categories to the Integration Lead.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, Finance")
                st.subheader("Risks")
                st.write("Forecast variance may indicate scope creep or unplanned integration costs.")
                st.subheader("Next Steps")
                st.write("Open the Budget tab to review detailed spend by category.")
            elif "coa" in question_lower or "account" in question_lower or "finance" in question_lower:
                st.write(
                    "IBM Bob identified finance mapping as the first priority. Chart of accounts alignment must be completed before the first consolidated close."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Finance & Account Mapping Agent")
                st.write("- Integration Navigator Agent")
                st.subheader("Recommended Actions")
                st.write("1. Upload and validate chart of accounts files.")
                st.write("2. Map key accounts to the IBM target structure.")
                st.write("3. Identify unresolved mapping gaps and assign owners.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, Finance, APAC Controller")
                st.subheader("Risks")
                st.write("Unresolved COA mapping blocks the first consolidated close and financial reporting.")
                st.subheader("Next Steps")
                st.write("Coordinate with Finance SME to validate COA mapping and confirm close calendar alignment.")
            elif "risk" in question_lower or "highest risk" in question_lower or "critical" in question_lower:
                top_risks = risks[risks["severity"].isin(["Critical", "High"])].head(5)
                st.write(
                    f"IBM Bob identified {critical_risks} Critical and {high_risks} High risks in the current integration. The highest priority risk is: '{risks.iloc[0]['risk']}' — owned by {risks.iloc[0]['owner']}."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Risk & Controls Agent")
                st.write("- Integration Navigator Agent")
                st.subheader("Top Critical & High Risks")
                st.dataframe(top_risks[["risk_id", "severity", "risk", "owner", "status", "mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions")
                st.write(f"1. Escalate all {critical_risks} Critical risks to the executive sponsor immediately.")
                st.write(f"2. Assign mitigation plans to all {high_risks} High risks within 48 hours.")
                st.write("3. Review the full risk register in the Risks tab.")
                st.write("4. Schedule a weekly risk review with all workstream owners.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, workstream owners per risk area")
                st.subheader("Timeline")
                st.write("Critical risks: resolve before Day 1. High risks: within first 2 weeks.")
                st.subheader("Risks")
                st.write("Unowned or unmitigated risks linked to Day 1 activities may block readiness.")
                st.subheader("Budget / Savings / Cash Impact")
                st.write("Unresolved risks may increase integration cost and delay value realization.")
                st.subheader("Next Steps")
                st.write("Open the Risks tab to review the full register and confirm all items have owners and mitigation plans.")
            elif "tax" in question_lower:
                st.write(
                    "IBM Bob identified tax registration gaps as a Critical Day 1 blocker. Incomplete tax registration prevents revenue recognition and increases compliance risk."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Risk & Controls Agent")
                st.write("- Integration Navigator Agent")
                st.subheader("Recommended Actions")
                st.write("1. Identify all entities with incomplete tax registration.")
                st.write("2. Engage Regional Tax Lead immediately to resolve gaps.")
                st.write("3. Do not recognize revenue in any entity with unresolved tax registration.")
                st.subheader("Owners")
                st.write("Regional Tax Lead, Legal, Integration Lead")
                st.subheader("Risks")
                st.write("Non-compliance with tax registration requirements may result in penalties and revenue recognition delays.")
                st.subheader("Next Steps")
                st.write("Open the Risks tab and review R006. Escalate to the Regional Tax Lead today.")
            elif "hr" in question_lower or "workforce" in question_lower or "employee" in question_lower or "headcount" in question_lower:
                st.write(
                    f"IBM Bob identified workforce alignment as a key Day 100 dependency. HR integration covers headcount, compensation, benefits, reporting lines, and change management for all acquired employees."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Workforce & Organization Mapping Agent")
                st.write("- SME Discovery Agent")
                st.subheader("Recommended Actions")
                st.write("1. Upload headcount and compensation data for all acquired employees.")
                st.write("2. Confirm reporting lines and role changes before Day 100.")
                st.write("3. Ensure all employees receive integration communications within Week 1.")
                st.write("4. Engage HR SME to lead change management through to Day 100.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, HR, Regional HR Leadership")
                st.subheader("Timeline")
                st.write(f"Payroll continuity by Day 1 ({day_1_date}). Full workforce alignment by Day 100 ({day_100_date}).")
                st.subheader("Risks")
                st.write("Unresolved reporting lines and delayed HR data migration may affect employee confidence and Day 1 readiness.")
                st.subheader("Budget / Savings / Cash Impact")
                st.write("HR integration delays may increase transition costs and extend the integration timeline.")
                st.subheader("Next Steps")
                st.write("Open the SME Directory and engage the HR Integration SME. Confirm payroll continuity plan for Day 1.")
            elif "sme" in question_lower or "who can help" in question_lower or "contact" in question_lower or "expert" in question_lower:
                st.write(
                    f"IBM Bob identified {len(sme_directory)} SME records across {sme_directory['function'].nunique()} functions and {sme_directory['geography'].nunique()} geographies. Use the SME Directory to find the right owner for each integration question."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- SME Discovery Agent")
                st.subheader("SME Directory Overview")
                st.dataframe(sme_directory[["function", "geography", "primary_sme", "backup_sme", "escalation_path"]], use_container_width=True)
                st.subheader("Recommended Actions")
                st.write("1. Search the SME Directory by function or geography.")
                st.write("2. Contact the primary SME first, then backup, then escalation path.")
                st.write("3. Flag any SME coverage gaps to the Integration Lead within 24 hours.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, functional leads per workstream")
                st.subheader("Next Steps")
                st.write("Open the SME Directory tab and search for your function or geography.")
            elif "readiness" in question_lower or "day 1" in question_lower or "day one" in question_lower:
                st.write(
                    f"Current integration readiness is {readiness_percent}%. {int(completed_areas)} of {total_areas} workstreams are complete. {int(at_risk_areas)} are At Risk and {int(not_started_areas)} have not started."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Integration Readiness Agent")
                st.write("- Risk & Controls Agent")
                st.subheader("Readiness by Status")
                st.dataframe(integration_status[["area", "status", "owner"]], use_container_width=True)
                st.subheader("Recommended Actions")
                st.write(f"1. Resolve all {int(at_risk_areas)} At Risk workstreams before Day 1.")
                st.write(f"2. Assign owners to all {int(not_started_areas)} Not Started workstreams immediately.")
                st.write("3. Schedule a Day 1 readiness review 2 weeks before the target date.")
                st.write("4. Confirm payroll, systems access, and legal entity structure are all cleared.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, all workstream owners")
                st.subheader("Timeline")
                st.write(f"Day 1 target: {day_1_date}. Day 100 target: {day_100_date}.")
                st.subheader("Risks")
                st.write("At Risk and Not Started workstreams are the primary threats to Day 1 readiness.")
                st.subheader("Next Steps")
                st.write("Open the Integration Status tab and address all At Risk items before the next checkpoint.")
            else:
                st.write(
                    f"IBM Bob reviewed the current workspace: readiness at {readiness_percent}%, {critical_risks} critical and {high_risks} high-risk items open, forecast spend of ${forecast_spend:,.0f}, and legal entity savings opportunity of ${total_action_savings:,.0f}."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- Integration Navigator")
                st.write("- Risk & Controls Agent")
                st.write("- Budget & Value Tracking Agent")
                st.write("- Legal Entity Optimization Agent")
                st.write("- SME Discovery Agent")
                st.subheader("Recommended Actions")
                st.write("1. Validate all uploaded acquisition data is complete and accurate.")
                st.write("2. Review and assign owners to all Critical and High risks immediately.")
                st.write("3. Confirm COA, workforce, and legal entity mapping is underway.")
                st.write("4. Assign SMEs to all open workstreams.")
                st.write("5. Schedule Day 1 readiness review 2 weeks before target date.")
                st.subheader("Owners")
                st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
                st.subheader("Timeline")
                st.write(f"Day 1 target: {day_1_date}  |  Day 100 target: {day_100_date}")
                st.subheader("Risks")
                st.write("Incomplete mappings, missing SMEs, and unresolved legal entity issues may delay readiness.")
                st.subheader("Budget / Savings / Cash Impact")
                st.write(f"Forecast spend: ${forecast_spend:,.0f}  |  Estimated savings: ${estimated_savings:,.0f}")
                st.write(f"Legal entity action savings: ${total_action_savings:,.0f}  |  Total value opportunity: ${total_value_opportunity:,.0f}")
                st.subheader("Next Steps")
                st.write(f"{integration_lead} to review open risks, legal entity candidates, and readiness gaps before next checkpoint.")
            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Live Command Center Alerts")
            if critical_risks > 0:
                st.error(f"{critical_risks} Critical risk(s) require immediate executive escalation.")
            if high_risks > 0:
                st.warning(f"{high_risks} High risk(s) need owner and mitigation plan within 48 hours.")
            if at_risk_areas > 0:
                st.warning(f"{at_risk_areas} workstream(s) are At Risk — review Integration Status tab.")
            if not_started_areas > 0:
                st.info(f"{not_started_areas} workstream(s) have not started — assign owners immediately.")
            st.info(f"Forecast spend is ${forecast_spend:,.0f} against a total budget of ${total_budget:,.0f}.")
            st.info(f"Estimated savings total ${estimated_savings:,.0f}.")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
        st.subheader("Target Outcomes")
        outcome_col1, outcome_col2, outcome_col3, outcome_col4, outcome_col5 = st.columns(5)
        outcome_col1.metric("Planning Time Reduced", "45%")
        outcome_col2.metric("SME Search Time Reduced", "60%")
        outcome_col3.metric("Mapping Effort Reduced", "35%")
        outcome_col4.metric("Readiness Review Accelerated", "50%")
        outcome_col5.metric("Estimated Value Opportunity", "$1.3M")
        st.markdown("</div>", unsafe_allow_html=True)

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            fig_budget = px.bar(
                budget,
                x="category",
                y=["budget", "actual_spend", "forecast_spend"],
                barmode="group",
                title="Budget Overview by Category (USD)",
                labels={"value": "Amount (USD)", "category": "Category", "variable": "Type"},
                color_discrete_map={"budget": "#0f62fe", "actual_spend": "#42be65", "forecast_spend": "#f1c21b"},
            )
            fig_budget.update_layout(legend_title_text="", xaxis_title="Category", yaxis_title="Amount (USD)", yaxis_tickformat="$,.0f")
            st.plotly_chart(fig_budget, use_container_width=True)
        with chart_col2:
            legal_action_df = legal_action_counts.reset_index()
            legal_action_df.columns = ["Action", "Count"]
            color_map = {"Retain": "#42be65", "Merge": "#f1c21b", "Dissolve": "#fa4d56", "Further Assessment": "#8a3ffc"}
            fig_legal = px.bar(
                legal_action_df,
                x="Action",
                y="Count",
                title="Legal Entity Actions",
                labels={"Count": "Number of Entities", "Action": "Recommended Action"},
                color="Action",
                color_discrete_map=color_map,
                text="Count",
            )
            fig_legal.update_traces(textposition="outside")
            fig_legal.update_layout(showlegend=False, xaxis_title="Recommended Action", yaxis_title="Number of Entities", yaxis_dtick=1)
            st.plotly_chart(fig_legal, use_container_width=True)

        status_df = status_counts.reset_index()
        status_df.columns = ["Status", "Count"]
        status_color_map = {"Complete": "#42be65", "In Progress": "#f1c21b", "At Risk": "#fa4d56", "Not Started": "#8d8d8d"}
        fig_status = px.bar(
            status_df,
            x="Status",
            y="Count",
            title="Integration Status Overview — Number of Workstreams by Status",
            labels={"Count": "Number of Workstreams", "Status": "Integration Status"},
            color="Status",
            color_discrete_map=status_color_map,
            text="Count",
        )
        fig_status.update_traces(textposition="outside")
        fig_status.update_layout(showlegend=False, xaxis_title="Integration Status", yaxis_title="Number of Workstreams", yaxis_dtick=1)
        st.plotly_chart(fig_status, use_container_width=True)

    # ── INTEGRATION STATUS TAB ─────────────────────────────────────────────────
    with status_tab:
        render_tab_header(
            "Integration Status",
            "Review current progress across all tracked integration workstreams. Identify incomplete areas and assign owners to drive Day 1 and Day 100 readiness.",
        )
        status_metric_col1, status_metric_col2, status_metric_col3, status_metric_col4 = st.columns(4)
        status_metric_col1.metric("Tracked Areas", total_areas)
        status_metric_col2.metric("Completed", int(completed_areas))
        status_metric_col3.metric("At Risk", int(at_risk_areas))
        status_metric_col4.metric("Readiness Score", f"{readiness_percent}%")
        st.progress(readiness_percent / 100)
        st.markdown("---")
        st.subheader("Workstream Status")
        for _, row in integration_status.iterrows():
            st.markdown(
                f"<div class='risk-row'><b>{row['area']}</b> &nbsp; {status_badge(row['status'])} &nbsp;&nbsp; Owner: {row['owner']}</div>",
                unsafe_allow_html=True,
            )
        st.markdown("---")
        st.subheader("Full Data Table")
        st.dataframe(integration_status, use_container_width=True)

    # ── RISKS TAB ──────────────────────────────────────────────────────────────
    with risks_tab:
        render_tab_header(
            "Risks",
            "Monitor all integration risks. Critical and High risks must have owners and mitigation plans. Escalate Critical risks to the executive sponsor immediately.",
        )
        risk_metric_col1, risk_metric_col2, risk_metric_col3, risk_metric_col4 = st.columns(4)
        risk_metric_col1.metric("Total Risks", len(risks))
        risk_metric_col2.metric("Critical", int(critical_risks))
        risk_metric_col3.metric("High", int(high_risks))
        risk_metric_col4.metric("Medium", int(medium_risks))
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
                "We acquired a company with different COA, 12 legal entities and 500 employees. What should we do first?",
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

        elif question == "We acquired a company with different COA, 12 legal entities and 500 employees. What should we do first?":
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
            st.write("2. Review finance mapping gaps and assign APAC Controller as Finance SME.")
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
            st.write("Finance mapping, workforce alignment, and legal entity simplification are the three critical readiness drivers for Day 100.")
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
