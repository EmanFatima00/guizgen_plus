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

def generate_quiz(text, num_questions=5):
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    quiz = []
    for i in range(min(num_questions, len(sentences))):
        q = random.choice(sentences)
        wrong = random.sample(sentences, 3) if len(sentences) > 3 else ["N/A", "N/A", "N/A"]
        quiz.append({
            "question": f"What is the main idea of: \"{q[:80]}...\"?",
            "options": random.sample([q] + wrong, 4),
            "answer": q
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