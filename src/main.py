import argparse
import tempfile
from .db import DB
from .narrative import Narrative

##########################################################
# in main we parse all the arguments and decide what to do
parser = argparse.ArgumentParser(description='A python software for improving your typing skills')
parser.add_argument(
        '-d', '--db',
        help='the sqlite3 db path (if none is configured we\'ll use the default)')


args = parser.parse_args()



tempDir = tempfile.gettempdir()
dbPath = tempDir + '/test_db_trainer.db' if not args.db else args.db
db = DB({'db': dbPath})

def main():
    Narrative(db)
