import sqlite3

db_name = 'trainer.db'

# in case the connection fails we should display an error prompting the user to run setup
conn = sqlite3.connect(db_name)

def getRecords():
    print('thats the score')



