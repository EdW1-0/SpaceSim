import unittest

from timingMaster import TimingMaster


class TestTimingMaster(unittest.TestCase):
    def testTimingMaster(self):
        self.assertTrue(TimingMaster)

    def testTimingMasterAttributes(self):
        tm = TimingMaster()
        self.assertTrue(hasattr(tm, "timestamp"))
        self.assertTrue(hasattr(tm, "running"))
        self.assertTrue(hasattr(tm, "increment"))

    def testTimingMasterConstructor(self):
        self.assertTrue(TimingMaster())
        tm = TimingMaster(0)
        self.assertTrue(tm)
        self.assertEqual(tm.timestamp, 0)
        self.assertEqual(TimingMaster(3780).timestamp, 3780)


class TestTimingMasterStartStop(unittest.TestCase):
    def setUp(self):
        self.tm = TimingMaster(0)

    def testTimingMasterStart(self):
        self.assertFalse(self.tm.running)
        self.tm.start()
        self.assertTrue(self.tm.running)
        self.tm.stop()
        self.assertFalse(self.tm.running)

    def testTimingMasterTick(self):
        start = self.tm.timestamp
        self.tm.tick()
        end = self.tm.timestamp
        self.assertEqual(start, end)

    def testTimingMasterIncrease(self):
        start = self.tm.timestamp
        self.tm.start()
        self.tm.tick()
        self.tm.stop()
        end = self.tm.timestamp
        self.assertNotEqual(start, end)
        self.assertEqual(start + self.tm.increment, end)
