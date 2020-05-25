
from time import time 
from .utils import getMillis, getWordsMin
from printy import printy

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
        printy (s.selectedTest['content'], '<o')
        _ = s.ctx_input("When you press ENTER the game will start")
        print('')
        s.start()



    def start(s):
        startTime = getMillis()

        #########################
        if s.ctx_input == None:
            print("GOOOOO !!!\n\n")
            txt = s.feed_test_by_line()

            if (txt != s.selectedTest['content']):
                print("You loose...")
                return
        #########################
        else:
            txt = s.ctx_input("GOOOOO !!!\n\n")

            if (txt != s.selectedTest['content']):
                print("You loose...")
                return
            
        endTime = getMillis()
        diff = endTime - startTime
        print("\nYou completed the test in {} seconds".format(diff))
        print('Words / Min: {}'.format('%.2f'%(getWordsMin(diff, s.selectedTest['content']))))

        id = s.db.insertTestResult(s.selectedTest['id'], startTime, endTime, s.selectedUser.id)
        position = s.db.getResultPosition(id, s.selectedTest['id'])

        print("This test is positioned {}".format(position))
        s.id = id
        s.position = position

    def feed_test_by_line(s):
        byLine = s.selectedTest['content'].split('\n')
        acc = []
        i = 0
        while i < len(byLine):
            printy(byLine[i], 'm>')
            line = input()
            acc.append(line)
            i = i + 1

        return '\n'.join(acc)






