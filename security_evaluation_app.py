import streamlit as st
from datetime import datetime
import pandas as pd
import re
import json
import os

class SecurityEvaluationApp:
    def __init__(self):
        self.ratings = {
            "IDEAL": "✅ Complete and accurate",
            "GOOD": "🟡 Needs minor improvements",
            "BAD": "❌ Needs major revision"
        }
        # Initialize session state
        if 'evaluations' not in st.session_state:
            # Try to load existing evaluations from file
            self.load_saved_evaluations()
        if 'current_responses' not in st.session_state:
            st.session_state.current_responses = None
        # Initialize criteria session state
        if 'evaluation_criteria' not in st.session_state:
            self.load_evaluation_criteria()

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
        
        # Add test buttons
        if st.button("Test: Check Stored Data"):
            self.check_stored_data()
        
        if st.button("Test: Clear All Data"):
            st.session_state.evaluation_criteria = {}
            st.session_state.evaluations = {}
            if os.path.exists('./.streamlit/evaluation_criteria.json'):
                os.remove('./.streamlit/evaluation_criteria.json')
            if os.path.exists('./.streamlit/evaluations.json'):
                os.remove('./.streamlit/evaluations.json')
            st.success("All data cleared!")
        
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
        st.markdown("""
            <style>
            .question-box {
                background-color: #262730;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                border-left: 5px solid #ff4b4b;
            }
            .question-text {
                font-size: 18px;
                color: #ffffff;
                font-weight: 500;
                margin-bottom: 15px;
            }
            .answer-box {
                background-color: #1E1E1E;
                border-radius: 8px;
                padding: 15px;
                margin: 10px 0;
            }
            .answer-label {
                color: #4CAF50;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .evaluation-section {
                background-color: #0E1117;
                border-radius: 8px;
                padding: 15px;
                margin-top: 15px;
            }
            .keyboard-hint {
                color: #8B8B8B;
                font-size: 14px;
                font-style: italic;
                margin: 10px 0;
                padding: 5px;
                background-color: #1E1E1E;
                border-radius: 5px;
            }
            </style>
        """, unsafe_allow_html=True)

        for idx, qa in enumerate(qa_pairs):
            # Question Box
            st.markdown(f"""
                <div class="question-box">
                    <div class="question-text">Q{idx + 1}: {qa['question']}</div>
                </div>
            """, unsafe_allow_html=True)

            # Answer Box
            st.markdown("""
                <div class="answer-box">
                    <div class="answer-label">Answer:</div>
                </div>
            """, unsafe_allow_html=True)
            st.write(qa['answer'])

            # Sources (if any)
            if qa['sources']:
                with st.expander("📚 View Sources"):
                    for source in qa['sources']:
                        st.write(f"• {source}")

            # Evaluation Section
            st.markdown('<div class="evaluation-section">', unsafe_allow_html=True)
            
            # Keyboard shortcuts hint
            st.markdown("""
                <div class="keyboard-hint">
                    ⌨️ Keyboard shortcuts:<br>
                    ➡️ (Right Arrow) = IDEAL<br>
                    ⬇️ (Down Arrow) = GOOD<br>
                    ⬅️ (Left Arrow) = BAD
                </div>
            """, unsafe_allow_html=True)

            # Create columns for the buttons
            col1, col2, col3 = st.columns(3)

            # Handle keyboard input
            key = st.text_input(
                label=f"Keyboard input for Q{idx + 1}",
                key=f"key_input_{idx}",
                label_visibility="collapsed"
            )

            # Get existing criteria
            criteria = st.session_state.evaluation_criteria.get(str(idx), {
                'selected': '',
                'notes': ''
            })

            # Buttons with improved styling
            with col1:
                if st.button("⬅️ BAD", 
                            key=f"bad_criteria_{idx}",
                            type="primary" if criteria.get('selected') == 'BAD' else "secondary",
                            use_container_width=True):
                    criteria_data = {'selected': 'BAD', 'notes': criteria.get('notes', '')}
                    self.save_criteria(idx, criteria_data)

            with col2:
                if st.button("⬇️ GOOD", 
                            key=f"good_criteria_{idx}",
                            type="primary" if criteria.get('selected') == 'GOOD' else "secondary",
                            use_container_width=True):
                    criteria_data = {'selected': 'GOOD', 'notes': criteria.get('notes', '')}
                    self.save_criteria(idx, criteria_data)

            with col3:
                if st.button("➡️ IDEAL", 
                            key=f"ideal_criteria_{idx}",
                            type="primary" if criteria.get('selected') == 'IDEAL' else "secondary",
                            use_container_width=True):
                    criteria_data = {'selected': 'IDEAL', 'notes': criteria.get('notes', '')}
                    self.save_criteria(idx, criteria_data)

            # Show current selection with improved styling
            if criteria.get('selected'):
                color = {
                    'IDEAL': '#4CAF50',
                    'GOOD': '#FFA500',
                    'BAD': '#FF4B4B'
                }.get(criteria['selected'], '#4CAF50')
                st.markdown(f"""
                    <div style='padding: 10px; border-radius: 8px; 
                               background-color: {color}20; 
                               border: 2px solid {color}; 
                               margin: 10px 0; 
                               text-align: center;
                               font-weight: bold;'>
                        Selected: {criteria['selected']}
                    </div>
                """, unsafe_allow_html=True)

            # Notes section
            st.markdown("#### 📝 Notes")
            notes = st.text_area(
                label=f"Notes for Q{idx + 1}",
                value=criteria.get('notes', ''),
                key=f"criteria_notes_{idx}",
                placeholder="Add your notes here...",
                label_visibility="collapsed",
                height=100
            )

            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)

    def save_evaluation(self, idx, rating=None, comment=None):
        """Save evaluation in session state and to file"""
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

        # Save to file after updating session state
        try:
            os.makedirs('./.streamlit', exist_ok=True)
            with open('./.streamlit/evaluations.json', 'w') as f:
                json.dump(st.session_state.evaluations, f)
        except Exception as e:
            st.error(f"Error saving evaluations: {e}")

    def export_evaluations(self):
        """Export evaluations and criteria to CSV"""
        export_data = {}
        
        for idx in st.session_state.evaluations:
            export_data[idx] = st.session_state.evaluations[idx].copy()
            # Add criteria if available
            criteria = st.session_state.evaluation_criteria.get(str(idx), {})
            export_data[idx].update({
                'criteria_type': criteria.get('selected', ''),
                'criteria_notes': criteria.get('notes', '')
            })
        
        df = pd.DataFrame.from_dict(export_data, orient='index')
        csv = df.to_csv().encode('utf-8')
        
        st.download_button(
            label="Download Evaluation Report",
            data=csv,
            file_name=f"security_qa_evaluation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime='text/csv'
        )

    def load_saved_evaluations(self):
        """Load evaluations from a JSON file"""
        try:
            if os.path.exists('./.streamlit/evaluations.json'):
                with open('./.streamlit/evaluations.json', 'r') as f:
                    st.session_state.evaluations = json.load(f)
            else:
                st.session_state.evaluations = {}
        except Exception as e:
            st.error(f"Error loading saved evaluations: {e}")
            st.session_state.evaluations = {}

    def load_evaluation_criteria(self):
        """Load evaluation criteria from JSON file"""
        try:
            if os.path.exists('./.streamlit/evaluation_criteria.json'):
                with open('./.streamlit/evaluation_criteria.json', 'r') as f:
                    st.session_state.evaluation_criteria = json.load(f)
            else:
                st.session_state.evaluation_criteria = {}
        except Exception as e:
            st.error(f"Error loading evaluation criteria: {e}")
            st.session_state.evaluation_criteria = {}

    def save_criteria(self, idx, criteria_data):
        """Save criteria for a specific question"""
        try:
            st.session_state.evaluation_criteria[str(idx)] = criteria_data
            os.makedirs('./.streamlit', exist_ok=True)
            with open('./.streamlit/evaluation_criteria.json', 'w') as f:
                json.dump(st.session_state.evaluation_criteria, f)
        except Exception as e:
            st.error(f"Error saving criteria: {e}")

    def check_stored_data(self):
        """Debug method to check stored data"""
        try:
            # Check evaluation criteria file
            criteria_path = './.streamlit/evaluation_criteria.json'
            if os.path.exists(criteria_path):
                with open(criteria_path, 'r') as f:
                    st.write("Evaluation Criteria File Contents:")
                    st.json(json.load(f))
            else:
                st.warning("No evaluation criteria file found")
                
            # Check evaluations file
            eval_path = './.streamlit/evaluations.json'
            if os.path.exists(eval_path):
                with open(eval_path, 'r') as f:
                    st.write("Evaluations File Contents:")
                    st.json(json.load(f))
            else:
                st.warning("No evaluations file found")
        except Exception as e:
            st.error(f"Error reading files: {e}")

if __name__ == "__main__":
    app = SecurityEvaluationApp()
    app.run() 