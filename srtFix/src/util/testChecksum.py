'''
Created on May 11, 2017

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


    def testNotExist(self):
        try:
          res=checksum.hashFile("not-exist")
          self.assertTrue("IOError" == res, "Should fail on file not found")
        except Exception as e:
          print (e)
          self.fail("Exception occured:"+e.output())
          pass
        else:
          pass
        finally:
          pass

    def testSmallFile(self):
        try:
          fl=os.environ['PROJECT_LOC']+"\\test-data\\test-eng.srt"
          res=checksum.hashFile(fl)
          self.assertTrue("SizeError" == res, 
                          "Input file:{}, expected ret val:{}, actual ret val:{}.".format(
                            fl,res, "SizeError"))
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
    print(os.environ['PROJECT_LOC'])
    
    unittest.main()
