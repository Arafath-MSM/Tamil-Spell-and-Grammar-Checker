from transformers import pipeline

# Load pre-trained BERT model for Tamil
model = pipeline("fill-mask", model="ai4bharat/indic-bert")

def spell_grammar_checker_dl(paragraph):
    corrected_text = []
    for word in paragraph.split():
        # Predict using BERT
        result = model(f"{word} [MASK]")[0]
        corrected_text.append(result["token_str"])
    return " ".join(corrected_text)

if __name__ == "__main__":
    paragraphs = [
        "வணக்கம் நான் நீங்கள் காதலிக்கிறேன்",
        "தமிழ் மிக அருமை ஆன்ல சொற்கள் பிழைகள் உள்ளது",
        "அவன் செல்லும் பார்",
        "நீங்கள் சிறந்த நண்பர்",
        "என் பேரு மாறி ஒழுங்கான வாக்கியம் எழுதுக"
    ]

    for i, paragraph in enumerate(paragraphs, 1):
        print(f"\nParagraph {i} - Original: {paragraph}")

        # Correct using DL-based approach
        corrected_paragraph = spell_grammar_checker_dl(paragraph)
        print("Corrected Paragraph:", corrected_paragraph)
