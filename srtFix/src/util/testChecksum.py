'''
Created on May 11, 2017
Test files taken from http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
@author: Ziv
'''
import inspect
import os
import unittest

import checksum


class TestCheckSum(unittest.TestCase):

    def setUp(self):
      TestCheckSum.tstDataDir=os.path.dirname(inspect.getfile(TestCheckSum))+"\\test-data"
      pass

    def tearDown(self):
      pass

    def testFiles(self):
      ''' runs a list of test cases on different files'''
      tData=({'fl':"not-exist",'rc':"IOError"},
             {'fl':TestCheckSum.tstDataDir+"\\test-eng.srt",  'rc':"SizeError"},
             {'fl':TestCheckSum.tstDataDir+"\\breakdance.avi",'rc':'8e245d9679d31e12'}
             #''{'fl':TestCheckSum.tstDataDir+"\\test-data\\dummy.bin",     'rc':'61f7751fc2a72bfb'}
             # commented out due to size of file (4G).
             )
      for td in tData:
        with self.subTest(td):
          self.ChkFile(td['fl'],td['rc'])

    def ChkFile(self, fl, rc):
      '''Perform a single test case'''
      try:
        res=checksum.hashFile(fl)
        self.assertTrue(rc == res,
                      "Input file:{}, expected ret val:{}, actual ret val:{}.".format(
                        fl, rc,res))
      except AssertionError:
        raise
      except Exception as e:
        print (e)
        self.fail("Exception occured:"+e.output())
        pass
      else:
        pass
      finally:
        pass



if __name__=="__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
