
import sqlite3
from time import time
from .model.Info import Info
from .model.User import User


class DB:
    conn = None
    createQueries = {
        'infoTableSql': """
            CREATE TABLE IF NOT EXISTS info(
                id integer PRIMARY KEY ,
                createdAt REAL,
                selectedTest INTEGER,
                userName TEXT,
                userMail TEXT
            )
        """,
        'createTestsTableSql' : """
            CREATE TABLE IF NOT EXISTS tests(
                id integer PRIMARY KEY ,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                createdAt REAL
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

    def populateInfo(s, name, mail = ''):
        c = s.conn.cursor()
        q = "INSERT INTO info (userName, createdAt, userMail) VALUES (?, ?, ?)"
        secTime = time()
        res = c.execute(q, [name, secTime, mail])
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
        


    #def getTestsWithRecords(s):
    #    c = s.conn.cursor()
    #    q = '''select M.id, M.name, M.content, M.createdAt, M.updatedAt, T.id, T.startedAt, T.finishedAt
    #        from tests M inner join testsResult T on M.id=T.testId '''
    #    cur = c.execute(q)
    #    res = cur.fetchall()


    def getInfo(s, userName='', mail=''):
        c = s.conn.cursor()
        q = '''select M.id, M.userName, M.userMail, M.createdAt, M.selectedTest,T.name, T.content from info M
            left join tests T on M.selectedTest = T.id
        ''' 

        if userName!= '':
            q = q + 'where M.userName = "{}"'.format(userName)
        if userName != '' and mail!= '':
            q = q + ' and M.userMail = "{}"'.format(userName)


        res = c.execute(q)
        userTup = res.fetchone()

        if userTup == None:
            return None
        
        info = User(id = userTup[0], name = userTup[1], mail = userTup[2], createdAt = userTup[3],
                selectedTest = userTup[4])
        return info

    #def getAllUsers(s):
    #    c = s.conn.cursor()
    #    q = '''select M.id, M.userName, M.userMail, M.createdAt, M.selectedTest, T.name, T.content from info M
    #        left join tests T on M.selectedTest = T.id
    #    ''' 
    #    res = c.execute(q)
    #    usersTup = res.fetchall()

    #    users = [Info(id = userTup[0], name = userTup[1], mail= userTup[2], createdAt = userTup[3],
    #            selectedTest = userTup[4], testName=userTup[5], testContent=userTup[6]) for userTup in usersTup]
    #    return users

    def getAllUsers(s):
        c = s.conn.cursor()
        q = 'select id, userName, userMail, createdAt, selectedTest from info' 
        res = c.execute(q)
        usersTup = res.fetchall()

        users = [User(id = userTup[0], name = userTup[1], mail= userTup[2], createdAt = userTup[3],
                selectedTest = userTup[4]) for userTup in usersTup]
        return users

    def updateUserInfo(s, userName, updateDic):
        c = s.conn.cursor()
        setString = ','.join([ str(k) + '=' + str(v) for k, v in updateDic.items()])
        q = 'update info set {} where userName = "{}"'.format(setString,  userName)
        res = c.execute(q)
        s.conn.commit()
        return s.getInfo(userName)

    def updateUserInfoById(s, id, updateDic):
        c = s.conn.cursor()
        setString = ','.join([ str(k) + '=' + str(v) for k, v in updateDic.items()])
        q = 'update info set {} where id = "{}"'.format(setString,  id)
        res = c.execute(q)
        s.conn.commit()
        return id 

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


    def getAllTests(s):
        c = s.conn.cursor()
        q = 'select id, name, content from tests'
        res = c.execute(q)
        arr = c.fetchall()
        return [{'id': x[0], 'name': x[1], 'content': x[2]} for x in arr]

    def deleteTest(s, id):
        c = s.conn.cursor()
        q = 'delete from tests where id = {}'.format(id)
        q2 = 'update info set selectedTest = null where selectedTest = {}'.format(id)
        res = c.execute(q)
        res2 = c.execute(q2)
        s.conn.commit()

    def getTestResult(s, id):
        c = s.conn.cursor()
        q = 'select id, startedAt, (finishedAt - startedAt) as duration from testsResult where testId = {}'.format(id)
        res = c.execute(q)
        arr = c.fetchall()
        return [{'startedAt': x[1], 'duration': x[2]} for x in arr]

    def getTests(s, name, txt):
        c = s.conn.cursor()
        q = 'select id, name, content from tests where name = "{}" and content = "{}"'.format(name, txt)
        res = c.execute(q)
        arr = c.fetchall()
        return [{'id': x[0], 'name': x[1], 'content': x[2]} for x in arr]

    def getTestById(s, id):
        c = s.conn.cursor()
        q = 'select id, name, content from tests where id = "{}"'.format(id)
        res = c.execute(q)
        x = c.fetchone()
        return {'id': x[0], 'name': x[1], 'content': x[2]}



