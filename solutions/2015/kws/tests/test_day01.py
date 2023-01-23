from aoc_2015_kws.day_01 import find_floor


def test_find_floor():
    assert find_floor("()") == 0
    assert find_floor("(((") == 3
    assert find_floor("(()(()(") == 3
    assert find_floor("))(((((") == 3
    assert find_floor("())") == -1
    assert find_floor("))(") == -1
    assert find_floor(")))") == -3
    assert find_floor(")())())") == -3
