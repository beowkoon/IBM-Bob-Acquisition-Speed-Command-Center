import streamlit as st
import pandas as pd

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
        background-color: #0f62fe;
        color: white;
        padding: 20px 24px;
        border-radius: 14px;
        margin-bottom: 16px;
    }
    .executive-card {
        background-color: #ffffff;
        border: 1px solid #dfe3e8;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.set_page_config(page_title="IBM Bob Acquisition Speed Command Center", layout="wide")

st.title("IBM Bob Acquisition Speed Command Center")
workspace_name = st.text_input("Acquisition Workspace Name", value="Company X Integration")
integration_lead = st.text_input("Integration Lead", value="BEOW KOON HENG")
region = st.selectbox("Region", ["APAC", "Americas", "EMEA", "Japan"])
date_col1, date_col2 = st.columns(2)
with date_col1:
    day_1_date = st.date_input("Day 1 Target Date")
with date_col2:
    day_100_date = st.date_input("Day 100 Target Date")
st.subheader(f"Prototype Dashboard - {workspace_name}")

st.write("This is the initial prototype for acquisition integration tracking.")


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


def render_tab_header(title, summary):
    st.caption("Private and Confidential")
    st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
    st.header(title)
    st.write(summary)
    st.markdown("</div>", unsafe_allow_html=True)


st.sidebar.header("Data Upload Center")
uploaded_integration_status = st.sidebar.file_uploader("Upload integration status CSV", type="csv")
uploaded_risks = st.sidebar.file_uploader("Upload risks CSV", type="csv")
uploaded_budget = st.sidebar.file_uploader("Upload budget CSV", type="csv")
uploaded_legal_entities = st.sidebar.file_uploader("Upload legal entities CSV", type="csv")
uploaded_sme_directory = st.sidebar.file_uploader("Upload SME directory CSV", type="csv")
uploaded_knowledge_library = st.sidebar.file_uploader("Upload knowledge library TXT", type="txt")


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
    total_areas = len(integration_status)
    readiness_percent = calculate_readiness_score(integration_status["status"])
    high_risks = (risks["severity"] == "High").sum()
    critical_risks = (risks["severity"] == "Critical").sum()
    total_budget = budget["budget"].sum()
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

    with dashboard_tab:
        st.caption("Private and Confidential")
        st.markdown(
            f"""
            <div class="executive-banner">
                <div style="font-size: 28px; font-weight: 700; margin-bottom: 6px;">Executive Integration Dashboard</div>
                <div style="font-size: 15px;">{workspace_name} | {region} | Integration Lead: {integration_lead}</div>
                <div style="font-size: 14px; margin-top: 6px;">Day 1: {day_1_date} | Day 100: {day_100_date}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.header("Dashboard Metrics")
        st.write(
            "This dashboard summarizes acquisition integration readiness, risk exposure, budget outlook, legal entity actions, and SME support for the current workspace."
        )
        metric_row_1 = st.columns(4)
        metric_row_2 = st.columns(4)

        metric_row_1[0].metric("Overall Readiness", f"{readiness_percent}%")
        metric_row_1[1].metric("High / Critical Risks", f"{high_risks} / {critical_risks}")
        metric_row_1[2].metric("Forecast Spend", f"${forecast_spend:,.0f}")
        metric_row_1[3].metric("Total Value Opportunity", f"${total_value_opportunity:,.0f}")

        metric_row_2[0].metric("Cash Release Opportunity", f"${cash_release_opportunity:,.0f}")
        metric_row_2[1].metric("Legal Entities to Simplify", len(merge_or_dissolve_entities))
        metric_row_2[2].metric("SME Actions Required", sme_actions_required)
        metric_row_2[3].metric("Knowledge Files Loaded", knowledge_files_loaded)
        st.caption(f"Total Budget: ${total_budget:,.0f}")

        left_col, center_col, right_col = st.columns([1, 1.2, 1])

        with left_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Integration Journey")
            st.write("1. Due Diligence")
            st.write("2. Day 1 Readiness")
            st.write("3. Finance Mapping")
            st.write("4. Workforce Alignment")
            st.write("5. Systems and Controls")
            st.write("6. Legal Entity Simplification")
            st.write("7. Steady State")
            st.markdown("</div>", unsafe_allow_html=True)

        with center_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Ask IBM Bob")
            st.write("Ask IBM Bob anything about this acquisition integration.")
            st.text_area(
                "",
                value="We acquired a company with different COA, 12 legal entities, 500 employees and incomplete tax registration. What should we do first?",
                height=120,
                key="dashboard_bob_question",
            )
            st.caption("Use the IBM Bob Q&A tab to view the structured response.")
            st.markdown("</div>", unsafe_allow_html=True)

        with right_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Live Command Center Metrics")
            st.info(f"{high_risks} high-risk items currently need executive attention.")
            st.info(f"Forecast spend is ${forecast_spend:,.0f} against a total budget of ${total_budget:,.0f}.")
            st.info(f"Estimated savings currently total ${estimated_savings:,.0f}.")
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
            st.subheader("Budget Overview")
            st.bar_chart(budget_chart_data)

        with chart_col2:
            st.subheader("Legal Entity Actions")
            st.bar_chart(legal_action_counts)

        st.subheader("Integration Status Overview")
        st.bar_chart(status_counts)

    with status_tab:
        render_tab_header(
            "Integration Status",
            "Review current progress across tracked integration areas and identify which workstreams remain incomplete.",
        )
        status_metric_col1, status_metric_col2, status_metric_col3 = st.columns(3)
        status_metric_col1.metric("Tracked Areas", total_areas)
        status_metric_col2.metric("Completed", completed_areas)
        status_metric_col3.metric("Readiness", f"{readiness_percent}%")
        st.dataframe(integration_status, use_container_width=True)

    with risks_tab:
        render_tab_header(
            "Risks",
            "Monitor risk exposure and focus leadership attention on the most critical blockers to integration readiness.",
        )
        risk_metric_col1, risk_metric_col2 = st.columns(2)
        risk_metric_col1.metric("Total Risks", len(risks))
        risk_metric_col2.metric("High Risks", high_risks)
        st.dataframe(risks, use_container_width=True)

    with budget_tab:
        render_tab_header(
            "Budget",
            "Compare budget, current spend, forecast, and expected savings to understand overall integration cost performance.",
        )
        budget_metric_col1, budget_metric_col2, budget_metric_col3 = st.columns(3)
        budget_metric_col1.metric("Total Budget", f"${total_budget:,.0f}")
        budget_metric_col2.metric("Forecast Spend", f"${forecast_spend:,.0f}")
        budget_metric_col3.metric("Estimated Savings", f"${estimated_savings:,.0f}")
        st.dataframe(budget, use_container_width=True)
        st.subheader("Totals")
        st.dataframe(budget_totals, use_container_width=True)

    with legal_tab:
        render_tab_header(
            "Legal Entities",
            "Review legal entity actions, audit cost exposure, and expected savings from simplification decisions.",
        )
        legal_metric_col1, legal_metric_col2, legal_metric_col3 = st.columns(3)
        legal_metric_col1.metric("Entities Tracked", len(legal_entities))
        legal_metric_col2.metric("Merge/Dissolve Candidates", len(merge_or_dissolve_entities))
        legal_metric_col3.metric("Action Savings", f"${total_action_savings:,.0f}")
        st.dataframe(
            legal_entities[[
                "entity_name",
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

    with sme_tab:
        render_tab_header(
            "SME Directory",
            "Use the SME directory to identify functional owners, backups, and escalation contacts for key integration questions.",
        )
        sme_metric_col1, sme_metric_col2 = st.columns(2)
        sme_metric_col1.metric("SME Records", len(sme_directory))
        sme_metric_col2.metric("Region Focus", region)
        st.dataframe(sme_directory, use_container_width=True)

    with knowledge_tab:
        render_tab_header(
            "Knowledge Library",
            "Reference approved knowledge, lessons learned, and reusable guidance to accelerate future acquisition decisions.",
        )
        st.text_area("Approved knowledge and lessons learned", knowledge_library_text, height=250)

    with bob_tab:
        render_tab_header(
            "IBM Bob Q&A",
            "Use structured IBM Bob responses to guide actions, identify owners, and accelerate acquisition decision-making.",
        )
        st.write("Ask IBM Bob anything about this acquisition integration. Example")
        st.code(
            "We acquired a company with different COA, 12 legal entities, 500 employees and incomplete tax registration. What should we do first?",
            language="text",
        )
        question = st.selectbox(
            "Select a sample question",
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
                f"Start by creating the {workspace_name} workspace for {region}, uploading core data, and addressing the {high_risks} current high-risk items while improving readiness from {readiness_percent}%."
            )
            st.subheader("Agent Capabilities Used")
            st.write("- Integration Navigator")
            st.write("- Risk & Controls")
            st.write("- Budget & Value Tracking")
            st.write("- Legal Entity Optimization")
            st.subheader("Recommended Actions")
            st.write(f"1. Create the {workspace_name} workspace and confirm Day 1 / Day 100 targets.")
            st.write("2. Upload chart of accounts, headcount, legal entity, risk, and budget files.")
            st.write(f"3. Review the {high_risks} high-risk items and assign owners for open actions.")
            st.subheader("Owners")
            st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
            st.subheader("Timeline")
            st.write(f"Immediate start in Week 1, targeting Day 1 on {day_1_date} and Day 100 on {day_100_date}.")
            st.subheader("Risks")
            st.write("Incomplete mappings, missing SMEs, and unresolved legal entity issues may delay readiness.")
            st.subheader("Budget / Savings / Cash Impact")
            st.write(f"Forecast spend: ${forecast_spend:,.0f}")
            st.write(f"Estimated savings: ${estimated_savings:,.0f}")
            st.write(f"Cash release opportunity: ${cash_release_opportunity:,.0f}")
            st.subheader("Readiness Impact")
            st.write(f"Current readiness is {readiness_percent}% with {high_risks} high-risk items requiring action.")
            st.subheader("Next Steps")
            st.write(f"Refresh the dashboard after each upload and route open issues to {integration_lead} and the correct functional owners.")

        elif question == "We acquired a company with different COA, 12 legal entities and 500 employees. What should we do first?":
            st.subheader("Executive Summary")
            st.write(
                f"Start by launching the {workspace_name} workspace for {region}, validating chart of accounts mapping, reviewing the 12 legal entities for simplification, and aligning the 500-employee workforce structure to target Day 1 and Day 100 milestones."
            )
            st.subheader("Agent Capabilities Used")
            st.write("- Integration Navigator")
            st.write("- Finance & Account Mapping")
            st.write("- Workforce & Organization Mapping")
            st.write("- Legal Entity Optimization")
            st.subheader("Recommended Actions")
            st.write("1. Upload COA, legal entity, workforce, risk, and budget files.")
            st.write("2. Review finance mapping gaps and workforce alignment dependencies.")
            st.write("3. Identify legal entities that may be retained, merged, or dissolved.")
            st.write(f"4. Assign {integration_lead} and functional owners to the highest-priority actions.")
            st.subheader("Owners")
            st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
            st.subheader("Timeline")
            st.write(f"Immediate mobilization, targeting Day 1 on {day_1_date} and Day 100 on {day_100_date}.")
            st.subheader("Risks")
            st.write("COA misalignment, unresolved entity structure, and workforce mapping issues may delay readiness.")
            st.subheader("Budget / Savings / Cash Impact")
            st.write(f"Forecast spend: ${forecast_spend:,.0f}")
            st.write(f"Estimated savings: ${estimated_savings:,.0f}")
            st.write(f"Total value opportunity: ${total_value_opportunity:,.0f}")
            st.subheader("Readiness Impact")
            st.write(f"Readiness depends on finance mapping, workforce alignment, and legal entity simplification progress ahead of Day 1.")
            st.subheader("Next Steps")
            st.write("Complete data uploads, confirm SME coverage, and refresh the dashboard to validate integration readiness.")

        elif question == "Which legal entities can be merged or dissolved and what is the cash impact?":
            st.subheader("Executive Summary")
            st.write(
                f"There are {len(merge_or_dissolve_entities)} legal entities currently flagged for merge or dissolve, with an estimated annual admin cost impact of ${annual_admin_cost_reduction:,.0f} and total action savings of ${total_action_savings:,.0f}."
            )
            st.subheader("Agent Capabilities Used")
            st.write("- Legal Entity Optimization")
            st.write("- Budget & Value Tracking")
            st.subheader("Recommended Actions")
            st.write("Review the recommended_action column in the Legal Entities tab.")
            st.dataframe(
                merge_or_dissolve_entities[[
                    "entity_name",
                    "external_auditors",
                    "annual_audit_fees",
                    "recommended_action",
                    "annual_admin_cost",
                    "saving_if_action_is_taken",
                ]],
                use_container_width=True,
            )
            st.subheader("Owners")
            st.write("Legal, Tax, Treasury, Integration Lead")
            st.subheader("Timeline")
            st.write("Assess in the current integration planning cycle")
            st.subheader("Risks")
            st.write("Active contracts, regulatory requirements, and incomplete information may block action.")
            st.subheader("Budget / Savings / Cash Impact")
            st.write(f"Annual admin cost impact: ${annual_admin_cost_reduction:,.0f}")
            st.write(f"Action savings: ${total_action_savings:,.0f}")
            st.write(f"Cash release opportunity: ${cash_release_opportunity:,.0f}")
            st.subheader("Readiness Impact")
            st.write("Entity simplification can reduce operational complexity and improve Day 100 stabilization.")
            st.subheader("Next Steps")
            st.write("Validate candidates and confirm whether the estimated admin cost reduction can be realized.")

        elif question == "Who can help with payroll integration in Japan?":
            st.subheader("Executive Summary")
            if not japan_payroll_sme.empty:
                payroll_row = japan_payroll_sme.iloc[0]
                st.write(
                    f"The primary payroll SME for Japan is {payroll_row['primary_sme']}, with backup support from {payroll_row['backup_sme']}."
                )
                st.subheader("Agent Capabilities Used")
                st.write("- SME Discovery")
                st.write("- Workforce & Organization Mapping")
                st.subheader("Recommended Actions")
                st.write("Engage the primary SME first, then use the backup SME or escalation path if needed.")
                st.subheader("Owners")
                st.write("HR, Payroll, Regional HR Leadership")
                st.subheader("Timeline")
                st.write("Immediate")
                st.subheader("Risks")
                st.write("Delays in payroll setup can affect Day 1 readiness and employee experience.")
                st.subheader("Budget / Savings / Cash Impact")
                st.write("Payroll delays may increase transition costs and readiness risk if unresolved.")
                st.subheader("Readiness Impact")
                st.write("Payroll SME alignment supports workforce readiness and Day 1 employee continuity.")
                st.subheader("Next Steps")
                st.write(f"Contact {payroll_row['primary_sme']} and escalate via {payroll_row['escalation_path']} if required.")
            else:
                st.write("No Japan payroll SME was found in the SME Directory.")

except Exception as e:
    st.error(f"Could not load sample data: {e}")
