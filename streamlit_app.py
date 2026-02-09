import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go

from rag.retriever import get_retriever
from pipeline.run_pipeline import run_corep_pipeline


st.set_page_config(page_title="COREP Assistant", layout="wide")

st.title("🏦 COREP Capital Analytics Dashboard")

st.markdown(
    "AI powered COREP extraction with compliance, audit, and explainability."
)

retriever = get_retriever()

query = st.text_area(
    "Enter Bank Capital Data",
    """
Bank reports:
CET1 = 120 million
AT1 = 20 million
Tier2 = 10 million
RWA = 900 million
"""
)

if st.button("Run COREP Pipeline"):

    docs = retriever.invoke(query)
    output = run_corep_pipeline(query, docs)
    st.subheader("COREP Reporting Extract")
    st.table(output["corep_template"])

    validated = output["validated_result"]
    compliance = output["compliance_results"]
    risk_flags = output["risk_flags"]
    explanations = output["explanations"]
    evidence = output["evidence"]

    # ====================================================
    # 📊 Capital Summary Chart
    # ====================================================

    st.header("📊 Capital Distribution")

    capital_df = pd.DataFrame({
        "Capital Type": ["CET1", "AT1", "Tier2"],
        "Amount": [
            validated.cet1_capital,
            validated.at1_capital,
            validated.tier2_capital
        ]
    })

    fig = go.Figure(
        data=[go.Bar(
            x=capital_df["Capital Type"],
            y=capital_df["Amount"]
        )]
    )

    st.plotly_chart(fig, use_container_width=True)

    # ====================================================
    # 📋 COREP Output Table
    # ====================================================

    st.header("📋 COREP Output")

    st.dataframe(pd.DataFrame([validated.model_dump()]))

    # ====================================================
    # ✅ Compliance Gauge
    # ====================================================

    st.header("✅ Compliance Ratios")

    col1, col2 = st.columns(2)

    with col1:
        fig_cet1 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=validated.cet1_ratio,
            title={"text": "CET1 Ratio (%)"},
            gauge={"axis": {"range": [0, 20]}}
        ))
        st.plotly_chart(fig_cet1)

    with col2:
        fig_total = go.Figure(go.Indicator(
            mode="gauge+number",
            value=validated.total_capital_ratio,
            title={"text": "Total Capital Ratio (%)"},
            gauge={"axis": {"range": [0, 25]}}
        ))
        st.plotly_chart(fig_total)

    # ====================================================
    # ⚠ Risk Flags With Severity Colors
    # ====================================================

    st.header("⚠ Risk Flags")

    if risk_flags:
        for flag in risk_flags:

            if flag["severity"] == "CRITICAL":
                st.error(flag["message"])

            elif flag["severity"] == "WARNING":
                st.warning(flag["message"])

            else:
                st.info(flag["message"])
    else:
        st.success("No Risk Flags")

    # ====================================================
    # 🧠 Explainability Viewer
    # ====================================================

    st.header("🧠 Explainability")

    for metric, info in explanations.items():
        with st.expander(metric.upper()):
            st.write(info)

    # ====================================================
    # 📄 Evidence Confidence Viewer
    # ====================================================

    st.header("📄 Evidence Confidence")

    evidence_rows = []

    for field, data in evidence.items():
        evidence_rows.append({
            "Field": field,
            "Value": data["value"],
            "Confidence": data["confidence"],
            "Source": data["source"],
            "Page": data["page"]
        })

    evidence_df = pd.DataFrame(evidence_rows)

    st.dataframe(evidence_df)

    # Confidence bar chart
    fig_conf = go.Figure(
        data=[go.Bar(
            x=evidence_df["Field"],
            y=evidence_df["Confidence"]
        )]
    )

    st.plotly_chart(fig_conf, use_container_width=True)

    # ====================================================
    # 📁 Audit Log Download
    # ====================================================

    st.header("📁 Audit Log")

    with open(output["audit_file"], "r") as f:
        audit_data = json.load(f)

    st.download_button(
        label="Download Audit Log",
        data=json.dumps(audit_data, indent=2),
        file_name="audit_log.json",
        mime="application/json"
    )
