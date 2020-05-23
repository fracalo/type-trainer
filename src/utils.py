import subprocess
import re
import sqlite3
from time import sleep

def printHeader ():
    c = 'figlet Type Trainer'
    process = subprocess.Popen(c.split())
    sleep(.1)

def yOrN(q):
    answer = ''
    while answer[:1].lower() != 'y' and answer[:1].lower() != 'n':
        answer = input(q) 
    return answer == 'y'

def checkDbCreated(func):
    def wrapper(s):
        try:
            return func(s)
        except sqlite3.OperationalError:
                print('''
sqlite3.OperationalError ->
we assume this is happening because you have not initialized the DB schema,
the provided dbPath is {}
    '''.format(s.db.db_name))
                initDb = yOrN('Do you want to initialize DB in this path?[y/n]')
                if initDb:
                    s.db.createDb()
                    #print('Resetting method')
                    return func(s)
                    exit('asdf')
                else:
                    exit('Exiting')
    return wrapper


lowerSnake = lambda s: s.lower().replace(' ', '_')

def toMap(keyFunc, arr):
    return { keyFunc(x): x for x in arr}

