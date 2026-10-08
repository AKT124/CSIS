import streamlit as sl

from Sourashtra_File import words
from Sourashtra_File import name

import os


def createAccountFile(username, password, language="Sourashtra"):
    file_path = f"{username}.txt"
    lines = [
        username,  # Line 0
        password,  # Line 1
        language,  # Line 2
        "0",  # Line 3 (Flashcard Line)
        "0",  # Line 4 (MCQ Line)
        "0",  # Line 5 (Stat 3)
        "0",  # Line 6 (Total completed)
        "10",  # Line 7 (Words left)
        "0",  # Line 8 (Current line)
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
        "flashcard_line": lines[3],
        "mcq_line": lines[4],
        "stat3": lines[5],
        "words_completed": lines[6],
        "words_left": lines[7],
        "current_line": lines[8],
    }


def updateAccountFile(
    username,
    password,
    language,
    flashcard_line,
    mcq_line,
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
        str(flashcard_line),
        str(mcq_line),
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

    elif sl.session_state.panel == "home":
        user_data = sl.session_state.current_user

        with open("Sourashtra.txt", "r", encoding="utf-8") as f:
            vocab_lines = [line.strip() for line in f.readlines() if line.strip()]

        total_words = len(vocab_lines) if len(vocab_lines) > 0 else 1

        fc_completed = int(user_data["flashcard_line"])
        mcq_completed = int(user_data["mcq_line"])

        fc_pct = round((fc_completed / total_words) * 100, 1)
        mcq_pct = round((mcq_completed / total_words) * 100, 1)

        sl.title(f"Hi, {user_data['username']}")
        sl.write(f"Language: {user_data['language']}")

        scol1, scol2, scol3 = sl.columns(3)
        with scol1:
            with sl.container(border=True):
                sl.metric(
                    "Flashcards Progress",
                    f"{fc_pct}%",
                    f"{fc_completed}/{total_words} words",
                )
        with scol2:
            with sl.container(border=True):
                sl.metric(
                    "MCQ Progress",
                    f"{mcq_pct}%",
                    f"{mcq_completed}/{total_words} words",
                )
        with scol3:
            with sl.container(border=True):
                total_completed = int(user_data["words_completed"])
                sl.metric("Total Answers Completed", total_completed)

        bcol1, bcol2, bcol3 = sl.columns([2, 1, 2])
        with bcol1:
            with sl.container(border=True):
                sl.write("Practice Flashcards")
                if sl.button("Start Flashcards"):
                    sl.session_state.panel = "flashcards"
                    sl.rerun()

        with bcol2:
            with sl.container(border=True):
                sl.write(f"Active Language: {user_data['language']}")

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
    current_idx = int(user_data["flashcard_line"])

    with open("Sourashtra.txt", "r", encoding="utf-8") as f:
        vocab_lines = [line.strip() for line in f.readlines() if line.strip()]

    if current_idx < len(vocab_lines):
        raw_line = vocab_lines[current_idx]

        if " " in raw_line:
            parts = raw_line.split(" ", 1)
            left_word = parts[0].strip()
            right_translation = parts[1].strip()
        else:
            left_word = raw_line
            right_translation = "Translation missing"

        if "show_answer" not in sl.session_state:
            sl.session_state.show_answer = False

        sl.write(f"Flashcard #{current_idx + 1} of {len(vocab_lines)}:")

        with sl.container(border=True):
            sl.subheader("Sourashtra:")
            sl.title(left_word)

            if sl.button("Show Answer"):
                sl.session_state.show_answer = True

            if sl.session_state.show_answer:
                sl.write("---")
                sl.subheader("English Translation:")
                sl.info(right_translation)

        sl.write("")

        if sl.button("Mark as Mastered & Next"):
            new_fc_line = current_idx + 1
            new_completed = int(user_data["words_completed"]) + 1
            new_left = int(user_data["words_left"]) - 1

            if new_left <= 0:
                new_left = 10

            sl.session_state.show_answer = False

            updateAccountFile(
                user_data["username"],
                user_data["password"],
                user_data["language"],
                new_fc_line,
                user_data["mcq_line"],
                user_data["stat3"],
                new_completed,
                new_left,
                user_data["current_line"],
            )

            sl.session_state.current_user = readAccountFile(
                user_data["username"]
            )
            sl.rerun()

    else:
        sl.success("You have completed all flashcards!")

    if sl.button("Back to Dashboard"):
        sl.session_state.show_answer = False
        sl.session_state.panel = "home"
        sl.rerun()

    #panel 5: mcq practice
    elif sl.session_state.panel == "mcq":
        sl.title("Multiple Choice Quiz")
        user_data = sl.session_state.current_user
        current_idx = int(user_data["mcq_line"])

        with open("Sourashtra.txt", "r", encoding="utf-8") as f:
            vocab_lines = [line.strip() for line in f.readlines() if line.strip()]

        if current_idx < len(vocab_lines):
            raw_line = vocab_lines[current_idx]

            if " " in raw_line:
                parts = raw_line.split(" ", 1)
                target_word = parts[0].strip()
                correct_translation = parts[1].strip()
            else:
                target_word = raw_line
                correct_translation = "Translation missing"

            sl.write(f"MCQ #{current_idx + 1} of {len(vocab_lines)}:")

            with sl.container(border=True):
                sl.subheader("What is the English translation for:")
                sl.title(target_word)

                if (
                        "mcq_options" not in sl.session_state
                        or sl.session_state.get("mcq_current_idx") != current_idx
                ):
                    all_translations = []
                    for line in vocab_lines:
                        if " " in line:
                            trans = line.split(" ", 1)[1].strip()
                            if (
                                    trans != correct_translation
                                    and trans not in all_translations
                            ):
                                all_translations.append(trans)

                    distractors = random.sample(
                        all_translations, min(3, len(all_translations))
                    )
                    options = distractors + [correct_translation]
                    random.shuffle(options)

                    sl.session_state.mcq_options = options
                    sl.session_state.mcq_current_idx = current_idx

                selected_option = sl.radio(
                    "Select the correct answer:", sl.session_state.mcq_options
                )

                if sl.button("Submit Answer"):
                    if selected_option == correct_translation:
                        sl.success("Correct!")

                        new_mcq_line = current_idx + 1
                        new_completed = int(user_data["words_completed"]) + 1
                        new_left = int(user_data["words_left"]) - 1

                        if new_left <= 0:
                            new_left = 10

                        updateAccountFile(
                            user_data["username"],
                            user_data["password"],
                            user_data["language"],
                            user_data["flashcard_line"],
                            new_mcq_line,
                            user_data["stat3"],
                            new_completed,
                            new_left,
                            user_data["current_line"],
                        )

                        sl.session_state.current_user = readAccountFile(
                            user_data["username"]
                        )
                        sl.rerun()
                    else:
                        sl.error("Incorrect! Try again.")

        else:
            sl.success("You have completed all MCQ questions!")

        if sl.button("Back to Dashboard"):
            sl.session_state.panel = "home"
            sl.rerun()








