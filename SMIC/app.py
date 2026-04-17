import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime

st.set_page_config(
    page_title="Sekhametsi Investment Consortium",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== FONT AWESOME + CUSTOM CSS ==========
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
    /* SMIC Brand Colors */
    :root {
        --smic-blue: #0a2540;
        --smic-gold: #d4af37;
        --smic-light-blue: #2a4b7c;
        --smic-dark-blue: #051a2c;
        --smic-gray: #f5f7fa;
    }
    
    /* Global */
    .stApp {
        background-color: var(--smic-gray);
    }
    
    /* Headers */
    .stApp h1 {
        color: var(--smic-blue);
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .stApp h2 {
        color: var(--smic-blue);
        font-size: 1.5rem;
        font-weight: 500;
        border-left: 4px solid var(--smic-gold);
        padding-left: 1rem;
        margin: 1rem 0;
    }
    .stApp h3 {
        color: var(--smic-light-blue);
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-left: 4px solid var(--smic-gold);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .metric-label {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--smic-blue);
    }
    .metric-delta {
        font-size: 0.8rem;
        color: var(--smic-gold);
    }
    
    /* Sidebar - FIXED TEXT COLORS */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--smic-dark-blue) 0%, var(--smic-blue) 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;  /* Light gray for all text */
    }
    [data-testid="stSidebar"] .stSelectbox label {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] .stMarkdown {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: var(--smic-gold);
    }
    /* Sidebar navigation links - specifically */
    .nav-link {
        color: #e0e0e0 !important;
    }
    .nav-link span {
        color: #e0e0e0 !important;
    }
    /* Sidebar select box options */
    .stSelectbox [data-baseweb="select"] {
        background-color: rgba(255,255,255,0.1);
    }
    .stSelectbox [data-baseweb="select"] * {
        color: #e0e0e0 !important;
    }
    
    /* Buttons */
    .stButton button {
        background-color: var(--smic-blue);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    .stButton button:hover {
        background-color: var(--smic-gold);
        color: var(--smic-dark-blue);
        transform: translateY(-1px);
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: var(--smic-light-blue);
        color: white;
        border-radius: 8px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        color: var(--smic-blue);
        font-weight: 500;
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom-color: var(--smic-gold);
        border-bottom-width: 3px;
    }
    
    /* Info/Warning/Success */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid var(--smic-gold);
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background-color: var(--smic-gold) !important;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
        font-size: 0.75rem;
        color: #666;
    }
    
    /* Hide default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom card containers */
    .dashboard-card {
        background: white;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'role' not in st.session_state:
    st.session_state.role = "CEO"
if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Dashboard"

# ========== SIDEBAR ==========
with st.sidebar:
    # Brand
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <i class="fas fa-building" style="font-size: 2.5rem; color: #d4af37;"></i>
        <h2 style="color: #d4af37; margin: 0.5rem 0 0 0;">SEKHAMETSI</h2>
        <p style="color: white; font-size: 0.8rem; opacity: 0.8;">Investment Consortium</p>
        <hr style="border-color: #d4af37; margin: 1rem 0;">
    </div>
    """, unsafe_allow_html=True)
    
    # Role selector with icon
    st.markdown('<i class="fas fa-user-shield" style="color: #d4af37; margin-right: 8px;"></i> <span style="color: #e0e0e0;">Demo View As</span>', unsafe_allow_html=True)
    role = st.selectbox(
        "",
        ["CEO", "Board Member", "Accounts"],
        key="role_selector",
        label_visibility="collapsed"
    )
    st.session_state.role = role
    
    st.markdown("<hr style='border-color: #d4af37; margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # Navigation menu with Font Awesome icons
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "Deal Flow", "Performance", "Risk Analytics", "Member Portal", 
                 "Scenario Analyzer", "Meetings", "Committees", "Voting Polls", "Fees", 
                 "Regulations", "Reports"],
        icons=["chart-line", "briefcase", "graph-up", "exclamation-triangle", "people",
               "magic", "calendar-check", "building", "ballot-check", "cash-stack",
               "file-contract", "file-alt"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0", "background": "transparent"},
            "icon": {"color": "#d4af37", "font-size": "1.1rem"},
            "nav-link": {"color": "white", "font-size": "0.9rem", "margin": "0.2rem 0"},
            "nav-link-selected": {"background-color": "#d4af37", "color": "#051a2c"},
        }
    )
    
    st.markdown("<hr style='border-color: #d4af37; margin: 1rem 0;'>", unsafe_allow_html=True)
    
    # Export button - fixed to show icon properly
if st.button("📥 Export Data", key="export_btn"):
    from data.hardcoded_data import investments, active_deals, members, capital_calls, shareholders, board_members
    import pandas as pd
    with pd.ExcelWriter('smic_export.xlsx') as writer:
        investments.to_excel(writer, sheet_name='Investments', index=False)
        active_deals.to_excel(writer, sheet_name='Deals', index=False)
        members.to_excel(writer, sheet_name='Members', index=False)
        shareholders.to_excel(writer, sheet_name='Shareholders', index=False)
        board_members.to_excel(writer, sheet_name='Board', index=False)
    with open('smic_export.xlsx', 'rb') as f:
        st.download_button("📥 Download Excel", f, file_name='smic_export.xlsx')
        
    st.caption(f"<i class='far fa-clock'></i> Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", unsafe_allow_html=True)

# ========== MAIN HEADER ==========
col_title, col_icon = st.columns([4, 1])
with col_title:
    st.markdown(f'<h1><i class="fas fa-chart-line" style="color: #d4af37; margin-right: 12px;"></i>Sekhametsi Investment Consortium</h1>', unsafe_allow_html=True)
    st.caption(f'<i class="fas fa-eye"></i> Viewing as: <strong>{st.session_state.role}</strong>', unsafe_allow_html=True)
with col_icon:
    st.markdown('<div style="text-align: right;"><i class="fas fa-chart-pie" style="font-size: 3rem; color: #d4af37; opacity: 0.5;"></i></div>', unsafe_allow_html=True)

st.markdown("---")

# ========== PAGE ROUTING ==========
from page_inc import (dashboard, deal_flow, performance, risk_analytics, member_portal, 
                      scenario_analyzer, meetings, committees, voting_polls, fees, 
                      regulations, reports)

if selected == "Dashboard":
    dashboard.show()
elif selected == "Deal Flow":
    deal_flow.show()
elif selected == "Performance":
    performance.show()
elif selected == "Risk Analytics":
    risk_analytics.show()
elif selected == "Member Portal":
    member_portal.show()
elif selected == "Scenario Analyzer":
    scenario_analyzer.show()
elif selected == "Meetings":
    meetings.show()
elif selected == "Committees":
    committees.show()
elif selected == "Voting Polls":
    voting_polls.show()
elif selected == "Fees":
    fees.show()
elif selected == "Regulations":
    regulations.show()
elif selected == "Reports":
    reports.show()

# Footer
st.markdown("""
<div class="footer">
    <i class="fas fa-shield-alt"></i> Sekhametsi Investment Consortium | Confidential & Proprietary | Data as of March 01, 2026
</div>
""", unsafe_allow_html=True)