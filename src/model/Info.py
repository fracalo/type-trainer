

class Info:
    def __init__(s, id = None, name = None, createdAt = None, selectedTest = None):
        print ('id is {}',  id)
        print ('createdAt is {}',  createdAt)
        print ('name is {}',  name)
        s.id = id
        s.createdAt = createdAt
        s.selectedTest = selectedTest
        s.name = name

