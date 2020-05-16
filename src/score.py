import inquirer

db_name = 'trainer.db'


def getRecords(db):
    tests = db.getAllTests()

    questions = [
        inquirer.List(
            "deleteTest",
            message="Remove a test from the list",
            choices=tests
        )
    ]

    answer = inquirer.prompt(questions)
    id = answer['deleteTest']['id']

    testsResultsForId = db.getTestResult(id)



