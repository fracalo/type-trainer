
import sqlite3
from time import time


class DB:
    conn = None
    createQueries = {
        'infoTableSql': """
            CREATE TABLE IF NOT EXISTS info(
                id integer PRIMARY KEY ,
                createdAt REAL,
                selectedTest INTEGER,
                userName TEXT
            )
        """,
        'createTestsTableSql' : """
            CREATE TABLE IF NOT EXISTS tests(
                id integer PRIMARY KEY ,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                createdAt REAL,
                updatedAt REAL
            )
        """,
        'createTestsResultsTableSql' : """
            CREATE TABLE IF NOT EXISTS testsResults(
                id integer PRIMARY KEY ,
                startedAt REAL,
                finishedAt REAL
                testId INTEGER
            )
        """
    }

    def __init__(self, config={}):
        db_name = 'trainer.db' if not 'db' in config else config['db']
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)

    def resetConn(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.db_name)

    def dropAll(self):
        c = self.conn.cursor()
        table_names = self.getTables()
        for t in table_names:
            #if t == 'sqlite_sequence': continue
            q = "drop table '{}'".format(t)
            print(q)
            c.execute(q)

    def getTables(self):
        c = self.conn.cursor()
        table_names = c.execute("select name from sqlite_master where type = 'table'").fetchall()
        return [x[0] for x in table_names]


    def createDb(self):
        for k, v in self.createQueries.items():
            print('executing {}'.format(k))
            self.conn.execute(v)

    def populateInfo(self, name):
        c = self.conn.cursor()
        q = "INSERT INTO info (userName, createdAt) VALUES (?, ?)"
        secTime = time()
        res = c.execute(q, [name, secTime])
        id = c.lastrowid
        self.conn.commit()
        return id

    def addTest(self, testName, testString ):
        c = self.conn.cursor()
        q = "INSERT INTO tests (name, content, createdAt) VALUES (?, ?, ?)"
        vals = (testName, testString, time())
        res = c.execute(q, vals)
        id = c.lastrowid
        self.conn.commit()
        return id

    def updateTest(self, id, testName, testString ):
        c = self.conn.cursor()
        q = "UPDATE tests set name = ?, content = ?, updatedAt = ? where id = ?"
        vals = (testName, testString, time(), id)
        res = c.execute(q, vals)
        id = c.lastrowid
        self.conn.commit()
        return id

    def getInfo(self):
        c = self.conn.cursor()
        q = "select * from info"
        res = c.execute(q)
        userTup = res.fetchone()
        userProps = ['id', 'createdAt', 'selectedTest', 'name']
        user = {x[1]: userTup[x[0]] for x in enumerate(userProps)}
        return user



if __name__ == '__main__':
    db = DB()
    #db.dropAll()
    #db.createDb()
    #db.populateInfo('ciccio')
    #db.addTest('primo test', ''' function() {
    #  return 42
    #}''')
    #db.updateTest(1, 'primo test bis', 'come quando fuori piove')
    db.getInfo()

