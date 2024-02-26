from math import gcd, lcm, log, isclose, floor, ceil


def global_is_close(a):
    return isclose(a, floor(a), abs_tol=1e-9) or isclose(a, ceil(a), abs_tol=1e-9)


def plus(a, b):
    return a + b


def minus(a, b):
    return abs(a - b)


def mult(a, b):
    return a * b


def divide(a, b):

    if b != 0 and a % b == 0:
        return a // b
    return -1


def exp(a, b):
    return a ** b


def log_base(a, b):
    try:
        ans = log(a, b)
        if global_is_close(ans):
            return floor(ans)
        return -1
    except ZeroDivisionError:
        return -1
    except ValueError:
        return -1


def root(a, b):
    if a == 0:
        return -1

    ans = b ** (1/a)

    if global_is_close(ans):
        return floor(ans)
    return -1


def concat(a, b):
    return int(str(a)+str(b))


def remainder(a, b):
    if b == 0:
        return -1
    return a % b


def bitwise_and(a, b):
    return a & b


def bitwise_or(a, b):
    return a | b


def bitwise_xor(a, b):
    return a ^ b


def bitwise_left_shift(a, b):
    return a << b


def arithmetic_mean(a, b):
    ans = (a + b) / 2
    if global_is_close(ans):
        return floor(ans)
    return -1


def geometric_mean(a, b):
    ans = (a * b) ** 0.5
    if global_is_close(ans):
        return floor(ans)
    return -1


commutative_math_funcs = [
    plus,
    minus,
    mult,
    gcd,
    lcm,
    min,
    max,
    # arithmetic_mean,
    # geometric_mean,
    # bitwise_and,
    # bitwise_or,
    # bitwise_xor
]

non_commutative_math_funcs = [
    divide,
    exp,
    log_base,
    root,
    concat,
    remainder,
    # bitwise_left_shift,
]


def split(n: str):
    if len(n) % 2 != 0:
        raise ValueError('Length has to be even!')
    middle = len(n) // 2
    return n[:middle], n[middle:]


def apply_funcs_iter(a, b, funcs, comm=True):
    ans = {}
    for f in funcs:
        ans[(f.__name__, a, b)] = f(a, b)
        if not comm:
            ans[(f.__name__, b, a)] = f(b, a)
    return ans


def apply_funcs(a, b):
    a_int = int(a)
    b_int = int(b)
    comm_ans = apply_funcs_iter(a_int, b_int, commutative_math_funcs)
    non_comm_ans = apply_funcs_iter(a_int, b_int, non_commutative_math_funcs, comm=False)
    return {k: v for k, v in {**comm_ans, **non_comm_ans}.items() if v >= 0}


def find_all_keys_by_value(d, value):
    return [key for key, val in d.items() if val == value]


def find_operations(numbers: list):
    for n in numbers:
        p1, p2 = split(n)
        p1_numbers = apply_funcs(*split(p1))
        p2_numbers = apply_funcs(*split(p2))
        inter = set(p1_numbers.values()).intersection(set(p2_numbers.values()))
        result_n = []
        for i in inter:
            result_n.append({
                'ans': i,
                'combinations_p1': find_all_keys_by_value(p1_numbers, i),
                'combinations_p2': find_all_keys_by_value(p2_numbers, i)
            })
        yield n, result_n


if __name__ == '__main__':
    overall_not_found_numbers = []
    all_possible_numbers = [f"{i:04d}" for i in range(0, 10000)]
    for number, answers in find_operations(all_possible_numbers):
        if len(answers) == 0:
            overall_not_found_numbers.append(number)
            print(number, answers)
        # print(number)
        # for answer in answers:
        #     print(answer['ans'])
        #     print(answer['combinations_p1'])
        #     print(answer['combinations_p2'])
        # print('-' * 40)
    print('-' * 40)
    print(len(overall_not_found_numbers))