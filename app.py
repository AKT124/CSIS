import streamlit as sl

from Sourashtra_File import words
from Sourashtra_File import name

import os


def createAccountFile(username, password, language="Sourashtra"):
    file_path = f"{username}.txt"
    lines = [
        username,  # Line 0 (1st row)
        password,  # Line 1 (2nd row)
        language,  # Line 2 (3rd row)
        "0",  # Line 3 Stat 1
        "0",  # Line 4 Stat 2
        "0",  # Line 5 Stat 3
        "0",  # Line 6 Total words completed
        "10",  # Line 7 Words left in current set
        "0",  # Line 8 Current line index in Sourashtra rtext file
    ]
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))


def readAccountFile(username):
    file_path = f"{username}.txt"
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    if len(lines) < 9:
        return None
    return {
        "username": lines[0],
        "password": lines[1],
        "language": lines[2],
        "stat1": lines[3],
        "stat2": lines[4],
        "stat3": lines[5],
        "words_completed": lines[6],
        "words_left": lines[7],
        "current_line": lines[8],
    }


def updateAccountFile(
    username,
    password,
    language,
    stat1,
    stat2,
    stat3,
    words_completed,
    words_left,
    current_line,
):
    file_path = f"{username}.txt"
    lines = [
        username,
        password,
        language,
        str(stat1),
        str(stat2),
        str(stat3),
        str(words_completed),
        str(words_left),
        str(current_line),
    ]
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

# need to display the login screen first and if they get both right proceed to the logged in screen
with open("Sourashtra.txt", "w", encoding="utf-8") as file_variable:
    file_variable.write(words)

#with open("Sourashtra.txt", "w", encoding="utf-8") as file_variable:
        #file_variable.write()

with open("Sourashtra.txt", "r", encoding="utf-8") as file_variable:
        variable_name = file_variable.read()
 
#login screen:
# Initialize session state for panel tracking
if "panel" not in sl.session_state:
    sl.session_state.panel = "login/create"

if "current_user" not in sl.session_state:
    sl.session_state.current_user = None

# --- PANEL 1: HOME ---
if sl.session_state.panel == "login/create":
    user_name = sl.text_input("Enter your name:")
    password = sl.text_input("Enter your password:", type="password")
    if sl.button("Log In"):
        account_data = readAccountFile(user_name)
        if account_data and account_data["password"] == password:
            sl.session_state.current_user = account_data
            sl.session_state.panel = "home"
            sl.rerun()
        else:
            sl.error("Incorrect username or password!")

    if sl.button("Don't have an account? Create One:"):
        sl.session_state.panel = "create"
        sl.rerun()

# --- PANEL 2: SECOND PANEL ---
elif sl.session_state.panel == "create":
    sl.title("Enter a Username and Password")
    sl.write("Fill out to Create a new account:")
    new_username = sl.text_input("Enter your username:")
    new_password = sl.text_input("Enter your password:", type="password")

    if sl.button("Create Account"):
        if new_username.strip() == "" or new_password.strip() == "":
            sl.warning("Please enter both username and password.")
        elif os.path.exists(f"{new_username}.txt"):
            sl.error("Account already exists!")
        else:
            createAccountFile(new_username, new_password)
            sl.session_state.current_user = readAccountFile(new_username)
            sl.session_state.panel = "home"
            sl.rerun()

    if sl.button("Back to Home"):
        sl.session_state.panel = "login/create"
        sl.rerun()
#logged in screen
elif sl.session_state.panel == "home":
    user_data = sl.session_state.current_user
    sl.title(f"Hi, {user_data['username']}")
    sl.write(f"Language: {user_data['language']}")
    #layout
    scol1, scol2, scol3 = sl.columns(3)
    with scol1:
        with sl.container(border=True):
            sl.write("Stat 1 Place holder")
    with scol2:
        with sl.container(border=True):
            sl.write("Stat 2 Place holder")
    with scol3:
        with sl.container(border=True):
            sl.write("Stat 3 Place holder")

    with open("Sourashtra.txt", "r", encoding="utf-8") as f:
        vocab_lines = [
            line.strip() for line in f.readlines() if line.strip()
        ]

    total_words = len(vocab_lines) if len(vocab_lines) > 0 else 1
    completed = int(user_data["words_completed"])
    completion_percentage = round((completed / total_words) * 100, 1)

    bcol1, bcol2, bcol3 = sl.columns([2, 1, 2])
    with bcol1:
        with sl.container(border=True):
            sl.write("Practice Flashcards")
            if sl.button("Start Flashcards"):
                sl.session_state.panel = "flashcards"
                sl.rerun()

    with bcol2:
        with sl.container(border=True):
            sl.write(f"{language}Total Progress: {completion_percentage}%")

    with bcol3:
        with sl.container(border=True):
            sl.write("Practice MCQs")
            if sl.button("Start MCQs"):
                sl.session_state.panel = "mcq"
                sl.rerun()

    with sl.container(border=True):
        sl.write(f"Words left in current set: {user_data['words_left']}")
# PANEL 4 FLASHCARDS PRACTICE
elif sl.session_state.panel == "flashcards":
    sl.title("Flashcards Practice")
    user_data = sl.session_state.current_user
    current_idx = int(user_data["current_line"])

    with open("Sourashtra.txt", "r", encoding="utf-8") as f:
        vocab_lines = [line.strip() for line in f.readlines() if line.strip()]

    if current_idx < len(vocab_lines):
        raw_line = vocab_lines[current_idx]

        # splitting at the first space so translarion is after
        if " " in raw_line:
            parts = raw_line.split(" ", 1)
            left_word = parts[0].strip()  # Sourashtra word
            right_translation = parts[1].strip()  # English translation
        else:
            left_word = raw_line
            right_translation = "translation coming"

        # make sure answer visibility state
        if "show_answer" not in sl.session_state:
            sl.session_state.show_answer = False

        sl.write(f"Word #{current_idx + 1} of {len(vocab_lines)}:")

        # the flashcard container
        with sl.container(border=True):
            sl.subheader("Sourashtra:")
            sl.title(left_word)  # Displays the left word in large text

            # Reveal button for translation
            if sl.button("Show Answer"):
                sl.session_state.show_answer = True

            if sl.session_state.show_answer:
                sl.write("---")
                sl.subheader("English Translation:")
                sl.info(right_translation)

        sl.write("")

        # refresh the screen for tyhe new word
        if sl.button("Mark as Mastered & Next"):
            new_completed = int(user_data["words_completed"]) + 1
            new_left = int(user_data["words_left"]) - 1
            new_line = current_idx + 1

            if new_left <= 0:
                new_left = 10  # Reset set countdown when set hits 0

            # Reset reveal toggle for next card
            sl.session_state.show_answer = False

            updateAccountFile(
                user_data["username"],
                user_data["password"],
                user_data["language"],
                user_data["stat1"],
                user_data["stat2"],
                user_data["stat3"],
                new_completed,
                new_left,
                new_line,
            )

            sl.session_state.current_user = readAccountFile(
                user_data["username"]
            )
            sl.rerun()

    else:
        sl.success("You have completed all available words!")

    if sl.button("Back to Dashboard"):
        sl.session_state.show_answer = False
        sl.session_state.panel = "home"
        sl.rerun()

    # --- PANEL 5: MCQ PRACTICE ---
elif sl.session_state.panel == "mcq":
    sl.title("Multiple Choice Questions")
    sl.write("MCQ section coming soon!")

    if sl.button("Back to Dashboard"):
        sl.session_state.panel = "home"
        sl.rerun()
    sl.text(name)








