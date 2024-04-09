sentence = input("Enter Sentence: ")
amount = input("Enter amount of times: ")
with open("CompletedPunishment.txt", "w") as file:
    for x in range(int(amount)):
        file.write(sentence + "\n")
file.close()