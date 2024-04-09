# https://www.w3schools.com/python/gloss_python_raise.asp --- referenced to throw errors (raise command)
# https://rollbar.com/blog/python-typeerror-int-object-not-iterable/ --- While trying to look for solutions to TypeError for testing for strings, i was recommended trying Try and except

from pickle import FALSE
from tkinter import TRUE
#import numpy as np

numbers = input("Please enter 2 or more numbers: ")
listNumbers = numbers.split()
if len(listNumbers) < 2:
    print("You did not enter 2 or more numbers. Please enter 2 or more numbers.") 
else:
    total = 0
    breakpoint = TRUE
    for i in range(len(listNumbers)):
        if(listNumbers[i].isnumeric()==TRUE):
            total += int(listNumbers[i])
        else:
            breakpoint = FALSE

    if(breakpoint==TRUE):
        print(total)
    else:
        print("You did not enter only numbers")