import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ========== INVESTMENT STRUCTURE (Equity ownership %) ==========
investments = pd.DataFrame({
    'entity': [
        'Letshego Financial Services',
        'Vodacom Lesotho Pty',
        'Sekhametsi Property Company',
        'Stanlib Lesotho',
        'Afri-Expo Textiles',
        'Moruo Development',
        'Sekhametsi Place'
    ],
    'ownership_pct': [4.0, 20.0, 71.0, 25.1, 30.0, 10.0, 100.0],
    'sector': ['Financial Services', 'Telecommunications', 'Real Estate', 
               'Asset Management', 'Manufacturing', 'Development', 'Real Estate'],
    'valuation_usd_m': [12.5, 45.0, 28.3, 18.2, 8.0, 6.5, 15.0],
    'last_dividend_usd_m': [0.5, 2.2, 1.1, 0.8, 0.3, 0.2, 0.6],
    'irr_estimate': [8.5, 12.0, 15.2, 9.8, 11.5, 7.2, 14.0]
})

# ========== SHAREHOLDERS (Individual & Institutional) ==========
shareholders = pd.DataFrame({
    'name': [
        'Sekhametsi Holdings (Pty) Ltd',
        'Thabo Lejone',
        'Lesotho National Development Corporation',
        'Teboho Family Trust',
        'Letsie Capital Partners',
        'Employee Share Trust'
    ],
    'type': ['Institution', 'Individual', 'Institution', 'Trust', 'Institution', 'Trust'],
    'shares_pct': [40.0, 15.0, 12.5, 10.0, 12.5, 10.0],
    'board_seat': [True, True, True, False, False, False],
    'since_year': [2018, 2018, 2019, 2020, 2021, 2022]
})

# ========== BOARD OF DIRECTORS ==========
board_members = pd.DataFrame({
    'name': [
        'Mr. John Letsie',
        'Ms. Teboho Masiu',
        'Dr. Thabo Mbeki',
        'Mrs. Nthabiseng Ntsane',
        'Mr. Lerato Molapo'
    ],
    'position': ['Chairperson', 'CEO', 'Independent Director', 'Finance Director', 'Shareholder Rep'],
    'committee_memberships': [
        'Directors Affairs, Investment',
        'Directors Affairs, Investment, VDI Adhoc',
        'Audit and Risk, Investment',
        'Audit and Risk',
        'AGM Electoral'
    ],
    'term_start': ['2023-01-01', '2023-01-01', '2024-01-01', '2023-06-01', '2024-01-01'],
    'term_end': ['2025-12-31', '2025-12-31', '2026-12-31', '2025-12-31', '2025-12-31']
})

# ========== COMMITTEES & MEMBERS ==========
committees = {
    'Directors Affairs Committee': ['Mr. John Letsie', 'Mr. Teboho Masiu'],
    'Audit and Risk Committee': ['Dr. Thabo Mbeki', 'Mrs. Nthabiseng Ntsane'],
    'Investment Committee': ['Mr. Teboho Masiu', 'Dr. Thabo Mbeki'],
    'VDI Adhoc Committee': ['Mr. Teboho Masiu'],
    'AGM Electoral Committee': ['Mr. Lerato Molapo']
}

# ========== DIRECTOR FEES (Quarterly) ==========
director_fees = pd.DataFrame({
    'director': board_members['name'],
    'quarterly_amount_usd': [5000, 7500, 4000, 4500, 3500],
    'annual_total': [20000, 30000, 16000, 18000, 14000]
})
# Payment schedule (hardcoded for 2025)
fee_payment_dates = pd.DataFrame({
    'quarter': ['Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025'],
    'payment_date': ['2025-03-31', '2025-06-30', '2025-09-30', '2025-12-31'],
    'status': ['Paid', 'Upcoming', 'Upcoming', 'Upcoming']
})

# ========== EMPLOYEE FEES (Monthly - sample) ==========
employee_fees = pd.DataFrame({
    'employee': ['Financial Manager', 'Investment Analyst', 'Compliance Officer', 'Admin Assistant'],
    'monthly_salary_usd': [3000, 2500, 2800, 1500],
    'annual_total': [36000, 30000, 33600, 18000]
})

# ========== INTERNAL & EXTERNAL REGULATIONS ==========
internal_regulations = [
    {'title': 'Consortium Charter', 'version': '3.2', 'effective_date': '2024-01-01', 'link': '#internal1'},
    {'title': 'Code of Conduct', 'version': '2.0', 'effective_date': '2023-06-01', 'link': '#internal2'},
    {'title': 'Investment Policy Statement', 'version': '5.1', 'effective_date': '2024-02-15', 'link': '#internal3'},
    {'title': 'Conflict of Interest Policy', 'version': '1.5', 'effective_date': '2023-09-01', 'link': '#internal4'},
]

