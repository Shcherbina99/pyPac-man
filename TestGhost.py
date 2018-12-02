import unittest
import Game

class MyTestCase(unittest.TestCase):
    def test_something(self):
        game = Game("Test1")
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
