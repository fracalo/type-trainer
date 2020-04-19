
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
                name TEXT
            )
        """,
        'createTestsTableSql' : """
            CREATE TABLE IF NOT EXISTS tests(
                id integer PRIMARY KEY ,
                name TEXT NOT NULL,
                createdAt REAL,
                userId integer
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

    def __init__(self):
        db_name = 'trainer.db'
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
        #q = "insert into info ('createdAt', 'name') VALUES ({},'{}')".format(time(), name)
        q = "INSERT INTO info (name) VALUES (?)"
        print('q is {}'.format(q))
        res = c.execute(q, [name])
        self.conn.commit()
        print('res is {}'.format(res))



if __name__ == '__main__':
    db = DB()
    #db.printSqlVer()
    db.dropAll()
    
    db.createDb()
    db.populateInfo('ciccio')

