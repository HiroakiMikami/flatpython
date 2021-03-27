from flatpython._lint import lint


def test_funcdef():
    assert lint("""def f():
    pass
""")
    assert not lint("""def f():
    def g():
        pass
""")


def test_for():
    assert lint("""for x in xs:
    pass
""")
    assert not lint("""def f():
    for x in xs:
        pass
""")


def test_while():
    assert lint("""while x:
    pass
""")
    assert not lint("""def f():
    while x:
        pass
""")


def test_if():
    assert lint("""if x:
    pass
""")
    assert not lint("""def f():
    if x:
        pass
""")


def test_ifexp():
    assert lint("""x if c else y""")
    assert not lint("""def f():
    x if c else y
""")


def test_lambda():
    assert lint("""lambda x: x + 1""")
    assert not lint("""def f():
    lambda x: x + 1
""")


def test_comprehension():
    assert lint("""[x for x in xs]""")
    assert not lint("""def f():
    [x for x in xs]
""")


def test_classdef():
    assert lint("""class X:
    pass
""")
    assert lint("""@dataclass
class X:
    x: int
    y: str
""")
    assert not lint("""class X:
    def __init__(self):
        pass
""")
