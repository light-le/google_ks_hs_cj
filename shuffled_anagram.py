from utils import get_input
from random import shuffle
from collections import Counter

INPUTS = """
8
start
jjj
vuiewvuwnvywjre
jij
jeejjejejeeejj
huihhhiu
abcab
hfuihfuiewqhfuyqeghfyuwqcbfuyeqwgbfyuebwgfuvewbiqcefgxyuwygfuyewrcfgnuewxyreuwiygfuiwesgyfwqgrvbuqrhbndciuwqbhuywrgfyur
"""

input = get_input(INPUTS)(input)

def solve(s):
    ans = s.copy()
    # shuffle(s)
    s = s[1:] + [s[0]]
    for i in range(len(ans)):
        origin = ans[i]
        for l, c in enumerate(s):
            if ans[i] != c:
                ans[i] = c
                s.pop(l)
                # print(ans, s)
                break
        if ans[i] == origin:
            return "IMPOSSIBLE"
    return ''.join(ans)


def is_shuffled_anagram(s, a):
    return all([s[i] != a[i] for i in range(len(s))])

def shuffle_str(s):
    sc = [c for c in s]
    shuffle(sc)
    return ''.join(sc)


def solve2(s):
    count = Counter(s)
    if count.most_common()[0][1] > len(s)/2:
        return "IMPOSSIBLE"
    ans = s.copy()
    ans = shuffle_str(ans)
    while is_shuffled_anagram(ans, s) != True:
        ans = shuffle_str(ans)
    return ans


class Letter:
    def __init__(self, label, origin=None, count=None):
        self.label = label
        self.origin = origin
        self.sorted = None
        self.swapped = None

        self.count = count
        self.accumulate = None

    def __repr__(self) -> str:
        return f'{self.label}: acc {self.accumulate}'

    def __eq__(self, o: object) -> bool:
        return self.label == o.label

    def __hash__(self) -> int:
        return hash(self.label)


def solve3(s):
    seq = [Letter(c, i) for i, c in enumerate(s)]
    count = Counter(seq)
    most_common_count = count.most_common()
    if most_common_count[0][1] > len(s)/2:
        return "IMPOSSIBLE"
    sortu = sorted([Letter(letter.label, count=cnt) for letter, cnt in most_common_count], key=lambda l: l.label)
    acc = 0
    for letter in sortu:
        letter.accumulate = acc
        acc+=letter.count
    return sortu


for case in range(1, int(input())+1):
    s = [c for c in input()]
    print(f'Case #{case}: {solve3(s)}')