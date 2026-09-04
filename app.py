import streamlit as st

st.title("My Python Website")
st.write("Website in python without html")

with open("filename.txt", "w", encoding="utf-8") as file_variable:
    file_variable.write("This was inside the file that I wrote to")

with open("filename.txt", "r", encoding="utf-8") as file_variable:
        variable_name = file_variable.read()

st.text(variable_name)






