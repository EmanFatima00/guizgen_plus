import streamlit as st
from logic import parse_file, summarize_text, generate_quiz, evaluate_answers, brainstorm_ideas
from database import init_db, save_attempt, get_history

st.set_page_config(page_title="QuizGen+", layout="wide")
init_db()

st.title("📚 QuizGen+ – Learn Better from Your Docs")

if "quiz" not in st.session_state:
    st.session_state.quiz = []
    st.session_state.answers = {}
    st.session_state.submitted = False
    st.session_state.summary = ""
    st.session_state.ideas = []

uploaded_file = st.file_uploader("📤 Upload your document", type=["pdf", "docx", "txt", "pptx"])

num_questions = st.slider("📝 Number of quiz questions", 3, 10, 5)

if uploaded_file:
    raw_text = parse_file(uploaded_file)
    st.session_state.raw_text = raw_text
    # ✅ Show preview of extracted text
    st.subheader("🧾 Extracted Text Preview")
    st.write(st.session_state.raw_text[:1500])


    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔍 Summarize Document"):
            st.session_state.summary = summarize_text(raw_text)
    with col2:
        if st.button("🧠 Brainstorm Key Ideas"):
            st.session_state.ideas = brainstorm_ideas(raw_text)
    with col3:
        if st.button("📝 Generate Quiz"):
            st.session_state.quiz = generate_quiz(raw_text, num_questions)
            st.session_state.submitted = False

    if st.session_state.summary:
        st.subheader("📝 Summary")
        st.write(st.session_state.summary)

    if st.session_state.ideas:
        st.subheader("🧠 Brainstormed Ideas")
        st.write(", ".join(st.session_state.ideas))

    if st.session_state.quiz:
        st.subheader("🧠 Quiz Time!")
        for idx, item in enumerate(st.session_state.quiz):
            st.session_state.answers[idx] = st.radio(
                f"Q{idx+1}: {item['question']}", item["options"], key=f"q{idx}")

        if st.button("📊 Submit Answers"):
            score, results = evaluate_answers(st.session_state.quiz, st.session_state.answers)
            st.session_state.submitted = True
            save_attempt(score, num_questions)
            st.success(f"🎉 Your Score: {score}/{num_questions}")
            for i, res in enumerate(results):
                st.write(f"✅ Q{i+1} Correct Answer: {res}")

       if st.button("🔁 Retake Quiz"):
       if st.session_state.get("raw_text"):
          st.session_state.quiz = generate_quiz(
              st.session_state.raw_text,
              st.session_state.get("num_questions", 5)
        )
        st.session_state.user_answers = []
        st.session_state.show_results = False
        st.rerun()
    else:
        st.warning("⚠️ Please upload a document before retaking the quiz.")

    st.subheader("📜 Quiz History")
    for row in get_history():
        st.write(f"🕒 {row[0]} — Score: {row[1]}/{row[2]}")
