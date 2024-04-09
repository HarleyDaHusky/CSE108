import json

with open("grades.txt", "r") as file:
    grades = json.load(file)

def saveGrades(grades):
    with open("grades.txt", "w") as file:
        json.dump(grades, file)

def createGrade(grades): #1
    name = input("Enter Student's Full Name: ")
    grade = input("Enter Student Grade: ")
    grades[name] = grade
    saveGrades(grades)

def getGrades(grades): #2
    name = input("Enter Student's Full Name: ")
    if name in grades:
        print(f"{grades[name]}")
    else:
        print("Student not found")

def editGrades(grades): #3
    name = input("Enter student's full name to edit: ")
    if name in grades:
        newGrade = input("Enter new student grade: ")
        grades[name] = newGrade
        saveGrades(grades)
    else:
        print("Student not found")

def deleteGrade(grades): #4
    name = input("Enter student's full name to delete grade: ")
    if name in grades:
        del grades[name]
        saveGrades(grades)
    else:
        print("Student not found")

while True:
    print("1. Create a new Grade")
    print("2. Get a existing Grade")
    print("3. Edit a existing Grade")
    print("4. Delete a existing Grade")
    print("5. Print grade list")
    print("6. Exit")

    choice = input("Please enter your choice(1-6): ")
    choice = int(choice)
    if(choice == 1):
        createGrade(grades)
    elif(choice == 2):
        getGrades(grades)
    elif(choice == 3):
        editGrades(grades)
    elif(choice==4):
        deleteGrade(grades)
    elif(choice==5):
        print(grades)
    elif(choice==6):
        break
    else:
        print("Please enter a valid choice")