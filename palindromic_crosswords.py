from utils import get_input

INPUTS = """
2
2 2
A.
.#
4 6
A...#.
B##...
B.###.
A...#.
"""

input = get_input(INPUTS)(input)

class Cell:
    def __init__(self, x, y, label) -> None:
        self.x = x
        self.y = y
        self.label = label
    
    def __repr__(self) -> str:
        return self.label

def solve(rows):
    """
    Passes test 1 but time limit error for test 2.
    Probably due to while nochange part. Need optimization to pass test 2.
    """
    words = []
    hword = []
    vwords = [[] for _ in rows[0]]
    ans = [[None for _ in rows[0]] for _ in rows]
    for r, row in enumerate(rows):
        for c, label in enumerate(row):
            cell = Cell(c, r, label)
            if label == '#':
                if len(hword) > 1:
                    words.append(hword)
                hword = []
                if len(vwords[c]) > 1:
                    words.append(vwords[c])
                vwords[c] = []
            else:
                hword.append(cell)
                vwords[c].append(cell)
            ans[r][c] = cell
        if len(hword) > 1:
            words.append(hword)
        hword = []
    [words.append(word) for word in vwords if len(word) > 1]

    nochange = True
    fillcount = 0
    while nochange:
        nochange = False
        for word in words:
            for c, cell in enumerate(word):
                if cell.label == '.' and word[-c-1].label != '.':
                    cell.label = word[-c-1].label
                    fillcount += 1
                    nochange = True
    return fillcount, ans


for case in range(1, int(input())+1):
    N, M = [int(s) for s in input().split(' ')]
    rows = [[c for c in input()] for _ in range(N)]
    count, ans = solve(rows)
    print(f'Case #{case}: {count}')
    for row in ans:
        print(''.join([cell.label for cell in row]))