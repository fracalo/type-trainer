import subprocess
from time import sleep
from .testConfig import createTest
from .utils import yOrN, printHeader

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






