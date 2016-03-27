
# encoding: utf-8
'''
srtFix.srtFix -- shortdesc

srtFix.srtFix is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2015 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''
'''
Created on May 24, 2015

@author: Ziv
'''
import sys
import os
from getArgs import getParams
from parse import parse

__all__ = []
__version__ = 0.1
__date__ = '2015-05-24'
__updated__ = '2015-05-24'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

def getNextSub(f):
    #file is at a beginning of a sub
    #returns three strings, None if EOF was reached
    #handle multiple empty lines
    line = f.readline()
    while line == '\n':
        line=f.readline()
    text=''
    num=line[:-1] #remove \n
    time=f.readline()[:-1]
    for line in f:
        if line == '' or line == '\n': 
            #end of sub
            return (num, time, text[:-1])
        text += line
    else:#EOF reached
        return (None, None, None)
        
def convertSubTimetoSec(subTime):
    #receives sub time, 12 characters string in the format hh:mm:ss,mmm
    #where mmm is miliceconds
    #returns the time in seconds, type float
    res=parse('{h:d}:{m:d}:{s:d},{ms:d}', subTime)
    return res['ms']/1000+res['s']+res['m']*60+res['h']*3600

def convertSectoSubTime(sec):
    H = sec//3600
    remain=sec%3600
    M = remain//60
    remain=remain%60
    S = remain//1
    remain=remain%1
    Mili = (remain*1000)//1 #make it an integer
    res= '{0:0=2n}:{1:0=2n}:{2:0=2n},{3:0=3n}'.format(H,M,S,Mili)
    return res

def getMovieLenFromFile(fileName):
    with open(fileName, mode='r') as f:
        return getMovieLenFromStream(f)
    
def getMovieLenFromStream(f):
    try:
        if f.seekable():
            f.seek(0, 2)
            l=f.tell()
            f.seek(l-200, 0)
        else:
            print ('cannot seek file')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    f.readline()    #flush till next line
    "find a separating line - an empty line"
    for line in f:
        if line == '\n': break
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
    
def calculateOffset(params):
    "Handle case were endDiff wasn't specified"
    if params.endDiff == None: 
        params.endDiff = params.startDiff
        
    "Calculates the offsets depending on the time of the entry"        
    if params.direction == 'movie-before': 
        "subtitle needs to be earlier, will negate the values"
        params.startDiff = -params.startDiff
        params.endDiff   = -params.endDiff
    params.movieLen = getMovieLenFromFile(params.fname)
    return params

def correctTime(args, subTime):
    t=convertSubTimetoSec(subTime)
    resT=t+args.startDiff+((args.endDiff-args.startDiff)*(t/args.movieLen))
    if resT<0: resT=0
    return convertSectoSubTime(resT)

def processFile(args):
    try:
        inFile = open(args.fname, mode='r')
        outFile= open(args.outfname, mode='w')
        (num, time, text) = getNextSub(inFile)
        while num is not None:
            t1=correctTime(args, time[:12]) 
            t2=correctTime(args, time[17:])
            outFile.write(num+'\n') 
            outFile.write(t1+' --> '+t2+'\n') 
            outFile.write(text+'\n\n') 
            (num, time, text) = getNextSub(inFile)
        inFile.close()
        outFile.close()
        
    except:
        print("Unexpected error:", sys.exc_info()[0])
        print("out file name:%s\n" % args.outfname)
        raise
    
        
    
    return True
    
def main(argv=None): # IGNORE:C0111
    program_name = os.path.basename(sys.argv[0])
    try:
        args = getParams(argv)
        if DEBUG or TESTRUN:
            print ("file:%s, %s, Start diff:%d, End diff: %s\n" % (args.fname,
                    args.direction, args.startDiff, args.endDiff))
        args = calculateOffset(args)
        processFile(args)
        print ("Done.")
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception:
        if DEBUG or TESTRUN:
            print('exception') #raise e
        indent = len(program_name) * " "
        #sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == '__main__':
    if DEBUG:
        #sys.argv.append("-h")
        #sys.argv.append("-v")
        #sys.argv.append("-r")
        pass
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'srtFix.srtFix_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())