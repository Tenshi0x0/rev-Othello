import copy

import numpy as np
import random
import time

from numba import jit

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
COLOR = 0
n = 0

random.seed(0)


def is_out(x, y, n):
    if x < 0 or x >= n or y < 0 or y >= n: return True
    return False


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
        global n
        self.candidate_list.clear()
        self.candidate_list = get_candidate_list(chessboard, COLOR)

        last = int(0)
        for i in range(n):
            for j in range(n):
                if chessboard[i][j] == COLOR_NONE: last += 1

        res = MCTS(chessboard, COLOR)
        if res[0] != -1: self.candidate_list.append(res)


class Node:
    def __init__(self, g, color, fa):
        self.g = copy.deepcopy(g)
        self.n = 0
        self.w = 0
        self.color = color
        self.fa = fa
        self.sons = []


def get_candidate_list(chessboard, color):
    global n
    me = color
    op = -me
    idx = np.where(chessboard == COLOR_NONE)
    idx = list(zip(idx[0], idx[1]))

    # get candidate_list
    res = []
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
            res.append((x, y))
    return res


def nxt(g, x, y, cur_player):
    op_player = -cur_player
    g[x][y] = cur_player
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0: continue

            ok = True
            kx = x + dx
            ky = y + dy
            if is_out(kx, ky, n): continue

            if g[kx][ky] == op_player:
                tx = kx
                ty = ky
                while g[kx][ky] == op_player:
                    kx += dx
                    ky += dy
                    if is_out(kx, ky, n):
                        ok = False
                        break

                if is_out(kx, ky, n) or g[kx][ky] != cur_player:
                    ok = False

                if ok:
                    kx = tx
                    ky = ty
                    while g[kx][ky] == op_player:
                        g[kx][ky] = cur_player  # flip
                        kx += dx
                        ky += dy
    return g


def result(g, color) -> int:
    global n
    x, y = 0, 0
    for i in range(n):
        for j in range(n):
            if g[i][j] == color:
                x += 1
            elif g[i][j] == -color:
                y += 1
    if x < y:
        return 1
    elif x == y:
        return 0
    elif x > y:
        return -1


def simulate(u: Node) -> int:
    g = copy.deepcopy(u.g)
    me_color = u.color
    op_color = -me_color
    while True:
        me_candi = get_candidate_list(g, me_color)
        if not me_candi:
            op_candi = get_candidate_list(g, op_color)
            if not op_candi:
                break
            else:
                me_candi = op_candi
                me_color = -me_color
                op_color = -op_color

        x, y = random.choice(me_candi)

        g = nxt(g, x, y, me_color)
        me_color = -me_color
        op_color = -op_color

    return result(g, u.fa.color)


def backup(u: Node, util):
    while u:
        u.n += 1
        u.w += util
        util = -util
        u = u.fa


def UCT(u: Node):
    C = 1.41
    return u.w / u.n + C * np.sqrt(np.log(u.fa.n) / u.n)


def bestson(u: Node) -> Node:
    return max(u.sons, key=UCT)


def sel(root: Node) -> Node:
    leaf = bestson(root)
    while leaf.sons:
        leaf = bestson(leaf)
    return leaf


def expand(u: Node):
    candi = get_candidate_list(u.g, u.color)
    if not candi:
        u.sons.append(Node(copy.deepcopy(u.g), -u.color, u))
    else:
        for x, y in candi:
            son_g = nxt(copy.deepcopy(u.g), x, y, u.color)
            u.sons.append(Node(son_g, -u.color, u))


def MCTS(chessboard, color):  # return the det pair
    start_time = time.time()
    root = Node(copy.deepcopy(chessboard), color, None)
    candi = get_candidate_list(chessboard, color)
    if not candi:
        return -1, -1
    for x, y in candi:
        son_g = nxt(copy.deepcopy(chessboard), x, y, color)
        son = Node(son_g, -color, root)
        root.sons.append(son)
        backup(son, simulate(son))

    cnt = 0
    while time.time() < start_time + 0.5:
        leaf = sel(root)
        expand(leaf)
        cnt += 1
        for son in leaf.sons: backup(son, simulate(son))
    print(cnt)

    val = -1
    res = (-1, -1)
    for i in range(len(candi)):
        x, y = candi[i]
        son = root.sons[i]
        if son.w / son.n > val:
            val = son.w / son.n
            res = (x, y)
    return res
