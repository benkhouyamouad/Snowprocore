import streamlit as st

# ----------------------------
# Snowflake Quiz Questions
# ----------------------------
quiz_questions = [
    {
        "id": 1,
        "question": "Snowflake provides a mechanism for its customers to override its natural clustering algorithms. This method is:",
        "options": [
            "A. Micro-partitions",
            "B. Clustering keys",
            "C. Key partitions",
            "D. Clustered partitions"
        ],
        "correctAnswer": ["B"],
        "multi": False,
        "explanation": "Clustering keys allow users to override Snowflake's natural clustering algorithms."
    },
    {
        "id": 2,
        "question": "Which of the following are valid Snowflake Virtual Warehouse Scaling Policies?",
        "options": [
            "A. Custom",
            "B. Economy",
            "C. Optimized",
            "D. Standard"
        ],
        "correctAnswer": ["B", "D"],
        "multi": True,
        "explanation": "The valid scaling policies are Economy and Standard."
    },
    {
        "id": 3,
        "question": "True or False: A single database can exist in more than one Snowflake account.",
        "options": [
            "A. True",
            "B. False"
        ],
        "correctAnswer": ["B"],
        "multi": False,
        "explanation": "A database exists in only one Snowflake account."
    },
    {
        "id": 4,
        "question": "Which of the following roles is recommended to be used to create and manage users and roles?",
        "options": [
            "A. SYSADMIN",
            "B. SECURITYADMIN",
            "C. PUBLIC",
            "D. ACCOUNTADMIN"
        ],
        "correctAnswer": ["D"],
        "multi": False,
        "explanation": "ACCOUNTADMIN is recommended for creating and managing users and roles."
    },
    {
        "id": 5,
        "question": "True or False: Bulk unloading of data from Snowflake supports the use of a SELECT statement.",
        "options": [
            "A. True",
            "B. False"
        ],
        "correctAnswer": ["A"],
        "multi": False,
        "explanation": "Bulk unloading supports SELECT statements."
    }
]

# ----------------------------
# Streamlit App State
# ----------------------------
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False
if "completed" not in st.session_state:
    st.session_state.completed = False

# ----------------------------
# Helper functions
# ----------------------------
def reset_quiz():
    st.session_state.current_q = 0
    st.session_state.user_answers = {}
    st.session_state.show_answer = False
    st.session_state.completed = False

def next_question():
    if st.session_state.current_q < len(quiz_questions) - 1:
        st.session_state.current_q += 1
        st.session_state.show_answer = False
    else:
        st.session_state.completed = True

def previous_question():
    if st.session_state.current_q > 0:
        st.session_state.current_q -= 1
        st.session_state.show_answer = False

def calculate_score():
    correct = 0
    for ans in st.session_state.user_answers.values():
        if set(ans["selected"]) == set(ans["correct"]):
            correct += 1
    return correct

# ----------------------------
# Render Completed Screen
# ----------------------------
if st.session_state.completed:
    score = calculate_score()
    total = len(quiz_questions)
    percentage = round((score / total) * 100)

    st.markdown("## 🎉 Quiz Completed!")
    st.markdown(f"### Score: **{score} / {total}**")
    st.markdown(f"### Percentage: **{percentage}%**")

    if percentage >= 80:
        st.success("Excellent work! 🎉")
    elif percentage >= 60:
        st.warning("Good job! Keep practicing! 👍")
    else:
        st.error("Keep studying! You've got this! 💪")

    if st.button("🔄 Restart Quiz"):
        reset_quiz()

    st.stop()

# ----------------------------
# Render Quiz Question
# ----------------------------
q = quiz_questions[st.session_state.current_q]

st.title("Snowflake Certification Quiz")
st.progress((st.session_state.current_q + 1) / len(quiz_questions))

st.markdown(f"### Question {st.session_state.current_q + 1} of {len(quiz_questions)}")
st.markdown(f"## {q['question']}")
st.write("---")

# Options input
if q["multi"]:
    selected = st.multiselect("Select all that apply:", q["options"])
else:
    selected = st.radio("Choose an option:", q["options"])

# Show answer button
if not st.session_state.show_answer:
    if st.button("Show Answer", disabled=(not selected)):
        st.session_state.show_answer = True
        selected_letters = [s.split(".")[0] for s in selected] if isinstance(selected, list) else [selected.split(".")[0]]
        st.session_state.user_answers[st.session_state.current_q] = {
            "selected": selected_letters,
            "correct": q["correctAnswer"]
        }

# Answer explanation
if st.session_state.show_answer:
    user_selected = st.session_state.user_answers[st.session_state.current_q]["selected"]
    correct = st.session_state.user_answers[st.session_state.current_q]["correct"]
    if set(user_selected) == set(correct):
        st.success(f"✓ Correct! **Correct Answer:** {', '.join(correct)}")
    else:
        st.error(f"✗ Incorrect! **Correct Answer:** {', '.join(correct)}")
    st.info(q["explanation"])

# Navigation buttons
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.button("← Previous", on_click=previous_question, disabled=st.session_state.current_q==0)
with col3:
    st.button(
        "Next →" if st.session_state.current_q < len(quiz_questions)-1 else "Finish Quiz",
        on_click=next_question,
        disabled=not st.session_state.show_answer
    )

# Progress indicators
st.write("---")
st.markdown("### Progress")
cols = st.columns(len(quiz_questions))
for i, col in enumerate(cols):
    with col:
        if i == st.session_state.current_q:
            st.markdown("🔵")
        elif i in st.session_state.user_answers:
            if set(st.session_state.user_answers[i]["selected"]) == set(st.session_state.user_answers[i]["correct"]):
                st.markdown("🟢")
            else:
                st.markdown("🔴")
        else:
            st.markdown("⚪")
