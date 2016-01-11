# -*- coding: utf_8 -*-
'''
Created on May 24, 2015

@author: Ziv
'''
import unittest
from getArgs import fixParams
from srtFix.main import convertSubTimetoSec, correctTime
from srtFix.main import getNextSub, calculateOffset, convertSectoSubTime
from io import StringIO
from unittest.mock import MagicMock
import srtFix

class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_convertSubTimetoSec(self):
        res=convertSubTimetoSec('02:13:25,416')
        self.assertEqual(res, 8005.416, '02:13:25,416: error')
        res=convertSubTimetoSec('00:00:00,000')
        self.assertEqual(res, 0.0, '00:00:00,000: error')

    def test_getNextSub(self):
        #replacing the open function
        Data1='''1457
02:13:33,481 --> 02:13:36,447
English text

1458
02:13:37,147 --> 02:13:38,513
Second sub text
contains too lines

'''
        f=StringIO(Data1)
        (num, time, text) = getNextSub(f)
        self.assertTrue(num == '1457', 'num')
        self.assertTrue(time == '02:13:33,481 --> 02:13:36,447', 'time')
        self.assertTrue(text == 'English text', 'text')
        Data1='''1457
02:13:33,481 --> 02:13:36,447
English text


1458
02:13:37,147 --> 02:13:38,513
Second sub text
contains too lines

'''
        f=StringIO(Data1)
        (num, time, text) = getNextSub(f)
        self.assertTrue(num == '1457', 'num')
        self.assertTrue(time == '02:13:33,481 --> 02:13:36,447', 'time')
        self.assertTrue(text == 'English text', 'text')
        Data2='''1458
02:13:37,147 --> 02:13:38,513
Second sub text
contains too lines

'''
        s2='''Second sub text\ncontains too lines'''
        f=StringIO(Data2)
        (num, time, text) = getNextSub(f)
        self.assertTrue(num == '1458', 'num')
        self.assertTrue(time == '02:13:37,147 --> 02:13:38,513', 'time')
        self.assertTrue(text == s2, 'text')

        f=StringIO('')
        (num, time, text) = getNextSub(f)
        self.assertTrue(num == None, 'At EOF')

        f=StringIO('\n')
        (num, time, text) = getNextSub(f)
        self.assertTrue(num == None, 'Single empty line')

    def test_calculateOffset(self):
        srtFix.main.getMovieLenFromFile=MagicMock(return_value=3)
        args=fixParams()
        args.direction,args.endDiff,args.startDiff='movie-before',2,3.3
        res=calculateOffset(args)
        self.assertTrue(res.direction  == args.direction and
                         res.endDiff   == -2             and
                         res.startDiff == -3.3           and
                         res.movieLen  == 3,
                         'Movie-Before, with end-diff')

        args.direction,args.startDiff,args.endDiff='movie-after',4.2,None
        res=calculateOffset(args)
        self.assertTupleEqual((res.direction, res.endDiff,res.startDiff),
                              (args.direction, 4.2, 4.2),
                         'Movie-after, without end-diff')

    def test_convertSectoSubTime1(self):
        self.assertEqual('00:00:00,000', convertSectoSubTime(0),
                         'Zeros')
            
    def test_convertSectoSubTime2(self):
        self.assertEqual('01:01:01,001', convertSectoSubTime(3661.001),
                         'Ones')

    def test_correctTime1(self):
        a=fixParams(d='Movie-Before',s=4,e=4,m=3600)
        r=correctTime(a,'00:00:00,000')
        self.assertEqual(r, '00:00:04,000', '4, 4, start')
        r=correctTime(a,'00:30:00,000')
        self.assertEqual(r, '00:30:04,000', '4, 4, middle')
        r=correctTime(a,'00:01:00,000')
        self.assertEqual(r, '00:01:04,000', '4, 4, end')
        
    def test_correctTime2(self):
        a=fixParams(d='Movie-Before',s=4,e=-4,m=3600)
        r=correctTime(a,'00:00:00,000')
        self.assertEqual(r, '00:00:04,000', '4, -4, start')
        r=correctTime(a,'00:30:00,000')
        self.assertEqual(r, '00:30:00,000', '4, -4, middle')
        r=correctTime(a,'01:00:00,000')
        self.assertEqual(r, '00:59:56,000', '4, -4, end')
        
    def test_correctTime3(self):
        a=fixParams(d='Movie-After',s=-4,e=4,m=3600)
        r=correctTime(a,'00:00:00,000')
        self.assertEqual(r, '00:00:00,000', '-4, 4, start')
        r=correctTime(a,'00:00:10,000')
        self.assertEqual(r, '00:00:06,022', '-4, 4, start')
        r=correctTime(a,'00:30:00,000')
        self.assertEqual(r, '00:30:00,000', '-4, 4, middle')
        r=correctTime(a,'01:00:00,000')
        self.assertEqual(r, '01:00:04,000', '-4, 4, end')
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()