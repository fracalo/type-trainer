
import re
from time import time 
from src.db import DB 

def game(db):
    info = db.getInfo()
    text = info.testContent
    
    print("""
        Hello {},
        the chosen text for your typing test is: 

        "{}"
    """.format(info.name, text))
    _ = input("When you press ENTER the game will start")

    startTime = getMillis()
    txt = input("GOOOOO !!!\n\n")

    if (txt != text):
        print("you loose")
        return
        
    endTime = getMillis()
    diff = endTime - startTime
    print("You completed the test in {} seconds".format(diff))
    print ("selected test is {}".format(info.selectedTest))
    db.insertTestResult(info.selectedTest, startTime, endTime)
    print ('inserted..')
    print ('start is.. {}'.format(startTime))
    print ('endTime is.. {}'.format(endTime))







def getMillis():
    return float('%.3f'%(time()))

