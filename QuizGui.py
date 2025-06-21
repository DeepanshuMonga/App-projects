import streamlit as st

# Initialize session state
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "answers" not in st.session_state:
    st.session_state.answers = []
if "missed" not in st.session_state:
    st.session_state.missed = 0
if "missedind" not in st.session_state:
    st.session_state.missedind = []

questions_list = [
    "1. Who wrote Sherlock Holmes?",
    "2. In Harry Potter, what position does Harry play in Quidditch?",
    "3. What is the first book in The Lord of the Rings series?",
    # ... (other questions, same as original)
]
options_list = [
    ["J.R.R. Tolkien", "Agatha Christie", "J.K. Rowling", "Arthur Conan Doyle"],
    ["Beater", "Seeker", "Chaser", "Keeper"],
    ["The Fellowship of the Ring", "The Two Towers", "The Return of the King", "The Hobbit"],
    # ... (other options, same as original)
]
solutions_tuple = (4, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 3, 2, 1, 2, 1)

if not st.session_state.submitted:
    # Display title and rules without time.sleep
    st.title("Welcome to The Geeky Gauntlet Quiz 💻🎬📚")
    st.subheader("The :rainbow[***rules***] of quiz are:")
    st.markdown("1. :orange[There are 20 questions in all.]")
    st.markdown("2. :red[There is no negative marking.]")
    st.markdown("3. :green[Each question carries 1 Mark.]")
    st.write("Let's start our Quiz then:")

    with st.form("Quiz"):
        store_answer = []
        missed_index = []
        missed_answer = 0
        for i in range(len(questions_list)):
            answer_user = st.radio(questions_list[i], options_list[i], index=None, key=f"q_{i}")
            if answer_user is not None:
                selected_index = options_list[i].index(answer_user)
            else:
                selected_index = None
                missed_answer += 1
                missed_index.append(i)
            store_answer.append(selected_index)
        submitted = st.form_submit_button("Submit", disabled=st.session_state.submitted)
        if submitted:
            st.session_state.answers = store_answer
            st.session_state.submitted = True
            st.session_state.missed = missed_answer
            st.session_state.missedind = missed_index

else:
    # Display results
    st.success("Form submitted ✅")
    corr = 0
    miss = st.session_state.missed
    correct_options = [x - 1 for x in solutions_tuple]
    correct_index = []
    incorrect_index = []
    for i in range(len(questions_list)):
        if st.session_state.answers[i] == correct_options[i]:
            correct_index.append(i)
            corr += 1
        elif st.session_state.answers[i] is not None:
            incorrect_index.append(i)
    st.subheader(f"✅ Correct Answers: {corr}")
    with st.expander("Correct questions:"):
        for i in correct_index:
            st.markdown(f"**{questions_list[i]}**")
            st.markdown(f"✔️ Correct Answer: `{options_list[i][correct_options[i]]}`")
    st.subheader(f"❌ Incorrect Answers: {len(questions_list) - corr - miss}")
    with st.expander("Incorrect questions:"):
        for i in incorrect_index:
            st.markdown(f"**{questions_list[i]}**")
            st.markdown(f"❌ Your answer: {options_list[i][st.session_state.answers[i]]}")
            st.markdown(f"✔️ Correct Answer: `{options_list[i][correct_options[i]]}`")
    st.subheader(f"⚠️ Missed Questions: {miss}")
    with st.expander("Missed questions:"):
        for i in st.session_state.missedind:
            st.markdown(f"**{questions_list[i]}**")
            st.markdown(f"✔️ Correct Answer: `{options_list[i][correct_options[i]]}`")
    per = (corr / 20) * 100
    st.subheader(f"Percentage = {per:.2f}%")
    mapp = ["one", "two", "three", "four", "five"]
    st.subheader("Before closing, please rate us:")
    selected = st.feedback("stars")
    if selected is not None:
        st.write(f"You selected {mapp[selected]} star(s).")
        st.write("Thanks for Rating.")
        st.balloons()
    st.subheader(":rainbow[Thanks for Playing. Hope You enjoyed. Have a Good Day ahead!]")
    if st.button("🔁 Restart Quiz"):
        # Reset only relevant session state keys
        st.session_state.submitted = False
        st.session_state.answers = []
        st.session_state.missed = 0
        st.session_state.missedind = []
