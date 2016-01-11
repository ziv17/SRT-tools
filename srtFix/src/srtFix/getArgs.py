#!/usr/local/bin/python2.7
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

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []
__version__ = 0.1
__date__ = '2015-05-24'
__updated__ = '2015-05-24'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class fixParams:
    def __init__(self, f=None, d=None,s=None,e=None,m=None,o=None):
        self.fname=f
        self.direction=d
        self.startDiff=s
        self.endDiff=e
        self.movieLen=m
        self.outfname=o

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def getParams(argv):
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)


    #program_version = "v%s" % __version__
    #program_build_date = str(__updated__)
    #program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = 'srtFix' #__import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2015 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    # Setup argument parser
    parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
    #parser.add_argument("-r", "--recursive", dest="recurse", action="store_true", help="recurse into subfolders [default: %(default)s]")
    #parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
    #parser.add_argument("-i", "--include", dest="include", help="only include paths matching this regex pattern. Note: exclude is given preference over include. [default: %(default)s]", metavar="RE" )
    #parser.add_argument("-e", "--exclude", dest="exclude", help="exclude paths matching this regex pattern. [default: %(default)s]", metavar="RE" )
    #parser.add_argument('-V', '--version', action='version', version=program_version_message)
    #parser.add_argument(dest="paths", help="paths to folder(s) with source file(s) [default: %(default)s]", metavar="path", nargs='+')
    parser.add_argument('direction', choices=['movie-before','movie-after'])
    parser.add_argument('-startDiff', type=float, required=True, 
                        help='difference at start of movie in seconds, e.g. 2.4')
    parser.add_argument('-endDiff', type=float, 
                        help='difference at END of movie in seconds, e.g. 2.4.')
    parser.add_argument('fileName')

    # Process arguments
    args = parser.parse_args()
    # checking the arguments
    if not os.path.exists(args.fileName):
        print('%(file)s: file does not exist' % {'file':args.fileName})
        args=None
    res = fixParams()
    res.direction = args.direction
    res.endDiff   = args.endDiff
    res.startDiff = args.startDiff
    res.fname     = args.fileName
    res.outfname  = args.fileName[:-4]+'.fixed'+args.fileName[-4:]
    return res


if __name__ == "__main__":
    pass