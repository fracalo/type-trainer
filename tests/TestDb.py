import unittest
import tempfile
import os
from src.db import DB 
from time import time

tempDir = tempfile.gettempdir()
dbPath = tempDir + '/test_db_trainer.db'

class TestDb(unittest.TestCase):

    def setUp(s): 
        if os.path.isfile(dbPath):
            os.remove(dbPath)
        if hasattr(s, 'db'): 
            s.db.dropAll()
        s.db = DB({'db': dbPath})
        s.db.createDb()

    def test_creation_of_name_for_jane(s):
        s.db.populateInfo('Jane')
        info = s.db.getInfo()
        s.assertEqual(info.name, 'Jane')
        createdAtDiff= time() - info.createdAt
        s.assertTrue(createdAtDiff < 2000)
        s.assertEqual(info.testName, None)

    def test_adding_updating_the_first_text(s):
        txt='''
        Humpty dumpty had a 
        fall
        '''
        id = s.db.addTest('jane first test', txt)
        s.assertEqual(id, 1)
        res = s.db.updateTest(1, 'Hello tests', 'This is the new modified version of test 1')
        s.assertEqual(1, res)
        txt2='''
        On a
        farm there are some horses
        '''
        id = s.db.addTest('jane second test', txt)
        s.assertEqual(id, 2)


    #def test_getting_some_records_back(s):
    #    s.db.populateInfo('Jane')
    #    id = s.db.addTest('jane test', 'I can t write abracadabra')
    #    t = time()
    #    s.db.insertTestResult(1, t - 10000, t)
    #    recordTable = s.db.getTestsWithRecords()

    def test_using_getInfo_we_also_get_current_test(s):
        s.db.populateInfo('Jane')
        id = s.db.addTest('jane test', 'I can t write abracadabra')
        info = s.db.updateUserInfo('Jane', {'selectedTest': id})
        s.assertEqual(info.selectedTest, id)
        s.assertEqual(info.testContent, 'I can t write abracadabra')

        

        


if __name__ == '__main__':
    unittest.main()
