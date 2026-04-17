import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data.hardcoded_data import holdings, monthly_returns
from utils.charts import create_bar_chart, create_line_chart, create_waterfall_chart

def show():
    st.header("📈 Investment Performance")
    role = st.session_state.role
    
    col1, col2 = st.columns(2)
    with col1:
        fig_returns = create_bar_chart(holdings, 'asset', 'return_pct', 'Returns by Asset', color='sector')
        st.plotly_chart(fig_returns, use_container_width=True, config={'displayModeBar': False})
    with col2:
        fig_monthly = create_line_chart(monthly_returns, 'date', 'portfolio_return', 'Monthly Returns vs Benchmark')
        fig_monthly.add_trace(go.Scatter(x=monthly_returns['date'], y=monthly_returns['benchmark_return'],
                                         mode='lines+markers', name='Benchmark',
                                         line=dict(color='#2a4b7c'), marker=dict(color='#0a2540')))
        st.plotly_chart(fig_monthly, use_container_width=True, config={'displayModeBar': False})
    
    st.subheader("📊 Contribution to Total Return")
    holdings['contribution'] = (holdings['value'] * holdings['return_pct'] / 100) / 1e6
    fig_waterfall = create_waterfall_chart(holdings['contribution'].tolist(), holdings['asset'].tolist(), 
                                           "Contribution to Total Return ($M)")
    st.plotly_chart(fig_waterfall, use_container_width=True, config={'displayModeBar': False})
    
    if role == "CEO" or role == "Board Member":
        st.subheader("📅 Rolling 3-Month Average Returns")
        rolling_returns = monthly_returns['portfolio_return'].rolling(window=3).mean()
        st.line_chart(rolling_returns)
