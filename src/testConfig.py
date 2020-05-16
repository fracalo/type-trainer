import inquirer

def setTest(db, ctx_input=input):
    info = db.getInfo()

    questions = [
        inquirer.List(
            "testName",
            message="Chose a test",
            choices=['function', 'multiple return']
        )
    ]

    answer = inquirer.prompt(questions)
    print ('the answer is {}'.format( answer))
   

def createTest(db):
    testString = input('Create a test:\n')

    print('you inserted\n')
    print(testString)
    name = input('\nTo confirm add the name otherwise ctrl C to cancel.\n')
    db.addTest(name, testString)
    

def deleteTest(db):
    tests = db.getAllTests()

    questions = [
        inquirer.List(
            "deleteTest",
            message="Remove a test from the list",
            choices=tests
        )
    ]

    answer = inquirer.prompt(questions)
    deleteId = answer['deleteTest']['id']

    db.deleteTest(deleteId)

def chooseTest(db):
    info = db.getInfo()

    tests = db.getAllTests()

    questions = [
        inquirer.List(
            "test",
            message="Remove a test from the list",
            choices=tests
        )
    ]

    answer = inquirer.prompt(questions)
    id = answer['test']['id']
    print(info.name )
    print(id)


    db.updateUserInfo(info.name, {'selectedTest': id})

    
     
def showTests(db):
    tests = db.getAllTests()
    print (tests)

    






    
