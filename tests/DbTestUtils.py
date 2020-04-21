
from src.db import DB 
from time import time

class DbTestUtils(object):
    def __init__(self):
        self.db = DB({'db': 'test_db_trainer.db'})
        self.create_db()
        self._status = ''

    def create_db(self):
        self.db.createDb()

    def drop_all(self):
        self.db.dropAll()

    def setup_app(self, name):
        self.db.populateInfo(name)

    def name_should_be(self, name):
        info = self.db.getInfo()
        if info['name'] != name:
            raise AssertionError("name was supposed to be '%s' but was '%s'."
                                 % (name, info['name']))

    def created_at_should_be_less_than_a_second_ago(self):
        info = self.db.getInfo()
        difference = (time() - info['createdAt']) 
        if not difference < 2000:
            raise AssertionError("The time difference is '%s'" % (difference))

    def status_should_be(self, expected_status):
        if expected_status != self._status:
            raise AssertionError("Expected status to be '%s' but was '%s'."
                                 % (expected_status, self._status))
