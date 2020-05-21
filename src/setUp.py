import subprocess
from time import sleep
from .testConfig import createTest

def config(db, ctx_input=input):
    printHeader()
    sleep(1)
    print("Using DB '{}'".format(db.db_name))
    doReset = yOrN("If you continue the db in use will be reset, do you want to proceed?")
    if not doReset:
        exit('exiting...')

    db.dropAll()
    db.createDb()
    name = input('Name:')
    db.populateInfo(name)
    testId = createTest(db)
    db.updateUserInfo(name, {'selectedTest': testId})



    #doReset = input("If you continue the db in use will be reset, do you want to proceed?")



def printHeader ():
    c = 'figlet Type Trainer'
    process = subprocess.Popen(c.split())

def yOrN(q):
    answer = ''
    while answer[:1].lower() != 'y' and answer[:1].lower() != 'n':
        answer = input(q) 
    return answer == 'y'
