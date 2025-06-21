import streamlit as st

questions_list = [
    "Who wrote Sherlock Holmes?",
    "In Harry Potter, what position does Harry play in Quidditch?",
    "What is the first book in The Lord of the Rings series?",
    "What classic novel features the character Jay Gatsby?",
    "Who is the author of 'A Song of Ice and Fire'?",
    "What does HTML stand for?",
    "In Python, what data structure is immutable: list or tuple?",
    "What is the time complexity of a binary search algorithm?",
    "Which programming language has 'write once, run anywhere'?",
    "What does the term 'recursion' mean in programming?",
    "What is the name of Iron Man’s AI assistant before FRIDAY?",
    "What was the first MCU film to cross $2 billion?",
    "Which movie won the Oscar for Best Picture in 2023?",
    "What is the highest-grossing animated movie of all time?",
    "Who is the main villain in Doctor Strange: Multiverse of Madness?",
    "What is the rarest blood type in humans?",
    "Who was the first person to step on the moon?",
    "What is the speed of light in vacuum (in km/s)?",
    "What is the national sport of Japan?",
    "What is the formula of the complex cisplatin?"
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

solutions_tuple = (
    4, 2, 1, 2, 2, 1, 2, 2, 2, 2,
    1, 2, 1, 2, 2, 3, 2, 1, 2, 1
)

st.set_page_config(page_title="Geeky Gauntlet Quiz", layout="wide")
st.title("🎮 The Geeky Gauntlet Quiz: Code, Movies & More!")

st.markdown("""
Answer all 20 questions below and then click **Submit** to view your score!  
There is **no time limit** and **no negative marking**.  
Good luck! 💻🎬📚
""")

with st.form("quiz_form"):
    user_answers = []
    for i in range(len(questions_list)):
        st.subheader(f"Q{i+1}. {questions_list[i]}")
        answer = st.radio(
            "Choose an option:",
            options_list[i],
            key=f"q{i}",
            index=None
        )
        user_answers.append(answer)

    submitted = st.form_submit_button("🚀 Submit Answers")

if submitted:
    score = 0
    st.markdown("---")
    st.header("📊 Results")

    for i in range(len(questions_list)):
        correct_option_index = solutions_tuple[i] - 1
        correct_option = options_list[i][correct_option_index]

        if user_answers[i] == correct_option:
            score += 1
            result = "✅ Correct"
        else:
            result = f"❌ Wrong (Correct: {correct_option})"

        st.markdown(f"**Q{i+1}:** {result}")

    st.markdown("---")
    st.subheader(f"🎯 Final Score: `{score}/20`")
    if score >= 15:
        st.success("🔥 Excellent! You're a true geek.")
    elif score >= 10:
        st.info("👍 Good! You know your stuff.")
    else:
        st.warning("📚 Keep learning — you're on the right path!")

    st.balloons()
