import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0

random.seed(0)

# vals = [
#     [70, -20, 20, 20, 20, 20, -15, 70],
#     [-20, -30, 5, 5, 5, 5, -30, -15],
#     [20, 5, 1, 1, 1, 1, 5, 20],
#     [20, 5, 1, 1, 1, 1, 5, 20],
#     [20, 5, 1, 1, 1, 1, 5, 20],
#     [20, 5, 1, 1, 1, 1, 5, 20],
#     [-20, -30, 5, 5, 5, 5, -30, -15],
#     [70, -15, 20, 20, 20, 20, -15, 70]
# ]

vals = [
    [65, -3, 6, 4, 4, 6, -3, 65],
    [-3, -29, 3, 1, 1, 3, -29, -3],
    [6, 3, 5, 3, 3, 5, 3, 6],
    [4, 1, 3, 1, 1, 3, 1, 4],
    [4, 1, 3, 1, 1, 3, 1, 4],
    [6, 3, 5, 3, 3, 5, 3, 6],
    [-3, -29, 3, 1, 1, 3, -29, -3],
    [65, -3, 6, 4, 4, 6, -3, 65],
]


def is_out(x, y, n):
    if x < 0 or x >= n or y < 0 or y >= n: return True
    return False


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []

    def go(self, chessboard):
        me = self.color
        op = -me
        n = self.chessboard_size
        self.candidate_list.clear()
        idx = np.where(chessboard == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))

        # get candidate_list
        for x, y in idx:
            # find?
            fl = False
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0: continue
                    # ok?
                    ok = True
                    kx = x + dx
                    ky = y + dy
                    if is_out(kx, ky, n): continue

                    if chessboard[kx][ky] == op:
                        while chessboard[kx][ky] == op:
                            kx += dx
                            ky += dy
                            if is_out(kx, ky, n):
                                ok = False
                                break

                        if is_out(kx, ky, n) or chessboard[kx][ky] != me:
                            ok = False

                        if ok: fl = True

            if fl:
                self.candidate_list.append((x, y))

        if len(self.candidate_list) == 0:
            return

        # get determine

        resx = 0
        resy = 0
        dis = 100
        for x, y in self.candidate_list:
            nval = vals[x][y]
            if nval < dis:
                dis = nval
                resx = x
                resy = y
        self.candidate_list.append((resx, resy))
