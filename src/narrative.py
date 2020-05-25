from .utils import printHeader, lowerSnake, yOrN, checkDbCreated, toMap, clearConsole
import inquirer
import sqlite3
from .play import Play 
from .score import Scoreboard


class Narrative():
    def __init__(s, db, selectedUser = None, selectedTest = None):
        s.db = db
        s.selectedUser = selectedUser 
        s.selectedTest = selectedTest 
        s.welcome()

    def welcome(s):
        printHeader()
        
        print("hello {}".format(
            (s.selectedUser and s.selectedUser.name)
            or "Stranger")
        )

        if s.selectedTest:
            print ("selected test is => {}".format(s.selectedTest['name']))

        choices =[
            'Select an existing player',
            'Create a new player'
        ]

        if s.selectedUser:
            choices.append('Select an existing test')
            choices.append('Create a new test')
            choices.append('Delete a test')

        if s.selectedTest:
            choices = ['Play', 'Show scoreboard for selected test'] + choices


        question = [
            inquirer.List(
                "first",
                message="what do you want to do?",
                choices=choices
            )
        ]

        answer = inquirer.prompt(question)
        methodName = lowerSnake(answer['first'])
        m = getattr(s,methodName )
        m()

    @checkDbCreated
    def select_an_existing_player(s):
        users = s.db.getAllUsers()
        if len(users) == 0:
            print('No users in db, before anything add a user')
            return s.create_a_new_player()


        byUserMail= toMap(
            lambda user: "{} - {}".format(user.name, user.mail),
            users
        )


        question = [
            inquirer.List(
                "user",
                message="Select a user from the list?",
                choices=byUserMail,
            )
        ]


        answer = inquirer.prompt(question)
# once we get here this will end the first stage of the game
# at this point we'll clear console and relaunch welcome with the choosen user
        user = byUserMail[answer['user']]
        # we reset selectedTest to None
        s.selectedTest = None
        s.selectedUser = user
        if user.selectedTest:
            test = s.db.getTestById(user.selectedTest)
            s.selectedTest = test

        clearConsole()
        s.welcome()

 
    @checkDbCreated
    def create_a_new_player(s):
        print('Enter your info')
        name = input('name:')
        while(name == ''):
            print('name field is required')
            name = input('name:')

        mail = input('mail:')

        checkExistingUser = s.db.getInfo(name, mail)
        if checkExistingUser:
            print('Error: a user with the same name & mail exists')
            return s.create_a_new_player()


        s.db.populateInfo(name, mail=mail)
        print('{} - {} has been added correctly'.format(name, mail))
        clearConsole()
        s.welcome()


    def select_an_existing_test(s):
        test = s._select_a_test()
        s.selectedTest = test
        s.db.updateUserInfoById(
            s.selectedUser.id,
            { 'selectedTest': test['id'] }
        )
        s.welcome()

    def create_a_new_test(s):
        name = input('name:')
        while(name == ''):
            print('name field is required')
            name = input('name:')

        text = input('text:')

        try:
            checkExistingTest = s.db.getTests(name, text)
            if checkExistingTest:
                print('Error: a test with the same name & content exists')
                return s.create_a_new_test()
        except sqlite3.Error as err:
            print(err)


        s.db.addTest(name, text)
        print('{} - test has been added correctly'.format(name))
        s.welcome()

    def _select_a_test(s):
        tests = s.db.getAllTests()
        if len(tests) == 0:
            print('No tests in db, before anything add a test')
            return s.create_a_new_test()

        byTestName = toMap(
            lambda test: "{}".format(test['name']),
            tests
        )


        question = [
            inquirer.List(
                "test",
                message="Select a test from the list?",
                choices=byTestName,
            )
        ]

        answer = inquirer.prompt(question)
        return byTestName[answer['test']]

    def delete_a_test(s):
        test = s._select_a_test()
        if s.selectedTest and 'id' in s.selectedTest and s.selectedTest['id'] == test['id']:
            s.selectedTest = None
        s.db.deleteTest(test['id'])
        s.welcome()

    def play(s):
        p = Play(s.db, s.selectedUser, s.selectedTest)
        if hasattr(p, 'id'):
            score = Scoreboard(s.db, s.selectedUser, s.selectedTest, testId=p.id)


        retry = yOrN('Do you want to retry?[y/n]')
        if retry:
            s.play()
        else: 
            print('Game over')

    def show_scoreboard_for_selected_test(s):
        Scoreboard(s.db, s.selectedUser, s.selectedTest)

        


    

    

  
