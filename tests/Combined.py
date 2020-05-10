import unittest
import TestDb
import TestGame

suiteList = [
    unittest.TestLoader().loadTestsFromTestCase(TestDb.TestDb),
    unittest.TestLoader().loadTestsFromTestCase(TestGame.TestGame)
]

combined  = unittest.TestSuite(suiteList)

unittest.TextTestRunner(verbosity = 0).run(combined)
