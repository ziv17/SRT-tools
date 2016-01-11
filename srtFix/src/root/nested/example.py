'''
Created on May 18, 2015

@author: Ziv
'''
import os
import argparse
from io import SEEK_END
from parse import parse

def getParams():
    "get command line parameters"
    parser=argparse.ArgumentParser(prog="srtFix", description="Adjust subtitles timing")
    parser.add_argument('direction', choices=['movie-before','movie-after'])
    parser.add_argument('-startDiff', type=float, required=True, 
                        help='difference at start of movie in seconds, e.g. 2.4')
    parser.add_argument('-endDiff', type=float, 
                        help='difference at END of movie in seconds, e.g. 2.4.')
    parser.add_argument('fileName')
    args=parser.parse_args()
    print (args.fileName)
    # checking the arguments
    if not os.path.exists(args.fileName):
        print('%(file)s: file does not exist' % {'file':args.fileName})
        args=None
    return args
def getNextSub(f):
    #file is at a beginning of a sub
    #returns three strings, None if EOF was reached
    text=''
    num=f.readline()
    time=f.readline()
    for line in f:
        if line == '': 
            #end of file
            return (num, time, text)
        text.join(line)
    else:#EOF reached
        return (None, None, None)
        
def zzzzconvertSubTimetoSec(subTime):
    #receives sub time, 12 characters string in the format hh:mm:ss,mmm
    #where mmm is miliceconds
    #returns the time in seconds, type float
    res=parse('{h:d}:{m:d}:{s:d},{ms:d}', subTime)
    return res['ms']/1000+res['s']+res['m']*60+res['h']*3600

def getMovieLen(fileName):
    with open(fileName, mode='r') as f:
        f.seek(-200, SEEK_END)
        f.readline()    #flush till next line
        "find a separating line - an empty line"
        for line in f:
            if line == '': break
        else: print('empty line not found')
        #get the next sub
        (num, time, text) = getNextSub(f)
        #get the last sub
        (a, b, c) = getNextSub(f)
        while a is not None:
            (num, time, text) = (a, b, c) 
            (a, b, c) = getNextSub(f)
        #now we have the last sub    
        return convertSubTimetoSec(time[0:12])
    
def calculateOffset(args):
    "Handle case were endDiff wasn't specified"
    res = {} #declare res as a dictionary
    if args.endDiff == None: 
        res['endDiff'] = args.startDiff
    else:
        res['endDiff'] = args.endDiff
        
    "Calculates the offsets depending on the time of the entry"        
    if args.direction == 'movie-before': 
        "subtitle needs to be earlier, will negate the values"
        res['startDiff'] = -args.startDiff
        res['endDiff']   = -res['endDiff']
    res['fileName'] = args.fileName
    res['movieLen'] = getMovieLen(res['fileName'])
    return res

def processFile(shiftValues):
    return True
    
if __name__ == '__main__':
    args = getParams()
    shiftValues = calculateOffset(args)
    processFile(shiftValues)
    print (args)
    print (type(args))
