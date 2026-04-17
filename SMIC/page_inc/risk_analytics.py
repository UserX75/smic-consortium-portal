import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from data.hardcoded_data import risk_metrics, holdings

def show():
    st.header("⚠️ Risk Analytics")
    role = st.session_state.role
    
    col1, col2, col3 = st.columns(3)
    risk_items = list(risk_metrics.items())
    for i, (k, v) in enumerate(risk_items[:3]):
        with [col1, col2, col3][i]:
            st.metric(k.replace('_', ' ').title(), f"{v:.2f}" if isinstance(v, float) else v)
    
    st.subheader("📊 Concentration Risk")
    top_holding_weight = holdings['value'].max() / holdings['value'].sum() * 100
    st.metric("Top Holding Weight", f"{top_holding_weight:.1f}%")
    st.progress(top_holding_weight / 100)
    
    # Simulated correlation matrix
    st.subheader("🔄 Asset Correlation Heatmap")
    np.random.seed(42)
    assets = holdings['asset'].tolist()
    n_assets = len(assets)
    corr_matrix = np.random.uniform(-0.3, 0.8, (n_assets, n_assets))
    corr_matrix = (corr_matrix + corr_matrix.T) / 2
    np.fill_diagonal(corr_matrix, 1)
    corr_df = pd.DataFrame(corr_matrix, index=assets, columns=assets)
    fig = px.imshow(corr_df, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r',
                    title="Asset Return Correlations")
    st.plotly_chart(fig, use_container_width=True)
    
    if role == "CEO":
        st.subheader("🏦 Stress Test Scenarios")
        scenario = st.selectbox("Select stress scenario", ["Market Crash (-20%)", "Interest Rate Hike (+200bps)", "Sector Concentration Risk"])
        if scenario == "Market Crash (-20%)":
            impact = -0.20 * holdings['value'].sum() / 1e6
            st.warning(f"Estimated loss: M{impact:.0f}M")
        elif scenario == "Interest Rate Hike (+200bps)":
            impact = -0.05 * holdings[holdings['sector'].isin(['Real Estate', 'Infrastructure'])]['value'].sum() / 1e6
            st.warning(f"Estimated impact on real estate/infra: M{impact:.0f}M")
        else:
            st.info("Concentration risk: Top 3 holdings represent >40% of AUM")