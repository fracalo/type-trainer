import subprocess
from time import time 
import re
import sqlite3
from time import sleep

def printHeader ():
    sleep(.1)
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
                else:
                    exit('Exiting')
    return wrapper


lowerSnake = lambda s: s.lower().replace(' ', '_')

def toMap(keyFunc, arr):
    return { keyFunc(x): x for x in arr}

def clearConsole():
    #print(chr(27) + "[2J")
    print("\033c", end="")

def getMillis(t = None):
    t = t if t is not None else time()
    return float('%.3f'%(t))

def multilineInput(q):
    acc = []
    line = input(q)
    while line != '':
        acc.append(line)
        line = input()

    return '\n'.join(acc)

def getWordsMin(duration, test):
    return (60 / duration) * (len(test) / 5)
