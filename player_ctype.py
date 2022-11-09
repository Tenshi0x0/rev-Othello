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
last = 0


# class Node:
#     def __init__(self, g, color, fa):
#         self.g = copy.deepcopy(g)
#         self.n = 0
#         self.w = 0
#         self.color = color
#         self.fa = fa
#         self.sons = []

MAXN = 2000050

G = [0] * MAXN
N = [0] * MAXN
W = [0] * MAXN
C = [0] * MAXN
Fa = [0] * MAXN
Sons = [[] for i in range(MAXN)]
root = 0
tot_node = 0

random.seed(0)
# root = Node(None, None, None)
round_count = 0


@jit(nopython=True)
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
        global n, last
        self.candidate_list.clear()
        self.candidate_list = get_candidate_list(chessboard, COLOR)

        last = int(0)
        for i in range(n):
            for j in range(n):
                if chessboard[i][j] == COLOR_NONE: last += 1

        res = (-1, -1)
        if last < 13:
            for x, y in self.candidate_list:
                cur_g = nxt(copy.deepcopy(chessboard), x, y, COLOR)
                if dfs(-COLOR, cur_g) == -1:
                    res = (x, y)
                    break
                elif dfs(-COLOR, cur_g) == 0:
                    res = (x, y)

        if res[0] == -1: res = MCTS(chessboard, COLOR)
        if res[0] != -1: self.candidate_list.append(res)


@jit(nopython=True)
def get_candidate_list(chessboard, color):
    global n
    me = color
    op = -me
    idx = []
    for i in range(n):
        for j in range(n):
            if chessboard[i][j] == 0:
                idx.append((i, j))

    # get candidate_list
    res = []
    DIRS = [(-1, 0), (-1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1)]
    for x, y in idx:
        # find?
        fl = False
        for dx, dy in DIRS:
            if fl: break
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


@jit(nopython=True)
def nxt(g, x, y, cur_player):
    op_player = -cur_player
    g[x][y] = cur_player
    DIRS = [(-1, 0), (-1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1)]
    for dx, dy in DIRS:
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


@jit(nopython=True)
def result(g, color) -> int:
    n = len(g)
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


@jit(nopython=True)
def simulate(g, u_col, fa_col) -> int:
    me_color = u_col
    op_color = -me_color
    cur_last = last

    vals = [[40, -20, 1, 1, 1, 1, -20, 40], [-20, -35, 0, 0, 0, 0, -35, -20],
            [1, 0, 1, 1, 1, 1, 0, 1], [1, 0, 1, 2, 2, 1, 0, 1],
            [1, 0, 1, 2, 2, 1, 0, 1], [1, 0, 1, 1, 1, 1, 0, 1],
            [-20, -35, 0, 0, 0, 0, -35, -20], [40, -20, 1, 1, 1, 1, -20, 40]
            ]
    while cur_last > 6:
        me_candi = get_candidate_list(g, me_color)
        if not me_candi:
            op_candi = get_candidate_list(g, op_color)
            if not op_candi:
                break
            else:
                me_candi = op_candi
                me_color = -me_color
                op_color = -op_color

        x, y = -1, -1
        val = 1000
        for tx, ty in me_candi:
            nval = vals[tx][ty]
            if nval < val:
                val = nval
                x, y = tx, ty

        cur_last -= 1

        g = nxt(g, x, y, me_color)
        me_color = -me_color
        op_color = -op_color

    res = dfs(me_color, g)
    if me_color == fa_col:
        return res
    else:
        return -res


def backup(u: int, util):
    while u != 0:
        N[u] += 1
        W[u] += util
        util = -util
        u = Fa[u]


def UCT(u: int):
    C = 1.41
    if N[u] == 0:
        return 0
    return W[u] / N[u] + C * np.sqrt(np.log(N[Fa[u]]) / N[u])


def bestson(u: int) -> int:
    return max(Sons[u], key=UCT)


def sel(root: int) -> int:
    leaf = bestson(root)
    while Sons[leaf]:
        leaf = bestson(leaf)
    return leaf

def add(g, color, fa) -> int:
    global tot_node
    tot_node += 1

    G.append(g)
    C.append(color)
    W.append(0)
    N.append(0)
    Fa.append(fa)
    Sons.append([])

    return tot_node

def expand(u: int):
    candi = get_candidate_list(G[u], C[u])
    if not candi:
        Sons[u].append(add(G[u].copy(), -C[u], u))
        # u.sons.append(Node(copy.deepcopy(u.g), -u.color, u))
    else:
        for x, y in candi:
            son_g = nxt(G[u].copy(), x, y, C[u])
            Sons[u].append(add(son_g, -C[u], u))


def op_sel_son(root: int, cur_g, color) -> int:
    if len(Sons[root]) == 1:
        return Sons[root][0]
    else:
        for son in Sons[root]:
            if (G[son] == cur_g).all():
                return son
        return add(cur_g.copy(), color, 0)
        # return Node(copy.deepcopy(cur_g), color, None)


def MCTS(chessboard, color):  # return the det pair
    global root, round_count
    round_count += 1

    start_time = time.time()

    if round_count == 1 or not Sons[root]:
        root = add(chessboard.copy(), color, 0)
        # root = Node(copy.deepcopy(chessboard), color, None)
    else:
        root = op_sel_son(root, chessboard, color)

    candi = get_candidate_list(chessboard, color)
    if not candi:
        return -1, -1

    for x, y in candi:
        son_g = nxt(copy.deepcopy(chessboard), x, y, color)

        exist = False
        for cur_son in Sons[root]:
            if (G[cur_son] == son_g).all():
                exist = True
                break
        if exist:
            continue

        son = add(son_g, -color, root)
        Sons[root].append(son)
        # root.sons.append(son)
        backup(son, simulate(G[son].copy(), C[son], C[Fa[son]]))

    cnt = 0
    lim_time = 0
    if round_count == 1:
        lim_time = 3.8
    else:
        lim_time = 4.8
    while time.time() < start_time + lim_time:
        leaf = sel(root)
        expand(leaf)
        cnt += 1
        for son in Sons[leaf]:
            backup(son, simulate(G[son].copy(), C[son], C[Fa[son]]))
    print(cnt)

    val = -1
    res = (-1, -1)
    rec_son = 0
    for i in range(len(candi)):
        x, y = candi[i]
        son = Sons[root][i]

        nval = N[son] + W[son]
        if nval > val:
            val = nval
            rec_son = son
            res = (x, y)
    root = rec_son
    return res


@jit(nopython=True)
def dfs(color, g) -> int:
    candi = get_candidate_list(g, color)
    if not candi:
        op_candi = get_candidate_list(g, -color)
        if not op_candi:
            return result(g, color)
        return -dfs(-color, g)

    res = int(-1)
    for x, y in candi:
        son_g = nxt(g.copy(), x, y, color)
        t = -dfs(-color, son_g)
        if t == 1:
            return 1
        res = max(res, t)
    return res
