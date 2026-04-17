import streamlit as st
import pandas as pd
import plotly.express as px
from data.hardcoded_data import investments

# Initialize reports in session state - MUST be first thing
if 'reports' not in st.session_state:
    from data.hardcoded_data import reports as initial_reports
    st.session_state.reports = initial_reports.copy()

# Try to load FinBERT, fallback to mock if fails
FINBERT_AVAILABLE = False
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    FINBERT_AVAILABLE = True
except ImportError:
    pass

def analyze_sentiment(text):
    if not FINBERT_AVAILABLE:
        return "neutral", 0.70
    
    try:
        tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment = ["negative", "neutral", "positive"][torch.argmax(probs).item()]
        confidence = probs.max().item()
        return sentiment, confidence
    except Exception as e:
        return "neutral", 0.70

def show():
    st.header("📊 Investment Reports & AI Analysis")
    role = st.session_state.role
    
    # Display existing reports
    st.subheader("📁 Report Library")
    if not st.session_state.reports.empty:
        st.dataframe(st.session_state.reports[['report_id', 'title', 'date', 'summary']], use_container_width=True, hide_index=True)
    else:
        st.info("No reports available. Click below to create one.")
    
    # AI Analysis section
    st.subheader("🤖 AI-Powered Sentiment Analysis (FinBERT)")
    if not FINBERT_AVAILABLE:
        st.info("💡 AI sentiment analysis will be available in the next update. Showing demo mode.")
    
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
            st.success("📈 Recommendation: Consider increasing position or maintaining exposure.")
        elif sentiment == "negative":
            st.warning("📉 Recommendation: Review position; consider hedging or reducing exposure.")
        else:
            st.info("ℹ️ Recommendation: Monitor closely; no immediate action required.")
    
    # AI Recommendations from existing reports
    st.subheader("📈 AI Investment Recommendations")
    if not st.session_state.reports.empty:
        latest_report = st.session_state.reports.iloc[-1]
        st.info(f"**From {latest_report['title']} ({latest_report['date']})**: {latest_report['ai_recommendation']}")
    else:
        st.info("No recommendations available. Create a report first.")
    
    # CRUD for reports (CEO only)
    if role == "CEO":
        st.subheader("✏️ Manage Reports (CRUD Demo)")
        
        with st.expander("➕ Add New Report"):
            col1, col2 = st.columns(2)
            with col1:
                new_title = st.text_input("Title")
                new_date = st.date_input("Date")
            with col2:
                new_summary = st.text_area("Summary", height=100)
                new_ai_rec = st.text_area("AI Recommendation", height=100)
            
            if st.button("Create Report"):
                if new_title and new_summary:
                    new_id = len(st.session_state.reports) + 1
                    new_row = pd.DataFrame({
                        'report_id': [new_id],
                        'title': [new_title],
                        'date': [str(new_date)],
                        'summary': [new_summary],
                        'ai_recommendation': [new_ai_rec]
                    })
                    st.session_state.reports = pd.concat([st.session_state.reports, new_row], ignore_index=True)
                    st.success("Report added successfully!")
                    st.rerun()
                else:
                    st.error("Please fill in at least Title and Summary.")
        
        with st.expander("✏️ Edit Existing Reports"):
            edited_reports = st.data_editor(st.session_state.reports, num_rows="dynamic", use_container_width=True)
            if st.button("Save Changes"):
                st.session_state.reports = edited_reports
                st.success("Reports updated successfully!")
                st.rerun()
