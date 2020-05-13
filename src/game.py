
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
    print ("selected test is {}".format(info.selectedTest))
    id = db.insertTestResult(info.selectedTest, startTime, endTime)
    #db.getResultPosition(id, info.selectedTest)


    






def getMillis():
    return float('%.3f'%(time()))

