import streamlit as st
import pandas as pd
from data.hardcoded_data import shareholders, board_members, members, capital_calls

def show():
    st.header("👥 Shareholders, Board & Member Portal")
    role = st.session_state.role
    
    tab1, tab2, tab3, tab4 = st.tabs(["Shareholders", "Board of Directors", "Member Commitments", "Capital Calls"])
    
    with tab1:
        st.subheader("Shareholder Registry")
        st.dataframe(shareholders, use_container_width=True)
    
    with tab2:
        st.subheader("Board of Directors")
        st.dataframe(board_members, use_container_width=True)
        st.caption("Same person can serve on multiple committees (see Committee Memberships column).")
    
    with tab3:
        st.subheader("Member Commitments & Performance")
        st.dataframe(members, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            st.bar_chart(members.set_index('name')[['committed_mm', 'allocated_mm']])
        with col2:
            st.bar_chart(members.set_index('name')['returns_mm'])
    
    with tab4:
        st.subheader("Capital Call Schedule")
        st.dataframe(capital_calls, use_container_width=True)
        if role in ["Accounts", "CEO"]:
            st.subheader("Capital Call Forecast")
            forecast = pd.DataFrame({
                'Month': pd.date_range(start='2024-04-01', periods=4, freq='M'),
                'Expected Call ($M)': [4.5, 5.0, 3.8, 6.2]
            })
            st.line_chart(forecast.set_index('Month'))