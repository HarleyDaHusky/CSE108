class Schedule:
    def __init__(self, classNum, department, number, name, credits, days, start, end, average):
        self.classNum = classNum
        self.department = department
        self.number = number
        self.name = name
        self.credits = credits 
        self.days = days
        self.start = start
        self.end = end
        self.average = average

    def print(self):
        print("COURSE " + self.classNum + ": " + self.department + self.number + ": " + self.name)
        print("Number of Credits: " + self.credits)
        print("Days of Lectures: " + self.days)
        print("Lecture Time: " + self.start + " –    " + self.end)
        print("Stat: on average, students get " + average + " in this course\n")

with open("classesInput.txt", "r") as file:
    line = file.readline()
    count = 1
    file_contents = ""
    while line:
        file_contents += line
        line = file.readline()
        count += 1

count = 1
classes = 1
classType = ""
classID = ""
className = ""
units = ""
days = ""
startTime = ""
endTime = ""
average = ""
for line in file_contents.split("\n"):
    if count==1:
        classType = line
        count+=1
    elif count==2:
        classID = line
        count+=1
    elif count==3:
        className = line
        count+=1
    elif count==4:
        units = line
        count+=1
    elif count==5:
        days = line
        count+=1
    elif count==6:
        startTime = line
        count+=1
    elif count==7:
        endTime = line
        count+=1
    elif count==8:
        average = line
        test = Schedule(str(classes), classType, classID, className, units, days, startTime, endTime, average)
        test.print()
        count = 1
        classes += 1