external_regulations = [
    {'title': 'Lesotho Companies Act 2011', 'authority': 'Government of Lesotho', 'link': '#external1'},
    {'title': 'Financial Institutions Act 2012', 'authority': 'Central Bank of Lesotho', 'link': '#external2'},
    {'title': 'Income Tax Act 1993 (as amended)', 'authority': 'Lesotho Revenue Authority', 'link': '#external3'},
    {'title': 'FIA Anti-Money Laundering Rules', 'authority': 'FIA Lesotho', 'link': '#external4'},
]

# ========== INVESTMENT REPORTS (CRUD simulation) ==========
reports = pd.DataFrame({
    'report_id': [1, 2, 3],
    'title': ['Q4 2024 Portfolio Review', 'Annual Report 2024', 'Investment Strategy 2025'],
    'date': ['2025-01-15', '2025-02-28', '2025-03-10'],
    'summary': [
        'Strong performance in real estate assets. IRR exceeded targets.',
        'Record dividends declared. New investments in fintech.',
        'Focus on ESG and diversification into renewable energy.'
    ],
    'ai_recommendation': [
        'Increase exposure to Sekhametsi Property Company (currently 71%, consider adding value-add developments).',
        'Reduce Vodacom stake to 15% and reallocate to infrastructure.',
        'Explore cross-border opportunities in SADC region.'
    ]
})

# ========== VOTING POLLS (for live simulation) ==========
polls = [
    {
        'id': 1,
        'title': 'Election of Board Chairperson 2025',
        'description': 'Nominees: John Letsie (incumbent), Teboho Masiu',
        'options': ['John Letsie', 'Teboho Masiu', 'Abstain'],
        'votes': [0, 0, 0],
        'active': True,
        'created_by': 'AGM Electoral Committee'
    },
    {
        'id': 2,
        'title': 'Approve 2025 Budget',
        'description': 'Proposed budget of $2.5M for operations and new investments.',
        'options': ['Approve', 'Reject', 'Abstain'],
        'votes': [0, 0, 0],
        'active': True,
        'created_by': 'Board of Directors'
    }
]

# ========== PORTFOLIO HOLDINGS (legacy, keep for dashboard) ==========
# We'll use investments as the primary holdings now
holdings = investments.rename(columns={'entity': 'asset', 'ownership_pct': 'return_pct'})
holdings['value'] = holdings['valuation_usd_m'] * 1e6
holdings['irr'] = holdings['irr_estimate']

# Sector allocation from investments
sector_allocation = investments.groupby('sector')['valuation_usd_m'].sum().reset_index()
sector_allocation.columns = ['sector', 'allocation']

# Risk metrics (same as before)
risk_metrics = {
    'sharpe_ratio': 1.42,
    'sortino_ratio': 1.85,
    'max_drawdown': -8.3,
    'var_95': -2.1,
    'cvar_95': -3.4,
    'beta': 1.15,
    'alpha': 4.2
}

# NAV history (simulate based on total valuation)
nav_history = pd.DataFrame({
    'date': pd.date_range(start='2023-01-01', periods=24, freq='M'),
    'nav': investments['valuation_usd_m'].sum() * 1e6 * (1 + np.cumsum(np.random.normal(0.01, 0.02, 24)) / 100)
})

# Monthly returns (keep for performance)
monthly_returns = pd.DataFrame({
    'date': pd.date_range(start='2024-01-01', periods=12, freq='M'),
    'portfolio_return': np.random.uniform(-1, 3, 12),
    'benchmark_return': np.random.uniform(-0.5, 2, 12)
})

# Active deals (same as before)
active_deals = pd.DataFrame({
    'deal': ['SolarGrid Inc', 'Quantum Computing Lab', 'Logistics AI Platform', 'Vertical Farming Co', 
             'Carbon Capture Fund', 'Fintech Lending Platform'],
    'stage': ['Due Diligence', 'Negotiation', 'Pre-screen', 'Due Diligence', 'Closing', 'Pre-screen'],
    'size_mm': [15, 22, 8, 12, 30, 10],
    'expected_irr': [28, 45, 22, 18, 25, 32],
    'industry': ['Energy', 'Tech', 'Tech', 'Agriculture', 'Energy', 'Fintech']
})

# Members (original consortium members)
members = pd.DataFrame({
    'name': ['Up In The L Inc', 'Beta Capital', 'Gamma Family Office', 'Delta Pension Fund', 'Epsilon Endowment'],
    'committed_mm': [75, 60, 45, 40, 30],
    'allocated_mm': [62, 58, 38, 35, 28],
    'returns_mm': [14.5, 12.3, 8.1, 7.2, 5.6]
})

# Capital calls (for accounts view)
capital_calls = pd.DataFrame({
    'date': pd.date_range(start='2024-01-01', periods=6, freq='M'),
    'amount_mm': [5.2, 3.8, 6.1, 4.5, 7.0, 2.9],
    'called_from': ['Up In The L Inc', 'Beta Capital', 'Gamma Family Office', 'Delta Pension Fund', 
                    'Up In The L Inc', 'Epsilon Endowment']
})