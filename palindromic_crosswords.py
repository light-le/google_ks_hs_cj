from utils import get_input

INPUTS = """
4
2 2
A.
.#
2 2
.A
..
4 6
A...#.
B##...
B.###.
A...#.
4 6
....#.
B##...
B.###A
....#.
"""

input = get_input(INPUTS)(input)

class Cell:
    def __init__(self, x, y, label) -> None:
        self.x = x
        self.y = y
        self.label = label
    
    def __repr__(self) -> str:
        return self.label

    def __str__(self) -> str:
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


class LinkedCell:
    def __init__(self, label, x, y) -> None:
        self.label = label
        self.coors = {(x, y)}
    def add_coor(self, x, y):
        self.coors.add((x, y))
    def __repr__(self) -> str:
        return self.label
    def __str__(self) -> str:
        return self.label


def mirrow_word(rows, coors):
    for x, y in coors:
        if isinstance(rows[y][x], LinkedCell) == False:
            rows[y][x] = LinkedCell(rows[y][x], x, y)
    if len(coors) == 1:
        return rows

    for ch, (x, y) in enumerate(coors[:int(len(coors)/2)]):
        ox, oy = coors[-ch-1]
        if rows[y][x].label != '.':
            for olx, oly in rows[oy][ox].coors:
                rows[oly][olx] = rows[y][x]
                rows[y][x].add_coor(olx, oly)
        else:
            for lx, ly in rows[y][x].coors:
                rows[ly][lx] = rows[oy][ox]
                rows[oy][ox].add_coor(lx, ly)
    return rows

def count_dot(rows, d='.'):
    return sum([str(row).count(d) for row in rows])

def solve2(rows):
    """
    still TLE for test 2
    """
    dot_before = count_dot(rows)
    hlen = 0
    collen = len(rows[0])
    vlens = [0 for _ in rows[0]]
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            if cell == '#':
                if hlen:
                    rows = mirrow_word(rows, [(x, r) for x in range(c-hlen, c)])
                    hlen = 0
            else:
                hlen+=1
        if hlen:
            rows = mirrow_word(rows, [(x, r) for x in range(collen-hlen, collen)])
            hlen = 0

        for c, cell in enumerate(row):
            if cell == '#':
                if vlens[c]:
                    rows = mirrow_word(rows, [(c, y) for y in range(r-vlens[c], r)])
                    vlens[c] = 0
            else:
                vlens[c]+=1
    rowlen = len(rows)
    for c, vlen in enumerate(vlens):
        if vlen:
            rows = mirrow_word(rows, [(c, y) for y in range(rowlen-vlen, rowlen)])
    dot_after = count_dot(rows)
    return dot_before-dot_after, rows


for case in range(1, int(input())+1):
    N, M = [int(s) for s in input().split(' ')]
    rows = [[c for c in input()] for _ in range(N)]
    count, ans = solve2(rows)
    print(f'Case #{case}: {count}')
    for row in ans:
        print(''.join([str(cell) for cell in row]))