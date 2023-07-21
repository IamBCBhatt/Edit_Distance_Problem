from flask import Flask, render_template, request,send_from_directory
import nltk
from nltk.metrics.distance import edit_distance
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('new.html')
@app.route('/dictionary')
def serve_dictionary():
    # Get the path to the static folder
    static_folder = os.path.join(app.root_path, 'static')
    # Serve the dictionary.txt file from the static folder
    return send_from_directory(static_folder, 'dictionary.txt')
@app.route('/sentance-correct')
def sentance_correct():
    return render_template('sentance.html')

@app.route('/plagiarism-checker')
def plagiarism_checker():
        return render_template('index.html')

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    file1 = request.files['file1']
    file2 = request.files['file2']

    content1 = file1.read().decode('utf-8')
    content2 = file2.read().decode('utf-8')

    sentences1 = nltk.sent_tokenize(content1)
    sentences2 = nltk.sent_tokenize(content2)

    total_sentences = len(sentences1)
    plagiarized_sentences = 0

    for sentence1 in sentences1:
        sentence1_words = nltk.word_tokenize(sentence1.lower())
        for sentence2 in sentences2:
            sentence2_words = nltk.word_tokenize(sentence2.lower())
            distance = edit_distance(sentence1_words, sentence2_words)
            max_length = max(len(sentence1_words), len(sentence2_words))
            similarity = 1 - (distance / max_length)
            if similarity > 0.8:
                plagiarized_sentences += 1
                break

    plagiarism_percentage = (plagiarized_sentences / total_sentences) * 100

    return render_template('result.html', plagiarism_percentage=plagiarism_percentage)

if __name__ == '__main__':
    app.run(debug=True)
