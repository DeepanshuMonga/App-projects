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

# Quiz data
questions_list = [
    "1. Who wrote Sherlock Holmes?",
    "2. In Harry Potter, what position does Harry play in Quidditch?",
    "3. What is the first book in The Lord of the Rings series?",
    "4. What classic novel features the character Jay Gatsby?",
    "5. Who is the author of 'A Song of Ice and Fire', the book series that inspired Game of Thrones?",
    "6. What does HTML stand for?",
    "7. In Python, what data structure is immutable: list or tuple?",
    "8. What is the time complexity of a binary search algorithm?",
    "9. Which programming language is known for having 'write once, run anywhere' capability?",
    "10. What does the term 'recursion' mean in programming?",
    "11. What is the name of Iron Man’s AI assistant before FRIDAY?",
    "12. What was the first MCU film to cross $2 billion at the box office?",
    "13. Which movie won the Oscar for Best Picture in 2023?",
    "14. What is the highest-grossing animated movie of all time?",
    "15. Who is the main villain in Doctor Strange in the Multiverse of Madness?",
    "16. What is the rarest blood type in humans?",
    "17. Who was the first person to step on the moon?",
    "18. What is the speed of light in vacuum (in km/s)?",
    "19. What is the national sport of Japan?",
    "20. What is the formula of the complex cisplatin, a chemotherapy drug?"
]

options_list = [
    ["J.R.R. Tolkien", "Agatha Christie", "J.K. Rowling", "Arthur Conan Doyle"],
    ["Beater", "Seeker", "Chaser", "Keeper"],
    ["The Fellowship of the Ring", "The Two Towers", "The Return of the King", "The Hobbit"],
    ["To Kill a Mockingbird", "The Great Gatsby", "Moby-Dick", "The Catcher in the Rye"],
    ["J.R.R. Tolkien", "George R.R. Martin", "J.K. Rowling", "Suzanne Collins"],
    ["HyperText Markup Language", "High Text Markup Language", "Hyper Transfer Markup Language", "HyperText Management Language"],
    ["List", "Tuple", "String", "Dictionary"],
    ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
    ["C", "Java", "Python", "Ruby"],
    ["Repeating block of code", "Calling a function within itself", "Running code in parallel", "Running code in a loop"],
    ["JARVIS", "VISION", "ULTRON", "PEPPER"],
    ["Avengers: Infinity War", "Avengers: Endgame", "Black Panther", "No Way Home"],
    ["Everything Everywhere All at Once", "The Fabelmans", "Top Gun: Maverick", "Avatar 2"],
    ["The Lion King", "Frozen II", "Toy Story 4", "Frozen"],
    ["Kang the Conqueror", "Scarlet Witch", "Loki", "Ultron"],
    ["A+", "O-", "AB-", "B+"],
    ["Buzz Aldrin", "Neil Armstrong", "John Glenn", "Alan Shepard"],
    ["300,000 km/s", "150,000 km/s", "186,000 km/s", "200,000 km/s"],
    ["Baseball", "Sumo", "Karate", "Judo"],
    ["[Pt(NH₃)₂Cl₂]", "[Co(NH₃)₆]³⁺", "[Fe(CN)₆]⁴⁻", "[Ag(NH₃)₂]⁺"]
]

solutions_tuple = (4, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2, 1, 2, 2, 3, 2, 1, 2, 1)

if not st.session_state.submitted:
    # Display title and rules
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
    correct_options = [x - 1 for x in solutions_tuple]  # Adjust for 0-based indexing
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
