import peertable.key
import unittest
import random


class TestKey(unittest.TestCase):

    def testInitDefaultRandom(self):
        rand = random.Random(1773)
        key = peertable.key.Key(rand=rand)
        self.assertEqual(
            key, b'j6\xc2\xc2Ls\x0c\xbe\x1d'
                 b'\\B\xd1\xd5\xb6oiem\xd0\x9d')
        self.assertEqual(
            str(key), '0x6a36c2c24c730cbe1d5'
                      'c42d1d5b66f69656dd09d')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 1)

    def testInitBucketsDefaultRandom(self):
        rand = random.Random(1773)
        key = peertable.key.Key(buckets=20, rand=rand)
        self.assertEqual(
            key, b'j6\xc2\xc2Ls\x0c\xbe\x1d'
                 b'\\B\xd1\xd5\xb6oiem\xd0\x9d')
        self.assertEqual(
            str(key), '0x6a36c2c24c730cbe1d5'
                      'c42d1d5b66f69656dd09d')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 1)

    def testInitStr(self):
        key = peertable.key.Key(value='1234')
        self.assertEqual(str(key), '0x31323334')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 130)

    def testInitStrEmpty(self):
        key = peertable.key.Key(value='')
        self.assertEqual(str(key), '0x0')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 159)

    def testInitBytes(self):
        key = peertable.key.Key(value=b'1234')
        self.assertEqual(str(key), '0x31323334')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 130)

    def testInitBytesEmpty(self):
        key = peertable.key.Key(value=b'')
        self.assertEqual(str(key), '0x0')
        self.assertEqual(len(key), 20)
        self.assertEqual(key.buckets, 20)
        self.assertEqual(key.prefix, 159)

    def testInitNoBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            peertable.key.Key(buckets=0)

    def testInitStrBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            peertable.key.Key(value='100', buckets=2)

    def testInitBytesBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            peertable.key.Key(value=b'100', buckets=2)

    def testInitByteArrayBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            peertable.key.Key(value=bytearray(1), buckets=2)

    def testInitTypeError(self):
        with self.assertRaises(TypeError):
            peertable.key.Key(value=0)

    def testStr(self):
        key = peertable.key.Key(value='\x01')
        self.assertEqual(str(key), '0x1')

    def testRepr(self):
        key = peertable.key.Key(value='\xff')
        self.assertEqual(repr(key), '0xff')

    def testXor(self):
        key1 = peertable.key.Key(value='34')
        key2 = peertable.key.Key(value='12')
        res = key1 ^ key2
        expect = peertable.key.Key(value='\x02\x06')
        self.assertEqual(res, expect)
        self.assertEqual(len(res), 20)
        self.assertEqual(res.buckets, 20)

    def testXorDifferentBucketsExpectValueError(self):
        with self.assertRaises(ValueError):
            key1 = peertable.key.Key(buckets=1)
            key2 = peertable.key.Key(buckets=2)
            key1 ^ key2

    def testRelativePrefix(self):
        key1 = peertable.key.Key(value='34', buckets=2)
        key2 = peertable.key.Key(value='12', buckets=2)
        res = key1.rprefix(key2)
        res2 = (key1 ^ key2).prefix
        self.assertEqual(res, 6)
        self.assertEqual(res, res2)

    def testBytePrefixerStr(self):
        p = peertable.key.Key._bp('a')
        self.assertEqual(p, 1)

    def testBytePrefixerZeroStr(self):
        p = peertable.key.Key._bp('\x00')
        self.assertEqual(p, 7)

    def testBytePrefixerBytes(self):
        p = peertable.key.Key._bp(b'9')
        self.assertEqual(p, 2)

    def testBytePrefixerZeroBytes(self):
        p = peertable.key.Key._bp(b'\x00')
        self.assertEqual(p, 7)

    def testBytePrefixerInt(self):
        p = peertable.key.Key._bp(255)
        self.assertEqual(p, 0)

    def testBytePrefixerZeroInt(self):
        p = peertable.key.Key._bp(0)
        self.assertEqual(p, 7)
