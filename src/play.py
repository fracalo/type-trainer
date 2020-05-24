
from time import time 
from .utils import getMillis

class Play():
    def __init__(s, db, selectedUser, selectedTest, ctx_input = input):
        s.db = db
        s.selectedUser = selectedUser 
        s.selectedTest = selectedTest 
        s.ctx_input = ctx_input

        s.intro()

    def intro(s):
        print ("selected test is => {}".format(s.selectedTest['name']))
        print ("content:")
        print (s.selectedTest['content'])
        _ = s.ctx_input("When you press ENTER the game will start")
        s.start()



    def start(s):
        startTime = getMillis()
        txt = s.ctx_input("GOOOOO !!!\n\n")

        if (txt != s.selectedTest['content']):
            print("You loose...")
            return
            
        endTime = getMillis()
        diff = endTime - startTime
        print("You completed the test in {} seconds".format(diff))
        id = s.db.insertTestResult(s.selectedTest['id'], startTime, endTime)
        position = s.db.getResultPosition(id, s.selectedTest['id'])

        print("This test is positioned {}".format(position))
        s.id = id
        s.position = position






