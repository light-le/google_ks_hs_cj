from utils import get_input
from random import shuffle
from collections import Counter
from math import ceil

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
        self.increment = 0

    def __repr__(self) -> str:
        return f'{self.label}: {self.sorted} {self.swapped} {self.origin}'

    def __eq__(self, o: object) -> bool:
        return self.label == o.label

    def __hash__(self) -> int:
        return hash(self.label)


def solve3(s):
    """
    This solution follows the post-event analysis
    """
    seq = [Letter(c, i) for i, c in enumerate(s)]
    count = Counter(seq)
    most_common_count = count.most_common()
    if most_common_count[0][1] > len(s)/2:
        return "IMPOSSIBLE"

    sortu = sorted([Letter(letter.label, count=cnt) for letter, cnt in most_common_count], key=lambda l: l.label)
    sortd = {letter.label: letter for letter in sortu}
    acc = 0
    for letter in sortu:
        letter.accumulate = acc
        acc+=letter.count
    sortseq = [None for _ in seq]
    for letter in seq:
        letter.sorted = sortd[letter.label].accumulate + sortd[letter.label].increment
        sortd[letter.label].increment+=1
        if letter.sorted < int(len(s)/2):
            letter.swapped = letter.sorted + ceil(len(s)/2)
        else:
            letter.swapped = letter.sorted - int(len(s)/2)
        sortseq[letter.sorted] = letter
    ans = ['' for _ in seq]
    for letter in sortseq:
        final = sortseq[letter.swapped].origin
        ans[final] = letter.label
    assert is_shuffled_anagram(s, ans), "WRONG ANSWER"
    return ''.join(ans)


for case in range(1, int(input())+1):
    s = [c for c in input()]
    print(f'Case #{case}: {solve3(s)}')