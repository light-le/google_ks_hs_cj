from utils import get_input
from random import shuffle
from collections import Counter

INPUTS = """
6
start
jjj
vuiewvuwnvywjre
jij
jeejjejejeeejj
huihhhiu
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
    


for case in range(1, int(input())+1):
    s = [c for c in input()]
    print(f'Case #{case}: {solve2(s)}')