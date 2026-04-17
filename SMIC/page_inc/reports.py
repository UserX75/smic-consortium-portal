import streamlit as st
import pandas as pd
import plotly.express as px
from data.hardcoded_data import investments
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Initialize reports in session state
if 'reports' not in st.session_state:
    from data.hardcoded_data import reports as initial_reports
    st.session_state.reports = initial_reports.copy()

@st.cache_resource
def load_finbert():
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    return tokenizer, model

def analyze_sentiment(text):
    tokenizer, model = load_finbert()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment = ["negative", "neutral", "positive"][torch.argmax(probs).item()]
    confidence = probs.max().item()
    return sentiment, confidence

def show():
    st.header("📊 Investment Reports & AI Analysis")
    role = st.session_state.role
    
    st.subheader("📁 Report Library")
    st.dataframe(st.session_state.reports[['report_id', 'title', 'date', 'summary']], use_container_width=True)
    
    st.subheader("🤖 AI-Powered Sentiment Analysis (FinBERT)")
    sample_news = [
        "Vodacom Lesotho reports strong subscriber growth and 5G rollout",
        "Sekhametsi Property Company acquires new prime land in Maseru",
        "Letshego Financial Services faces regulatory scrutiny over loan practices"
    ]
    selected_news = st.selectbox("Select a news headline to analyze:", sample_news)
    if st.button("Analyze Sentiment"):
        sentiment, confidence = analyze_sentiment(selected_news)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sentiment", sentiment.capitalize())
        with col2:
            st.metric("Confidence", f"{confidence:.2%}")
        if sentiment == "positive":
            st.success("Recommendation: Consider increasing position or maintaining exposure.")
        elif sentiment == "negative":
            st.warning("Recommendation: Review position; consider hedging or reducing exposure.")
        else:
            st.info("Recommendation: Monitor closely; no immediate action required.")
    
    st.subheader("📈 AI Investment Recommendations (from latest reports)")
    if not st.session_state.reports.empty:
        latest_report = st.session_state.reports.iloc[-1]
        st.info(f"**From {latest_report['title']} ({latest_report['date']})**: {latest_report['ai_recommendation']}")
    
    if role == "CEO":
        st.subheader("✏️ Manage Reports (CRUD Demo)")
        with st.expander("Add New Report"):
            new_title = st.text_input("Title")
            new_date = st.date_input("Date")
            new_summary = st.text_area("Summary")
            new_ai_rec = st.text_area("AI Recommendation")
            if st.button("Create Report"):
                new_id = len(st.session_state.reports) + 1
                new_row = pd.DataFrame({
                    'report_id': [new_id],
                    'title': [new_title],
                    'date': [str(new_date)],
                    'summary': [new_summary],
                    'ai_recommendation': [new_ai_rec]
                })
                st.session_state.reports = pd.concat([st.session_state.reports, new_row], ignore_index=True)
                st.success("Report added!")
                st.rerun()
        
        edited_reports = st.data_editor(st.session_state.reports, num_rows="dynamic")
        if st.button("Save Report Changes"):
            st.session_state.reports = edited_reports
            st.success("Reports updated")
            st.rerun()