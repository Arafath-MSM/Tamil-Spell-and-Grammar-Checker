import streamlit as st
from models.rule_based_model import RuleBasedChecker
from models.statistical_model import StatisticalChecker
from models.deep_learning_model import DeepLearningChecker

def compare_model(text, model):
    try:
        if model == 'Rule-based':
            checker = RuleBasedChecker()
        elif model == 'Statistical':
            checker = StatisticalChecker()
        elif model == 'Deep Learning':
            checker = DeepLearningChecker()
        else:
            return [], {}

        # Check text and log the results
        errors = checker.check_text(text)
        suggestions = checker.get_suggestions(text)

        # Debugging: Log the errors detected by the model
        print("Detected Errors:", errors)  # Add this line for debugging

    except Exception as e:
        errors = [('error', f'Error processing text: {str(e)}', text)]
        suggestions = {}
    
    return errors, suggestions

def evaluate_model_performance(errors, model_name):
    """Evaluate the model performance based on errors."""
    total_errors = len(errors)
    # Placeholder for calculating accuracy, you can improve this logic based on your criteria
    if total_errors == 0:
        accuracy = 100
    else:
        accuracy = max(100 - (total_errors * 10), 0)  # Decrease 10% per error, capped at 0%

    return accuracy

def display_results(text_input, errors, suggestions, performance_scores):
    st.markdown("### Input Text")
    st.markdown(f'<div class="result-box">{text_input}</div>', unsafe_allow_html=True)

    st.markdown("### Analysis Results")
    if errors:
        for error_type, msg, context in errors:
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
    
    if suggestions:
        st.markdown("### Suggestions")
        for key, suggestion in suggestions.items():
            st.markdown(f"**{key}**: {suggestion}")

    st.markdown("### Model Performance Comparison")
    for model_name, score in performance_scores.items():
        st.markdown(f"**{model_name}**: {score}%")

def setup_css():
    st.markdown("""
        <style>
        .main { padding: 2rem; }
        .stTitle { font-size: 2.5rem !important; font-weight: bold !important; text-align: center; color: #4CAF50; }
        .result-box { background-color: #f0f4f8; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; border: 1px solid #ccc; }
        .error-type { color: #d73027; font-weight: bold; }
        .message { color: #4575b4; }
        .context { color: #666; font-style: italic; }
        .sidebar { background-color: #fafafa; padding: 2rem; border-radius: 8px; }
        </style>
    """, unsafe_allow_html=True)

def main():
    setup_css()
    st.markdown("<h1 class='stTitle'>Tamil Text Checker</h1>", unsafe_allow_html=True)

    # Sidebar for model selection and input type
    st.sidebar.header("Settings")
    use_rule_based = st.sidebar.checkbox("Rule-based Model", value=True)
    use_statistical = st.sidebar.checkbox("Statistical Model", value=True)
    use_deep_learning = st.sidebar.checkbox("Deep Learning Model", value=True)

    input_type = st.sidebar.radio("Select Input Type", ["Enter custom text", "Example Sentence"])
    
    # Example texts
    example_texts = {
        'Correct sentence': 'நான் பள்ளிக்கு செல்கிறேன்.',
        'Spelling error': 'நான் பள்ளிக்கு சல்கிறேன்.',
        'Grammar error': 'நான் பள்ளிக்கு செல்கிறது.',
        'Mixed errors': 'நாங்கள் பள்ளிக்கு செல்கிறான் சல்கிறேன்.',
        'Complex sentence': 'நேற்று நான் பள்ளிக்கு செல்கிறேன். இன்று நண்பர்களுடன் விளையாட வந்தேன்.',
        'Pronoun error': 'நான் பள்ளிக்கு போகிறான்.',
        'Verb tense error': 'நான் நேற்று பள்ளிக்கு செல்கிறேன்.',
        'Noun usage error': 'நான் ஒரு பெரிய புத்தகம் படிக்கிறேன்.',
        'Adjective error': 'அவர் மிகவும் அழகான பன்டையார்.',
        'Colloquial error': 'நான் படிச்சேன்',
    }

    # Main text input area
    if input_type == "Enter custom text":
        text_input = st.text_area("Enter Tamil text:", height=150, placeholder="Type or paste your Tamil text here...")
    else:
        selected_example = st.selectbox("Choose an example:", list(example_texts.keys()))
        text_input = example_texts[selected_example]
        st.text_area("Selected example:", value=text_input, height=150, disabled=True)

    # Model selection
    models = []
    if use_rule_based:
        models.append("Rule-based")
    if use_statistical:
        models.append("Statistical")
    if use_deep_learning:
        models.append("Deep Learning")

    # Dictionary to store performance scores
    performance_scores = {}

    # Check button
    if st.sidebar.button("Check Text"):
        if text_input and models:
            st.markdown("---")
            errors = []
            suggestions = {}
            for model in models:
                # Compare each model
                model_errors, model_suggestions = compare_model(text_input, model)
                errors += model_errors
                suggestions.update(model_suggestions)
                # Evaluate performance
                accuracy = evaluate_model_performance(model_errors, model)
                performance_scores[model] = accuracy
            display_results(text_input, errors, suggestions, performance_scores)
        else:
            st.error("Please select a model and enter text to analyze.")

if __name__ == "__main__":
    main()
