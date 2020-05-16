import unittest
import tempfile
import os
from src.db import DB 
from src.game import game
from time import time
from time import sleep

tempDir = tempfile.gettempdir()
dbPath = tempDir + '/test_db_trainer.db'

class TestGame(unittest.TestCase):

     
    def setUp(cls): 
        if os.path.isfile(dbPath):
            os.remove(dbPath)
        #game gets an instance of db in the constructor
        cls.db = DB({'db': dbPath})
        cls.db.createDb()
        cls.db.populateInfo('Gino')
        cls.testId = cls.db.addTest('Gino', 'function ciao() { return "Ciao" }')
        cls.db.updateUserInfo('Gino', {"selectedTest": cls.testId})

    def mocked_input(s, mockedResponses):
        i = 0
        i = i+1
        def curried(_):
            sleep(mockedResponses[i]['wait'])

            return mockedResponses[i]['text']
        return curried

    def test_creation_of_game_2_1_3(s):
        game(s.db, s.mocked_input([
            {"text":'/n', "wait": .3},
            {"text":'function ciao() { return "Ciao" }', "wait": .2}
        ]))

        game(s.db, s.mocked_input([
            {"text":'/n', "wait": .2},
            {"text":'function ciao() { return "Ciao" }', "wait": .15}
        ]))

        game(s.db, s.mocked_input([
            {"text":'/n', "wait": .1},
            {"text":'function ciao() { return "Ciao" }', "wait": .22}
        ]))

        pos1 = s.db.getResultPosition(1, s.testId)
        pos2 = s.db.getResultPosition(2, s.testId)
        pos3 = s.db.getResultPosition(3, s.testId)

        s.assertEqual(pos1, 2)
        s.assertEqual(pos2, 1)
        s.assertEqual(pos3, 3)

    def test_creation_of_game_3_2_1(s):
        game(s.db, s.mocked_input([
            {"text":'/n', "wait": .3},
            {"text":'function ciao() { return "Ciao" }', "wait": .2}
        ]))

        game(s.db, s.mocked_input([
            {"text":'/n', "wait": .2},
            {"text":'function ciao() { return "Ciao" }', "wait": .15}
        ]))

        game(s.db, s.mocked_input([
            {"text":'/n', "wait": .1},
            {"text":'function ciao() { return "Ciao" }', "wait": .1}
        ]))

        pos1 = s.db.getResultPosition(1, s.testId)
        pos2 = s.db.getResultPosition(2, s.testId)
        pos3 = s.db.getResultPosition(3, s.testId)

        s.assertEqual(pos1, 3)
        s.assertEqual(pos2, 2)
        s.assertEqual(pos3, 1)

        

        


if __name__ == '__main__':
    unittest.main()
