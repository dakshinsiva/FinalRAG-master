import streamlit as st
from vision import SecurityQuestionnaire, process_rag_queries
from datetime import datetime

# Initialize session state for tracking verifications and feedback
if 'verifications' not in st.session_state:
    st.session_state.verifications = {}
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}

def display_ai_disclaimer():
    st.markdown("""
        <div style='background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            <h4 style='color: #1f2937; margin: 0;'>🤖 AI-Generated Responses - Human Verification Required</h4>
            <p style='color: #4b5563; margin: 0.5rem 0 0 0;'>
                All AI-generated responses must be verified by a human reviewer. 
                Please review each response carefully and indicate whether it is accurate and complete.
            </p>
        </div>
    """, unsafe_allow_html=True)

def save_verification(q_key: str, verification_data: dict):
    """Save verification data with timestamp and reviewer info"""
    st.session_state.verifications[q_key] = {
        **verification_data,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'reviewer': st.session_state.get('current_user', 'Unknown')
    }

def display_verification_status(q_key: str):
    """Display the verification status of a response"""
    if q_key in st.session_state.verifications:
        verification = st.session_state.verifications[q_key]
        status_color = {
            'Approved': 'green',
            'Needs Revision': 'red',
            'Pending Changes': 'orange'
        }.get(verification['status'], 'gray')
        
        st.markdown(f"""
            <div style='background-color: {status_color}15; padding: 0.5rem; border-radius: 0.5rem; margin: 0.5rem 0;'>
                <p style='color: {status_color}; margin: 0;'>
                    ✓ Verified by: {verification['reviewer']} <br>
                    📅 Date: {verification['timestamp']} <br>
                    📋 Status: {verification['status']}
                </p>
            </div>
        """, unsafe_allow_html=True)

def question_response_block(section: str, q_key: str, question: str):
    """Display a question with its response and verification controls"""
    with st.expander(f"Q: {question}", expanded=True):
        # AI Response Section
        st.markdown("### 🤖 AI-Generated Response")
        # Placeholder for answer display
        st.text_area("Answer", value="", key=f"answer_{q_key}")
        # Add feedback options
        st.radio("Rate the answer quality:", ["Excellent", "Good", "Needs Improvement"], key=f"rating_{q_key}")

# Load questionnaire
questionnaire = SecurityQuestionnaire()

# Create tabs for each section
section_tabs = st.tabs([questionnaire.get_section_name(section) for section in questionnaire.questions.keys()])

# Iterate over sections and display questions in tabs
for i, section in enumerate(questionnaire.questions.keys()):
    with section_tabs[i]:
        st.header(questionnaire.get_section_name(section))
        for q_key, question in questionnaire.questions[section].items():
            question_response_block(section, q_key, question)

# Add a button to process all questions
if st.button("Process All Questions"):
    results = process_rag_queries(questionnaire)
    st.session_state.results = results
    st.success("Processing complete!")

# Display results if available
if 'results' in st.session_state:
    st.write(st.session_state.results) 