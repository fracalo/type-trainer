import inquirer

   

def createTest(db):
    testString = input('Create a test:\n')

    print('you inserted\n')
    print(testString)
    name = input('\nTo confirm add the name otherwise ctrl C to cancel.\n')
    id = db.addTest(name, testString)
    return id
    

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
    print('{} chose test {}'.format(info.name, id))


    db.updateUserInfo(info.name, {'selectedTest': id})

    
     
def showTests(db):
    tests = db.getAllTests()
    for  test in tests:
        print('{} - {} - {}'.format(test['id'], test['name'], test['content']))

    






    
