import time

import numpy as np

import playerB
import playerA

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
Aturn = -1
Bturn = 1
# Aturn, Bturn = Bturn, Aturn
DIRS = [(-1, 0), (-1, -1), (-1, 1), (0, 1), (0, -1), (1, 0), (1, 1), (1, -1)]
n = 8
g = np.zeros((n, n))

A = playerA.AI(n, Aturn, 5)
B = playerB.AI(n, Bturn, 5)

cur_player = -1


def is_out(x, y, n):
    if x < 0 or x >= n or y < 0 or y >= n: return True
    return False


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
        for dx, dy in DIRS:
            if dx == 0 and dy == 0: continue
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


def going():
    A.candidate_list = get_candidate_list(g, Aturn)
    B.candidate_list = get_candidate_list(g, Bturn)
    return len(A.candidate_list) != 0 or len(B.candidate_list) != 0


#########################################################################

if __name__ == "__main__":
    g[3][3] = g[4][4] = 1
    g[3][4] = g[4][3] = -1

    while going():
        if cur_player == Aturn and len(A.candidate_list) == 0:
            cur_player = Bturn
        elif cur_player == Bturn and len(B.candidate_list) == 0:
            cur_player = Aturn

        start = time.time()
        x = -1
        y = -1
        if cur_player == Aturn:
            A.go(g)
            x, y = A.candidate_list.pop()
            # print(x, y)

        if cur_player == Bturn:
            B.go(g)
            x, y = B.candidate_list.pop()

        op_player = cur_player * (-1)

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

        g[x][y] = cur_player

        cur_player *= -1

        # print(g)

        # for i in range(n):
        #     for j in range(n):
        #         if g[i][j] == Aturn:
        #             print('O ', end='')
        #         elif g[i][j] == Bturn:
        #             print('X ', end='')
        #         else:
        #             print('. ', end='')
        #     print('')
        # print('')

        # print(time.time() - start)

    ############################################################################################

    # judge winner

    Acnt = 0
    Bcnt = 0

    for i in range(0, n):
        for j in range(0, n):
            if g[i][j] == Aturn:
                Acnt += 1
            elif g[i][j] == Bturn:
                Bcnt += 1

    #  print final result: g
    for i in range(0, n):
        print(g[i])

    print(Acnt)

    if Acnt < Bcnt:
        print("A wins!")
    elif Acnt > Bcnt:
        print("B wins!")
    else:
        print("DRAW!")
