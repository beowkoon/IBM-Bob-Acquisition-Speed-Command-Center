import streamlit as st
import pandas as pd

st.set_page_config(page_title="IBM Bob Acquisition Speed Command Center", layout="wide")

st.title("IBM Bob Acquisition Speed Command Center")
st.subheader("Prototype Dashboard")

st.write("This is the initial prototype for acquisition integration tracking.")

try:
    integration_status = pd.read_csv("sample_data/integration_status.csv")
    risks = pd.read_csv("sample_data/risks.csv")
    budget = pd.read_csv("sample_data/budget.csv")
    legal_entities = pd.read_csv("sample_data/legal_entities.csv")
    sme_directory = pd.read_csv("sample_data/sme_directory.csv")

    completed_areas = (integration_status["status"] == "Complete").sum()
    total_areas = len(integration_status)
    readiness_percent = round((completed_areas / total_areas) * 100) if total_areas else 0
    high_risks = (risks["severity"] == "High").sum()
    total_budget = budget["budget"].sum()
    forecast_spend = budget["forecast_spend"].sum()
    estimated_savings = budget["estimated_savings"].sum()

    dashboard_tab, status_tab, risks_tab, budget_tab, legal_tab, sme_tab = st.tabs(
        ["Dashboard", "Integration Status", "Risks", "Budget", "Legal Entities", "SME Directory"]
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

except Exception as e:
    st.error(f"Could not load sample data: {e}")
