import streamlit as st
import pandas as pd

st.set_page_config(page_title="IBM Bob Acquisition Speed Command Center", layout="wide")

st.title("IBM Bob Acquisition Speed Command Center")
workspace_name = st.text_input("Acquisition Workspace Name", value="Company X Integration")
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
    japan_payroll_sme = sme_directory[
        (sme_directory["function"] == "Payroll") & (sme_directory["geography"] == "Japan")
    ]

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
            st.subheader("Current Workspace Summary")
            st.write(f"{total_areas} integration areas are being tracked in {workspace_name}.")
            st.write(f"Day 1 target: {day_1_date} | Day 100 target: {day_100_date}")
            st.write(f"{len(merge_or_dissolve_entities)} legal entities are flagged for merge or dissolve review.")
            st.write(f"The current estimated annual admin cost opportunity is ${annual_admin_cost_reduction:,.0f}.")

        with highlights_col:
            st.subheader("Key Highlights")
            st.info(f"{high_risks} high-risk items currently need executive attention.")
            st.info(f"Forecast spend is ${forecast_spend:,.0f} against a total budget of ${total_budget:,.0f}.")
            st.info(f"Estimated savings currently total ${estimated_savings:,.0f}.")

    with status_tab:
        st.header("Integration Status")
        st.dataframe(integration_status)

    with risks_tab:
        st.header("Risks")
        st.dataframe(risks)

    with budget_tab:
        st.header("Budget")
        st.dataframe(budget)

    with legal_tab:
        st.header("Legal Entities")
        st.dataframe(legal_entities)

    with sme_tab:
        st.header("SME Directory")
        st.dataframe(sme_directory)

    with knowledge_tab:
        st.header("Knowledge Library")
        st.text_area("Approved knowledge and lessons learned", knowledge_library_text, height=250)

    with bob_tab:
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
                f"Start by creating the {workspace_name} workspace, uploading core data, and addressing the {high_risks} current high-risk items while improving readiness from {readiness_percent}%."
            )
            st.subheader("Recommended Actions")
            st.write(f"1. Create the {workspace_name} workspace and confirm Day 1 / Day 100 targets.")
            st.write("2. Upload chart of accounts, headcount, legal entity, risk, and budget files.")
            st.write(f"3. Review the {high_risks} high-risk items and assign owners for open actions.")
            st.subheader("Owners / Functions")
            st.write("Integration Lead, Finance, HR, Legal, Tax")
            st.subheader("Timeline")
            st.write(f"Immediate start in Week 1, targeting Day 1 on {day_1_date} and Day 100 on {day_100_date}.")
            st.subheader("Risks and Dependencies")
            st.write("Incomplete mappings, missing SMEs, and unresolved legal entity issues may delay readiness.")
            st.subheader("Next Steps")
            st.write("Refresh the dashboard after each upload and route open issues to the correct owners.")

        elif question == "Which legal entities can be merged or dissolved and what is the cash impact?":
            st.subheader("Executive Summary")
            st.write(
                f"There are {len(merge_or_dissolve_entities)} legal entities currently flagged for merge or dissolve, with an estimated annual admin cost impact of ${annual_admin_cost_reduction:,.0f}."
            )
            st.subheader("Recommended Actions")
            st.write("Review the recommended_action column in the Legal Entities tab.")
            st.dataframe(
                merge_or_dissolve_entities[["entity_name", "recommended_action", "annual_admin_cost"]]
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
