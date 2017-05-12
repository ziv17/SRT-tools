'''
Created on May 11, 2017
Test files taken from http://trac.opensubtitles.org/projects/opensubtitles/wiki/HashSourceCodes
@author: Ziv
'''
import os
import unittest

import checksum


class Test(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass


    def testFiles(self):
      tData=({'fl':"not-exist",'rc':"IOError"},
             {'fl':os.environ['PROJECT_LOC']+"\\test-data\\test-eng.srt",  'rc':"SizeError"},
             {'fl':os.environ['PROJECT_LOC']+"\\test-data\\breakdance.avi",'rc':'8e245d9679d31e12'}
             #''{'fl':os.environ['PROJECT_LOC']+"\\test-data\\dummy.bin",     'rc':'61f7751fc2a72bfb'}
             # commented out due to size of file (4G).
             )
      for td in tData:
        self.testFile(td['fl'],td['rc'])

    def testFile(self, fl, rc):
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
    suite = unittest.TestSuite()
    suite.addTest(Test('testFiles'))
    unittest.TextTestRunner().run(suite)
    
    # unittest.main()
