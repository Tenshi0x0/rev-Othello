import os

Awin = 0
Bwin = 0
Draw = 0

if __name__ == '__main__':
    tot = 20
    for i in range(tot):
        os.system("python train_test.py")
    for i in range(tot):
        os.system("python train_test2.py")
    # print(Awin)
    # print(Bwin)
    # print(Draw)
