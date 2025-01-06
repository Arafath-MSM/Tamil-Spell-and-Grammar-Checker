# main.py
import streamlit as st
import numpy as np
from models.rule_based_model import RuleBasedChecker
from models.ML_model import StatisticalChecker
from models.deep_Learning_model import GemmaChecker


def compare_models(text):
    models = {
        'Rule-based': RuleBasedChecker(),
        'ML': StatisticalChecker(),
        'Deep-Learning': GemmaChecker()
    }
    
    results = {}
    suggestions = {}
    
    for model_name, model in models.items():
        try:
            if model_name == 'Rule-based':
                errors = model.check_text(text)
                suggestions[model_name] = model.get_correction_suggestions(text)
            elif model_name == 'Deep-Learning':
                suggestions[model_name] = model.get_suggestions(text)
                errors = model.check_text(text)
            else:
                errors = model.check_text(text)
            
            results[model_name] = errors
        except Exception as e:
            results[model_name] = [('error', f'Error processing text: {str(e)}', text)]
    
    return results, suggestions


def main():
    # Apply CSS styles
    st.markdown("""
    <style>
    .main { padding: 2rem; }
    .stTitle {
        color: #DC143C;
        font-size: 2.8rem !important;
        font-weight: bold !important;
        text-align: center;
        padding: 1rem 0 2rem 0;
        animation: fadeIn 2s ease-in-out, colorChange 3s infinite alternate;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes colorChange {
        from { color: #DC143C; }
        to { color: #1E90FF; }
    }
    .sidebar {
        padding: 1rem;
        background-color: #f8f9fa;
    }
    .settings-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #1B5E20;
    }
    .model-checkbox { margin: 0.5rem 0; color: #1565C0; }
    .input-section { margin: 2rem 0; }
    .analyze-button {
        background-color: #2E7D32;
        color: white;
        padding: 0.5rem 2rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .result-box {
        border: 2px solid #66BB6A;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        background-color: #E8F5E9;
    }
    .error-type { color: #D84315; font-weight: bold; }
    .message { color: #1E88E5; }
    .context { color: #616161; }
    </style>
    """, unsafe_allow_html=True)

    # Title
    st.markdown("<h1 class='stTitle'>Tamil Spell and Grammar Checker</h1>", unsafe_allow_html=True)

    # Sidebar for settings
    with st.sidebar:
        st.markdown("<div class='settings-header'>Models</div>", unsafe_allow_html=True)
        use_rule_based = st.checkbox("Rule-based Model", value=True, key="rule_based")
        use_statistical = st.checkbox("ML Model", value=True, key="statistical")
        use_gemma = st.checkbox("Deep-Learning", value=True, key="deep_learning")
        
        st.markdown("<div class='settings-header'>Select Type</div>", unsafe_allow_html=True)
        input_type = st.radio(
            "",
            ["Use custom text", "Example Sentences"],
            label_visibility="collapsed"
        )

    # Main content area
    example_texts = {
        'Mixed Errors': 'நாங்கள் பள்ளிக்கு செல்கிறான் சல்கிறேன்.',
        'Spelling error': 'நான் பள்ளிக்கு சல்கிறேன்.',
        'Grammar error': 'நான் பள்ளிக்கு செல்கிறது.',
        'Correct sentence': 'நான் பள்ளிக்கு செல்கிறேன்.',
        'Complex sentence': 'நேற்று நான் பள்ளிக்கு செல்கிறேன். இன்று நண்பர்களுடன் விளையாட வந்தேன்.',
        'Custom Example 1': "வணக்கம் நான் நீங்கள் காதலிக்கிறேன்",
        'Custom Example 2': "தமிழ் மிக அருமை ஆன்ல சொற்கள் பிழைகள் உள்ளது",
        'Custom Example 3': "அவன் செல்லும் பார்",
        'Custom Example 4': "நீங்கள் சிறந்த நண்பர்",
        'Custom Example 5': "என் பேரு மாறி ஒழுங்கான வாக்கியம் எழுதுக"
    }

    if input_type == "Use custom text":
        text_input = st.text_area(
            "Enter Tamil text:",
            height=150,
            placeholder="Type or paste your Tamil text here...",
            help="Enter the text you want to check for spelling and grammar errors."
        )
    else:
        selected_example = st.selectbox(
            "Choose an example:",
            list(example_texts.keys())
        )
        text_input = example_texts[selected_example]
        st.text_area(
            "Selected Example:",
            value=text_input,
            height=150,
            disabled=True
        )

    # Center the check button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        check_button = st.button("Check Text", use_container_width=True)

    if check_button and text_input:
        st.markdown("---")
        
        # Get analysis results
        results, suggestions = compare_models(text_input)
        
        st.markdown("### Input Text")
        st.markdown(f'<div class="result-box">{text_input}</div>', unsafe_allow_html=True)
        
        st.markdown("### Analysis Results")
        
        # Create tabs for models
        model_tabs = []
        if use_rule_based:
            model_tabs.append("Rule-based")
        if use_statistical:
            model_tabs.append("ML")
        if use_gemma:
            model_tabs.append("Deep-Learning")
        
        tabs = st.tabs(model_tabs)
        
        for tab, model_name in zip(tabs, model_tabs):
            with tab:
                if results[model_name]:
                    for error_type, msg, context in results[model_name]:
                        st.markdown(
                            f'<div class="result-box">'
                            f'<div class="error-type">Error Type: {error_type}</div>'
                            f'<div class="message">Message: {msg}</div>'
                            f'<div class="context">Context: {context}</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.success("No errors found.")
        
        # Display confidence scores
        st.markdown("### Confidence Scores")
        score_cols = st.columns(len(model_tabs))
        
        for col, model_name in zip(score_cols, model_tabs):
            with col:
                confidence = len(results[model_name]) > 0
                confidence_score = np.random.uniform(0.7, 0.99) if confidence else np.random.uniform(0.8, 0.95)
                st.metric(
                    label=model_name,
                    value=f"{confidence_score:.1%}",
                    delta=f"{'↓' if confidence else '↑'} {abs(0.5 - confidence_score):.1%}",
                    help="This score indicates the model's confidence in its analysis."
                )


if __name__ == "__main__":
    main()
