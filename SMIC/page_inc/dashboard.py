import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from data.hardcoded_data import investments, sector_allocation, risk_metrics, nav_history, monthly_returns, holdings
from utils.charts import create_pie_chart, create_bar_chart, create_line_chart, create_treemap

def show():
    role = st.session_state.role
    
    # ========== KPI ROW ==========
    col1, col2, col3, col4 = st.columns(4)
    total_aum = investments['valuation_usd_m'].sum()
    total_return = investments['irr_estimate'].mean()
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label"><i class="fas fa-chart-line"></i> Total AUM</div>
            <div class="metric-value">${total_aum:.1f}M</div>
            <div class="metric-delta"><i class="fas fa-arrow-up"></i> +12% YoY</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label"><i class="fas fa-percent"></i> Avg IRR</div>
            <div class="metric-value">{total_return:.1f}%</div>
            <div class="metric-delta"><i class="fas fa-chart-line"></i> Above target</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label"><i class="fas fa-briefcase"></i> Active Deals</div>
            <div class="metric-value">6</div>
            <div class="metric-delta"><i class="fas fa-plus"></i> +2 this quarter</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label"><i class="fas fa-chart-simple"></i> Sharpe Ratio</div>
            <div class="metric-value">{risk_metrics['sharpe_ratio']:.2f}</div>
            <div class="metric-delta"><i class="fas fa-thumbs-up"></i> Strong</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== CEO VIEW ==========
    if role == "CEO":
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📊 Sector Allocation")
            fig = create_pie_chart(sector_allocation, 'sector', 'allocation', '')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.subheader("📈 Top 5 Investments")
            top = investments.nlargest(5, 'valuation_usd_m')[['entity', 'valuation_usd_m', 'ownership_pct']]
            st.dataframe(top, use_container_width=True, hide_index=True)
        
        st.subheader("📉 NAV Growth Trend")
        fig_line = create_line_chart(nav_history, 'date', 'nav', '')
        st.plotly_chart(fig_line, use_container_width=True, config={'displayModeBar': False})
        
        # Search & Filter (non-redundant)
        with st.expander("🔍 Filter Holdings", expanded=False):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                search = st.text_input("Search by entity name", placeholder="e.g., Sekhametsi")
            with col_f2:
                sector_filter = st.multiselect("Filter by sector", options=investments['sector'].unique())
            
            filtered = investments.copy()
            if search:
                filtered = filtered[filtered['entity'].str.contains(search, case=False)]
            if sector_filter:
                filtered = filtered[filtered['sector'].isin(sector_filter)]
            st.dataframe(filtered[['entity', 'sector', 'ownership_pct', 'valuation_usd_m', 'irr_estimate']], 
                        use_container_width=True, hide_index=True)
    
    # ========== BOARD MEMBER VIEW ==========
    elif role == "Board Member":
        st.subheader("🏛️ Governance Overview")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="dashboard-card"><i class="fas fa-check-circle"></i> Compliance Score: <strong>98/100</strong></div>', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-card"><i class="fas fa-users"></i> Board Attendance: <strong>94%</strong></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="dashboard-card"><i class="fas fa-balance-scale"></i> Audit Findings: <strong>0</strong></div>', unsafe_allow_html=True)
            st.markdown('<div class="dashboard-card"><i class="fas fa-leaf"></i> ESG Rating: <strong>AA</strong></div>', unsafe_allow_html=True)
        
        st.subheader("📊 Top & Bottom Performers")
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Top 3 by IRR")
            top = investments.nlargest(3, 'irr_estimate')[['entity', 'irr_estimate']]
            st.dataframe(top, hide_index=True)
        with col2:
            st.caption("Bottom 3 by IRR")
            bottom = investments.nsmallest(3, 'irr_estimate')[['entity', 'irr_estimate']]
            st.dataframe(bottom, hide_index=True)
    
    # ========== ACCOUNTS VIEW ==========
    else:
        st.subheader("💰 Financial Operations")
        from data.hardcoded_data import capital_calls
        st.dataframe(capital_calls, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Fee Summary")
            fee_data = pd.DataFrame({
                'Category': ['Management Fees', 'Performance Fees', 'Director Fees (Q1)'],
                'Amount ($M)': [1.24, 2.90, 0.15]
            })
            st.dataframe(fee_data, hide_index=True)
        with col2:
            st.subheader("Capital Call Forecast")
            forecast = pd.DataFrame({
                'Month': ['Apr', 'May', 'Jun', 'Jul'],
                'Amount ($M)': [4.5, 5.0, 3.8, 6.2]
            })
            st.bar_chart(forecast.set_index('Month'))