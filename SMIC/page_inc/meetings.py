import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    st.header("🗓️ Meetings & Attendance")
    role = st.session_state.role
    
    meetings = pd.DataFrame({
        'date': [datetime(2025, 4, 15), datetime(2025, 5, 20), datetime(2025, 6, 10)],
        'title': ['Quarterly Investment Review', 'Deal Approval: AI Ventures', 'Risk Committee'],
        'type': ['All Members', 'Board + CEO', 'Risk Team'],
        'online_link': [
            'https://meet.google.com/smic-q1-2025',
            'https://zoom.us/j/123456789',
            'https://teams.microsoft.com/l/meetup-join/abc123'
        ],
        'in_person_location': ['SMIC HQ - Boardroom', 'SMIC HQ - Conference A', 'Virtual Only']
    })
    
    st.subheader("📅 Upcoming Meetings")
    
    for idx, meeting in meetings.iterrows():
        with st.expander(f"{meeting['date'].strftime('%b %d, %Y')} - {meeting['title']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Type:** {meeting['type']}")
                st.markdown(f"**In-person location:** {meeting['in_person_location']}")
            with col2:
                st.markdown(f"**Online link:** [Click to join]({meeting['online_link']})")
                # Enhancement #6: Email reminder link
                st.markdown(f'<a href="mailto:?subject=Reminder: {meeting["title"]}&body=Join online: {meeting["online_link"]}" target="_blank">📧 Email Reminder</a>', unsafe_allow_html=True)
            
            st.markdown("**Your attendance:**")
            attendance = st.radio(
                "Will you attend?",
                ["Attend in person", "Attend online", "Cannot attend"],
                key=f"rsvp_{idx}",
                horizontal=True
            )
            if attendance == "Attend online":
                st.success(f"Great! Use this link to join: {meeting['online_link']}")
            elif attendance == "Attend in person":
                st.info(f"See you at {meeting['in_person_location']}")
            else:
                st.warning("Meeting minutes will be shared after the session.")
    
    st.markdown("---")
    st.subheader("📜 Past Meetings & Recordings")
    past_meetings = pd.DataFrame({
        'date': ['Jan 19, 2026', 'March 5, 2026'],
        'title': ['Annual General Meeting', 'Budget Approval'],
        'recording': ['https://drive.google.com/file/d/abc', 'https://drive.google.com/file/d/xyz']
    })
    for _, meeting in past_meetings.iterrows():
        st.markdown(f"**{meeting['date']}** - {meeting['title']} - [Watch Recording]({meeting['recording']})")
    
    if role == "CEO" or role == "Board Member":
        st.markdown("---")
        st.subheader("📊 Attendance Analytics (Demo)")
        attendance_data = pd.DataFrame({
            'Member': ['Up In The L Inc', 'AXE Capital', 'Ralejoe Consultancy'],
            'Meetings Attended (last 4)': [4, 3, 2],
            'Online Attendance %': [25, 67, 100]
        })
        st.dataframe(attendance_data, use_container_width=True)
        st.caption("In a real system, this would track actual attendance and send reminders.")