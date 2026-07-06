import streamlit as st
import pandas as pd

st.set_page_config(page_title="IBM Bob Acquisition Speed Command Center", layout="wide")

st.title("IBM Bob Acquisition Speed Command Center")
st.subheader("Prototype Dashboard")

st.write("This is the initial prototype for acquisition integration tracking.")

st.header("Sample Data Preview")

try:
    integration_status = pd.read_csv("sample_data/integration_status.csv")
    risks = pd.read_csv("sample_data/risks.csv")
    budget = pd.read_csv("sample_data/budget.csv")

    st.write("Integration Status")
    st.dataframe(integration_status)

    st.write("Risks")
    st.dataframe(risks)

    st.write("Budget")
    st.dataframe(budget)

except Exception as e:
    st.error(f"Could not load sample data: {e}")