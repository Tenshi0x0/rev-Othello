import copy

import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
COLOR = 0
INF = 0x3f3f3f3f
lim_dep = 7
n = 0
resx = -1
resy = -1

random.seed(0)


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


def cal(g):
    ret = 0
    for i in range(n):
        for j in range(n):
            ret += vals[i][j] * g[i][j]
    return -ret * COLOR


class AI(object):
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        self.color = color
        self.time_out = time_out
        self.candidate_list = []
        global n, COLOR
        n = chessboard_size
        COLOR = color

    def go(self, chessboard):
        me = self.color
        op = -me
        global n, resx, resy, lim_dep
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

        resx = -1
        resy = -1

        chessboard_backup = copy.deepcopy(chessboard)

        if len(idx) < 30: lim_dep = 8;
        elif len(idx) < 20: lim_dep = 9;
        elif len(idx) < 10: lim_dep = 10;
        self.dfs(-INF, INF, True, self.color, 0, chessboard_backup)
        if resx != -1: self.candidate_list.append((resx, resy))

    def dfs(self, a, b, is_max, me, dep, g):
        global n, resx, resy
        op = -me
        idx = np.where(g == COLOR_NONE)
        idx = list(zip(idx[0], idx[1]))
        # find the son points
        son = []
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

                    if g[kx][ky] == op:
                        while g[kx][ky] == op:
                            kx += dx
                            ky += dy
                            if is_out(kx, ky, n):
                                ok = False
                                break

                        if is_out(kx, ky, n) or g[kx][ky] != me:
                            ok = False

                        if ok: fl = True

            if fl:
                son.append((x, y))

        # cannot find the drop or limited (in fact, we can continue search...)

        if len(son) == 0 or dep == lim_dep:
            return cal(g)

        np.random.shuffle(son)
        # print('orz')
        if is_max:
            for x, y in son:
                tmp = copy.deepcopy(g)
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0: continue

                        ok = True
                        kx = x + dx
                        ky = y + dy
                        if is_out(kx, ky, n): continue

                        if tmp[kx][ky] == op:
                            tx = kx
                            ty = ky
                            while tmp[kx][ky] == op:
                                kx += dx
                                ky += dy
                                if is_out(kx, ky, n):
                                    ok = False
                                    break

                            if is_out(kx, ky, n) or tmp[kx][ky] != me:
                                ok = False

                            if ok:
                                kx = tx
                                ky = ty
                                while tmp[kx][ky] == op:
                                    tmp[kx][ky] = me  # flip
                                    kx += dx
                                    ky += dy
                # search down
                new_a = self.dfs(a, b, not is_max, -me, dep + 1, g)
                g = copy.deepcopy(tmp)
                if new_a > a:
                    a = new_a
                    if dep == 0:
                        resx, resy = x, y
                if a >= b:
                    break
            # print((a, b))
            return a

        else:
            for x, y in son:
                tmp = copy.deepcopy(g)
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx == 0 and dy == 0: continue

                        ok = True
                        kx = x + dx
                        ky = y + dy
                        if is_out(kx, ky, n): continue

                        if tmp[kx][ky] == op:
                            tx = kx
                            ty = ky
                            while tmp[kx][ky] == op:
                                kx += dx
                                ky += dy
                                if is_out(kx, ky, n):
                                    ok = False
                                    break

                            if is_out(kx, ky, n) or tmp[kx][ky] != me:
                                ok = False

                            if ok:
                                kx = tx
                                ky = ty
                                while tmp[kx][ky] == op:
                                    tmp[kx][ky] = me  # flip
                                    kx += dx
                                    ky += dy
                # search down
                new_b = self.dfs(a, b, not is_max, -me, dep + 1, g)
                g = copy.deepcopy(tmp)
                if new_b < b:
                    b = new_b

                if a >= b:
                    break
            # print((a, b))
            return b
