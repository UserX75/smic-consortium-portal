import streamlit as st
import pandas as pd
from data.hardcoded_data import director_fees, employee_fees, fee_payment_dates

def show():
    st.header("💰 Directors & Employees Fees")
    role = st.session_state.role
    
    tab1, tab2 = st.tabs(["Directors (Quarterly)", "Employees (Monthly)"])
    
    with tab1:
        st.subheader("Director Fee Schedule")
        st.dataframe(director_fees, use_container_width=True)
        st.subheader("Payment Calendar 2025")
        st.dataframe(fee_payment_dates, use_container_width=True)
        total_director_fees = director_fees['annual_total'].sum()
        st.metric("Total Annual Director Fees", f"${total_director_fees:,.0f}")
        
        if role in ["CEO", "Accounts"]:
            with st.expander("Edit Director Fees (CRUD Demo)"):
                edited_df = st.data_editor(director_fees, num_rows="dynamic")
                if st.button("Save Changes"):
                    st.success("Fees updated (demo - no persistent storage)")
    
    with tab2:
        st.subheader("Employee Monthly Salaries")
        st.dataframe(employee_fees, use_container_width=True)
        total_employee_fees = employee_fees['annual_total'].sum()
        st.metric("Total Annual Employee Fees", f"${total_employee_fees:,.0f}")
        st.caption("Note: Employees also receive performance bonuses (not shown).")