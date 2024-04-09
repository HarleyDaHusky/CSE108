# https://www.programiz.com/python-programming/methods/string/lower
# https://stackoverflow.com/questions/31845482/iterating-through-a-string-word-by-word 
# https://blog.enterprisedna.co/python-remove-punctuation-from-string/#:~:text=To%20remove%20punctuation%20from%20a,new%20string%20excluding%20punctuation%20marks.

import string

with open("PythonSummary.txt", "r") as file:
    line = file.readline()
    count = 1
    file_contents = ""
    while line:
        file_contents += line.lower()
        line = file.readline()
        count += 1

wordIn = input("Please enter a word: ")
wordIn = wordIn.lower()
times = 0

for word in file_contents.replace('-', " ").split(" "):
    word = word.translate(str.maketrans("", "", string.punctuation))
    if(wordIn == word):
        times += 1
print(times)
