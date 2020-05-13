
import sqlite3
from time import time
from .model.Info import Info


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
            CREATE TABLE IF NOT EXISTS testsResult(
                id integer PRIMARY KEY ,
                startedAt REAL,
                finishedAt REAL,
                testId INTEGER
            )
        """
    }

    def __init__(s, config={}):
        db_name = 'trainer.db' if not 'db' in config else config['db']
        s.db_name = db_name
        s.conn = sqlite3.connect(db_name)

    def resetConn(s):
        s.conn.close()
        s.conn = sqlite3.connect(s.db_name)

    def dropAll(s):
        c = s.conn.cursor()
        table_names = s.getTables()
        for t in table_names:
            #if t == 'sqlite_sequence': continue
            q = "drop table '{}'".format(t)
            c.execute(q)

    def getTables(s):
        c = s.conn.cursor()
        table_names = c.execute("select name from sqlite_master where type = 'table'").fetchall()
        return [x[0] for x in table_names]


    def createDb(s):
        for k, v in s.createQueries.items():
            s.conn.execute(v)

    def populateInfo(s, name):
        c = s.conn.cursor()
        q = "INSERT INTO info (userName, createdAt) VALUES (?, ?)"
        secTime = time()
        res = c.execute(q, [name, secTime])
        id = c.lastrowid
        s.conn.commit()
        return id

    def addTest(s, testName, testString ):
        c = s.conn.cursor()
        q = "INSERT INTO tests (name, content, createdAt) VALUES (?, ?, ?)"
        vals = (testName, testString, time())
        res = c.execute(q, vals)
        id = c.lastrowid
        s.conn.commit()
        return id

    def updateTest(s, id, testName, testString ):
        c = s.conn.cursor()
        q = "UPDATE tests set name = ?, content = ?, updatedAt = ? where id = ?"
        vals = (testName, testString, time(), id)
        res = c.execute(q, vals)
        id = c.lastrowid
        s.conn.commit()
        return id

    def insertTestResult(s, testId, startedAt, finishedAt):
        c = s.conn.cursor()
        q = "insert into testsResult (testId, startedAt, finishedAt) values (?, ?, ?)"
        res = c.execute(q, (testId, startedAt, finishedAt))
        id = c.lastrowid
        s.conn.commit()
        return id
        


    def getTestsWithRecords(s):
        c = s.conn.cursor()
        q = '''select M.id, M.name, M.content, M.createdAt, M.updatedAt, T.id, T.startedAt, T.finishedAt
            from tests M inner join testsResult T on M.id=T.testId '''
        cur = c.execute(q)
        res = cur.fetchall()


    def getInfo(s, userName=''):
        c = s.conn.cursor()
        q = '''select M.id, M.userName, M.createdAt, M.selectedTest, T.name, T.content from info M
            left join tests T on M.selectedTest = T.id
        ''' 

        if userName!= '':
            q = q + 'where userName = "{}"'.format(userName)

        res = c.execute(q)
        userTup = res.fetchone()
        info = Info(id = userTup[0], name = userTup[1], createdAt = userTup[2],
                selectedTest = userTup[3], testName=userTup[4], testContent=userTup[5])
        return info

    def updateUserInfo(s, userName, updateDic):
        c = s.conn.cursor()
        setString = ','.join([ str(k) + '=' + str(v) for k, v in updateDic.items()])
        q = 'update info set {} where userName = "{}"'.format(setString,  userName)
        res = c.execute(q)
        return s.getInfo(userName)

    def getResultPosition(s, id, testId):
        c = s.conn.cursor()
        q = '''select row_number () over ( order by (M.finishedAt - M.startedAt)) rowNumber, (M.finishedAt - M.startedAt) as duration, M.id, M.startedAt,  T.name
        from testsResult M join tests T on T.id = M.testId
        where M.testId = {} '''.format(testId)

        res = c.execute(q)
        arr = c.fetchall()

        for i, item in enumerate(arr):
            if item[2] == id:
                return i + 1



