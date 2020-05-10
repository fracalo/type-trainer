import unittest
import tempfile
import os
from src.db import DB 
from src.game import game
from time import time

tempDir = tempfile.gettempdir()
dbPath = tempDir + '/test_db_trainer.db'

class TestGame(unittest.TestCase):

    @classmethod
    def setUpClass(cls): 
        if os.path.isfile(dbPath):
            os.remove(dbPath)
        #game gets an instance of db in the constructor
        cls.db = DB({'db': dbPath})
        cls.db.createDb()
        cls.db.populateInfo('Gino')
        testId = cls.db.addTest('Gino', 'function ciao() { return "Ciao" }')
        cls.db.updateUserInfo('Gino', {"selectedTest": testId})

        cls.game = game(cls.db)


    def test_creation_of_name_for_jane(s):
        print(s)
        #info = s.db.getInfo()
        #s.assertEqual(info.name, 'Gino')
        #createdAtDiff= time() - info.createdAt
        #s.assertTrue(createdAtDiff < 2000)
        #s.assertEqual(info.testName, None)


        

        


if __name__ == '__main__':
    unittest.main()
