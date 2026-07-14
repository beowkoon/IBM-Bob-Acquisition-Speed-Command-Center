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
                ("Finance Mapping",           "In Progress"),
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
                        <div style="width:130px;font-size:13px;color:#e0e0e0;">{step}</div>
                        <div style="flex:1;background:#2a2a3a;border-radius:4px;height:14px;">
                            <div style="width:{bw}%;background:{bc};height:14px;border-radius:4px;"></div>
                        </div>
                        <div style="width:90px;text-align:right;font-size:12px;font-weight:600;color:{lbl_color};">{s}</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            st.markdown("</div>", unsafe_allow_html=True)

            # Ask Bob box below journey
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.markdown("**Ask IBM Bob**")
            st.write("Ask anything about this acquisition integration.")
            dashboard_bob_question = st.text_area(
                "",
                value="We acquired a company with different COA, 12 legal entities, 500 employees and incomplete tax registration. What should we do first?",
                height=100,
                key="dashboard_bob_question",
            )
            dashboard_ask = st.button("Ask Bob", key="dashboard_ask_bob")
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

        # ── Bob response full-width below ──
        if dashboard_ask and dashboard_bob_question:
            question_lower = dashboard_bob_question.lower()
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("IBM Bob Response")
            st.subheader("Executive Summary")
            if "legal entity" in question_lower or "entities" in question_lower:
                st.write(f"IBM Bob identified {len(merge_or_dissolve_entities)} legal entities for merge or dissolve review, with total action savings of ${total_action_savings:,.0f} and annual admin cost reduction of ${annual_admin_cost_reduction:,.0f}.")
                st.subheader("Agent Capabilities Used")
                st.write("- Legal Entity Optimization Agent\n- Budget & Value Tracking Agent")
                st.subheader("Recommended Actions")
                st.write("1. Review entity-level recommendations and confirm approval requirements.\n2. Validate compliance risk, active contracts, and tax dependencies.\n3. Obtain Legal, Tax, and Treasury sign-off before executing any action.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Legal, Tax, Treasury")
                st.subheader("Risks"); st.write("Active contracts or regulatory gaps may block dissolution or merger actions.")
                st.subheader("Budget / Savings / Cash Impact"); st.write(f"Action savings: ${total_action_savings:,.0f}  |  Admin cost reduction: ${annual_admin_cost_reduction:,.0f}")
                st.subheader("Next Steps"); st.write("Open the Legal Entities tab and validate candidates for merge or dissolve.")
            elif "payroll" in question_lower or "japan" in question_lower:
                st.write("IBM Bob identified the payroll SME routing path for Japan and highlighted the readiness dependency for Day 1 employee continuity.")
                st.subheader("Agent Capabilities Used"); st.write("- SME Discovery Agent\n- Workforce & Organization Mapping Agent")
                st.subheader("Recommended Actions"); st.write("1. Contact the primary Japan payroll SME immediately.\n2. Confirm payroll setup timeline and Day 1 continuity plan.\n3. Track payroll readiness as a Critical Day 1 dependency.")
                st.subheader("Owners"); st.write("HR Director Japan, Integration Lead")
                st.subheader("Risks"); st.write("Delays in payroll setup can affect Day 1 readiness and employee experience.")
                st.subheader("Next Steps"); st.write("Open the SME Directory tab and engage the Japan payroll SME immediately.")
            elif "budget" in question_lower:
                st.write(f"IBM Bob reviewed integration spend: forecast of ${forecast_spend:,.0f} against a total budget of ${total_budget:,.0f}, with estimated savings of ${estimated_savings:,.0f}. Budget variance is {budget_variance_pct:+.1f}%.")
                st.subheader("Agent Capabilities Used"); st.write("- Budget & Value Tracking Agent")
                st.subheader("Recommended Actions"); st.write("1. Review current spend by category against plan.\n2. Validate forecast assumptions and savings targets.\n3. Escalate any overspend categories to the Integration Lead.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance")
                st.subheader("Risks"); st.write("Forecast variance may indicate scope creep or unplanned integration costs.")
                st.subheader("Next Steps"); st.write("Open the Budget tab to review detailed spend by category.")
            elif "coa" in question_lower or "account" in question_lower or "finance" in question_lower:
                st.write("IBM Bob identified finance mapping as the first priority. Chart of accounts alignment must be completed before the first consolidated close.")
                st.subheader("Agent Capabilities Used"); st.write("- Finance & Account Mapping Agent\n- Integration Navigator Agent")
                st.subheader("Recommended Actions"); st.write("1. Upload and validate chart of accounts files.\n2. Map key accounts to the IBM target structure.\n3. Identify unresolved mapping gaps and assign owners.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance, APAC Controller")
                st.subheader("Risks"); st.write("Unresolved COA mapping blocks the first consolidated close and financial reporting.")
                st.subheader("Next Steps"); st.write("Coordinate with Finance SME to validate COA mapping and confirm close calendar alignment.")
            elif "risk" in question_lower or "highest risk" in question_lower or "critical" in question_lower:
                top_risks = risks[risks["severity"].isin(["Critical", "High"])].head(5)
                st.write(f"IBM Bob identified {critical_risks} Critical and {high_risks} High risks. The highest priority risk is: '{risks.iloc[0]['risk']}' — owned by {risks.iloc[0]['owner']}.")
                st.subheader("Agent Capabilities Used"); st.write("- Risk & Controls Agent\n- Integration Navigator Agent")
                st.subheader("Top Critical & High Risks"); st.dataframe(top_risks[["risk_id", "severity", "risk", "owner", "status", "mitigation"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write(f"1. Escalate all {critical_risks} Critical risks to the executive sponsor immediately.\n2. Assign mitigation plans to all {high_risks} High risks within 48 hours.\n3. Schedule a weekly risk review.")
                st.subheader("Owners"); st.write(f"{integration_lead}, workstream owners per risk area")
                st.subheader("Next Steps"); st.write("Open the Risks tab to review the full register and confirm all items have owners and mitigation plans.")
            elif "tax" in question_lower:
                st.write("IBM Bob identified tax registration gaps as a Critical Day 1 blocker. Incomplete tax registration prevents revenue recognition and increases compliance risk.")
                st.subheader("Agent Capabilities Used"); st.write("- Risk & Controls Agent\n- Integration Navigator Agent")
                st.subheader("Recommended Actions"); st.write("1. Identify all entities with incomplete tax registration.\n2. Engage Regional Tax Lead immediately to resolve gaps.\n3. Do not recognize revenue in any entity with unresolved tax registration.")
                st.subheader("Owners"); st.write("Regional Tax Lead, Legal, Integration Lead")
                st.subheader("Next Steps"); st.write("Open the Risks tab and review R006. Escalate to the Regional Tax Lead today.")
            elif "hr" in question_lower or "workforce" in question_lower or "employee" in question_lower or "headcount" in question_lower:
                st.write(f"IBM Bob identified workforce alignment as a key Day 100 dependency. HR integration covers headcount, compensation, benefits, reporting lines, and change management.")
                st.subheader("Agent Capabilities Used"); st.write("- Workforce & Organization Mapping Agent\n- SME Discovery Agent")
                st.subheader("Recommended Actions"); st.write(f"1. Upload headcount and compensation data.\n2. Confirm reporting lines before Day 100.\n3. Ensure all employees receive communications within Week 1.\n4. Engage HR SME for change management.")
                st.subheader("Owners"); st.write(f"{integration_lead}, HR, Regional HR Leadership")
                st.subheader("Next Steps"); st.write("Open the SME Directory and engage the HR Integration SME. Confirm payroll continuity plan for Day 1.")
            elif "sme" in question_lower or "who can help" in question_lower or "contact" in question_lower or "expert" in question_lower:
                st.write(f"IBM Bob identified {len(sme_directory)} SME records across {sme_directory['function'].nunique()} functions and {sme_directory['geography'].nunique()} geographies.")
                st.subheader("Agent Capabilities Used"); st.write("- SME Discovery Agent")
                st.subheader("SME Directory Overview"); st.dataframe(sme_directory[["function", "geography", "primary_sme", "backup_sme", "escalation_path"]], use_container_width=True)
                st.subheader("Next Steps"); st.write("Open the SME Directory tab and search for your function or geography.")
            elif "readiness" in question_lower or "day 1" in question_lower or "day one" in question_lower:
                st.write(f"Current integration readiness is {readiness_percent}%. {int(completed_areas)} of {total_areas} workstreams complete. {int(at_risk_areas)} At Risk, {int(not_started_areas)} Not Started.")
                st.subheader("Agent Capabilities Used"); st.write("- Integration Readiness Agent\n- Risk & Controls Agent")
                st.subheader("Readiness by Status"); st.dataframe(integration_status[["area", "status", "owner"]], use_container_width=True)
                st.subheader("Recommended Actions"); st.write(f"1. Resolve all {int(at_risk_areas)} At Risk workstreams before Day 1.\n2. Assign owners to all {int(not_started_areas)} Not Started workstreams.\n3. Schedule Day 1 readiness review 2 weeks before target.")
                st.subheader("Next Steps"); st.write("Open the Integration Status tab and address all At Risk items before the next checkpoint.")
            else:
                st.write(f"IBM Bob reviewed the current workspace: readiness at {readiness_percent}%, {critical_risks} critical and {high_risks} high-risk items open, forecast spend of ${forecast_spend:,.0f}, legal entity savings of ${total_action_savings:,.0f}.")
                st.subheader("Agent Capabilities Used"); st.write("- Integration Navigator\n- Risk & Controls Agent\n- Budget & Value Tracking Agent\n- Legal Entity Optimization Agent\n- SME Discovery Agent")
                st.subheader("Recommended Actions"); st.write("1. Validate all uploaded acquisition data.\n2. Review and assign owners to all Critical and High risks.\n3. Confirm COA, workforce, and legal entity mapping.\n4. Assign SMEs to all open workstreams.\n5. Schedule Day 1 readiness review 2 weeks before target.")
                st.subheader("Owners"); st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
                st.subheader("Timeline"); st.write(f"Day 1: {day_1_date}  |  Day 100: {day_100_date}")
                st.subheader("Budget / Savings / Cash Impact"); st.write(f"Forecast: ${forecast_spend:,.0f}  |  Savings: ${estimated_savings:,.0f}  |  Value opportunity: ${total_value_opportunity:,.0f}")
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
