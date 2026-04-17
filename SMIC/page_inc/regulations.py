import streamlit as st
import pandas as pd
from data.hardcoded_data import internal_regulations, external_regulations

def show():
    st.header("📜 Internal & External Regulations")
    
    tab1, tab2 = st.tabs(["Internal Regulations", "External Regulations"])
    
    with tab1:
        st.subheader("Consortium Policies & Charters")
        df_internal = pd.DataFrame(internal_regulations)
        st.dataframe(df_internal, use_container_width=True)
        for reg in internal_regulations:
            st.markdown(f"- **{reg['title']}** v{reg['version']} (effective {reg['effective_date']}) - [View](#)")
    
    with tab2:
        st.subheader("Legal & Regulatory Framework")
        df_external = pd.DataFrame(external_regulations)
        st.dataframe(df_external, use_container_width=True)
        for reg in external_regulations:
            st.markdown(f"- **{reg['title']}** ({reg['authority']}) - [Access](#)")
    
    st.info("In a production system, documents would be stored as PDFs with version control and access logging.")