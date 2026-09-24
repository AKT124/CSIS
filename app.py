import streamlit as sl

from Sourashtra_File import words
from Sourashtra_File import name

import os


def create_account_file(username, password, language="Sourashtra"):
    file_path = f"{username}.txt"
    lines = [
        username,  # Line 0 (1st row)
        password,  # Line 1 (2nd row)
        language,  # Line 2 (3rd row)
        "0",  # Line 3 (4th row - Stat 1)
        "0",  # Line 4 (5th row - Stat 2)
        "0",  # Line 5 (6th row - Stat 3)
        "0",  # Line 6 (7th row - Total words completed)
        "10",  # Line 7 (8th row - Words left to master)
    ]
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

def read_account_file(username):
    file_path = f"{username}.txt"
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file.readlines()]
    if len(lines) < 8:
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
    }

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
        account_data = read_account_file(user_name)
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
            create_account_file(new_username, new_password)
            sl.session_state.current_user = read_account_file(new_username)
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

    bcol1, bcol2, bcol3 = sl.columns([2,1,2])
    with bcol1:
        with sl.container(border=True):
            sl.write("Flashcards link placeholder")
    with bcol2:
        with sl.container(border=True):
            sl.write("Total % words")
    with bcol3:
        with sl.container(border=True):
            sl.write("MCQs link Placeholder")


    with sl.container(border=True):
        sl.write("words mastered till next set placeholder")

    sl.text(name)

def createAccount(username, password, languageLearning ):
    with open(username+".txt", "w", encoding="utf-8") as file_variable:
        file_variable.write(username+"\n")
        file_variable.write(password+"\n")
        file_variable.write(languageLearning+"\n")
        file_variable.write(username+"\n")







