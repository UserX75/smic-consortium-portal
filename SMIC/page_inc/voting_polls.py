import streamlit as st
import pandas as pd
import plotly.express as px

# Force initialization at module level
def _init_session_state():
    """Initialize session state for polls - called at module load"""
    if 'polls' not in st.session_state:
        from data.hardcoded_data import polls as initial_polls
        st.session_state.polls = initial_polls.copy()

# Call initialization immediately when module loads
_init_session_state()

def show():
    """Main show function for Voting Polls page"""
    # Re-initialize to be safe
    if 'polls' not in st.session_state:
        from data.hardcoded_data import polls as initial_polls
        st.session_state.polls = initial_polls.copy()
    
    st.header("🗳️ Voting Polls & Elections")
    st.markdown("*AGM Electoral Committee - Live Voting Simulation*")
    role = st.session_state.role
    
    if not st.session_state.polls or len(st.session_state.polls) == 0:
        st.info("No active polls available. Use the management section below to create one.")
    
    # Display active polls
    active_polls_found = False
    for poll in st.session_state.polls:
        if poll.get('active', False):
            active_polls_found = True
            st.subheader(f"📋 {poll['title']}")
            st.caption(poll.get('description', 'No description provided.'))
            st.write(f"*Created by: {poll.get('created_by', 'Unknown')}*")
            
            choice = st.radio("Cast your vote:", poll['options'], key=f"vote_{poll['id']}")
            
            if st.button(f"✅ Submit Vote for {poll['title']}", key=f"submit_{poll['id']}"):
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
    
    if not active_polls_found:
        st.info("No active polls at this time. Check back later or create a new poll below.")
    
    # Management section for CEO
    if role == "CEO":
        st.subheader("🔧 Poll Management")
        
        with st.expander("➕ Create New Poll", expanded=False):
            new_title = st.text_input("Poll Title")
            new_desc = st.text_area("Description")
            new_options = st.text_input("Options (comma separated)")
            
            if st.button("Create Poll", key="create_poll_btn"):
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
        
        with st.expander("✏️ Manage Existing Polls", expanded=False):
            for idx, poll in enumerate(st.session_state.polls):
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"**{poll['title']}**")
                with col2:
                    new_active = st.checkbox("Active", value=poll.get('active', False), key=f"active_{idx}")
                    if new_active != poll.get('active', False):
                        st.session_state.polls[idx]['active'] = new_active
                        st.rerun()
                with col3:
                    if st.button("🗑️ Delete", key=f"delete_{idx}"):
                        st.session_state.polls.pop(idx)
                        st.rerun()
