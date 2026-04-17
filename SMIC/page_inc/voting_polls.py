import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize polls in session state - MUST be first thing
if 'polls' not in st.session_state:
    from data.hardcoded_data import polls as initial_polls
    st.session_state.polls = initial_polls.copy()

def show():
    st.header("🗳️ Voting Polls & Elections")
    st.markdown("*AGM Electoral Committee - Live Voting Simulation*")
    role = st.session_state.role
    
    if not st.session_state.polls:
        st.info("No active polls available. Create one using the management section below.")
    
    for poll in st.session_state.polls:
        if poll['active']:
            st.subheader(f"📋 {poll['title']}")
            st.caption(poll['description'])
            st.write(f"*Created by: {poll['created_by']}*")
            
            choice = st.radio("Cast your vote:", poll['options'], key=f"vote_{poll['id']}")
            
            if st.button(f"Submit Vote for {poll['title']}", key=f"submit_{poll['id']}"):
                idx = poll['options'].index(choice)
                poll['votes'][idx] += 1
                st.success(f"Your vote for '{choice}' has been recorded. Thank you!")
                st.rerun()
            
            st.write("**Current Results:**")
            results_df = pd.DataFrame({'Option': poll['options'], 'Votes': poll['votes']})
            fig = px.bar(results_df, x='Option', y='Votes', title="Live Vote Tally",
                         color='Option', text='Votes',
                         color_discrete_sequence=['#0a2540', '#d4af37', '#2a4b7c'])
            fig.update_traces(textposition='outside')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("---")
    
    if role == "CEO":
        st.subheader("🔧 Committee Management (CRUD Demo)")
        
        with st.expander("➕ Create New Poll"):
            new_title = st.text_input("Poll Title")
            new_desc = st.text_area("Description")
            new_options = st.text_input("Options (comma separated)")
            
            if st.button("Create Poll"):
                if new_title and new_options:
                    opts = [o.strip() for o in new_options.split(',')]
                    new_poll = {
                        'id': len(st.session_state.polls) + 1,
                        'title': new_title,
                        'description': new_desc,
                        'options': opts,
                        'votes': [0] * len(opts),
                        'active': True,
                        'created_by': 'AGM Electoral Committee (Demo)'
                    }
                    st.session_state.polls.append(new_poll)
                    st.success("Poll created successfully!")
                    st.rerun()
                else:
                    st.error("Please provide both title and options.")
        
        with st.expander("✏️ Manage Existing Polls"):
            for idx, poll in enumerate(st.session_state.polls):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{poll['title']}**")
                with col2:
                    new_active = st.checkbox("Active", value=poll['active'], key=f"active_{idx}")
                    if new_active != poll['active']:
                        st.session_state.polls[idx]['active'] = new_active
                        st.rerun()
