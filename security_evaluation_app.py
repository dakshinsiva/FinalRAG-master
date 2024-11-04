import streamlit as st
from datetime import datetime
import pandas as pd
import re

class SecurityEvaluationApp:
    def __init__(self):
        self.ratings = {
            "IDEAL": "✅ Complete and accurate",
            "GOOD": "🟡 Needs minor improvements",
            "BAD": "❌ Needs major revision"
        }
        # Initialize session state
        if 'evaluations' not in st.session_state:
            st.session_state.evaluations = {}
        if 'current_responses' not in st.session_state:
            st.session_state.current_responses = None

    def parse_qa_pairs(self, content):
        """Parse Q&A pairs from the text content"""
        sections = content.split("________________________________________________________________________________")
        qa_pairs = []
        
        for section in sections:
            if "📝 Question:" in section and "🔍 Answer:" in section:
                question = re.search(r"📝 Question:\s*(.*?)\s*\n", section, re.DOTALL)
                answer = re.search(r"🔍 Answer:\s*(.*?)\s*\n📚", section, re.DOTALL)
                sources = re.findall(r"• (.*?)\n", section)
                
                if question and answer:
                    qa_pairs.append({
                        'question': question.group(1).strip(),
                        'answer': answer.group(1).strip(),
                        'sources': sources
                    })
        
        return qa_pairs

    def run(self):
        st.title("Security Questionnaire Response Evaluation")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload security questionnaire responses", type=['txt'])
        if uploaded_file:
            content = uploaded_file.getvalue().decode("utf-8")
            qa_pairs = self.parse_qa_pairs(content)
            st.session_state.current_responses = qa_pairs
            self.display_evaluations(qa_pairs)

        # Export button
        if st.session_state.evaluations:
            if st.button("Export Evaluations"):
                self.export_evaluations()

    def display_evaluations(self, qa_pairs):
        """Display each Q&A pair with evaluation options"""
        for idx, qa in enumerate(qa_pairs):
            with st.expander(f"Q{idx + 1}: {qa['question']}", expanded=False):
                # Display question and answer
                st.markdown("**Answer:**")
                st.write(qa['answer'])
                
                # Display sources
                if qa['sources']:
                    st.markdown("**Sources:**")
                    for source in qa['sources']:
                        st.write(f"• {source}")
                
                # Rating buttons
                st.markdown("**Evaluation:**")
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
                    "Improvement Notes:",
                    value=st.session_state.evaluations.get(idx, {}).get('comment', ''),
                    key=f"comment_{idx}"
                )
                
                if comment:
                    self.save_evaluation(idx, 
                                      st.session_state.evaluations.get(idx, {}).get('rating'),
                                      comment)

                # Display current evaluation
                if idx in st.session_state.evaluations:
                    st.info(f"Current Rating: {st.session_state.evaluations[idx]['rating']}")

    def save_evaluation(self, idx, rating=None, comment=None):
        """Save evaluation in session state"""
        if idx not in st.session_state.evaluations:
            st.session_state.evaluations[idx] = {}
        
        if rating:
            st.session_state.evaluations[idx]['rating'] = rating
        if comment:
            st.session_state.evaluations[idx]['comment'] = comment
            
        st.session_state.evaluations[idx]['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add question and answer to evaluation
        if st.session_state.current_responses:
            qa = st.session_state.current_responses[idx]
            st.session_state.evaluations[idx]['question'] = qa['question']
            st.session_state.evaluations[idx]['answer'] = qa['answer']

    def export_evaluations(self):
        """Export evaluations to CSV"""
        df = pd.DataFrame.from_dict(st.session_state.evaluations, orient='index')
        csv = df.to_csv().encode('utf-8')
        
        st.download_button(
            label="Download Evaluation Report",
            data=csv,
            file_name=f"security_qa_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime='text/csv'
        )

if __name__ == "__main__":
    app = SecurityEvaluationApp()
    app.run() 