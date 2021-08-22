from utils import get_input

INPUT = """
2
5 4
1 2
6 7
9 12
24 24
41 50
14 24 24 4
1 1
42 42
24
"""

input = get_input(INPUT)(input)

from functools import reduce

def assign(a, value, fr=0, to=None):
    if to is None:
        to = len(a)
    a[fr:to] = [value]*(to-fr)
    return a

def solve(test_diff, students, N):
    test_sort = sorted(test_diff, key=lambda x: x[0])
    assigns = [None] * max(test_sort[-1][1], max(students))
    for i, test_range in enumerate(test_sort):
        test_min, test_max = test_range
        if i == N-1:
            assigns = assign(assigns, value=test_max, fr=test_max)
            # assigns[test_max:] = test_max
        else:
            if i == 0:
                # assigns[:test_min] = test_min
                assigns = assign(assigns, test_min, to=test_min)
            next_min, next_max = test_sort[i+1]
            mid_point = int((next_min + test_max)/2)
            assigns = assign(assigns, test_max, fr=test_max, to=mid_point+1)# assigns[test_max:mid_point+1] = test_max
            assigns = assign(assigns, next_min, fr=mid_point+1, to=next_min)# assigns[mid_point+1:next_min] = next_min
        assigns[test_min:test_max] = list(range(test_min, test_max))
    
    '''
    #iterating over students
    student_test = [None for _ in students]
    for st, student in enumerate(students):
        best_test = assigns[student]
        student_test[st] = best_test
        assigns[student] = None
    '''
    return assigns

def solve2(test_diff, students, N):
    test_sort = sorted(test_diff, key=lambda x:x[0])
    test_lvs = reduce((lambda x, y: x+y), [list(range(a, b+1)) for a, b in test_sort])
    student_test = [None for _ in students]
    for st, student in enumerate(students):
        if len(test_lvs) == 1:
            student_test[st] = test_lvs[0]
            break
        diff = abs(student - test_lvs[0])
        best_lv = test_lvs[0]
        for t, test_lv in enumerate(test_lvs):
            if abs(student - test_lv) < diff:
                diff = abs(student - test_lv)
                best_lv = test_lv
            elif abs(student - test_lv) > diff:
                student_test[st] = best_lv
                test_lvs.pop(t-1)
                break
    return ' '.join([str(s) for s in student_test])
        


for case in range(1, int(input())+1):
    N, M = [int(s) for s in input().split(' ')]
    test_diff = [list(map(int, input().split(' '))) for _ in range(N)]
    students = [int(s) for s in input().split(' ')]
    print(f'Case #{case}: {solve2(test_diff, students, N)}')