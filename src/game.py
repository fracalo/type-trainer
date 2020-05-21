
import re
from time import time 
from src.db import DB 

def game(db, ctx_input=input):
    info = db.getInfo()
    text = info.testContent
    
    print("""
        Hello {},
        the chosen text for your typing test is: 

        "{}"
    """.format(info.name, text))
    _ = ctx_input("When you press ENTER the game will start")

    startTime = getMillis()
    txt = ctx_input("GOOOOO !!!\n\n")

    if (txt != text):
        print("you loose")
        return
        
    endTime = getMillis()
    diff = endTime - startTime
    print("You completed the test in {} seconds".format(diff))
    id = db.insertTestResult(info.selectedTest, startTime, endTime)
    position = db.getResultPosition(id, info.selectedTest)

    print("This test is positioned {}".format(position))



    






def getMillis():
    return float('%.3f'%(time()))

