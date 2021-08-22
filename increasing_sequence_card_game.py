from utils import get_input
from random import choice

INPUT = """
5
10
20
30
40
50
"""
input = get_input(INPUT)(input)
def monter_carlo(n):
    cards = list(range(1, n+1))
    hand = choice(cards)
    cards.remove(hand)
    keep = 1
    while len(cards) > 0:
        take = choice(cards)
        if take > hand:
            keep+=1
            hand = take
        cards.remove(take)
    return keep

def solve_monter(n, times = 1000):
    scores = [monter_carlo(n) for _ in range(times)]
    return sum(scores)/len(scores)


def recursive_solve(cards, hand=None, keep=0):
    if hand is not None:
        cards = [c for c in cards if c > hand]
    if len(cards) <= 1:
        return keep+len(cards)
    prob = 1/len(cards)
    expected = [None for _ in range(len(cards))]
    for c, card in enumerate(cards):
        copycards = cards.copy()
        hand = copycards.pop(c)
        expected[c] = recursive_solve(copycards, hand, keep+1)
    return sum(expected)*prob


def solve(n):
    cards = list(range(1, n+1))
    return recursive_solve(cards)

for case in range(1, int(input())+1):
    N = int(input())
    print(f'Case #{case}: {solve(N)}')
