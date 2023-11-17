from typing import Callable


def execute(*args):
    lambda f, g: lambda x: g(f(x))
