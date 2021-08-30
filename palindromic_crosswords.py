from utils import get_input
from collections import defaultdict

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


class Letter:
    def __init__(self, label, x, y, row_mirror=False, col_mirror=False) -> None:
        self.label = label
        self.x = x
        self.y = y
        self.row_mirror = row_mirror
        self.col_mirror = col_mirror

    def check_opposite(self, rc, co):
        # return x/y of the opposite
        
        left = 0
        right = 0
        for r in range(co+1, len(rc)):
            if rc[r] == '#':
                break
            right+=1
        for l in range(co-1, -1, -1):
            if rc[l] == '#':
                break
            left+=1
        return co - left + right


def solve3(rows):
    nrow = len(rows)
    ncol = len(rows[0])
    dot_before = count_dot(rows)
    if dot_before == 0:
        return 0, rows
    frontier = []
    for r, row in enumerate(rows):
        for c, cell in enumerate(row):
            if cell not in ['#', '.']:
                frontier.append(Letter(cell, c, r))
    count = 0
    while frontier:
        letter = frontier.pop()
        if not letter.row_mirror:
            xopp = letter.check_opposite(rows[letter.y], letter.x)
            if rows[letter.y][xopp] == '.':
                rows[letter.y][xopp] = letter.label
                count+=1
                frontier.append(Letter(letter.label, xopp, letter.y, row_mirror=True))
        if not letter.col_mirror:
            yopp = letter.check_opposite([rows[c][letter.x] for c in range(nrow)], letter.y)
            if rows[yopp][letter.x] == '.':
                rows[yopp][letter.x] = letter.label
                count+=1
                frontier.append(Letter(letter.label, letter.x, yopp, col_mirror=True))
    return count, rows



for case in range(1, int(input())+1):
    N, M = [int(s) for s in input().split(' ')]
    rows = [[c for c in input()] for _ in range(N)]
    count, ans = solve3(rows)
    print(f'Case #{case}: {count}')
    for row in ans:
        print(''.join([str(cell) for cell in row]))