import streamlit as sl

from Sourashtra_File import words
from Sourashtra_File import name

sl.title("Hi, Arya")
sl.write(name+":")

with open("Sourashtra.txt", "w", encoding="utf-8") as file_variable:
    file_variable.write(words)

#with open("Sourashtra.txt", "w", encoding="utf-8") as file_variable:
        #file_variable.write()

with open("Sourashtra.txt", "r", encoding="utf-8") as file_variable:
        variable_name = file_variable.read()

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
        sl.write("Total % words completed Placeholder")
with bcol3:
    with sl.container(border=True):
        sl.write("MCQs link Placeholder")
sl.text(name)






