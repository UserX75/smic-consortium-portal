import streamlit as st
import pandas as pd
from data.hardcoded_data import active_deals

def show():
    st.subheader("📋 Deal Flow Pipeline")
    role = st.session_state.role
    
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = []
    
    stages = ["Pre-screen", "Due Diligence", "Negotiation", "Closing"]
    cols = st.columns(len(stages))
    
    for idx, stage in enumerate(stages):
        with cols[idx]:
            st.markdown(f"<h3 style='text-align: center;'>{stage}</h3>", unsafe_allow_html=True)
            stage_deals = active_deals[active_deals['stage'] == stage]
            st.caption(f"{len(stage_deals)} deals")
            for _, deal in stage_deals.iterrows():
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 12px; margin-bottom: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 3px solid #d4af37;">
                    <strong>{deal['deal']}</strong><br>
                    <i class="fas fa-chart-line"></i> ${deal['size_mm']}M<br>
                    <i class="fas fa-percent"></i> IRR: {deal['expected_irr']}%<br>
                    <i class="fas fa-industry"></i> {deal['industry']}
                </div>
                """, unsafe_allow_html=True)
    
    # Pipeline metrics
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    total_potential = active_deals['size_mm'].sum()
    avg_irr = active_deals['expected_irr'].mean()
    with col1:
        st.metric("Total Pipeline Value", f"${total_potential}M")
    with col2:
        st.metric("Average Expected IRR", f"{avg_irr:.1f}%")
    with col3:
        st.metric("Active Deals", len(active_deals))
    
    if role == "CEO":
        with st.expander("✏️ Edit Pipeline (CEO only)"):
            edited = st.data_editor(active_deals, num_rows="dynamic", use_container_width=True)
            if st.button("Save Changes"):
                st.success("Pipeline updated (demo)")
                st.rerun()