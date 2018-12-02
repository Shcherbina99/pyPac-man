class Ghost:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def go(self, game):
        path = game.FindPaths(self, game.player)
        if path is not None and len(path) != 0:
            point = path.pop(-1)
            self.x = point[0]
            self.y = point[1]
