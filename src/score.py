import inquirer
import datetime
from printy import printy
from .utils import getMillis, getWordsMin


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
                printy('=> {} - {}s'.format(formattedTime, '%.3f'%(result['duration'])), 'bm')
            else:
                print('   {} - {}s - {} (words/min {})'.format(
                    formattedTime,
                    '%.3f'%(result['duration']),
                    result['userName'],
                    '%.2f'%(getWordsMin(result['duration'], s.selectedTest['content']))
                ))









