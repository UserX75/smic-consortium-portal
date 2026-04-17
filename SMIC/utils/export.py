import streamlit as st
import pandas as pd
from io import BytesIO
import base64
from fpdf import FPDF
from datetime import datetime

def to_excel_download(df, filename="data.xlsx"):
    """Convert dataframe to Excel download link"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel</a>'
    return href

def generate_pdf_report(title, dataframes_dict):
    """Generate simple PDF report from dataframes"""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=title, ln=1, align='C')
    pdf.ln(10)
    
    for name, df in dataframes_dict.items():
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(200, 10, txt=name, ln=1)
        pdf.set_font("Arial", size=8)
        # Convert dataframe to string table
        col_width = pdf.w / (len(df.columns) + 1)
        # Headers
        for col in df.columns:
            pdf.cell(col_width, 10, str(col), border=1)
        pdf.ln()
        # Rows
        for i in range(min(len(df), 20)):  # limit rows
            for col in df.columns:
                pdf.cell(col_width, 10, str(df.iloc[i][col])[:20], border=1)
            pdf.ln()
        pdf.ln(10)
    
    return pdf.output(dest='S').encode('latin-1')

def add_export_buttons(data_context):
    """Add export buttons in sidebar or wherever called"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("📎 Export Data")
    
    # Excel export for current view
    if st.sidebar.button("Export Current Table to Excel"):
        if data_context is not None and isinstance(data_context, pd.DataFrame):
            href = to_excel_download(data_context, f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
            st.sidebar.markdown(href, unsafe_allow_html=True)
        else:
            st.sidebar.warning("No table data to export")
    
    # PDF export placeholder - we'll generate a report combining key metrics
    if st.sidebar.button("Generate PDF Report"):
        # Collect key data from session state or global
        from data.hardcoded_data import holdings, active_deals, members
        pdf_data = {
            "Portfolio Holdings": holdings,
            "Active Deals": active_deals,
            "Member Commitments": members
        }
        pdf_bytes = generate_pdf_report("SMIC Investment Report", pdf_data)
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        href_pdf = f'<a href="data:application/pdf;base64,{b64_pdf}" download="smic_report.pdf">Download PDF Report</a>'
        st.sidebar.markdown(href_pdf, unsafe_allow_html=True)