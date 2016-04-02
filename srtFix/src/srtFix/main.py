
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
from processFile import calculateOffset
from processFile import processFile

__all__ = []
__version__ = 0.1
__date__ = '2015-05-24'
__updated__ = '2015-05-24'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

    
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