import streamlit as st
from datetime import datetime
import pandas as pd
import json

class EvaluationApp:
    def __init__(self):
        self.ratings = {
            "IDEAL": "✅ Complete and detailed response",
            "GOOD": "🟡 Adequate but could be improved",
            "BAD": "❌ Incomplete or inadequate response"
        }
        # Initialize session state for storing evaluations
        if 'evaluations' not in st.session_state:
            st.session_state.evaluations = {}

    def run(self):
        st.title("Response Evaluation System")
        
        # File uploader for responses
        uploaded_file = st.file_uploader("Upload responses JSON file", type=['json'])
        if uploaded_file:
            responses = json.load(uploaded_file)
            self.display_evaluations(responses)

        # Export button
        if st.session_state.evaluations:
            if st.button("Export Evaluations"):
                self.export_evaluations()

    def display_evaluations(self, responses):
        """Display each response with evaluation options"""
        for idx, response in enumerate(responses):
            with st.expander(f"Response #{idx + 1}", expanded=True):
                # Display response content
                st.subheader("Response:")
                st.write(response['content'])
                
                # Rating buttons
                st.subheader("Evaluation:")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✅ IDEAL", key=f"ideal_{idx}"):
                        self.save_evaluation(idx, "IDEAL")
                with col2:
                    if st.button("🟡 GOOD", key=f"good_{idx}"):
                        self.save_evaluation(idx, "GOOD")
                with col3:
                    if st.button("❌ BAD", key=f"bad_{idx}"):
                        self.save_evaluation(idx, "BAD")

                # Comments section
                comment = st.text_area(
                    "Additional Comments:",
                    value=st.session_state.evaluations.get(idx, {}).get('comment', ''),
                    key=f"comment_{idx}"
                )
                
                # Save comment
                if comment:
                    self.save_evaluation(idx, 
                                      st.session_state.evaluations.get(idx, {}).get('rating'),
                                      comment)

                # Display current evaluation if it exists
                if idx in st.session_state.evaluations:
                    st.info(f"Current Rating: {st.session_state.evaluations[idx]['rating']}")

    def save_evaluation(self, idx, rating=None, comment=None):
        """Save or update evaluation in session state"""
        if idx not in st.session_state.evaluations:
            st.session_state.evaluations[idx] = {}
        
        if rating:
            st.session_state.evaluations[idx]['rating'] = rating
        if comment:
            st.session_state.evaluations[idx]['comment'] = comment
        
        st.session_state.evaluations[idx]['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def export_evaluations(self):
        """Export evaluations to CSV"""
        df = pd.DataFrame.from_dict(st.session_state.evaluations, orient='index')
        csv = df.to_csv().encode('utf-8')
        
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"evaluations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime='text/csv'
        )

if __name__ == "__main__":
    app = EvaluationApp()
    app.run() 