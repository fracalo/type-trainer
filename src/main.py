import argparse
from .game import play
from .score import getRecords 

##########################################################
# in main we parse all the arguments and decide what to do
parser = argparse.ArgumentParser(description='A python software for improving your typing skills')
parser.add_argument(
        '--score',
        dest='main',
        action='store_const',
        const='score',
        help='sum the integers (default: find the max)')

parser.add_argument(
        '-w', '--wtf',
        help='What is it that you\'re doing')

args = parser.parse_args()

def nothingConfigured() :
    print('you got nothing configured')

mainLogic = {
        'score': getRecords,
        'play': play,
        None: nothingConfigured
    }

action = mainLogic[args.wtf]

def main():
    action()
    print("args.wtf {}".format(args.wtf))
    print("__name__ from main {}".format(__name__))
