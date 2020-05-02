
from src.db import DB 

text = 'ciao ciao micio bao'
def play(db):
    info = db.getInfo()
    #test = 
    print("""
        hello {},
        the chosen text for your typing test is: 
        "{}"
        when you press enter the game will start..
    """.format(info.name, text))



