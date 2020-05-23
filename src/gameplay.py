from .utils import printHeader, lowerSnake, yOrN, checkDbCreated, toMap
import inquirer
import sqlite3


class Narrative():
    def __init__(s, db):
        s.db = db
        s.welcome()
        #deleteId = answer['deleteTest']['id']

    def welcome(s):
        printHeader()
        print("hello stranger")

        question = [
            inquirer.List(
                "first",
                message="what do you want to do?",
                choices=[
                    'Select an existing player',
                    'Create a new player'
                    ]
            )
        ]

        answer = inquirer.prompt(question)
        methodName = lowerSnake(answer['first'])
        m = getattr(s,methodName )
        m()

    @checkDbCreated
    def select_an_existing_player(s):
        users = s.db.getAllUsers()
        print(users)
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
                choices=byUserMail.keys(),
            )
        ]


        answer = inquirer.prompt(question)
        print(byUserMail[answer['user']])

 
    @checkDbCreated
    def create_a_new_player(s):
        print('Enter your info')
        name = input('name:')
        while(name == ''):
            print('name field is required')
            name = input('name:')

        mail = input('mail:')

        checkExistingUser = s.db.getInfo(name, mail)
        print(checkExistingUser)
        if checkExistingUser:
            print('Error: a user with the same name & mail exists')
            return s.create_a_new_player()


        s.db.populateInfo(name, mail=mail)
        print('{} - {} has been added correctly'.format(name, mail))



    

    

  
