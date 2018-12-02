import unittest

from Game import *


class MyTestCase(unittest.TestCase):
    def test__init_fromText(self):
        game = Game("Test")
        self.assertEqual((1, 1), (game.player.x, game.player.y))
        self.assertEqual(25, len(game.chekings))

    def test__findPath(self):
        game = Game("Test1")
        path = game.FindPaths(game.ghosts[0], game.player)
        print(path[0])
        self.assertEquals(1, len(game.ghosts))
        self.assertEqual((1, 1), (game.player.x, game.player.y))
        self.assertEqual(24, len(game.chekings))


if __name__ == '__main__':
    unittest.main()
