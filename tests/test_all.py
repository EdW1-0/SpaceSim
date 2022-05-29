import unittest



if __name__ == '__main__':
    testSuite = unittest.defaultTestLoader.discover(".")
    runner = unittest.TextTestRunner()
    runner.run(testSuite)