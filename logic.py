import fitz  # PyMuPDF
import docx
import re
import random
from collections import Counter

def parse_file(uploaded_file):
    ext = uploaded_file.name.split('.')[-1]
    if ext == 'pdf':
        text = ""
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif ext == 'docx':
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])
    elif ext == 'txt':
        return uploaded_file.read().decode('utf-8')
    return ""

def summarize_text(text, sentence_count=5):
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    top_sentences = sorted(sentences, key=len, reverse=True)[:sentence_count]
    return " ".join(top_sentences)

def brainstorm_ideas(text, top_n=10):
    words = re.findall(r'\b\w{5,}\b', text.lower())
    freq = Counter(words)
    return [w for w, _ in freq.most_common(top_n)]

def extract_keywords(text, top_n=10):
    words = re.findall(r'\b[a-zA-Z]{5,}\b', text.lower())
    stopwords = set([
        "about", "above", "after", "again", "against", "all", "among", "an", "and",
        "any", "are", "as", "at", "be", "because", "been", "before", "being", "below",
        "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down",
        "during", "each", "few", "for", "from", "further", "had", "has", "have", "having",
        "he", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i",
        "if", "in", "into", "is", "it", "its", "itself", "me", "more", "most", "my",
        "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
        "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "should",
        "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
        "then", "there", "these", "they", "this", "those", "through", "to", "too", "under",
        "until", "up", "very", "was", "we", "were", "what", "when", "where", "which", "while",
        "who", "whom", "why", "with", "would", "you", "your", "yours", "yourself", "yourselves"
    ])
    words = [w for w in words if w not in stopwords]
    freq = Counter(words)
    return [w for w, _ in freq.most_common(top_n)]

def generate_quiz(text, num_questions=5):
    keywords = extract_keywords(text, top_n=20)
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]

    quiz = []
    for i in range(min(num_questions, len(keywords))):
        keyword = keywords[i]
        question = f"What is the meaning or role of '{keyword}' in this context?"
        correct_sentence = next((s for s in sentences if keyword in s.lower()), None)
        if not correct_sentence:
            continue

        # Generate wrong options from other keyword-based sentences
        wrongs = []
        for k in keywords:
            if k != keyword:
                sentence = next((s for s in sentences if k in s.lower()), None)
                if sentence and sentence != correct_sentence:
                    wrongs.append(sentence)
            if len(wrongs) >= 3:
                break

        options = [correct_sentence] + wrongs[:3]
        random.shuffle(options)

        quiz.append({
            "question": question,
            "options": options,
            "answer": correct_sentence
        })

    return quiz

def evaluate_answers(quiz, user_answers):
    score = 0
    correct = []
    for i, item in enumerate(quiz):
        if user_answers.get(i) == item["answer"]:
            score += 1
        correct.append(item["answer"])
    return score, correct
