import inquirer
import datetime

db_name = 'trainer.db'


def getScoreboardForCurrentTest(db):
    info = db.getInfo()

    results = db.getTestResult(info.selectedTest)
    for result in results:
        d = datetime.datetime.fromtimestamp(result['startedAt'])
        formattedTime = d.strftime('%Y-%m-%d %H:%M:%S')

        print('{} - {}'.format(formattedTime, result['duration']))




