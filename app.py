import streamlit as sl

from Sourashtra_File import words
from Sourashtra_File import name


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

# --- PANEL 1: HOME ---
if sl.session_state.panel == "login/create":
    sl.write("This content only shows on the Home panel.")
    user_name = sl.text_input("Enter your name:")
    password = sl.text_input("Enter your password:")
    if sl.button("Log In"):
        if user_name == "Arya" and password==password:# Check if the entered name matches later when you actually create the account file
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
#this needs tbe mdoified to create neqw file after they create a new account like an account file
    # Add any text, inputs, or columns for Panel 2 here:
    sl.write("Fill out to Create a new account:")
    user_name = sl.text_input("Enter your username:")
    password = sl.text_input("Enter your password:")

    if sl.button("Back to Home"):
        sl.session_state.panel = "login/create"
        sl.rerun()
#logged in screen
elif sl.session_state.panel == "home":
    sl.title("Hi, Arya")
    sl.write(name + ":")
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





