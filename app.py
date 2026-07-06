import streamlit as st
import pandas as pd

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #f2f4f8;
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

    completed_areas = (integration_status["status"] == "Complete").sum()
    total_areas = len(integration_status)
    readiness_percent = round((completed_areas / total_areas) * 100) if total_areas else 0
    high_risks = (risks["severity"] == "High").sum()
    total_budget = budget["budget"].sum()
    forecast_spend = budget["forecast_spend"].sum()
    estimated_savings = budget["estimated_savings"].sum()
    merge_or_dissolve_entities = legal_entities[
        legal_entities["recommended_action"].isin(["Merge", "Dissolve"])
    ]
    annual_admin_cost_reduction = merge_or_dissolve_entities["annual_admin_cost"].sum()
    total_action_savings = merge_or_dissolve_entities["saving_if_action_is_taken"].sum()
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
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Readiness %", f"{readiness_percent}%")
        col2.metric("High Risks", high_risks)
        col3.metric("Forecast Spend", f"${forecast_spend:,.0f}")
        col4.metric("Estimated Savings", f"${estimated_savings:,.0f}")
        st.caption(f"Total Budget: ${total_budget:,.0f}")

        summary_col, highlights_col = st.columns(2)

        with summary_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Current Workspace Summary")
            st.write(f"{total_areas} integration areas are being tracked in {workspace_name}.")
            st.write(f"Integration lead: {integration_lead}")
            st.write(f"Region: {region}")
            st.write(f"Day 1 target: {day_1_date} | Day 100 target: {day_100_date}")
            st.write(f"{len(merge_or_dissolve_entities)} legal entities are flagged for merge or dissolve review.")
            st.write(f"The current estimated annual admin cost opportunity is ${annual_admin_cost_reduction:,.0f}.")
            st.write(f"The total savings if recommended actions are taken is ${total_action_savings:,.0f}.")
            st.markdown("</div>", unsafe_allow_html=True)

        with highlights_col:
            st.markdown("<div class='executive-card'>", unsafe_allow_html=True)
            st.subheader("Key Highlights")
            st.info(f"{high_risks} high-risk items currently need executive attention.")
            st.info(f"Forecast spend is ${forecast_spend:,.0f} against a total budget of ${total_budget:,.0f}.")
            st.info(f"Estimated savings currently total ${estimated_savings:,.0f}.")
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
        st.caption("Private and Confidential")
        st.header("Integration Status")
        st.dataframe(integration_status)

    with risks_tab:
        st.caption("Private and Confidential")
        st.header("Risks")
        st.dataframe(risks)

    with budget_tab:
        st.caption("Private and Confidential")
        st.header("Budget")
        st.dataframe(budget)
        st.subheader("Totals")
        st.dataframe(budget_totals)

    with legal_tab:
        st.caption("Private and Confidential")
        st.header("Legal Entities")
        st.dataframe(legal_entities)
        st.subheader("Totals")
        st.dataframe(legal_entity_totals)

    with sme_tab:
        st.caption("Private and Confidential")
        st.header("SME Directory")
        st.dataframe(sme_directory)

    with knowledge_tab:
        st.caption("Private and Confidential")
        st.header("Knowledge Library")
        st.text_area("Approved knowledge and lessons learned", knowledge_library_text, height=250)

    with bob_tab:
        st.caption("Private and Confidential")
        st.header("IBM Bob Q&A")
        question = st.selectbox(
            "Select a sample question",
            [
                "What should we do first after acquiring Company X?",
                "Which legal entities can be merged or dissolved and what is the cash impact?",
                "Who can help with payroll integration in Japan?",
            ],
        )

        if question == "What should we do first after acquiring Company X?":
            st.subheader("Executive Summary")
            st.write(
                f"Start by creating the {workspace_name} workspace for {region}, uploading core data, and addressing the {high_risks} current high-risk items while improving readiness from {readiness_percent}%."
            )
            st.subheader("Recommended Actions")
            st.write(f"1. Create the {workspace_name} workspace and confirm Day 1 / Day 100 targets.")
            st.write("2. Upload chart of accounts, headcount, legal entity, risk, and budget files.")
            st.write(f"3. Review the {high_risks} high-risk items and assign owners for open actions.")
            st.subheader("Owners / Functions")
            st.write(f"{integration_lead}, Finance, HR, Legal, Tax")
            st.subheader("Timeline")
            st.write(f"Immediate start in Week 1, targeting Day 1 on {day_1_date} and Day 100 on {day_100_date}.")
            st.subheader("Risks and Dependencies")
            st.write("Incomplete mappings, missing SMEs, and unresolved legal entity issues may delay readiness.")
            st.subheader("Next Steps")
            st.write(f"Refresh the dashboard after each upload and route open issues to {integration_lead} and the correct functional owners.")

        elif question == "Which legal entities can be merged or dissolved and what is the cash impact?":
            st.subheader("Executive Summary")
            st.write(
                f"There are {len(merge_or_dissolve_entities)} legal entities currently flagged for merge or dissolve, with an estimated annual admin cost impact of ${annual_admin_cost_reduction:,.0f} and total action savings of ${total_action_savings:,.0f}."
            )
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
                ]]
            )
            st.subheader("Owners / Functions")
            st.write("Legal, Tax, Treasury, Integration Lead")
            st.subheader("Timeline")
            st.write("Assess in the current integration planning cycle")
            st.subheader("Risks and Dependencies")
            st.write("Active contracts, regulatory requirements, and incomplete information may block action.")
            st.subheader("Next Steps")
            st.write("Validate candidates and confirm whether the estimated admin cost reduction can be realized.")

        elif question == "Who can help with payroll integration in Japan?":
            st.subheader("Executive Summary")
            if not japan_payroll_sme.empty:
                payroll_row = japan_payroll_sme.iloc[0]
                st.write(
                    f"The primary payroll SME for Japan is {payroll_row['primary_sme']}, with backup support from {payroll_row['backup_sme']}."
                )
                st.subheader("Recommended Actions")
                st.write("Engage the primary SME first, then use the backup SME or escalation path if needed.")
                st.subheader("Owners / Functions")
                st.write("HR, Payroll, Regional HR Leadership")
                st.subheader("Timeline")
                st.write("Immediate")
                st.subheader("Risks and Dependencies")
                st.write("Delays in payroll setup can affect Day 1 readiness and employee experience.")
                st.subheader("Next Steps")
                st.write(f"Contact {payroll_row['primary_sme']} and escalate via {payroll_row['escalation_path']} if required.")
            else:
                st.write("No Japan payroll SME was found in the SME Directory.")

except Exception as e:
    st.error(f"Could not load sample data: {e}")
