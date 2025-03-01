from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Load bad words from the file
def load_bad_words(file_path):
    with open(file_path, 'r') as file:
        bad_words = [line.strip() for line in file if line.strip()]
    return bad_words

# Path to the bad words file
BAD_WORDS_FILE = "en.txt"
bad_words = load_bad_words(BAD_WORDS_FILE)

# Function to detect bad words in text
def detect_bad_words(text):
    detected_words = []
    words = re.findall(r'\b\w+\b', text)  # Split text into words
    for i, word in enumerate(words):
        if word.lower() in bad_words:
            detected_words.append({"word": word, "position": i})
    return detected_words

# Function to censor bad words in text
def censor_text(text, detected_words):
    for entry in detected_words:
        word = entry["word"]
        # Replace bad words with ***
        text = re.sub(r'\b' + re.escape(word) + r'\b', '***', text, flags=re.IGNORECASE)
    return text

# API endpoint
@app.route('/filter', methods=['POST'])
def filter_text():
    data = request.json
    text = data.get('text', '')

    # Detect bad words
    detected_words = detect_bad_words(text)
    # Censor the text
    censored_text = censor_text(text, detected_words)

    # Prepare response
    response = {
        "original_text": text,
        "censored_text": censored_text,
        "detected_words": detected_words
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)