import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from data.hardcoded_data import holdings

def show():
    st.header("🔮 What-If Scenario Analyzer")
    st.markdown("Adjust sliders to see impact on portfolio returns.")
    
    total_aum = holdings['value'].sum()
    base_return = (holdings['value'] * holdings['return_pct'] / 100).sum() / total_aum * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Sector Return Adjustments")
        sectors = holdings['sector'].unique()
        sector_adjust = {}
        for sector in sectors:
            sector_adjust[sector] = st.slider(
                f"{sector} Adjustment (%)", -20.0, 20.0, 0.0, step=1.0,
                help="Percentage points added/subtracted from base returns"
            )
    with col2:
        st.subheader("Macro Adjustments")
        market_adjust = st.slider("Market Sentiment (%)", -15.0, 15.0, 0.0, 1.0)
        interest_rate = st.slider("Interest Rate Shock (bps)", -200, 200, 0, 25)
    
    adjusted_returns = []
    for idx, row in holdings.iterrows():
        adj = sector_adjust.get(row['sector'], 0)
        new_return = row['return_pct'] + adj + market_adjust
        if row['sector'] in ['Real Estate', 'Infrastructure']:
            new_return -= interest_rate / 100
        adjusted_returns.append(max(new_return, -50))
    
    holdings_adj = holdings.copy()
    holdings_adj['return_pct'] = adjusted_returns
    scenario_return = (holdings_adj['value'] * holdings_adj['return_pct'] / 100).sum() / total_aum * 100
    
    st.subheader("📊 Scenario Results")
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Base Return", f"{base_return:.1f}%")
    with metric_col2:
        st.metric("Scenario Return", f"{scenario_return:.1f}%", 
                  delta=f"{scenario_return - base_return:.1f}%")
    with metric_col3:
        delta_value = (scenario_return - base_return) / 100 * total_aum / 1e6
        st.metric("Value Impact", f"M{delta_value:.1f}M", delta=None)
    
    comp_df = pd.DataFrame({
        'Scenario': ['Base', 'Adjusted'],
        'Total Return (%)': [base_return, scenario_return]
    })
    fig = px.bar(comp_df, x='Scenario', y='Total Return (%)', color='Scenario', 
                 text='Total Return (%)',
                 color_discrete_sequence=['#0a2540', '#d4af37'])
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(title_font_color='#0a2540')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': True})
    
    st.subheader("📋 Impact by Investment")
    holdings_adj['return_change'] = holdings_adj['return_pct'] - holdings['return_pct']
    impact_df = holdings_adj[['asset', 'sector', 'return_pct', 'return_change']].sort_values('return_change', ascending=False)
    st.dataframe(impact_df, use_container_width=True)
    
    # Enhancement #4: Monte Carlo Simulation
    st.markdown("---")
    st.subheader("🎲 Monte Carlo Simulation (1000 scenarios)")
    if st.button("Run Simulation"):
        sim_returns = np.random.normal(scenario_return, 5, 1000)
        fig_hist = px.histogram(sim_returns, nbins=30, 
                                title="Distribution of Possible Portfolio Returns",
                                labels={'value': 'Return (%)'},
                                color_discrete_sequence=['#d4af37'])
        fig_hist.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': True})
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Expected Return", f"{scenario_return:.1f}%")
        with col2:
            st.metric("95% Confidence Interval", 
                      f"{np.percentile(sim_returns, 2.5):.1f}% to {np.percentile(sim_returns, 97.5):.1f}%")
    
    st.info("💡 This is a simplified model. In production, you'd link to pricing engines.")