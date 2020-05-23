import argparse
import tempfile
from .game import game
from .score import getScoreboardForCurrentTest 
from .setUp import config
from .db import DB
from .testConfig import createTest, deleteTest, showTests, chooseTest
from .gameplay import Narrative

##########################################################
# in main we parse all the arguments and decide what to do
parser = argparse.ArgumentParser(description='A python software for improving your typing skills')
parser.add_argument(
        '--score',
        dest='main',
        action='store_const',
        const='score',
        help='sum the integers (default: find the max)')

parser.add_argument(
        '-w', '--wtf',
        help='What is it that you\'re doing')

parser.add_argument(
        '-d', '--db',
        help='the sqlite3 db path (if none is configured we\'ll use the default)')


args = parser.parse_args()


mainLogic = {
        'score': getScoreboardForCurrentTest,
        'play': game,
        'createTest': createTest,
        'chooseTest': chooseTest,
        'deleteTest': deleteTest,
        'showTests': showTests,
        'config': config,
        None: Narrative
    }

tempDir = tempfile.gettempdir()
dbPath = tempDir + '/test_db_trainer.db' if not args.db else args.db
db = DB({'db': dbPath})
action = mainLogic[args.wtf]

def main():
    action(db)
