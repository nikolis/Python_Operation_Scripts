import unittest


class TestStringMethods(unittest.TestCase):
    
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FfOO')


suite = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
unittest.TextTestRunner(verbosity=2).run(suite)
