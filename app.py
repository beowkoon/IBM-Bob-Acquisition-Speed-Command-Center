import streamlit as st
import pandas as pd

st.set_page_config(page_title="IBM Bob Acquisition Speed Command Center", layout="wide")

st.title("IBM Bob Acquisition Speed Command Center")
st.subheader("Prototype Dashboard")

st.write("This is the initial prototype for acquisition integration tracking.")


def recommend_legal_entity_action(entity):
    if entity["regulatory_required"] == "Yes":
        return "Retain"
    if entity["employees"] == 0 and entity["annual_revenue"] == 0 and entity["active_contracts"] == "No":
        return "Dissolve"
    if entity["duplicate_ibm_presence"] == "Yes" and entity["regulatory_required"] == "No":
        return "Merge"
    return "Further Assessment"


try:
    integration_status = pd.read_csv("sample_data/integration_status.csv")
    risks = pd.read_csv("sample_data/risks.csv")
    budget = pd.read_csv("sample_data/budget.csv")
    legal_entities = pd.read_csv("sample_data/legal_entities.csv")
    sme_directory = pd.read_csv("sample_data/sme_directory.csv")

    legal_entities["recommended_action"] = legal_entities.apply(recommend_legal_entity_action, axis=1)

    completed_areas = (integration_status["status"] == "Complete").sum()
    total_areas = len(integration_status)
    readiness_percent = round((completed_areas / total_areas) * 100) if total_areas else 0
    high_risks = (risks["severity"] == "High").sum()
    total_budget = budget["budget"].sum()
    forecast_spend = budget["forecast_spend"].sum()
    estimated_savings = budget["estimated_savings"].sum()

    dashboard_tab, status_tab, risks_tab, budget_tab, legal_tab, sme_tab, bob_tab = st.tabs(
        [
            "Dashboard",
            "Integration Status",
            "Risks",
            "Budget",
            "Legal Entities",
            "SME Directory",
            "IBM Bob Q&A",
        ]
    )

    with dashboard_tab:
        st.header("Dashboard Metrics")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Readiness %", f"{readiness_percent}%")
        col2.metric("High Risks", high_risks)
        col3.metric("Forecast Spend", f"${forecast_spend:,.0f}")
        col4.metric("Estimated Savings", f"${estimated_savings:,.0f}")
        st.caption(f"Total Budget: ${total_budget:,.0f}")

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
            st.write("Start by creating the acquisition workspace, uploading core finance, HR, legal, risk, and budget data, and validating Day 1 readiness gaps.")
            st.subheader("Recommended Actions")
            st.write("1. Create workspace and confirm Day 1 / Day 100 targets.")
            st.write("2. Upload chart of accounts, headcount, legal entity, risk, and budget files.")
            st.write("3. Review dashboard metrics and assign owners for open items.")
            st.subheader("Owners / Functions")
            st.write("Integration Lead, Finance, HR, Legal, Tax")
            st.subheader("Timeline")
            st.write("Immediate start in Week 1")
            st.subheader("Risks and Dependencies")
            st.write("Incomplete mappings, missing SMEs, and unresolved legal entity issues may delay readiness.")
            st.subheader("Next Steps")
            st.write("Refresh the dashboard after each upload and route open issues to the correct owners.")

        elif question == "Which legal entities can be merged or dissolved and what is the cash impact?":
            st.subheader("Executive Summary")
            st.write("Entities with duplicate IBM presence and no regulatory requirement may be candidates for merge, while inactive entities with no employees or revenue may be candidates for dissolution.")
            st.subheader("Recommended Actions")
            st.write("Review the recommended_action column in the Legal Entities tab.")
            st.write("Validate merge and dissolve candidates with Legal, Tax, and Treasury.")
            st.subheader("Owners / Functions")
            st.write("Legal, Tax, Treasury, Integration Lead")
            st.subheader("Timeline")
            st.write("Assess in the current integration planning cycle")
            st.subheader("Risks and Dependencies")
            st.write("Active contracts, regulatory requirements, and incomplete information may block action.")
            st.subheader("Next Steps")
            st.write("Estimate annual admin cost reduction from entities marked for merge or dissolve.")

        elif question == "Who can help with payroll integration in Japan?":
            st.subheader("Executive Summary")
            st.write("The SME Directory identifies the payroll SME coverage for Japan.")
            st.subheader("Recommended Actions")
            st.write("Engage the primary SME first, then use the backup SME or escalation path if needed.")
            st.subheader("Owners / Functions")
            st.write("HR, Payroll, Regional HR Leadership")
            st.subheader("Timeline")
            st.write("Immediate")
            st.subheader("Risks and Dependencies")
            st.write("Delays in payroll setup can affect Day 1 readiness and employee experience.")
            st.subheader("Next Steps")
            st.write("Review the Japan payroll row in the SME Directory tab and contact the listed SME.")

except Exception as e:
    st.error(f"Could not load sample data: {e}")
