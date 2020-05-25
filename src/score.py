import inquirer
import datetime
from printy import printy
from .utils import getMillis

db_name = 'trainer.db'



class Scoreboard():
    def __init__(s, db, selectedUser, selectedTest, testId = None):
        s.db = db
        s.selectedUser = selectedUser 
        s.selectedTest = selectedTest 
        s.testId = testId 
        s.scores = None
        s.printScores()

    def printScores(s):
        results = s.db.getTestResult(s.selectedTest['id'])
        for result in results:
            d = datetime.datetime.fromtimestamp(result['startedAt'])
            formattedTime = d.strftime('%Y-%m-%d %H:%M:%S')
            if s.testId and result['id'] == s.testId:
                printy('=> {} - {} <='.format(formattedTime, getMillis(result['duration'])), 'bm')
            else:
                print('   {} - {} ({})'.format(formattedTime, getMillis(result['duration']), result['userName']))









