import streamlit as st
import pandas as pd
from data.hardcoded_data import board_members, committees

def show():
    st.header("🏛️ Committee Dashboards")
    
    committee_tab = st.tabs([
        "Directors Affairs", 
        "Audit and Risk", 
        "Investment", 
        "VDI Adhoc", 
        "AGM Electoral"
    ])
    
    # Committee 1: Directors Affairs
    with committee_tab[0]:
        st.subheader("Directors Affairs Committee")
        members_list = committees['Directors Affairs Committee']
        st.write("**Members:**", ", ".join(members_list))
        st.write("**Responsibilities:** Director nominations, succession planning, board evaluations.")
        st.dataframe(board_members[['name', 'position', 'term_start', 'term_end']])
    
    # Committee 2: Audit and Risk
    with committee_tab[1]:
        st.subheader("Audit and Risk Committee")
        members_list = committees['Audit and Risk Committee']
        st.write("**Members:**", ", ".join(members_list))
        st.write("**Responsibilities:** Financial reporting oversight, internal controls, risk management.")
        from data.hardcoded_data import risk_metrics
        st.metric("Current Risk Score", "Low-Medium")
        st.json(risk_metrics)
    
    # Committee 3: Investment
    with committee_tab[2]:
        st.subheader("Investment Committee")
        members_list = committees['Investment Committee']
        st.write("**Members:**", ", ".join(members_list))
        st.write("**Responsibilities:** Deal flow review, portfolio allocation, performance monitoring.")
        from data.hardcoded_data import investments, active_deals
        st.dataframe(investments[['entity', 'ownership_pct', 'valuation_usd_m', 'irr_estimate']])
        st.subheader("Active Deals")
        st.dataframe(active_deals)
    
    # Committee 4: VDI Adhoc
    with committee_tab[3]:
        st.subheader("VDI Adhoc Committee")
        members_list = committees['VDI Adhoc Committee']
        st.write("**Members:**", ", ".join(members_list))
        st.write("**Responsibilities:** Digital transformation, cybersecurity, IT infrastructure projects.")
        st.info("Current project: Implementation of SMIC Investor Portal (this app!)")
        st.progress(75, text="VDI Project Completion")
    
    # Committee 5: AGM Electoral
    with committee_tab[4]:
        st.subheader("AGM Electoral Committee")
        members_list = committees['AGM Electoral Committee']
        st.write("**Members:**", ", ".join(members_list))
        st.write("**Responsibilities:** Organize AGM elections, manage nominations, oversee voting.")
        st.success("Next AGM scheduled: June 15, 2025")
        # Replace page_link with a button that uses the navigation (optional)
        if st.button("🗳️ Go to Voting Polls"):
            st.session_state.selected_page = "Voting Polls"
            st.rerun()
        # Or simply a markdown note
        st.markdown("*To vote, navigate to 'Voting Polls' from the sidebar menu.*")