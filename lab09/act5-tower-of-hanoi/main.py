'''
    Tower of Hanoi
    Author: Abhi Jain
'''

import argparse
n = argparse.ArgumentParser()
n.add_argument("n", type=int)
args = n.parse_args()
n = args.n

moves = []

def hanoi(n, src, aux, dst):
    if n == 1:
        moves.append(f"{src} {dst}")
        return
    hanoi(n-1, src, dst, aux)
    moves.append(f"{src} {dst}")
    hanoi(n-1, aux, src, dst)

hanoi(n, 1, 2, 3)
print(len(moves))
for m in moves:
    print(m)
