INPUTS = """
5
1 2
3 4
5 6
7 8
9 0"""

def get_input(inputs):
    # get_input(INPUTS)(input)
    def yield_input(docstr=INPUTS):
        def generate_input(docstr):
            for inp in docstr.split("\n"):
                if inp != '':
                    yield inp
        inputs = generate_input(docstr)
        return inputs

    ins = yield_input(inputs)

    def inner(f):
        def wrapper():
            return next(ins)
        return wrapper
    return inner


def print_args(f):
    def inner(*args):
        print(args)
        result = f(*args)
        print('result', result)
        return result
    return inner

if __name__ == '__main__':
    print(input())
    print(input())
    print(input())
    print(input())
    print(input())